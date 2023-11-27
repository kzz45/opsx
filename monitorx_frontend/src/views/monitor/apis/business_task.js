/* eslint-disable */

import request from "@/utils/request";

export function getBusinessTaskList(params) {
  return request({
    url: "/api/monitor/business_task/",
    method: "get",
    params: params,
  });
}

export function createBusinessTask(data) {
  return request({
    url: "/api/monitor/business_task/",
    method: "post",
    data: data,
  });
}

export function updateBusinessTask(id, data) {
  return request({
    url: "/api/monitor/business_task/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteBusinessTask(id) {
  return request({
    url: "/api/monitor/business_task/" + id + "/",
    method: "delete",
  });
}
