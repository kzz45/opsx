/* eslint-disable */

import request from "@/utils/request";

export function getBillList(params) {
  return request({
    url: "/api/bills/bill/",
    method: "get",
    params: params,
  });
}

export function getBillPie(params) {
  return request({
    url: "/api/bills/bill/bill_pie/",
    method: "get",
    params: params,
  });
}

export function createBill(data) {
  return request({
    url: "/api/bills/bill/",
    method: "post",
    data: data,
  });
}

export function updateBill(id, data) {
  return request({
    url: "/api/bills/bill/" + id + "/",
    method: "patch",
    data: data,
  });
}

export function deleteBill(id) {
  return request({
    url: "/api/bills/bill/" + id + "/",
    method: "delete",
  });
}
