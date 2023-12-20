/* eslint-disable */

import request from '@/utils/request'

export function getGroupList(params) {
    return request({
        url: '/api/monitor/group/',
        method: 'get',
        params: params
    })
}

export function createGroup(data) {
    return request({
        url: '/api/monitor/group/',
        method: 'post',
        data: data
    })
}

export function updateGroupByID(id, data) {
    return request({
        url: '/api/monitor/group/' + id + '/',
        method: 'patch',
        data: data
    })
}

export function deleteGroupByID(id) {
    return request({
        url: '/api/monitor/group/' + id + '/',
        method: 'delete'
    })
}