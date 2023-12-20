/* eslint-disable */

import request from '@/utils/request'

export function getProjectList(params) {
    return request({
        url: '/api/cmdb/project/',
        method: 'get',
        params: params
    })
}

export function createProject(data) {
    return request({
        url: "/api/cmdb/project/",
        method: "post",
        data: data
    })
}

export function updateProjectByID(id, data) {
    return request({
        url: '/api/cmdb/project/' + id + '/',
        method: 'patch',
        data: data
    })
}

export function deleteProjectByID(id) {
    return request({
        url: '/api/cmdb/project/' + id + '/',
        method: 'delete'
    })
}