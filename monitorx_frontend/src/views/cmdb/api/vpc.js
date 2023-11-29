/* eslint-disable */

import request from '@/utils/request'

export function getVPCList(params) {
    return request({
        // url: '/ops/vpc/query/vpc',
        url: '/api/cmdb/vpc/',
        method: 'get',
        params: params
    })
}

export function updateVPCByID(id, data) {
    return request({
        url: '/api/cmdb/vpc/' + id + '/',
        method: 'patch',
        data: data
    })
}

export function addVpc(data){
    return request({
        url: '/ops/vpc/add/vpc',
        method: 'post',
        data: data
    })
}

export function cidrCheck(param) {
    return request({
        url: '/ops/vpc/checkCidrCanBeUse',
        method: 'get',
        params: param
    })
}