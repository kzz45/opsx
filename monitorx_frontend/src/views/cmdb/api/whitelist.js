/* eslint-disable */

import request from '@/utils/request'

export function getWhitelist(params) {
    return request({
        url: '/api/cmdb/whitelist/',
        method: 'get',
        params: params
    })
}

export function createWhitelist(data) {
    return request({
        url: '/api/cmdb/whitelist/',
        method: 'post',
        data: data
    })
}


export function updateWhitelistByID(id, data) {
    return request({
        url: '/api/cmdb/whitelist/' + id + '/',
        method: 'patch',
        data: data
    })
}

export function deleteWhitelistByID(id) {
    return request({
        url: `/api/cmdb/whitelist/${id}`,
        method: 'delete'
    })
}