/* eslint-disable */

import request from '@/utils/request'

export function getLabelList(params) {
    return request({
        url: '/api/monitor/label/',
        method: 'get',
        params: params
    })
}

export function createLabel(data) {
    return request({
        url: '/api/monitor/label/',
        method: 'post',
        data: data
    })
}

export function updateLabelByID(id, data) {
    return request({
        url: '/api/monitor/label/' + id + '/',
        method: 'patch',
        data: data
    })
}

export function deleteLabelByID(id) {
    return request({
        url: '/api/monitor/label/' + id + '/',
        method: 'delete'
    })
}