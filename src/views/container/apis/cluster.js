/* eslint-disable */

import request from "@/utils/request";

export function getClusterList(params) {
  return request({
    url: "/api/container/cluster/",
    method: "get",
    params: params,
  });
}

export function getClusterNsList(params) {
  return request({
    url: "/api/container/namespace/",
    method: "get",
    params: params,
  });
}

export function createCluster(data) {
  return request({
    url: "/api/container/cluster/",
    method: "post",
    data: data,
  });
}

export function updateCluster(id, data) {
  return request({
    url: "/api/container/cluster/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteCluster(id) {
  return request({
    url: "/api/container/cluster/" + id + "/",
    method: "delete",
  });
}
