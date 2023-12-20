/* eslint-disable */

import request from '@/utils/request'

export function getAlertList(params) {
    return request({
        url: '/api/monitor/alert/',
        method: 'get',
        params: params
    })
}

export function createAlert(data) {
    return request({
        url: '/api/monitor/alert/',
        method: 'post',
        data: data
    })
}

export function updateAlertByID(id, data) {
    return request({
        url: '/api/monitor/alert/' + id + '/',
        method: 'patch',
        data: data
    })
}

export function deleteAlertByID(id) {
    return request({
        url: '/api/monitor/alert/' + id + '/',
        method: 'delete'
    })
}