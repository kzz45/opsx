/* eslint-disable */

import request from "@/utils/request";

export function getDashboardList(params) {
  return request({
    url: "/api/monitor/dashboard/",
    method: "get",
    params: params,
  });
}

export function createDashboard(data) {
  return request({
    url: "/api/monitor/dashboard/",
    method: "post",
    data: data,
  });
}

export function updateDashboard(id, data) {
  return request({
    url: "/api/monitor/dashboard/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteDashboard(id) {
  return request({
    url: "/api/monitor/dashboard/" + id + "/",
    method: "delete",
  });
}
