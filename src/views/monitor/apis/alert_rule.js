/* eslint-disable */

import request from "@/utils/request";

export function getAlertRuleList(params) {
  return request({
    url: "/api/monitor/alert_rule/",
    method: "get",
    params: params,
  });
}

export function createAlertRule(data) {
  return request({
    url: "/api/monitor/alert_rule/",
    method: "post",
    data: data,
  });
}

export function updateAlertRule(id, data) {
  return request({
    url: "/api/monitor/alert_rule/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteAlertRule(id) {
  return request({
    url: "/api/monitor/alert_rule/" + id + "/",
    method: "delete",
  });
}
