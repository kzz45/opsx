/* eslint-disable */

import axios from 'axios'
import {
    MessageBox,
    Message
} from 'element-ui'
import store from '@/store'
import {
    getToken,getCsrfToken
} from '@/utils/auth'

// create an axios instance
const service = axios.create({
    baseURL: process.env.VUE_APP_BASE_API, // url = base url + request url
    withCredentials: true, // send cookies when cross-domain requests
    timeout: 6000 * 10 // request timeout
})

// request interceptor
service.interceptors.request.use(
    config => {
        config.metadata = {
                startTime: new Date()
            }
            // console.log(config.url, '============')
        if (store.getters.token) {
            config.headers['Authorization'] = getToken()
        }
        var csrfToken = getCsrfToken()
        if (csrfToken){
            config.headers['X-CSRFToken'] = csrfToken
        }
        if (!config.headers['Content-Type']) {
            config.headers['Content-Type'] = 'application/json'
        }
        return config
    },
    error => {
        // console.log(error) // for debug
        return Promise.reject(error)
    }
)

// response interceptor
service.interceptors.response.use(
    response => {
        response.config.metadata.endTime = new Date()
        response.duration = response.config.metadata.endTime - response.config.metadata.startTime
        return response
    },
    error => {
        // if (error.response.status === 404) {
        //     Message({
        //         message: 'url:' + error.response.config.url + '不存在',
        //         type: "error",
        //         duration: 5 * 1000
        //     })
        // } else if (error.response.status === 401 || error.response.status === 402 || error.response.status === 403) {
        //     Message({
        //         // message: "没有权限哦",
        //         message: error.response.data.detail,
        //         type: "error",
        //         duration: 5 * 1000
        //     })
        // } else if (error.response.status === 500) {
        //     Message({
        //         // message: "服务器内部错误",
        //         message: error.response.data.detail,
        //         type: "error",
        //         duration: 5 * 1000
        //     })
        // }
        return Promise.reject(error.response.data)
    }
)

export default service