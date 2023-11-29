/* eslint-disable */

import request from '@/utils/request'

export function getDashboardList(params) {
    return request({
        url: '/api/monitor/dashboard/',
        method: 'get',
        params: params
    })
}

export function createDashboard(data) {
    return request({
        url: '/api/monitor/dashboard/',
        method: 'post',
        data: data
    })
}

export function updateDashboardByID(id, data) {
    return request({
        url: '/api/monitor/dashboard/' + id + '/',
        method: 'patch',
        data: data
    })
}

export function deleteDashboardByID(id) {
    return request({
        url: '/api/monitor/dashboard/' + id + '/',
        method: 'delete'
    })
}