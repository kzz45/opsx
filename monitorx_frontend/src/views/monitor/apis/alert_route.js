/* eslint-disable */

import request from "@/utils/request";

export function getAlertRouteList(params) {
  return request({
    url: "/api/monitor/alert_route/",
    method: "get",
    params: params,
  });
}

export function createAlertRoute(data) {
  return request({
    url: "/api/monitor/alert_route/",
    method: "post",
    data: data,
  });
}

export function updateAlertRoute(id, data) {
  return request({
    url: "/api/monitor/alert_route/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteAlertRoute(id) {
  return request({
    url: "/api/monitor/alert_route/" + id + "/",
    method: "delete",
  });
}
