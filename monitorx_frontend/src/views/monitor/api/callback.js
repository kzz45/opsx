/* eslint-disable */

import request from "@/utils/request";

export function getCallbackList(params) {
  return request({
    url: "/api/monitor/callback/",
    method: "get",
    params: params
  });
}

export function createCallback(data) {
  return request({
    url: "/api/monitor/callback/",
    method: "post",
    data: data
  });
}

export function updateCallbackByID(id, data) {
  return request({
    url: "/api/monitor/callback/" + id + "/",
    method: "patch",
    data: data
  });
}

export function deleteCallbackByID(id) {
  return request({
    url: "/api/monitor/callback/" + id + "/",
    method: "delete"
  });
}
