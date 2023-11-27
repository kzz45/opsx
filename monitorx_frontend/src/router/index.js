/* eslint-disable */

import Vue from "vue";
import Router from "vue-router";

Vue.use(Router);

import Layout from "@/layout";
import jobsRoute from "@/router/jobs";
import testRoute from "@/router/test";
import billsRoute from "@/router/bills";
import extendRoute from "@/router/extend";
import monitorRoute from "@/router/monitor";
import settingsRoute from "@/router/settings";
import containerRoute from "@/router/container";

export const constantRoutes = [
  {
    path: "/",
    component: Layout,
    redirect: "/dashboard",
    children: [
      {
        path: "dashboard",
        component: () => import("@/views/dashboard/index"),
        name: "Dashboard",
        meta: {
          title: "首页",
          icon: "home",
          affix: true,
        },
      },
    ],
  },
  {
    path: "/login",
    component: () => import("@/views/login/index"),
    hidden: true,
  },

  {
    path: "/404",
    component: () => import("@/views/404"),
    hidden: true,
  },
];

export const asyncRoutes = [
  // ...jobsRoute,
  ...monitorRoute,
  // ...containerRoute,
  ...settingsRoute,
  // ...extendRoute,
  // ...billsRoute,
  // ...testRoute,
  // {
  //   path: "系统文档",
  //   component: Layout,
  //   children: [
  //     {
  //       path: "https://kzz45.github.io/blogs/",
  //       meta: { title: "系统文档", icon: "document" },
  //     },
  //   ],
  // },
  {
    path: "*",
    redirect: "/404",
    hidden: true,
  },
];
const createRouter = () =>
  new Router({
    mode: "history", // require service support
    scrollBehavior: () => ({
      y: 0,
    }),
    // routes: constantRoutes.concat(asyncRoutes),
    routes: constantRoutes,
  });

const router = createRouter();

export function resetRouter() {
  const newRouter = createRouter();
  router.matcher = newRouter.matcher; // reset router
}

export default router;
