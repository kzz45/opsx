/* eslint-disable */

import request from '@/utils/request'

export function getInstanceTypeList(params) {
    return request({
        url: '/api/monitor/instance_type/',
        method: 'get',
        params: params
    })
}

export function createInstanceType(data) {
    return request({
        url: '/api/monitor/instance_type/',
        method: 'post',
        data: data
    })
}

export function updateInstanceTypeByID(id, data) {
    return request({
        url: '/api/monitor/instance_type/' + id + '/',
        method: 'patch',
        data: data
    })
}

export function deleteInstanceTypeByID(id) {
    return request({
        url: '/api/monitor/instance_type/' + id + '/',
        method: 'delete'
    })
}