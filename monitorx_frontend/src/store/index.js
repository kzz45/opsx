/* eslint-disable */

import Vue from 'vue'
import Vuex from 'vuex'
import getters from './getters'
import app from './modules/app'
import settings from './modules/settings'
import user from './modules/user'
import user_list from './modules/user_list'
import global_product from './modules/product'

Vue.use(Vuex)

const store = new Vuex.Store({
    modules: {
        app,
        settings,
        user,
        user_list,
        global_product
    },
    getters
})

export default store