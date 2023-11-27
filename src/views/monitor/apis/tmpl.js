/* eslint-disable */

import request from "@/utils/request";

export function getTmplList(params) {
  return request({
    url: "/api/monitor/tmpl/",
    method: "get",
    params: params,
  });
}

export function createTmpl(data) {
  return request({
    url: "/api/monitor/tmpl/",
    method: "post",
    data: data,
  });
}

export function updateTmpl(id, data) {
  return request({
    url: "/api/monitor/tmpl/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteTmpl(id) {
  return request({
    url: "/api/monitor/tmpl/" + id + "/",
    method: "delete",
  });
}
