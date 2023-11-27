/* eslint-disable */

import request from "@/utils/request";

export function getUtilsList(params) {
  return request({
    url: "/api/bills/utils/",
    method: "get",
    params: params
  });
}

export function getProjectList(params) {
  return request({
    url: "/api/bills/utils/project_list/",
    method: "get",
    params: params,
  });
}

export function createUtils(data) {
  return request({
    url: "/api/bills/utils/",
    method: "post",
    data: data
  });
}

export function updateUtils(id, data) {
  return request({
    url: "/api/bills/utils/" + id + "/",
    method: "patch",
    data: data
  });
}

export function deleteUtils(id) {
  return request({
    url: "/api/bills/utils/" + id + "/",
    method: "delete"
  });
}
