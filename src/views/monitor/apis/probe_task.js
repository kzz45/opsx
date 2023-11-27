/* eslint-disable */

import request from "@/utils/request";

export function getProbeTaskList(params) {
  return request({
    url: "/api/monitor/probe_task/",
    method: "get",
    params: params,
  });
}

export function createProbeTask(data) {
  return request({
    url: "/api/monitor/probe_task/",
    method: "post",
    data: data,
  });
}

export function updateProbeTask(id, data) {
  return request({
    url: "/api/monitor/probe_task/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteProbeTask(id) {
  return request({
    url: "/api/monitor/probe_task/" + id + "/",
    method: "delete",
  });
}
