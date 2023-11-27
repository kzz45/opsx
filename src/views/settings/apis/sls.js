/* eslint-disable */

import request from "@/utils/request";

export function getSlsList(params) {
  return request({
    url: "/api/public/sls/",
    method: "get",
    params: params,
  });
}

export function createSls(data) {
  return request({
    url: "/api/public/sls/",
    method: "post",
    data: data,
  });
}

export function updateSls(id, data) {
  return request({
    url: "/api/public/sls/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteSls(id) {
  return request({
    url: "/api/public/sls/" + id + "/",
    method: "delete",
  });
}
