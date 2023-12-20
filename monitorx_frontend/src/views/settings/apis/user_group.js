/* eslint-disable */

import request from "@/utils/request";

export function getCmdbUserGroupList(param) {
  return request({
    url: "/api/cmdb/user_group/",
    method: "get",
    params: param
  });
}

export function createCmdbUserGroup(data) {
  return request({
    url: "/api/cmdb/user_group/",
    method: "post",
    data: data
  });
}

export function deleteCmdbUserGroup(id) {
  return request({
    url: `/api/cmdb/user_group/${id}`,
    method: "delete"
  });
}

export function updateCmdbUserGroup(id, data) {
  return request({
    url: `/api/cmdb/user_group/${id}/`,
    method: "patch",
    data: data
  });
}
