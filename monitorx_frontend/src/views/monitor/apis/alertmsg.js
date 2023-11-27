/* eslint-disable */

import request from "@/utils/request";

export function getAlertMsgList(params) {
  return request({
    url: "/api/monitor/alert_msg/",
    method: "get",
    params: params,
  });
}

export function createAlertMsg(data) {
  return request({
    url: "/api/monitor/alert_msg/",
    method: "post",
    data: data,
  });
}

export function updateAlertMsg(id, data) {
  return request({
    url: "/api/monitor/alert_msg/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteAlertMsg(id) {
  return request({
    url: "/api/monitor/alert_msg/" + id + "/",
    method: "delete",
  });
}
