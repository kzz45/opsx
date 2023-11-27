/* eslint-disable */

import request from "@/utils/request";

export function getHistoryList(params) {
  return request({
    url: "/api/public/history/",
    method: "get",
    params: params,
  });
}

export function createHistory(data) {
  return request({
    url: "/api/public/history/",
    method: "post",
    data: data,
  });
}

export function updateHistory(id, data) {
  return request({
    url: "/api/public/history/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteHistory(id) {
  return request({
    url: "/api/public/history/" + id + "/",
    method: "delete",
  });
}
