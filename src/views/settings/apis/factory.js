/* eslint-disable */

import request from "@/utils/request";

export function getFactoryList(params) {
  return request({
    url: "/api/public/factory/",
    method: "get",
    params: params,
  });
}

export function createFactory(data) {
  return request({
    url: "/api/public/factory/",
    method: "post",
    data: data,
  });
}

export function updateFactory(id, data) {
  return request({
    url: "/api/public/factory/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteFactory(id) {
  return request({
    url: "/api/public/factory/" + id + "/",
    method: "delete",
  });
}
