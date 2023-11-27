/* eslint-disable */

import request from "@/utils/request";

export function getHelmConfigList(params) {
  return request({
    url: "/api/container/helm_config/",
    method: "get",
    params: params,
  });
}

export function createHelmConfig(data) {
  return request({
    url: "/api/container/helm_config/",
    method: "post",
    data: data,
  });
}

export function updateHelmConfig(id, data) {
  return request({
    url: "/api/container/helm_config/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteHelmConfig(id) {
  return request({
    url: "/api/container/helm_config/" + id + "/",
    method: "delete",
  });
}
