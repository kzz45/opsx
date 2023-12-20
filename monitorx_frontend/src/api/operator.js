/* eslint-disable */

import request from '@/utils/request'


export function getOperatorList(params) {
    return request({
        url: '/api/cmdb/operator/',
        method: 'get',
        params: params
    })
}

export function createOperator(data) {
    return request({
        url: '/api/cmdb/operator/',
        method: 'post',
        data: data
    })
}

export function updateOperatorID(id, data) {
    return request({
        url: '/api/cmdb/operator/' + id + '/',
        method: 'patch',
        data: data
    })
}

export function deleteOperatorByID(id) {
    return request({
        url: '/api/cmdb/operator/' + id + '/',
        method: 'delete'
    })
}