/* eslint-disable */

import request from "@/utils/request";

export function getReleaseList(params) {
  return request({
    url: "/api/container/release/",
    method: "get",
    params: params,
  });
}

export function createRelease(data) {
  return request({
    url: "/api/container/release/",
    method: "post",
    data: data,
  });
}

export function createReleaseConfig(data) {
  return request({
    url: "/api/container/release/create_config/",
    method: "post",
    data: data,
  });
}

export function updateReleaseConfig(data) {
  return request({
    url: "/api/container/release/update_config/",
    method: "post",
    data: data,
  });
}

export function createReleaseHelmPackage(data) {
  return request({
    url: "/api/container/release/create_helm_package/",
    method: "post",
    data: data,
  });
}

export function installRelease(data) {
  return request({
    url: "/api/container/release/install_release/",
    method: "post",
    data: data,
  });
}

export function getReleaseInfo(data) {
  return request({
    url: "/api/container/release/get_release_info/",
    method: "post",
    data: data,
  });
}


export function updateRelease(id, data) {
  return request({
    url: "/api/container/release/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteRelease(id) {
  return request({
    url: "/api/container/release/" + id + "/",
    method: "delete",
  });
}
