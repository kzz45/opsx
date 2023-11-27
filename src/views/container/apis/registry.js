/* eslint-disable */

import request from "@/utils/request";

export function getRegistryList(params) {
  return request({
    url: "/api/container/registry/",
    method: "get",
    params: params,
  });
}

export function getRegistryNsList(params) {
  return request({
    url: "/api/container/registry_ns/",
    method: "get",
    params: params,
  });
}

export function createRegistry(data) {
  return request({
    url: "/api/container/registry/",
    method: "post",
    data: data,
  });
}

export function updateRegistry(id, data) {
  return request({
    url: "/api/container/registry/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteRegistry(id) {
  return request({
    url: "/api/container/registry/" + id + "/",
    method: "delete",
  });
}
