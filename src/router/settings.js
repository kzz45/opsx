/* eslint-disable */

import Layout from "@/layout";

const settingsRoute = [
  {
    path: "/settings",
    name: "settings",
    component: Layout,
    alwaysShow: true,
    redirect: "/settings/system",
    meta: {
      title: "系统管理",
      icon: "settings",
    },
    children: [
      {
        path: "rbac",
        name: "RBAC",
        component: () => import("@/views/settings/rbac"),
        meta: {
          title: "角色权限",
          icon: "role_perm",
        },
      },
      {
        path: "product",
        name: "Product",
        component: () => import("@/views/settings/product"),
        meta: {
          title: "产品项目",
          icon: "product",
        },
      },
      {
        path: "factory",
        name: "Factory",
        component: () => import("@/views/settings/factory"),
        meta: {
          title: "云厂管理",
          icon: "factory",
          roles: ["admin"],
        },
      },
      {
        path: "park",
        name: "Park",
        component: () => import("@/views/settings/park"),
        meta: {
          title: "园区管理",
          icon: "park",
          roles: ["admin"],
        },
      },
      {
        path: "audit",
        name: "Audit",
        component: () => import("@/views/settings/audit"),
        meta: {
          title: "操作审计",
          icon: "audit",
          roles: ["admin"],
        },
      },
      {
        hidden: true,
        path: "profile",
        name: "Profile",
        component: () => import("@/views/settings/profile"),
        meta: {
          title: "个人信息",
          icon: "profile",
        },
      },
    ],
  },
];

export default settingsRoute;
