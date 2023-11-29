/* eslint-disable */

import request from '@/utils/request'

export function getSLSList(params) {
    return request({
        url: '/api/monitor/sls/',
        method: 'get',
        params: params
    })
}

export function createSLS(data) {
    return request({
        url: '/api/monitor/sls/',
        method: 'post',
        data: data
    })
}

export function updateSLSByID(id, data) {
    return request({
        url: '/api/monitor/sls/' + id + '/',
        method: 'patch',
        data: data
    })
}

export function deleteSLSByID(id) {
    return request({
        url: '/api/monitor/sls/' + id + '/',
        method: 'delete'
    })
}

export function getSLSURL(data) {
    return request({
        url: '/api/monitor/get_sls_url/',
        method: 'post',
        data: data
    })
}