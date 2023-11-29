/* eslint-disable */

import request from '@/utils/request'

export function getAddOnList(params) {
    return request({
        url: '/api/monitor/addon/',
        method: 'get',
        params: params
    })
}

export function createAddOn(data) {
    return request({
        url: '/api/monitor/addon/',
        method: 'post',
        data: data
    })
}

export function updateAddOnByID(id, data) {
    return request({
        url: '/api/monitor/addon/' + id + '/',
        method: 'patch',
        data: data
    })
}

export function deleteAddOnByID(id) {
    return request({
        url: '/api/monitor/addon/' + id + '/',
        method: 'delete'
    })
}