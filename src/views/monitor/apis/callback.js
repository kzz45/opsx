/* eslint-disable */

import request from "@/utils/request";

export function getCallBackList(params) {
  return request({
    url: "/api/monitor/callback/",
    method: "get",
    params: params,
  });
}

export function createCallBack(data) {
  return request({
    url: "/api/monitor/callback/",
    method: "post",
    data: data,
  });
}

export function updateCallBack(id, data) {
  return request({
    url: "/api/monitor/callback/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteCallBack(id) {
  return request({
    url: "/api/monitor/callback/" + id + "/",
    method: "delete",
  });
}
