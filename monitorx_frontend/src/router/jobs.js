/* eslint-disable */

import Layout from "@/layout";

const jobsRoute = [
  {
    path: "/jobs",
    name: "Jobs",
    component: Layout,
    alwaysShow: true,
    redirect: "/jobs/scripts",
    meta: {
      title: "作业平台",
      icon: "publish",
    },
    children: [
      {
        path: "scripts",
        name: "Scripts",
        component: () => import("@/views/jobs/scripts"),
        meta: {
          title: "脚本市场",
          icon: "script_library",
        },
      },
      {
        path: "execution",
        name: "Execution",
        component: () => import("@/views/jobs/execute"),
        meta: {
          title: "快速执行",
          icon: "execute",
        },
      },
      {
        hidden: true,
        path: "actions",
        name: "Actions",
        component: () => import("@/views/jobs/actions"),
        meta: {
          title: "动作管理",
          icon: "action_list",
        },
      },
      {
        path: "logs",
        name: "Logs",
        component: () => import("@/views/jobs/logs"),
        meta: {
          title: "作业日志",
          icon: "logs",
        },
        children: [],
      },
      {
        path: "settings",
        name: "JobsSettings",
        component: () => import("@/views/jobs/settings"),
        meta: {
          title: "作业配置",
          icon: "settings",
        },
      },
    ],
  },
];

export default jobsRoute;
