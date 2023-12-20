/* eslint-disable */

import Layout from "@/layout";

const monitorRoute = [
  {
    path: "/monitor",
    name: "Monitor",
    component: Layout,
    alwaysShow: true,
    redirect: "/monitor/alert_wall",
    meta: {
      title: "监控平台",
      icon: "monitor"
    },
    children: [
      {
        // hidden: true,
        path: "dashboard_list",
        name: "DashboardList",
        component: () => import("@/views/monitor/dashboard_list"),
        meta: {
          title: "大盘列表",
          icon: "dashboard_list"
        }
      },
      {
        path: "alert_wall",
        name: "AlertWall",
        component: () => import("@/views/monitor/alert_wall"),
        meta: {
          title: "告警大屏",
          icon: "alert"
        }
      },
      {
        path: "silence",
        name: "Silence",
        component: () => import("@/views/monitor/silence"),
        meta: {
          title: "告警维护",
          icon: "silence"
        }
      },
      {
        hidden: true,
        path: "malfunction",
        name: "Malfunction",
        component: () => import("@/views/monitor/alert_malfunction"),
        meta: {
          title: "告警故障",
          icon: "malfunction"
        }
      },
      {
        path: "instance",
        name: "InstanceObject",
        component: () => import("@/views/monitor/instance/instance_obj"),
        meta: {
          title: "监控对象",
          icon: "instance_object"
        }
      },
      {
        path: "config",
        name: "AlertConfig",
        component: () => import("@/views/monitor/alert_config/alert_config"),
        meta: {
          title: "监控配置",
          icon: "alert_config"
        }
      },
      {
        hidden: true,
        path: "task_detail",
        name: "TaskDetail",
        component: () => import("@/views/monitor/alert_config/task_detail"),
        meta: {
          title: "任务详情",
          icon: "task_manage"
        }
      },
      {
        path: "settings",
        name: "MonitorSettings",
        component: () => import("@/views/monitor/settings/settings"),
        meta: {
          title: "监控管理",
          icon: "settings"
        }
      },
      {
        hidden: true,
        path: "server",
        name: "CollectServer",
        component: () => import("@/views/monitor/settings/server"),
        meta: {
          title: "采集节点",
          icon: "collect"
        }
      },
    ]
  }
];

export default monitorRoute;
