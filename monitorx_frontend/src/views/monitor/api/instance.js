/* eslint-disable */

import request from '@/utils/request'

export function getInstanceList(params) {
    return request({
        url: '/api/monitor/instance/',
        method: 'get',
        params: params
    })
}

export function createInstance(data) {
    return request({
        url: '/api/monitor/instance/',
        method: 'post',
        data: data
    })
}

export function updateInstanceByID(id, data) {
    return request({
        url: '/api/monitor/instance/' + id + '/',
        method: 'patch',
        data: data
    })
}

export function deleteInstanceByID(id) {
    return request({
        url: '/api/monitor/instance/' + id + '/',
        method: 'delete'
    })
}