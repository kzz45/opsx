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
      icon: "monitor",
    },
    children: [
      {
        path: "dashboard_list",
        name: "DashboardList",
        component: () => import("@/views/monitor/dashboard_list"),
        meta: {
          title: "监控大盘",
          icon: "dashboard_list",
        },
      },
      {
        path: "alert_wall",
        name: "AlertWall",
        component: () => import("@/views/monitor/alert_wall"),
        meta: {
          title: "告警大屏",
          icon: "alert",
        },
      },
      {
        path: "malfunction",
        name: "Malfunction",
        component: () => import("@/views/monitor/alert_malfunction"),
        meta: {
          title: "告警故障",
          icon: "malfunction",
        },
      },
      {
        path: "silence",
        name: "Silence",
        component: () => import("@/views/monitor/silence"),
        meta: {
          title: "告警维护",
          icon: "silence",
        },
      },
      {
        path: "instance",
        name: "InstanceObject",
        component: () => import("@/views/monitor/instance/"),
        meta: {
          title: "监控对象",
          icon: "instance_object",
        },
      },
      {
        path: "tasks",
        name: "AlertTasks",
        component: () => import("@/views/monitor/tasks/"),
        meta: {
          title: "监控任务",
          icon: "tasks",
        },
      },
      {
        path: "config",
        name: "AlertConfig",
        component: () => import("@/views/monitor/alert_config/"),
        meta: {
          title: "监控配置",
          icon: "alert_config",
        },
      },
      {
        path: "settings",
        name: "MonitorSettings",
        component: () => import("@/views/monitor/settings/"),
        meta: {
          title: "监控管理",
          icon: "settings",
          roles: ["admin"],
        },
      },
    ],
  },
];

export default monitorRoute;
