/* eslint-disable */

import request from '@/utils/request'

export function getCurrentAlertList(params) {
    return request({
        url: '/api/monitor/current_alert/',
        method: 'get',
        params: params
    })
}