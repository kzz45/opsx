/* eslint-disable */

import request from '@/utils/request'

export function getSubnetList(params) {
    return request({
        // url: '/ops/queryCmdb/query/relation/' + param.vpc + '/contain',
        url: '/api/cmdb/subnet/',
        method: 'get',
        params: params
    })
}

export function updateSubnetByID(id, data) {
    return request({
        url: '/api/cmdb/subnet/' + id + '/',
        method: 'patch',
        data: data
    })
}

export function addSubnet(data) {
    return request({
        // url: '/api/cmdb/subnet/',
        url: '/ops/vpc/add/subnet',
        method: 'post',
        data: data
    })
}

// export function getSubnetInfo(id) {
//     return request({
//         url: '/ops/queryCmdb/query/asset?assetId=' + id,
//         method: 'get',
//     })
// }