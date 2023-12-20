/* eslint-disable */

import request from '@/utils/request'

export function getServerList(params) {
    return request({
        url: '/api/monitor/server/',
        method: 'get',
        params: params
    })
}

export function createServer(data) {
    return request({
        url: '/api/monitor/server/',
        method: 'post',
        data: data
    })
}

export function updateServerByID(id, data) {
    return request({
        url: '/api/monitor/server/' + id + '/',
        method: 'patch',
        data: data
    })
}

export function deleteServerByID(id) {
    return request({
        url: '/api/monitor/server/' + id + '/',
        method: 'delete'
    })
}