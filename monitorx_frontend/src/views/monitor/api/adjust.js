/* eslint-disable */

import request from '@/utils/request'

export function getAdJustList(params) {
    return request({
        url: '/api/monitor/adjust/',
        method: 'get',
        params: params
    })
}

export function createAdJust(data) {
    return request({
        url: '/api/monitor/adjust/',
        method: 'post',
        data: data
    })
}

export function updateAdJustByID(id, data) {
    return request({
        url: '/api/monitor/adjust/' + id + '/',
        method: 'patch',
        data: data
    })
}

export function deleteAdJustByID(id) {
    return request({
        url: '/api/monitor/adjust/' + id + '/',
        method: 'delete'
    })
}