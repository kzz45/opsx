/* eslint-disable */

import Vue from "vue";
import Router from "vue-router";

Vue.use(Router);

import Layout from "@/layout";
import cmdbRoute from "@/router/cmdb";
import monitorRoute from "@/router/monitor";
import settingRoute from "@/router/settings";

export const constantRoutes = [
  {
    hidden: true,
    path: "/login",
    component: () => import("@/views/login/index")
  },
  {
    hidden: true,
    path: "/auth-redirect",
    component: () => import("@/views/login/auth-redirect")
  },
  {
    hidden: true,
    path: "/404",
    component: () => import("@/views/404")
  },
  {
    hidden: true,
    path: "/logout",
    component: () => import("@/views/logout")
  },
  {
    path: "/",
    component: Layout,
    redirect: "/dashboard",
    children: [
      {
        path: "dashboard",
        name: "Dashboard",
        component: () => import("@/views/dashboard/index"),
        meta: {
          title: "首页",
          icon: "home"
        }
      }
    ]
  },
  {
    path: "*",
    redirect: "/404",
    hidden: true
  }
];

export const asyncRouter = [...cmdbRoute, ...monitorRoute, ...settingRoute];
const createRouter = () =>
  new Router({
    mode: "history",
    scrollBehavior: () => ({
      y: 0
    }),
    routes: constantRoutes.concat(asyncRouter)
  });

const router = createRouter();

export default router;
