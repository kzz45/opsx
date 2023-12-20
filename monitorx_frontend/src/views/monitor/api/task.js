/* eslint-disable */

import request from '@/utils/request'

export function getTaskList(params) {
    return request({
        url: '/api/monitor/task/',
        method: 'get',
        params: params
    })
}

export function createTask(data) {
    return request({
        url: '/api/monitor/task/',
        method: 'post',
        data: data
    })
}

export function updateTaskByID(id, data) {
    return request({
        url: '/api/monitor/task/' + id + '/',
        method: 'patch',
        data: data
    })
}

export function deleteTaskByID(id) {
    return request({
        url: '/api/monitor/task/' + id + '/',
        method: 'delete'
    })
}