/* eslint-disable */

import request from "@/utils/request";

export function getProjectList(params) {
  return request({
    url: "/api/bills/detail/project_list/",
    method: "get",
    params: params,
  });
}

export function getProductList(params) {
  return request({
    url: "/api/bills/detail/product_list/",
    method: "get",
    params: params,
  });
}


export function getDetailList(params) {
  return request({
    url: "/api/bills/detail/",
    method: "get",
    params: params,
  });
}
