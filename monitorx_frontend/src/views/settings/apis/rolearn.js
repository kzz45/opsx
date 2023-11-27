/* eslint-disable */

import request from "@/utils/request";

export function getAssumeRoleList(params) {
  return request({
    url: "/api/public/assumeRole/",
    method: "get",
    params: params,
  });
}

export function createAssumeRole(data) {
  return request({
    url: "/api/public/assumeRole/",
    method: "post",
    data: data,
  });
}

export function updateAssumeRole(id, data) {
  return request({
    url: "/api/public/assumeRole/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteAssumeRole(id) {
  return request({
    url: "/api/public/assumeRole/" + id + "/",
    method: "delete",
  });
}
