/* eslint-disable */

import request from "@/utils/request";

export function getAlertRouteChildList(params) {
  return request({
    url: "/api/monitor/alert_route_child/",
    method: "get",
    params: params,
  });
}

export function createAlertRouteChild(data) {
  return request({
    url: "/api/monitor/alert_route_child/",
    method: "post",
    data: data,
  });
}

export function updateAlertRouteChild(id, data) {
  return request({
    url: "/api/monitor/alert_route_child/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteAlertRouteChild(id) {
  return request({
    url: "/api/monitor/alert_route_child/" + id + "/",
    method: "delete",
  });
}
