/* eslint-disable */

import Cookies from 'js-cookie'

const TokenKey = 'AccessToken'
const IdTokenKey = 'IdToken'
const UserInfoKey = 'AccessUser'

export function getToken() {
    return localStorage.getItem(TokenKey)
}

export function getCsrfToken() {
    return Cookies.get('csrftoken')
}

export function getIdToken() {
    return localStorage.getItem(IdTokenKey)
}

export function setFactoryMap(factory_map) {
    localStorage.setItem('factory_map', factory_map)
    return
}

export function setTemplateActiveTab(name) {
    localStorage.setItem('templ_active_tab', name)
    return
}

export function getTemplateActiveTab() {
    return localStorage.getItem("templ_active_tab", '')
}

export function getFactoryMap(factory_id) {
    var item = localStorage.getItem('factory_map')
    item = JSON.parse(item)
    return Object.keys(item).includes(factory_id)? item[factory_id] : factory_id
}

export function setProjectMap(project_map) {
    localStorage.setItem('project_map', project_map)
    return
}

export function getProjectMap(project_id) {
    var item = localStorage.getItem('project_map')
    item = JSON.parse(item)
    return Object.keys(item).includes(project_id)? item[project_id] : project_id
}

export function setToken(token) {
    localStorage.setItem(TokenKey, token)
    return Cookies.set(TokenKey, token, {
        expires: 30
    })
}

export function setIdToken(token) {
    localStorage.setItem(IdTokenKey, token)
    return Cookies.set(IdTokenKey, token, {
        expires: 30
    })
}


export function removeToken() {
    localStorage.removeItem(TokenKey)
    return Cookies.remove(TokenKey)
}

export function removeIdToken() {
    localStorage.removeItem(IdTokenKey)
    return Cookies.remove(IdTokenKey)
}


export function getUserID() {
    return localStorage.getItem(UserInfoKey)
}

export function setUserID(user_id) {
    localStorage.setItem(UserInfoKey, user_id)
    return Cookies.set(UserInfoKey, user_id, {
        expires: 30
    })
}