/* eslint-disable */

import request from "@/utils/request";

export function getImageList(params) {
  return request({
    url: "/api/container/image/",
    method: "get",
    params: params,
  });
}

export function getImageTagList(params) {
  return request({
    url: "/api/container/image_tag/",
    method: "get",
    params: params,
  });
}

export function createImage(data) {
  return request({
    url: "/api/container/image/",
    method: "post",
    data: data,
  });
}

export function updateImage(id, data) {
  return request({
    url: "/api/container/image/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteImage(id) {
  return request({
    url: "/api/container/image/" + id + "/",
    method: "delete",
  });
}
