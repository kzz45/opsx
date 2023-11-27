/* eslint-disable */

import request from "@/utils/request";

export function getChartList(params) {
  return request({
    url: "/api/container/chart/",
    method: "get",
    params: params,
  });
}

export function getChartTagList(params) {
  return request({
    url: "/api/container/chart_tag/",
    method: "get",
    params: params,
  });
}

export function createChart(data) {
  return request({
    url: "/api/container/chart/",
    method: "post",
    data: data,
  });
}

export function updateChart(id, data) {
  return request({
    url: "/api/container/chart/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteChart(id) {
  return request({
    url: "/api/container/chart/" + id + "/",
    method: "delete",
  });
}
