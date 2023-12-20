/* eslint-disable */

import request from '@/utils/request'

export function getZoneList(params) {
    return request({
        url: '/api/cmdb/zone/',
        method: 'get',
        params: params
    })
}

export function updateZoneByID(id, data) {
    return request({
        url: '/api/cmdb/zone/' + id + '/',
        method: 'patch',
        data: data
    })
}