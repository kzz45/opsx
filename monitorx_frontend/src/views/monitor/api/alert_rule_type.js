/* eslint-disable */

import request from '@/utils/request'

export function getAlertRuleTypeList(params) {
    return request({
        url: '/api/monitor/alert_rule_type/',
        method: 'get',
        params: params
    })
}

export function createAlertRuleType(data) {
    return request({
        url: '/api/monitor/alert_rule_type/',
        method: 'post',
        data: data
    })
}

export function updateAlertRuleTypeByID(id, data) {
    return request({
        url: '/api/monitor/alert_rule_type/' + id + '/',
        method: 'patch',
        data: data
    })
}

export function deleteAlertRuleTypeByID(id) {
    return request({
        url: '/api/monitor/alert_rule_type/' + id + '/',
        method: 'delete'
    })
}