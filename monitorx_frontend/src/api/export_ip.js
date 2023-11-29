/* eslint-disable */

import request from "@/utils/request";

export function getExportIPList(params) {
  return request({
    url: "/api/cmdb/export_ip/",
    method: "get",
    timeout: 10 * 1000,
    params: params
  });
}

export function createExportIP(data) {
  return request({
    url: "/api/cmdb/export_ip/",
    method: "post",
    data: data
  });
}

export function updateExportIPID(id, data) {
  return request({
    url: "/api/cmdb/export_ip/" + id + "/",
    method: "patch",
    data: data
  });
}

export function deleteExportIPByID(id, data) {
  return request({
    url: "/api/cmdb/export_ip/" + id + "/",
    method: "delete",
    data: data
  });
}
