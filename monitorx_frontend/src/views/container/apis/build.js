/* eslint-disable */

import request from "@/utils/request";

export function getBuildList(params) {
  return request({
    url: "/api/container/build/",
    method: "get",
    params: params,
  });
}

export function createBuild(data) {
  return request({
    url: "/api/container/build/",
    method: "post",
    data: data,
  });
}

export function updateBuild(id, data) {
  return request({
    url: "/api/container/build/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteBuild(id) {
  return request({
    url: "/api/container/build/" + id + "/",
    method: "delete",
  });
}
