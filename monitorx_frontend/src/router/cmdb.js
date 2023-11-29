/* eslint-disable */

import Layout from "@/layout";

const cmdbRoute = [
  {
    path: "/cmdb",
    name: "CMDB",
    component: Layout,
    // alwaysShow: true,
    redirect: "/cmdb/machine",
    meta: {
      title: "资源管理",
      icon: "cmdb"
    },
    children: [
      {
        path: "machine",
        name: "Machine",
        component: () => import("@/views/cmdb/machine"),
        meta: {
          title: "机器",
          icon: "ecs"
        }
      },
      {
        // hidden: true,
        path: "redis",
        name: "Redis",
        component: () => import("@/views/cmdb/redis"),
        meta: {
          title: "Redis",
          icon: "redis"
        }
      },
      {
        // hidden: true,
        path: "mysql",
        name: "MySQL",
        component: () => import("@/views/cmdb/mysql"),
        meta: {
          title: "MySQL",
          icon: "mysql"
        }
      },
      {
        // hidden: true,
        path: "mongodb",
        name: "MongoDB",
        component: () => import("@/views/cmdb/mongodb"),
        meta: {
          title: "Mongo",
          icon: "mongodb"
        }
      },
      {
        // hidden: true,
        path: "slb",
        name: "SLB",
        component: () => import("@/views/cmdb/slb"),
        meta: {
          title: "负载均衡",
          icon: "slb"
        }
      },
      {
        hidden: true,
        path: "zone_list",
        name: "ZoneList",
        component: () => import("@/views/cmdb/zone_list"),
        meta: {
          title: "Zone管理",
          icon: "zone"
        }
      },
      {
        hidden: true,
        path: "subnet_list",
        name: "SubnetList",
        component: () => import("@/views/cmdb/subnet_list"),
        meta: {
          title: "子网管理",
          icon: "subnet"
        }
      },
      {
        hidden: true,
        path: "security_list",
        name: "SecurityList",
        component: () => import("@/views/cmdb/security_list"),
        meta: {
          title: "安全组管理",
          icon: "security_group"
        }
      },
      {
        hidden: true,
        path: "security_rule_list",
        name: "securityRuleList",
        component: () => import("@/views/cmdb/security_rule_list"),
        meta: {
          title: "安全组规则管理",
          icon: "security_group"
        }
      },
      {
        hidden: true,
        path: "domain_record_list",
        name: "DomainRecordList",
        component: () => import("@/views/cmdb/domain_record"),
        meta: {
          title: "域名记录值",
          icon: "security_group"
        }
      },
      {
        hidden: true,
        path: "domain_operation_record",
        name: "DomainOperationRecord",
        component: () => import("@/views/cmdb/domain_operation_record"),
        meta: {
          title: "域名操作记录",
          icon: "security_group"
        }
      },
      {
        hidden: true,
        path: "domain_ssl_check_port",
        name: "DomainCheckPortList",
        component: () => import("@/views/cmdb/domain_ssl_check_port"),
        meta: {
          title: "特殊端口域名",
          icon: "security_group"
        }
      },
      {
        hidden: true,
        path: "domain_ssl_alert_focus",
        name: "DomainAlertFocus",
        component: () => import("@/views/cmdb/domain_ssl_alert_focus"),
        meta: {
          title: "报警关注列表",
          icon: "security_group"
        }
      }
    ]
  }
];

export default cmdbRoute;
