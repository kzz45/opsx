/* eslint-disable */

import request from "@/utils/request";

export function getProductList(params) {
  return request({
    url: "/api/bills/product/",
    method: "get",
    params: params,
  });
}

export function createProduct(data) {
  return request({
    url: "/api/bills/product/",
    method: "post",
    data: data,
  });
}

export function updateProduct(id, data) {
  return request({
    url: "/api/bills/product/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteProduct(id) {
  return request({
    url: "/api/bills/product/" + id + "/",
    method: "delete",
  });
}
