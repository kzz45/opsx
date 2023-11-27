/* eslint-disable */

import request from "@/utils/request";

export function getGroupList(params) {
  return request({
    url: "/api/group/",
    method: "get",
    params: params,
  });
}

export function createGroup(data) {
  return request({
    url: "/api/group/",
    method: "post",
    data: data,
  });
}

export function updateGroup(id, data) {
  return request({
    url: "/api/group/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteGroup(id) {
  return request({
    url: "/api/group/" + id + "/",
    method: "delete",
  });
}
