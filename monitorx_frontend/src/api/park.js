/* eslint-disable */

import request from '@/utils/request'


export function getParkList(params) {
    return request({
        url: '/api/cmdb/park/',
        method: 'get',
        params: params
    })
}

export function createPark(data) {
    return request({
        url: '/api/cmdb/park/',
        method: 'post',
        data: data
    })
}

export function updateParkID(id, data) {
    return request({
        url: '/api/cmdb/park/' + id + '/',
        method: 'patch',
        data: data
    })
}

export function deleteParkByID(id) {
    return request({
        url: '/api/cmdb/park/' + id + '/',
        method: 'delete'
    })
}