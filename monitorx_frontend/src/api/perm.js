/* eslint-disable */

import request from '@/utils/request'

export function getPermList(params) {
    return request({
        url: '/api/perm/',
        method: 'get',
        params: params
    })
}

export function createPerm(data) {
    return request({
        url: '/api/perm/',
        method: 'post',
        data: data
    })
}

export function updatePermByID(id, data) {
    return request({
        url: '/api/perm/' + id + '/',
        method: 'patch',
        data: data
    })
}

export function deletePermByID(id) {
    return request({
        url: '/api/perm/' + id + '/',
        method: 'delete'
    })
}