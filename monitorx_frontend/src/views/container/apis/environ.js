/* eslint-disable */

import request from "@/utils/request";

export function getEnvironList(params) {
  return request({
    url: "/api/container/environ/",
    method: "get",
    params: params,
  });
}

export function createEnviron(data) {
  return request({
    url: "/api/container/environ/",
    method: "post",
    data: data,
  });
}

export function updateEnviron(id, data) {
  return request({
    url: "/api/container/environ/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteEnviron(id) {
  return request({
    url: "/api/container/environ/" + id + "/",
    method: "delete",
  });
}
