/* eslint-disable */

import request from '@/utils/request'

export function getLabelNameList(params) {
    return request({
        url: '/api/monitor/label_name/',
        method: 'get',
        params: params
    })
}

export function createLabelName(data) {
    return request({
        url: '/api/monitor/label_name/',
        method: 'post',
        data: data
    })
}

export function updateLabelNameByID(id, data) {
    return request({
        url: '/api/monitor/label_name/' + id + '/',
        method: 'patch',
        data: data
    })
}

export function deleteLabelNameByID(id) {
    return request({
        url: '/api/monitor/label_name/' + id + '/',
        method: 'delete'
    })
}