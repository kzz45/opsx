/* eslint-disable */

import request from '@/utils/request'

export function getRedisList(params) {
    return request({
        url: '/api/cmdb/redis/',
        method: 'get',
        params: params
    })
}

export function updateRedisByID(id, data) {
    return request({
        url: '/api/cmdb/redis/' + id + '/',
        method: 'patch',
        data: data
    })
}