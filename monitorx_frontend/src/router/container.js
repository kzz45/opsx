/* eslint-disable */

import Layout from "@/layout";

const containerRoute = [
  {
    path: "/container",
    name: "Container",
    component: Layout,
    alwaysShow: true,
    redirect: "/container/overview",
    meta: {
      title: "容器平台",
      icon: "kubernetes",
    },
    children: [
      {
        path: "overview",
        name: "ContainerOverview",
        component: () => import("@/views/container/overview"),
        meta: {
          title: "应用列表",
          icon: "application",
          noCache: true,
        },
      },
      {
        hidden: true,
        path: "app_info",
        name: "ContainerAppInfo",
        component: () => import("@/views/container/overview/app_info"),
        meta: {
          title: "应用详情",
          icon: "application",
          noCache: true,
        },
      },
      {
        path: "settings",
        name: "ClusterSettings",
        component: () => import("@/views/container/cluster"),
        meta: {
          title: "集群管理",
          icon: "cluster_settings",
          noCache: true,
        },
      },
      {
        hidden: true,
        path: "cluster_ns",
        name: "ClusterClusterNs",
        component: () => import("@/views/container/cluster/cluster_ns"),
        meta: {
          title: "集群空间",
        },
      },
      {
        hidden: true,
        path: "registry_ns",
        name: "ClusterRegistryNs",
        component: () => import("@/views/container/cluster/registry_ns"),
        meta: {
          title: "仓库空间",
        },
      },
    ],
  },
];

export default containerRoute;
