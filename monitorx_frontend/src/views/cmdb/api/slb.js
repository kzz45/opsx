/* eslint-disable */

import request from '@/utils/request'

export function getSLBList(params) {
    return request({
        url: '/api/cmdb/slb/',
        method: 'get',
        params: params
    })
}

export function updateSLBByID(id, data) {
    return request({
        url: '/api/cmdb/slb/' + id + '/',
        method: 'patch',
        data: data
    })
}