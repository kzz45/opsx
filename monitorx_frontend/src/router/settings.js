/* eslint-disable */

import Layout from "@/layout";

const settingRoute = [
  {
    path: "/settings",
    name: "配置管理",
    component: Layout,
    alwaysShow: true,
    redirect: "/settings/rbac",
    meta: {
      title: "配置管理",
      icon: "settings"
    },
    children: [
      {
        path: "rbac",
        name: "RBAC",
        component: () => import("@/views/settings/rbac"),
        meta: {
          title: "角色权限",
          icon: "role_perm"
        }
      },
      {
        path: "product",
        name: "Product",
        component: () => import("@/views/settings/product"),
        meta: {
          title: "产品管理",
          icon: "product",
          roles: ["admin"]
        }
      },
      {
        // hidden: true,
        path: "factory",
        name: "Factory",
        component: () => import("@/views/settings/factory"),
        meta: {
          title: "云厂管理",
          icon: "factory"
        }
      },
      {
        hidden: true,
        path: "profile",
        name: "Profile",
        component: () => import("@/views/settings/profile"),
        meta: {
          title: "个人信息",
          icon: "profile"
        }
      }
    ]
  }
];

export default settingRoute;
