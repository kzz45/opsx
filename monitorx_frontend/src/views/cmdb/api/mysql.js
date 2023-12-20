/* eslint-disable */

import request from '@/utils/request'

export function getMySQLList(params) {
    return request({
        url: '/api/cmdb/mysql/',
        method: 'get',
        params: params
    })
}

export function updateMySQLByID(id, data) {
    return request({
        url: '/api/cmdb/mysql/' + id + '/',
        method: 'patch',
        data: data
    })
}