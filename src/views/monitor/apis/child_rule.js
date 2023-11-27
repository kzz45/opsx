/* eslint-disable */

import request from "@/utils/request";

export function getAlertRuleChildList(params) {
  return request({
    url: "/api/monitor/alert_rule_child/",
    method: "get",
    params: params,
  });
}

export function createAlertRuleChild(data) {
  return request({
    url: "/api/monitor/alert_rule_child/",
    method: "post",
    data: data,
  });
}

export function updateAlertRuleChild(id, data) {
  return request({
    url: "/api/monitor/alert_rule_child/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteAlertRuleChild(id) {
  return request({
    url: "/api/monitor/alert_rule_child/" + id + "/",
    method: "delete",
  });
}
