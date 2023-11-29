/* eslint-disable */

import request from "@/utils/request";

export function login(username, password) {
  const data = {
    username,
    password
  };
  return request({
    url: "/api/login/",
    method: "post",
    data
  });
}

export function getInfo(params) {
  return request({
    url: "/api/user/",
    method: "get",
    params: params
  });
}

export function logout() {
  return request({
    url: "/api/logout/",
    method: "post"
  });
}

export function getUserList(params) {
  return request({
    url: "/api/user/",
    method: "get",
    params: params
  });
}

export function getUserGroups() {
  return request({
    url: "/api/user_group/",
    method: "get"
  });
}

export function createUserGroups(data) {
  return request({
    url: "/api/user_group/",
    method: "post",
    data: data
  });
}

export function deleteUserGroup(id) {
  return request({
    url: `/api/user_group/${id}`,
    method: "delete"
  });
}

export function updateUserGroup(id, data) {
  return request({
    url: `/api/user_group/${id}/`,
    method: "patch",
    data: data
  });
}

export function createUser(data) {
  return request({
    url: "/api/user/",
    method: "post",
    data: data
  });
}

export function updateUserByID(id, data) {
  return request({
    url: "/api/user/" + id + "/",
    method: "patch",
    data: data
  });
}

export function deleteUserByID(id) {
  return request({
    url: "/api/user/" + id + "/",
    method: "delete"
  });
}
