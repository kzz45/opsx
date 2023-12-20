/* eslint-disable */

import request from "@/utils/request";

export function getHistoryList(params) {
  return request({
    url: "/api/cmdb/history/",
    method: "get",
    params: params
  });
}
