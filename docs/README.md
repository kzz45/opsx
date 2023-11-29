# 操作说明

## 操作步骤

### 新增用户和用户组

![新增用户](./新增用户.png)

![新增权限分组](./新增权限分组.png)

### 新增产品

![新增产品](./新增产品.png)

### 监控管理

![新增采集组](./新增采集组.png)

![新增采集点](./新增采集点.png)

![新增实例类型](./新增实例类型.png)

![新增标签](./新增标签.png)

![新增告警规则类型](./新增告警规则类型.png)

### 监控配置

![新增监控任务](./新增监控任务.png)

![新增监控子任务](./新增监控子任务.png)

![告警规则](./新增告警规则.png)

![告警通知组](./新增告警通知组.png)

![新增告警路由](./新增告警路由.png)

### 监控对象

![监控对象](./录入监控对象.png)

### 告警大屏

![告警大屏](./告警大屏.png)

---

### 新增 Grafana 数据源

![新增数据源](新增数据源.png)

### 导入 Dashboard

导入 Grafana Dashboard，我们采用 https://grafana.com/grafana/dashboards/1860-node-exporter-full/ ，但是还需要稍作变量调整

![dashboard变量调整](dashboard变量调整.png)

或者直接修改 dashboard 的 JSON 模型， 复制文件 ./docs/node_exporter_full.json

![dashboard_json_model](dashboard_json_model.png)

https://prometheus.io/download/

![download](./download.png)

![node_exporter](./node_exporter.png)
