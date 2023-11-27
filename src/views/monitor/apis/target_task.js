/* eslint-disable */

import request from "@/utils/request";

export function getTargetTaskList(params) {
  return request({
    url: "/api/monitor/target_task/",
    method: "get",
    params: params,
  });
}

export function createTargetTask(data) {
  return request({
    url: "/api/monitor/target_task/",
    method: "post",
    data: data,
  });
}

export function updateTargetTask(id, data) {
  return request({
    url: "/api/monitor/target_task/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteTargetTask(id) {
  return request({
    url: "/api/monitor/target_task/" + id + "/",
    method: "delete",
  });
}
