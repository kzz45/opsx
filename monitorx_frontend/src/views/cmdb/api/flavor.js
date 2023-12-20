/* eslint-disable */

import request from '@/utils/request'

export function getFlavorList(params) {
    return request({
        url: '/api/cmdb/flavor/',
        method: 'get',
        params: params
    })
}

export function addFlavor(data) {
    return request({
        url: '/api/cmdb/flavor/',
        method: 'post',
        data: data
    })
}

export function deleteFlavorByID(id) {
    return request({
        url: `/api/cmdb/flavor/${id}`,
        method: 'delete'
    })
}

export function patchFlavorByID(id, data) {
    return request({
        url: `/api/cmdb/flavor/${id}/`,
        method: 'patch',
        data: data
    })
}