/* eslint-disable */

import request from "@/utils/request";

export function getAlertRuleLevelList(params) {
  return request({
    url: "/api/monitor/alert_rule_level/",
    method: "get",
    params: params,
  });
}

export function createAlertRuleLevel(data) {
  return request({
    url: "/api/monitor/alert_rule_level/",
    method: "post",
    data: data,
  });
}

export function updateAlertRuleLevel(id, data) {
  return request({
    url: "/api/monitor/alert_rule_level/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteAlertRuleLevel(id) {
  return request({
    url: "/api/monitor/alert_rule_level/" + id + "/",
    method: "delete",
  });
}
