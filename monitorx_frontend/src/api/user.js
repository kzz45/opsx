/* eslint-disable */

import request from "@/utils/request";

export function login(username, password) {
  const data = {
    username,
    password,
  };
  return request({
    url: "/api/login/",
    method: "post",
    data,
  });
}

export function getInfo(params) {
  return request({
    url: "/api/user/",
    method: "get",
    params: params,
  });
}
export function logout() {
  return request({
    url: "/api/logout/",
    method: "post",
  });
}
