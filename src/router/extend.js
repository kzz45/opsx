/* eslint-disable */

import Layout from "@/layout";

const extendRoute = [
  {
    path: "/extend",
    name: "Extend",
    component: Layout,
    alwaysShow: true,
    meta: {
      title: "扩展服务",
      icon: "extend",
    },
    redirect: "/extend/sls",
    children: [
      {
        path: "sls",
        name: "Sls",
        component: () => import("@/views/extend/sls/"),
        meta: {
          title: "日志服务",
          icon: "logs",
        },
      },
      {
        path: "exportip",
        name: "ExportIP",
        component: () => import("@/views/extend/exportip/"),
        meta: {
          title: "出口地址",
          icon: "export_ip",
        },
      },
      {
        path: "bill",
        name: "Bill",
        component: () => import("@/views/bills/"),
        meta: {
          title: "账单管理",
          icon: "bills",
        },
      },
    ],
  },
];

export default extendRoute;
