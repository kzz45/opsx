/* eslint-disable */

import request from '@/utils/request'

export function getServerGroupInstanceList(params) {
    return request({
        url: '/api/monitor/server_group_instance/',
        method: 'get',
        params: params
    })
}

export function createServerGroupInstance(data) {
    return request({
        url: '/api/monitor/server_group_instance/',
        method: 'post',
        data: data
    })
}

export function updateServerGroupInstanceByID(id, data) {
    return request({
        url: '/api/monitor/server_group_instance/' + id + '/',
        method: 'patch',
        data: data
    })
}

export function deleteServerGroupInstanceByID(id) {
    return request({
        url: '/api/monitor/server_group_instance/' + id + '/',
        method: 'delete'
    })
}