/* eslint-disable */

import request from '@/utils/request'


export function getBuildingList(params) {
    return request({
        url: '/api/cmdb/building/',
        method: 'get',
        params: params
    })
}

export function createBuilding(data) {
    return request({
        url: '/api/cmdb/building/',
        method: 'post',
        data: data
    })
}

export function updateBuildingID(id, data) {
    return request({
        url: '/api/cmdb/building/' + id + '/',
        method: 'patch',
        data: data
    })
}

export function deleteBuildingByID(id) {
    return request({
        url: '/api/cmdb/building/' + id + '/',
        method: 'delete'
    })
}