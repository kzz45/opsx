/* eslint-disable */

import request from "@/utils/request";

export function getCurrentAlertList(params) {
  return request({
    url: "/api/monitor/current_alert/",
    method: "get",
    params: params,
  });
}

export function getCurrentAlertWallList(params) {
  return request({
    url: "/api/monitor/current_alert/alert_wall/",
    method: "get",
    params: params,
  });
}

export function createCurrentAlert(data) {
  return request({
    url: "/api/monitor/current_alert/",
    method: "post",
    data: data,
  });
}

export function updateCurrentAlert(id, data) {
  return request({
    url: "/api/monitor/current_alert/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteCurrentAlert(id) {
  return request({
    url: "/api/monitor/current_alert/" + id + "/",
    method: "delete",
  });
}
