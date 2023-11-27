/* eslint-disable */

import request from "@/utils/request";

export function getAccountList(params) {
  return request({
    url: "/api/bills/account/",
    method: "get",
    params: params,
  });
}

export function createAccount(data) {
  return request({
    url: "/api/bills/account/",
    method: "post",
    data: data,
  });
}

export function updateAccount(id, data) {
  return request({
    url: "/api/bills/account/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteAccount(id) {
  return request({
    url: "/api/bills/account/" + id + "/",
    method: "delete",
  });
}
