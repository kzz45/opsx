/* eslint-disable */

import request from '@/utils/request'


export function getFactoryList(params) {
    return request({
        url: '/api/cmdb/factory/',
        method: 'get',
        params: params
    })
}

export function createFactory(data) {
    return request({
        url: '/api/cmdb/factory/',
        method: 'post',
        data: data
    })
}

export function updateFactoryID(id, data) {
    return request({
        url: '/api/cmdb/factory/' + id + '/',
        method: 'put',
        data: data
    })
}

export function deleteFactoryByID(id) {
    return request({
        url: '/api/cmdb/factory/' + id + '/',
        method: 'delete'
    })
}