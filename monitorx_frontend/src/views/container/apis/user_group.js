/* eslint-disable */

import request from "@/utils/request";

export function getUserGroupList(params) {
  return request({
    url: "/api/public/user_group/",
    method: "get",
    params: params,
  });
}

export function createUserGroup(data) {
  return request({
    url: "/api/public/user_group/",
    method: "post",
    data: data,
  });
}

export function updateUserGroup(id, data) {
  return request({
    url: "/api/public/user_group/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteUserGroup(id) {
  return request({
    url: "/api/public/user_group/" + id + "/",
    method: "delete",
  });
}
