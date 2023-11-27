/* eslint-disable */

import Vue from "vue";

import "normalize.css/normalize.css"; // A modern alternative to CSS resets

import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
import locale from "element-ui/lib/locale/lang/zh-CN"; // lang i18n

import "@/styles/index.scss"; // global css

import App from "./App";
import store from "./store";
import router from "./router";

import "@/icons"; // icon
import "@/permission"; // permission control

// 代码编辑器
import VueCodemirror from "vue-codemirror";
import "codemirror/lib/codemirror.css";
Vue.use(VueCodemirror);

import * as echarts from 'echarts'
// require('echarts/theme/macarons')
Vue.prototype.$echarts = echarts;

// set ElementUI lang to EN
Vue.use(ElementUI, {
  locale,
});
// 如果想要中文版 element-ui，按如下方式声明
// Vue.use(ElementUI)

Vue.config.productionTip = false;

new Vue({
  el: "#app",
  router,
  store,
  render: (h) => h(App),
});