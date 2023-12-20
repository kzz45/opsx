/* eslint-disable */

import request from '@/utils/request'

export function getSecurityList(params) {
    return request({
        url: '/api/cmdb/security/',
        method: 'get',
        params: params
    })
}

export function updateSecurityByID(id, data) {
    return request({
        url: '/api/cmdb/security/' + id + '/',
        method: 'patch',
        data: data
    })
}

export function getSecurityRuleList(params) {
    return request({
        url: '/api/cmdb/rule/',
        method: 'get',
        params: params
    })
}