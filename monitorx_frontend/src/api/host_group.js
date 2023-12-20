/* eslint-disable */

import request from '@/utils/request'

export function getHostGroupList(params) {
    return request({
        url: '/api/cmdb/group/',
        method: 'get',
        params: params
    })
}

export function createHostGroup(data) {
    return request({
        url: '/api/cmdb/group/',
        method: 'post',
        data: data
    })
}


export function updateHostGroupByID(id, data) {
    return request({
        url: '/api/cmdb/group/' + id + '/',
        method: 'patch',
        data: data
    })
}


export function deleteHostGroupByID(id) {
    return request({
        url: '/api/cmdb/group/' + id + '/',
        method: 'delete'
    })
}