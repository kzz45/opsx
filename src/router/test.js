/* eslint-disable */

import Layout from "@/layout";

const testRoute = [
  {
    path: "/test",
    name: "Test",
    component: Layout,
    redirect: "/grafana",
    children: [
      {
        path: "grafana",
        name: "Grafana",
        component: () => import("@/views/test/"),
        meta: {
          title: "本地测试",
          icon: "test",
        },
      },
    ],
  },
];

export default testRoute;
