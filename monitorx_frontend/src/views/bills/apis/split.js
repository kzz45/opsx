/* eslint-disable */

import request from "@/utils/request";

export function getSplitList(params) {
  return request({
    url: "/api/bills/split/",
    method: "get",
    params: params
  });
}

export function createSplit(data) {
  return request({
    url: "/api/bills/split/",
    method: "post",
    data: data
  });
}

export function updateSplit(id, data) {
  return request({
    url: "/api/bills/split/" + id + "/",
    method: "patch",
    data: data
  });
}

export function deleteSplit(id) {
  return request({
    url: "/api/bills/split/" + id + "/",
    method: "delete"
  });
}
