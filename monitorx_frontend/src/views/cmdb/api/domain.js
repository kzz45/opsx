/* eslint-disable */

import request from '@/utils/request'

export function getDomainList(params) {
    return request({
        url: '/api/cmdb/domain/',
        method: 'get',
        params: params
    })
}

export function addDomain(data) {
    return request({
        url: '/api/cmdb/domain/',
        method: 'post',
        data: data
    })
}

export function deleteDomainByID(id) {
    return request({
        url: `/api/cmdb/domain/${id}`,
        method: 'delete'
    })
}

export function updateDomainByID(id, data) {
    return request({
        url: `/api/cmdb/domain/${id}/`,
        method: 'patch',
        data: data
    })
}