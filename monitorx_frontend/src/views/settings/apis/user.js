/* eslint-disable */

import request from "@/utils/request";

export function getUserList(params) {
  return request({
    url: "/api/user/",
    method: "get",
    params: params,
  });
}

export function createUser(data) {
  return request({
    url: "/api/user/",
    method: "post",
    data: data,
  });
}

export function updateUser(id, data) {
  return request({
    url: "/api/user/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteUser(id) {
  return request({
    url: "/api/user/" + id + "/",
    method: "delete",
  });
}
