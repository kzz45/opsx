/* eslint-disable */

import request from '@/utils/request'

// export function getUserGroup(params) {
//     return request({
//         url: '/api/cmdb/user_role_group/',
//         method: 'get',
//         params: params
//     })
// }

export function getRolerList(params) {
    return request({
        url: '/api/cmdb/role/',
        method: 'get',
        params: params
    })
}
export function getUserRoleGroup(params) {
    return request({
        url: '/api/cmdb/user_role_group/',
        method: 'get',
        params: params
    })
}

export function createUserRoleGroup(data) {
    // console.log("createUserRoleGroup", data)
    return request({
        url: '/api/cmdb/user_role_group/',
        method: 'post',
        data: data
    })
}

export function updateUserRoleGroupByID(id, data) {
    // console.log("updateUserRoleGroupByID", id, data)
    return request({
        url: '/api/cmdb/user_role_group/' + id + '/',
        method: 'put',
        data: data
    })
}

export function deleteUserRoleGroup(id) {
    // console.log("updateUserRoleGroupByID", id, data)
    return request({
        url: '/api/cmdb/user_role_group/' + id + '/',
        method: 'delete',
    })
}