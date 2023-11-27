/* eslint-disable */

import Cookies from 'js-cookie'

const TokenKey = 'AccessToken'
const UserInfoKey = 'AccessUser'

export function getToken() {
    return localStorage.getItem(TokenKey)
}

export function setToken(token) {
    localStorage.setItem(TokenKey, token)
    return Cookies.set(TokenKey, token, {
        expires: 30
    })
}

export function removeToken() {
    localStorage.removeItem(TokenKey)
    return Cookies.remove(TokenKey)
}

export function getUserID() {
    return localStorage.getItem(UserInfoKey)
}

export function setUserID(user_id) {
    localStorage.setItem(UserInfoKey, user_id)
    return Cookies.set(UserInfoKey, user_id, { expires: 30 })
}