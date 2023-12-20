/* eslint-disable */

import request from '@/utils/request'

export function getAlertLevelList(params) {
    return request({
        url: '/api/monitor/alert_level/',
        method: 'get',
        params: params
    })
}

export function createAlertLevel(data) {
    return request({
        url: '/api/monitor/alert_level/',
        method: 'post',
        data: data
    })
}

export function updateAlertLevelByID(id, data) {
    return request({
        url: '/api/monitor/alert_level/' + id + '/',
        method: 'patch',
        data: data
    })
}

export function deleteAlertLevelByID(id) {
    return request({
        url: '/api/monitor/alert_level/' + id + '/',
        method: 'delete'
    })
}