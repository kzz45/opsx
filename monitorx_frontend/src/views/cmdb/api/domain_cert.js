/* eslint-disable */

import request from '@/utils/request'

export function getDomainCertList(params) {
    return request({
        url: '/api/cmdb/cert/',
        method: 'get',
        params: params
    })
}

export function addDomainCert(data) {
    return request({
        url: '/api/cmdb/cert/',
        method: 'post',
        data: data
    })
}

export function deleteDoaminCertByID(id) {
    return request({
        url: `/api/cmdb/cert/${id}`,
        method: 'delete'
    })
}

export function updateDomainCertByID(id, data) {
    return request({
        url: `/api/cmdb/cert/${id}/`,
        method: 'patch',
        data: data
    })
}