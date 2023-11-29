/* eslint-disable */

import request from '@/utils/request'

export function getAlertWallList(params) {
    return request({
        url: '/api/monitor/alert_wall/',
        method: 'get',
        params: params
    })
}