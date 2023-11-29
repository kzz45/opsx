/* eslint-disable */

import request from '@/utils/request'

export function getRegionList(params) {
    return request({
        url: '/api/cmdb/region/',
        method: 'get',
        params: params
    })
}

export function updateRegionByID(id, data) {
    return request({
        url: '/api/cmdb/region/' + id + '/',
        method: 'patch',
        data: data
    })
}