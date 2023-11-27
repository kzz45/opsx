/* eslint-disable */

import request from "@/utils/request";

export function getOperatorList(params) {
  return request({
    url: "/api/public/operator/",
    method: "get",
    params: params,
  });
}

export function createOperator(data) {
  return request({
    url: "/api/public/operator/",
    method: "post",
    data: data,
  });
}

export function updateOperator(id, data) {
  return request({
    url: "/api/public/operator/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteOperator(id) {
  return request({
    url: "/api/public/operator/" + id + "/",
    method: "delete",
  });
}
