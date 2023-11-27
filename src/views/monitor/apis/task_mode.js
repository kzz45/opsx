/* eslint-disable */

import request from "@/utils/request";

export function getTaskModeList(params) {
  return request({
    url: "/api/monitor/task_mode/",
    method: "get",
    params: params,
  });
}

export function createTaskMode(data) {
  return request({
    url: "/api/monitor/task_mode/",
    method: "post",
    data: data,
  });
}

export function updateTaskMode(id, data) {
  return request({
    url: "/api/monitor/task_mode/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteTaskMode(id) {
  return request({
    url: "/api/monitor/task_mode/" + id + "/",
    method: "delete",
  });
}
