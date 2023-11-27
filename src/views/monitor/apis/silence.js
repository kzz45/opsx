/* eslint-disable */

import request from "@/utils/request";

export function getSilenceList(params) {
  return request({
    url: "/api/monitor/silence/",
    method: "get",
    params: params,
  });
}

export function createSilence(data) {
  return request({
    url: "/api/monitor/silence/",
    method: "post",
    data: data,
  });
}

export function updateSilence(id, data) {
  return request({
    url: "/api/monitor/silence/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteSilence(id) {
  return request({
    url: "/api/monitor/silence/" + id + "/",
    method: "delete",
  });
}
