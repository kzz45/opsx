/* eslint-disable */

import Layout from "@/layout";

const billsRoute = [
  {
    path: "/bills",
    name: "Bills",
    component: Layout,
    redirect: "/bill",
    children: [
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

export default billsRoute;
