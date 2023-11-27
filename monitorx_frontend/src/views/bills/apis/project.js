/* eslint-disable */

import request from "@/utils/request";

export function getProjectList(params) {
  return request({
    url: "/api/bills/project/",
    method: "get",
    params: params,
  });
}

export function createProject(data) {
  return request({
    url: "/api/bills/project/",
    method: "post",
    data: data,
  });
}

export function updateProject(id, data) {
  return request({
    url: "/api/bills/project/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteProject(id) {
  return request({
    url: "/api/bills/project/" + id + "/",
    method: "delete",
  });
}
