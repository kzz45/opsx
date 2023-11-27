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
	g.Logger.Infof("[状态]:%s [等级]:%s [告警名称]:%s [接收人]:%s [告警数量]:%d [告警消息]:%v\n",
		notification.Status,
		notification.CommonLabels["level"],
		notification.CommonLabels["alertname"],
		notification.Receiver,
		len(notification.Alerts),
		notification.Alerts[len(notification.Alerts)-1].Annotations)
	// 全部告警
	if err := g.AlertsRPush("alerts", notification); err != nil {
		g.Logger.Errorf("push all alert message to redis error: %v", err)
		return nil
	}
	// 合并告警
	var notice_msg_merge NoticeMsg
	notice_msg_merge.Receiver = notification.Receiver
	notice_msg_merge.StartsAt = time.Now().Format("2006-01-02 15:04:05")
	notice_msg_merge.Level = notification.CommonLabels["level"]
	notice_msg_merge.AlertNum = len(notification.Alerts)
	if notification.Status == "firing" {
		notice_msg_merge.MergeStatus = "崩盘"
	} else if notification.Status == "resolved" {
		notice_msg_merge.MergeStatus = "恢复"
	} else {
		notice_msg_merge.MergeStatus = notification.Status
	}
	alert_status := make(map[string]int)
	alert_products := make(map[string]int)
	// 每一条告警 日志存储
	for _, alert := range notification.Alerts {
		// 每一条告警 日志存储 (供前端大屏显示)
		if err := g.AlertsRPush("endpoints", alert); err != nil {
			g.Logger.Errorf("push each alert message to redis error: %v", err)
		}
		status := alert.Status
		product_name := alert.Labels["_product_name"]
		if _, ok := alert_products[product_name]; ok {
			alert_products[product_name] += 1
		} else {
			alert_products[product_name] = 1
		}
		if _, ok := alert_status[status]; ok {
			alert_status[status] += 1
		} else {
			alert_status[status] = 1
		}
	}
	var product_str_list []string
	for k, v := range alert_products {
		product_str := fmt.Sprintf("%s=%d", k, v)
		product_str_list = append(product_str_list, product_str)
	}
	var status_str_list []string
	for k, v := range alert_status {
		status_str := fmt.Sprintf("%s=%d", k, v)
		status_str_list = append(status_str_list, status_str)
	}
	notice_msg_merge.AlertStatus = alert_status
	notice_msg_merge.AlertStatusStr = strings.Join(status_str_list, ",")
	notice_msg_merge.AlertProduct = alert_products
	notice_msg_merge.AlertProductStr = strings.Join(product_str_list, ",")
	notice_msg_merge.CommonLabels = notification.CommonLabels
	notice_msg_merge.CommonAnnotations = notification.CommonAnnotations
	webhook, _ := get_user_group_webhook(notification.Receiver)
	wechat_original(notification, webhook)
	return nil
}

func wechat_original(notification AlertManagerNotification, webhook string) bool {
	for _, alert := range notification.Alerts {
		var wechat_msg WeChatMsg
		wechat_msg.MsgType = "markdown"
		markdown_content := make(map[string]string)
		if notification.Status == "firing" {
			markdown_content["content"] = fmt.Sprintf(
				"告警等级: <font color =\"warning\">%s</font>\n告警状态: <font color =\"warning\">%s</font>\n告警名称: %s\n告警时间: %s\n告警概述: %s\n告警产品: %s\n告警实例: %s\n实例名称: %s\n",
				"崩盘",
				notification.Status,
				notification.CommonLabels["alertname"],
				time.Now().Format("2006-01-02 15:04:05"),
				alert.Annotations["summary"],
				alert.Labels["_product_name"],
				alert.Labels["_endpoint"],
				alert.Labels["_name"],
			)
		} else if notification.Status == "resolved" {
			markdown_content["content"] = fmt.Sprintf(
				"告警等级: <font color =\"info\">%s</font>\n告警状态: <font color =\"info\">%s</font>\n告警名称: %s\n恢复时间: %v\n告警概述: %s\n告警产品: %s\n告警实例: %s\n实例名称: %s\n",
				"恢复",
				notification.Status,
				notification.CommonLabels["alertname"],
				time.Now().Format("2006-01-02 15:04:05"),
				alert.Annotations["summary"],
				alert.Labels["_product_name"],
				alert.Labels["_endpoint"],
				alert.Labels["_name"],
			)
		}

		wechat_msg.MarkDown = markdown_content
		msg_body, err := json.Marshal(wechat_msg)
		if err != nil {
			return false
		}
		req, err := http.NewRequest("POST", webhook, bytes.NewBuffer(msg_body))
		req.Header.Set("Content-Type", "application/json")
		if err != nil {
			g.Logger.Errorf("make wechat request error: %s", err)
			return false
		}
		client := &http.Client{}
		resp, err := client.Do(req)
		if err != nil {
			g.Logger.Errorf("post wechat alert msg error: %s", err)
			return false
		}
		defer resp.Body.Close()
	}
	return true
}
