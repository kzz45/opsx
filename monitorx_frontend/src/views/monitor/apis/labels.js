/* eslint-disable */

import request from "@/utils/request";

export function getLabelsList(params) {
  return request({
    url: "/api/monitor/labels/",
    method: "get",
    params: params,
  });
}

export function createLabels(data) {
  return request({
    url: "/api/monitor/labels/",
    method: "post",
    data: data,
  });
}

export function updateLabels(id, data) {
  return request({
    url: "/api/monitor/labels/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteLabels(id) {
  return request({
    url: "/api/monitor/labels/" + id + "/",
    method: "delete",
  });
}
