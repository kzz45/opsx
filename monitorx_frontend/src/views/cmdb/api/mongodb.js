/* eslint-disable */

import request from '@/utils/request'

export function getMongodbList(params) {
    return request({
        url: '/api/cmdb/mongodb/',
        method: 'get',
        params: params
    })
}

export function updateMongodbByID(id, data) {
    return request({
        url: '/api/cmdb/mongodb/' + id + '/',
        method: 'patch',
        data: data
    })
}
