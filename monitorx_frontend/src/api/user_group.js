/* eslint-disable */

import request from '@/utils/request'

export function getUserGroups() {
    return request({
        url: '/api/user_group/',
        method: 'get'
    })
}

export function createUserGroups(data) {
    return request({
        url: '/api/user_group/',
        method: 'post',
        data: data
    })
}

export function deleteUserGroup(id) {
    return request({
        url: `/api/user_group/${id}`,
        method: 'delete'
    })
}

export function updateUserGroup(id, data) {
    return request({
        url: `/api/user_group/${id}/`,
        method: 'patch',
        data: data
    })
}