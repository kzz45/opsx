package funcs

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"opsx/monitorx_proxy/g"
	"os"
	"strings"
	"time"

	"github.com/gin-gonic/gin"
)

func NoticeServer() {
	if g.Config().Deubg {
		gin.SetMode(gin.DebugMode)
		gin.DefaultWriter = os.Stdout
	} else {
		gin.SetMode(gin.ReleaseMode)
		gin.DefaultWriter = g.LogWriter
	}
	router := gin.Default()
	v1_group := router.Group("/api/v1")

	v1_group.POST("/notice", notice_receive)

	router.Use(gin.Logger())
	router.Use(gin.Recovery())

	notice_proxy := &http.Server{
		Addr:           fmt.Sprintf("%s:%d", g.Config().Notice.Addr, g.Config().Notice.Port),
		Handler:        router,
		MaxHeaderBytes: 1 << 20,
	}

	g.Logger.Infof("jobs proxy run at: %s:%d", g.Config().Notice.Addr, g.Config().Notice.Port)
	notice_proxy.ListenAndServe()
}

// 接收alertmanager的告警信息
func notice_receive(c *gin.Context) {
	body, err := ioutil.ReadAll(c.Request.Body)
	if err != nil {
		g.Logger.Errorf("i got alert msg error: %v", err)
		c.JSON(http.StatusBadRequest, gin.H{
			"code":    http.StatusBadRequest,
			"message": "i got alert msg error",
		})
		return
	}

	var notification AlertManagerNotification
	if err := json.Unmarshal(body, &notification); err != nil {
		g.Logger.Errorf("json umarshal notice body error: %v", err)
		c.JSON(http.StatusNotImplemented, gin.H{
			"code":    http.StatusNotImplemented,
			"message": "i got alert msg but json unmarshal error",
		})
		return
	}

	parse_notice(notification)

	c.JSON(http.StatusOK, gin.H{
		"code":    http.StatusOK,
		"message": "i got alert success",
	})
}

func parse_notice(notification AlertManagerNotification) error {
	// g.Logger.Errorf("notification: %v\n", notification)
	webhook, _ := get_user_group_webhook(notification.Receiver)

	endpoints := make([]string, 0)
	for _, alert := range notification.Alerts {
		endpoints = append(endpoints, alert.Labels["_endpoint"])
	}
	endpoints_str := strings.Join(endpoints, ",")
	g.Logger.Errorf("[状态]:%s [等级]:%s [告警名称]:%s [接收人]:%s [告警实例]:%s [告警数量]: %d\n",
		notification.Status,
		notification.CommonLabels["level"],
		notification.CommonLabels["alertname"],
		webhook.Name,
		endpoints_str,
		len(notification.Alerts),
	)
	// 全部告警
	if err := g.AlertsRPush("alerts", notification); err != nil {
		g.Logger.Errorf("push all alert message to redis error: %v", err)
		return nil
	}
	var group_notification AlertManagerNotification
	// 同类超过5个就合并了
	if len(notification.Alerts) > 5 {
		group_notification = AlertManagerNotification{
			Receiver:          notification.Receiver,
			Status:            notification.Status,
			GroupLabels:       notification.GroupLabels,
			CommonLabels:      notification.CommonLabels,
			CommonAnnotations: notification.CommonAnnotations,
			ExternalURL:       notification.ExternalURL,
			Alerts:            notification.Alerts,
		}
		feishu_group(group_notification, webhook.WebHook)
	} else {
		feishu(notification, webhook.WebHook)
	}
	return nil
}

func feishu(notification AlertManagerNotification, webhook string) bool {
	for _, alert := range notification.Alerts {
		var feishu_msg FeiShuMsg
		feishu_msg.MsgType = "interactive"
		if notification.Status == "firing" && alert.Labels["level"] == "crit" {
			feishu_msg.Card.Header.Template = "red"
			feishu_msg.Card.Header.Title.Content = fmt.Sprintf("崩盘 - %s - %s", alert.Labels["_product_name"], alert.Annotations["summary"])
			feishu_msg.Card.Header.Title.Tag = "plain_text"
			content := fmt.Sprintf(
				"**告警名称**: %s\n**告警时间**: %s\n**告警概述**: %s\n**告警产品**: %s\n**告警实例**: %s\n**实例名称**: %s\n",
				notification.CommonLabels["alertname"],
				time.Now().Format("2006-01-02 15:04:05"),
				alert.Annotations["summary"],
				alert.Labels["_product_name"],
				alert.Labels["_endpoint"],
				alert.Labels["_name"],
			)
			field := FieldContent{
				IsShort: true,
				Text:    ContentTag{Tag: "lark_md", Content: content},
			}

			fields := make([]FieldContent, 0)
			fields = append(fields, field)
			element := CardElement{
				Tag:    "div",
				Fields: fields,
			}
			elements := make([]CardElement, 0)
			elements = append(elements, element)
			feishu_msg.Card.Elements = elements

		} else if notification.Status == "resolved" {
			feishu_msg.Card.Header.Template = "green"
			feishu_msg.Card.Header.Title.Content = fmt.Sprintf("恢复 - %s - %s ", alert.Labels["_product_name"], alert.Annotations["summary"])
			feishu_msg.Card.Header.Title.Tag = "plain_text"
			content := fmt.Sprintf(
				"**告警名称**: %s\n**恢复时间**: %s\n**告警概述**: %s\n**告警产品**: %s\n**告警实例**: %s\n**实例名称**: %s\n",
				notification.CommonLabels["alertname"],
				time.Now().Format("2006-01-02 15:04:05"),
				alert.Annotations["summary"],
				alert.Labels["_product_name"],
				alert.Labels["_endpoint"],
				alert.Labels["_name"],
			)
			field := FieldContent{
				IsShort: true,
				Text:    ContentTag{Tag: "lark_md", Content: content},
			}

			fields := make([]FieldContent, 0)
			fields = append(fields, field)
			element := CardElement{
				Tag:    "div",
				Fields: fields,
			}
			elements := make([]CardElement, 0)
			elements = append(elements, element)
			feishu_msg.Card.Elements = elements
		}
		msg_body, err := json.Marshal(feishu_msg)
		if err != nil {
			return false
		}
		req, err := http.NewRequest("POST", webhook, bytes.NewBuffer(msg_body))
		req.Header.Set("Content-Type", "application/json")
		if err != nil {
			g.Logger.Errorf("make feishu request error: %s", err)
			return false
		}
		client := &http.Client{}
		resp, err := client.Do(req)
		if err != nil {
			g.Logger.Errorf("post feishu alert msg error: %s", err)
			return false
		}
		defer resp.Body.Close()
	}
	return true
}

