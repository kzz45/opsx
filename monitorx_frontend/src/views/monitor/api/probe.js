/* eslint-disable */

import request from '@/utils/request'

export function getProbeList(params) {
    return request({
        url: '/api/monitor/probe/',
        method: 'get',
        params: params
    })
}

export function getProbeTaskList(params) {
    return request({
        url: '/api/monitor/probe_task/',
        method: 'get',
        params: params
    })
}


export function createProbe(data) {
    return request({
        url: '/api/monitor/probe/',
        method: 'post',
        data: data
    })
}

export function createProbeTask(data) {
    return request({
        url: '/api/monitor/probe_task/',
        method: 'post',
        data: data
    })
}


export function updateProbeByID(id, data) {
    return request({
        url: '/api/monitor/probe/' + id + '/',
        method: 'patch',
        data: data
    })
}

export function updateProbeTaskByID(id, data) {
    return request({
        url: '/api/monitor/probe_task/' + id + '/',
        method: 'patch',
        data: data
    })
}

export function deleteProbeByID(id) {
    return request({
        url: '/api/monitor/probe/' + id + '/',
        method: 'delete'
    })
}

export function deleteProbeTaskByID(id) {
    return request({
        url: '/api/monitor/probe_task/' + id + '/',
        method: 'delete'
    })
}