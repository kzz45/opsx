/* eslint-disable */

import request from '@/utils/request'

export function getImageList(params) {
    return request({
        url: '/api/cmdb/image/',
        method: 'get',
        params: params
    })
}

export function addImage(data) {
    return request({
        url: '/api/cmdb/image/',
        method: 'post',
        data: data
    })
}

export function updateImageByID(id, data) {
    return request({
        url: '/api/cmdb/image/' + id + '/',
        method: 'patch',
        data: data
    })
}