func contains(x []string, y string) bool {
	for _, i := range x {
		if i == y {
			return true
		}
	}
	return false
}

func feishu_group(notification AlertManagerNotification, webhook string) bool {
	var feishu_msg FeiShuMsg
	names := make([]string, 0)
	endpoints := make([]string, 0)
	summarys := make([]string, 0)
	feishu_msg.MsgType = "interactive"
	for _, alert := range notification.Alerts {
		names = append(names, alert.Labels["_name"])
		is_contains := contains(summarys, alert.Annotations["summary"])
		if !is_contains {
			summarys = append(summarys, alert.Annotations["summary"])
		}
		endpoints = append(endpoints, alert.Labels["_endpoint"])
	}
	names_str := strings.Join(names, ",")
	summarys_str := strings.Join(summarys, "\n")
	endpoints_str := strings.Join(endpoints, ",")
	if notification.Status == "firing" && notification.CommonLabels["level"] == "crit" {
		feishu_msg.Card.Header.Template = "red"
		feishu_msg.Card.Header.Title.Content = fmt.Sprintf("崩盘 - %s - %s - 很多", notification.CommonLabels["_product_name"], notification.CommonLabels["alertname"])
		feishu_msg.Card.Header.Title.Tag = "plain_text"
		content := fmt.Sprintf(
			"**告警名称**: %s\n**告警时间**: %s\n**告警产品**: %s\n**告警概述**: \n%s\n**告警实例**: \n%s\n**实例名称**: %s\n",
			notification.CommonLabels["alertname"],
			time.Now().Format("2006-01-02 15:04:05"),
			notification.CommonLabels["_product_name"],
			summarys_str,
			endpoints_str,
			names_str,
		)
		field := FieldContent{
			IsShort: true,
			Text:    ContentTag{Tag: "lark_md", Content: content},
		}

		fields := make([]FieldContent, 0)
		fields = append(fields, field)
		element := CardElement{
			Tag:    "div",
			Fields: fields,
		}
		elements := make([]CardElement, 0)
		elements = append(elements, element)
		feishu_msg.Card.Elements = elements
	} else if notification.Status == "resolved" {
		feishu_msg.Card.Header.Template = "green"
		feishu_msg.Card.Header.Title.Content = fmt.Sprintf("恢复 - %s - %s 很多", notification.CommonLabels["_product_name"], notification.CommonLabels["alertname"])
		feishu_msg.Card.Header.Title.Tag = "plain_text"
		content := fmt.Sprintf(
			"**告警名称**: %s\n**恢复时间**: %s\n**告警产品**: %s\n**告警概述**: \n%s\n**告警实例**: %s\n**实例名称**: %s\n",
			notification.CommonLabels["alertname"],
			time.Now().Format("2006-01-02 15:04:05"),
			notification.CommonLabels["_product_name"],
			summarys_str,
			endpoints_str,
			names_str,
		)
		field := FieldContent{
			IsShort: true,
			Text:    ContentTag{Tag: "lark_md", Content: content},
		}

		fields := make([]FieldContent, 0)
		fields = append(fields, field)
		element := CardElement{
			Tag:    "div",
			Fields: fields,
		}
		elements := make([]CardElement, 0)
		elements = append(elements, element)
		feishu_msg.Card.Elements = elements
	}
	msg_body, err := json.Marshal(feishu_msg)
	if err != nil {
		return false
	}
	req, err := http.NewRequest("POST", webhook, bytes.NewBuffer(msg_body))
	req.Header.Set("Content-Type", "application/json")
	if err != nil {
		g.Logger.Errorf("make feishu request error: %s", err)
		return false
	}
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		g.Logger.Errorf("post feishu alert msg error: %s", err)
		return false
	}
	defer resp.Body.Close()
	return true
}
