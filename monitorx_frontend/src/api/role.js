/* eslint-disable */

import request from '@/utils/request'

export function getRoleList(params) {
    return request({
        url: '/api/role/',
        method: 'get',
        params: params
    })
}

export function createRole(data) {
    return request({
        url: '/api/role/',
        method: 'post',
        data: data
    })
}

export function updateRoleByID(id, data) {
    return request({
        url: '/api/role/' + id + '/',
        method: 'patch',
        data: data
    })
}

export function deleteRoleByID(id) {
    return request({
        url: '/api/role/' + id + '/',
        method: 'delete'
    })
}