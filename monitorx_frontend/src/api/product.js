/* eslint-disable */

import request from '@/utils/request'

export function getProductList(params) {
    return request({
        url: '/api/cmdb/product/',
        method: 'get',
        timeout: 10 * 1000,
        params: params
    })
}

export function createProduct(data) {
    return request({
        url: '/api/cmdb/product/',
        method: 'post',
        data: data
    })
}

export function updateProductID(id, data) {
    return request({
        url: '/api/cmdb/product/' + id + '/',
        method: 'patch',
        data: data
    })
}

export function deleteProductByID(id) {
    return request({
        url: '/api/cmdb/product/' + id + '/',
        method: 'delete'
    })
}