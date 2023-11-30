package funcs

import "time"

type AlertRule struct {
	Alert  string `json:"alert"`
	Expr   string `json:"expr"`
	For    string `json:"for"`
	Labels struct {
		Level    string `json:"level"`
		AlertID  int    `json:"alert_id"`
		AdjustID int    `json:"adjust_id"`
	} `json:"labels"`
	Annotations struct {
		Summary     string `json:"summary"`
		Description string `json:"description"`
	} `json:"annotations"`
}

type GlobalAlertRule struct {
	Rules []AlertRule `json:"rules"`
}
type GlobalAlertRoute struct {
	Routes    []AlertRoute        `json:"routes"`
	Receivers []AlertRouteReciver `json:"receivers"`
}

type AlertRoute struct {
	Receiver       string          `json:"receiver"`
	GroupWait      int             `json:"group_wait"`
	GroupInterval  int             `json:"group_interval"`
	RepeatInterval int             `json:"repeat_interval"`
	GroupBy        []string        `json:"group_by"`
	Continue       bool            `json:"continue"`
	Match          interface{}     `json:"match"`
	SubRoute       []SubAlertRoute `json:"routes"`
}

type SubAlertRoute struct {
	Receiver       string      `json:"receiver"`
	GroupWait      int         `json:"group_wait"`
	GroupInterval  int         `json:"group_interval"`
	RepeatInterval int         `json:"repeat_interval"`
	GroupBy        []string    `json:"group_by"`
	Continue       bool        `json:"continue"`
	Match          interface{} `json:"match"`
}
type AlertRouteReciver struct {
	Name           string `json:"name"`
	WebhookConfigs string `json:"webhook_configs"`
}

type Servers struct {
	Results []Server `json:"results"`
}

type Server struct {
	Name            string `json:"name"`
	Code            string `json:"code"`
	UUID            string `json:"uuid"`
	IPAddr          string `json:"ipaddr"`
	ServerGroupName string `json:"server_group__name"`
}

type JobTask struct {
	TaskID     int           `json:"task_id"`
	TaskName   string        `json:"task_name"`
	ServerUUID string        `json:"server_uuid"`
	AddOns     []JobAddOn    `json:"addons"`
	Instances  []JobInstance `json:"instances"`
}

// 抓取任务
type JobAddOn struct {
	TaskID   int         `json:"task_id"`
	ID       int         `json:"id"`
	Name     string      `json:"name"`
	Mode     string      `json:"mode"`
	Scheme   string      `json:"scheme"`
	Port     int         `json:"port"`
	Args     string      `json:"args"`
	Metric   string      `json:"metric"`
	Params   interface{} `json:"params"`
	Interval int         `json:"interval"`
	TimeOut  int         `json:"timeout"`
}

type JobInstance struct {
	IP       string      `json:"_ip"`
	Name     string      `json:"_name"`
	Endpoint string      `json:"_endpoint"`
	Labels   interface{} `json:"labels"`
	Port     int         `json:"port"`
}

type UserGroupResp struct {
	Results []UserGroup `json:"results"`
}

type UserGroup struct {
	ID       int    `json:"id"`
	Name     string `json:"name"`
	Channel  string `json:"channel"`
	WebHook  string `json:"webhook"`
	UserList []User `json:"user_list"`
}

type User struct {
	ID        int    `json:"id"`
	UserName  string `json:"username"`
	FirstName string `json:"first_name"`
}
type AlertManagerNotification struct {
	Receiver          string            `json:"receiver"`
	Status            string            `json:"status"`
	Alerts            []Alert           `json:"alerts"`
	GroupLabels       map[string]string `json:"groupLabels"`
	CommonLabels      map[string]string `json:"commonLabels"`
	CommonAnnotations map[string]string `json:"commonAnnotations"`
	ExternalURL       string            `json:"externalURL"`
}

type Alert struct {
	Status      string            `json:"status"`
	Labels      map[string]string `json:"labels"`
	Annotations map[string]string `json:"annotations"`
	StartsAt    time.Time         `json:"startsAt"`
	EndsAt      time.Time         `json:"endsAt"`
}

type NoticeMsg struct {
	Receiver          string            `json:"receiver"`
	AlertNum          int               `json:"alert_num"`
	MergeStatus       string            `json:"merge_status"`
	AlertStatus       map[string]int    `json:"alert_status"`
	AlertStatusStr    string            `json:"alert_status_str"`
	AlertProduct      map[string]int    `json:"alert_product"`
	AlertProductStr   string            `json:"alert_product_str"`
	Level             string            `json:"level"`
	CommonLabels      map[string]string `json:"commonLabels"`
	CommonAnnotations map[string]string `json:"commonAnnotations"`
	StartsAt          string            `json:"startsAt"`
	EndsAt            time.Time         `json:"endsAt"`
}

type WeChatMsg struct {
	MsgType  string            `json:"msgtype"`
	MarkDown map[string]string `json:"markdown"`
}

type FeiShuMsg struct {
	Card    MsgCard `json:"card"`
	MsgType string  `json:"msg_type"`
}

type MsgCard struct {
	Header   CardHeader    `json:"header"`
	Elements []CardElement `json:"elements"`
}

type CardHeader struct {
	Template string `json:"template"`
	Title    ContentTag
}
type ContentTag struct {
	Content string `json:"content"`
	Tag     string `json:"tag"`
}

type CardElement struct {
	Tag    string         `json:"tag"`
	Fields []FieldContent `json:"fields"`
}

type FieldContent struct {
	IsShort bool       `json:"is_short"`
	Text    ContentTag `json:"text"`
}
type Silence struct {
	IsChange bool          `json:"is_change"`
	Data     []SilenceData `json:"data"`
}

type SilenceData struct {
	CreatedBy string `json:"createdBy"`
	StartsAt  int64  `json:"startsAt"`
	EndsAt    int64  `json:"endsAt"`
	Comment   string `json:"comment"`
	Matchers  []KV   `json:"matchers"`
}

type KV struct {
	IsRegex bool   `json:"isRegex"`
	Name    string `json:"name"`
	Value   string `json:"value"`
}

type AmSilence struct {
	ID     string `json:"id"`
	Status struct {
		State string `json:"state"`
	} `json:"status"`
	UpdatedAt time.Time `json:"updatedAt"`
	Comment   string    `json:"comment"`
	CreatedBy string    `json:"createdBy"`
	EndsAt    time.Time `json:"endsAt"`
	StartsAt  time.Time `json:"startsAt"`
	Matchers  []KV      `json:"matchers"`
}

type CRUDSilenceData struct {
	ID        string `json:"id"`
	CreatedBy string `json:"createdBy"`
	StartsAt  string `json:"startsAt"`
	EndsAt    string `json:"endsAt"`
	Comment   string `json:"comment"`
	Matchers  []KV   `json:"matchers"`
}
