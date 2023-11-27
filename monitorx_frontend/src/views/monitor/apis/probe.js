/* eslint-disable */

import request from "@/utils/request";

export function getProbeList(params) {
  return request({
    url: "/api/monitor/probe/",
    method: "get",
    params: params,
  });
}

export function createProbe(data) {
  return request({
    url: "/api/monitor/probe/",
    method: "post",
    data: data,
  });
}

export function updateProbe(id, data) {
  return request({
    url: "/api/monitor/probe/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteProbe(id) {
  return request({
    url: "/api/monitor/probe/" + id + "/",
    method: "delete",
  });
}
