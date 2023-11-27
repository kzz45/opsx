/* eslint-disable */

import request from "@/utils/request";

export function getReceiverList(params) {
  return request({
    url: "/api/monitor/receiver/",
    method: "get",
    params: params,
  });
}

export function createReceiver(data) {
  return request({
    url: "/api/monitor/receiver/",
    method: "post",
    data: data,
  });
}

export function updateReceiver(id, data) {
  return request({
    url: "/api/monitor/receiver/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteReceiver(id) {
  return request({
    url: "/api/monitor/receiver/" + id + "/",
    method: "delete",
  });
}
