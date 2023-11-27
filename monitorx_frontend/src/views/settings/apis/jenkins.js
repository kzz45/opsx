/* eslint-disable */

import request from "@/utils/request";

export function getJenkinsList(params) {
  return request({
    url: "/api/public/jenkins/",
    method: "get",
    params: params,
  });
}

export function createJenkins(data) {
  return request({
    url: "/api/public/jenkins/",
    method: "post",
    data: data,
  });
}

export function createJenkinsFolders(data) {
  return request({
    url: "/api/public/jenkins/create_folders/",
    method: "post",
    data: data,
  });
}

export function createJenkinsItem(data) {
  return request({
    url: "/api/public/jenkins/create_item/",
    method: "post",
    data: data,
  });
}


export function getJenkinsJobURL(data) {
  return request({
    url: "/api/public/jenkins/get_job_url/",
    method: "post",
    data: data,
  });
}

export function updateJenkins(id, data) {
  return request({
    url: "/api/public/jenkins/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteJenkins(id) {
  return request({
    url: "/api/public/jenkins/" + id + "/",
    method: "delete",
  });
}
