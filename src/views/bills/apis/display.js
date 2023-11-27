/* eslint-disable */

import request from "@/utils/request";

export function getDisplayList(params) {
  return request({
    url: "/api/bills/display/",
    method: "get",
    params: params,
  });
}
