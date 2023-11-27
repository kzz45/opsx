/* eslint-disable */

import request from "@/utils/request";

export function getGitlabList(params) {
  return request({
    url: "/api/public/gitlab/",
    method: "get",
    params: params,
  });
}

export function createGitlab(data) {
  return request({
    url: "/api/public/gitlab/",
    method: "post",
    data: data,
  });
}

export function updateGitlab(id, data) {
  return request({
    url: "/api/public/gitlab/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteGitlab(id) {
  return request({
    url: "/api/public/gitlab/" + id + "/",
    method: "delete",
  });
}
