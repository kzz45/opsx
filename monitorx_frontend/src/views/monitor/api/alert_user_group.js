/* eslint-disable */

import request from '@/utils/request'

export function getAlertUserGroupList(params) {
    return request({
        url: '/api/monitor/user_group/',
        method: 'get',
        params: params
    })
}

export function createAlertUserGroup(data) {
    return request({
        url: '/api/monitor/user_group/',
        method: 'post',
        data: data
    })
}

export function updateAlertUserGroupByID(id, data) {
    return request({
        url: '/api/monitor/user_group/' + id + '/',
        method: 'patch',
        data: data
    })
}

export function deleteAlertUserGroupByID(id) {
    return request({
        url: '/api/monitor/user_group/' + id + '/',
        method: 'delete'
    })
}