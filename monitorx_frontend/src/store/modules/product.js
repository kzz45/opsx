/* eslint-disable */
// 定义一些全局共享的产品信息
import Cookies from 'js-cookie'

function getCurrentSelectProductIDFromCookie() {
    if (Cookies.get('current_select_product_id')) {
        return Number(Cookies.get('current_select_product_id'))
    } else {
        return -1
    }
}

function getCurrentSelectProductNameFromCookie() {
    if (Cookies.get('current_select_product_name')) {
        return Cookies.get('current_select_product_name')
    } else {
        return '-'
    }
}

const global_product = {
    // 定义全局共享的产品信息
    state: {
        global_product_list: [],
        global_product_map: {},
        current_select_product_id: getCurrentSelectProductIDFromCookie(),
        current_select_product_name: getCurrentSelectProductNameFromCookie()
    },
    actions: {
        set_product({
                commit
            },
            val
        ) {
            commit('SET_SELECT_PRODUCT', val)
        }

    },
    // 一些异步的操作
    mutations: {
        SET_SELECT_PRODUCT_LIST: (state, playload) => {
            state.global_product_list = playload.global_product_list
            for(let index in state.global_product_list) {
                state.global_product_map[state.global_product_list[index]['id']] = state.global_product_list[index]['name']
            }
        },
        SET_SELECT_PRODUCT: (state, payload) => {
            Cookies.set('current_select_product_id', payload.current_select_product_id)
            state.current_select_product_id = payload.current_select_product_id
            Cookies.set('current_select_product_name', payload.current_select_product_name)
            state.current_select_product_name = payload.current_select_product_name
        }
    }
}


export default global_product