/* eslint-disable */

import request from "@/utils/request";

export function getBuildingList(params) {
  return request({
    url: "/api/public/building/",
    method: "get",
    params: params,
  });
}

export function createBuilding(data) {
  return request({
    url: "/api/public/building/",
    method: "post",
    data: data,
  });
}

export function updateBuilding(id, data) {
  return request({
    url: "/api/public/building/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteBuilding(id) {
  return request({
    url: "/api/public/building/" + id + "/",
    method: "delete",
  });
}
