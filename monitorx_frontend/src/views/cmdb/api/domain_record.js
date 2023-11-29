/* eslint-disable */

import request from '@/utils/request'

export function getDomainList(params) {
    return request({
        // url: '/api/cmdb/domain_record/',
        url: '/ops/dns/query/supplier',
        method: 'get',
        params: params
    })
}

export function getDomainRecordList(params) {
    return request({
        // url: '/api/cmdb/domain_record/',
        url: '/ops/dns/query/records',
        method: 'get',
        params: params
    })
}

export function addDomainRecord(data) {
    return request({
        // url: '/api/cmdb/domain_record/',
        url: '/ops/dns/add/record',
        method: 'post',
        data: data
    })
}

export function deleteDomainRecordByID(id) {
    return request({
        url: `/api/cmdb/domain_record/${id}`,
        method: 'delete'
    })
}

export function updateDomainRecordByID(id, data) {
    return request({
        url: `/api/cmdb/domain_record/${id}/`,
        method: 'patch',
        data: data
    })
}

export function updateDomainRecord(data) {
    return request({
        url: `/ops/dns/update/record`,
        method: 'put',
        data: data
    })
}

export function updateDomainRecordStatus(data) {
    return request({
        url: `/ops/dns/update/recordStatus`,
        method: 'put',
        data: data
    })
}

export function getDomainLineList(params) {
    return request({
        url: '/ops/dns/query/lines',
        method: 'get',
        params: params
    })
}

export function getRecordAudit(params) {
    return request({
        url: '/ops/dns/query/audit',
        method: 'get',
        params: params 
    })
}

export function updateAliWeight(data) {
    return request({
        url: `/ops/dns/update/aliWeight`,
        method: 'put',
        data: data
    })
}

export function getAwsLb(data) {
    return request({
        url: `/ops/dns/query/lb`,
        method: 'get',
        params: data
    })
}

export function getCheckPort(data) {
    return request({
        url: `/ops/dns/query/checkPort`,
        method: 'get',
        params: data
    })
}

export function addCheckPort(data) {
    return request({
        url: '/ops/dns/add/checkPort',
        method: 'post',
        data: data
    })
}

export function updateCheckPort(data) {
    return request({
        url: '/ops/dns/update/checkPort',
        method: 'put',
        data: data
    })
}

export function getAlertFocus(params) {
    return request({
        url: '/ops/dns/query/focusAlert',
        method: 'get',
        params: params 
    })
}

export function addAlertFocust(data) {
    return request({
        url: '/ops/dns/add/focusAlert',
        method: 'post',
        data: data
    })
}

export function delAlertFocust(id) {
    return request({
        url: '/ops/dns/delete/focusAlert/' + id ,
        method: 'delete'
    })
}

export function checkSsl(data) {
    return request({
        url: '/ops/dns/checkSsl',
        method: 'post',
        data: data
    })
}