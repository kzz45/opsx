/* eslint-disable */

import request from '@/utils/request'

export function getServerGroupList(params) {
    return request({
        url: '/api/monitor/server_group/',
        method: 'get',
        params: params
    })
}

export function createServerGroup(data) {
    return request({
        url: '/api/monitor/server_group/',
        method: 'post',
        data: data
    })
}

export function updateServerGroupByID(id, data) {
    return request({
        url: '/api/monitor/server_group/' + id + '/',
        method: 'patch',
        data: data
    })
}

export function deleteServerGroupByID(id) {
    return request({
        url: '/api/monitor/server_group/' + id + '/',
        method: 'delete'
    })
}