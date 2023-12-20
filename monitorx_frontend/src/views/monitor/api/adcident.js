/* eslint-disable */

import request from '@/utils/request'

export function getAdCidentList(params) {
    return request({
        url: '/api/monitor/adcident/',
        method: 'get',
        params: params
    })
}

export function createAdCident(data) {
    return request({
        url: '/api/monitor/adcident/',
        method: 'post',
        data: data
    })
}

export function updateAdCidentByID(id, data) {
    return request({
        url: '/api/monitor/adcident/' + id + '/',
        method: 'patch',
        data: data
    })
}

export function deleteAdCidentByID(id) {
    return request({
        url: '/api/monitor/adcident/' + id + '/',
        method: 'delete'
    })
}