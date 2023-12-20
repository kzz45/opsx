/* eslint-disable */

import request from '@/utils/request'

export function getMachineList(params) {
    return request({
        url: '/api/cmdb/machine/',
        method: 'get',
        params: params
    })
}

export function updateMachineByID(id, data) {
    return request({
        url: '/api/cmdb/machine/' + id + '/',
        method: 'patch',
        data: data
    })
}

export function postUpload (file) {
    return request({
        url: '/ops/resourceImport/import',
        method: 'post',
        data: file,
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
}