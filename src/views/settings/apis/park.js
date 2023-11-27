/* eslint-disable */

import request from "@/utils/request";

export function getParkList(params) {
  return request({
    url: "/api/public/park/",
    method: "get",
    params: params,
  });
}

export function createPark(data) {
  return request({
    url: "/api/public/park/",
    method: "post",
    data: data,
  });
}

export function updatePark(id, data) {
  return request({
    url: "/api/public/park/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deletePark(id) {
  return request({
    url: "/api/public/park/" + id + "/",
    method: "delete",
  });
}
