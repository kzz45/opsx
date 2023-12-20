/* eslint-disable */

import Vue from "vue";

import "normalize.css/normalize.css"; // A modern alternative to CSS resets

import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
// import locale from 'element-ui/lib/locale/lang/en' // lang i18n
import locale from "element-ui/lib/locale/lang/zh-CN"; // lang i18n

import "@/styles/index.scss"; // global css

import App from "./App";
import router from "./router";
import store from "./store";

import "@/icons"; // icon
import "@/permission"; // permission control

import JsonViewer from "vue-json-viewer";
Vue.use(JsonViewer);

// 代码编辑器
import "codemirror/lib/codemirror.css";
import VueCodemirror from "vue-codemirror";
Vue.use(VueCodemirror);

import * as echarts from "echarts";
// require('echarts/theme/macarons')
Vue.prototype.$echarts = echarts;

import VueClipboard from "vue-clipboard2";
Vue.use(VueClipboard);

// set ElementUI lang to EN
Vue.use(ElementUI, { locale });

Vue.config.productionTip = false;

new Vue({
  el: "#app",
  router,
  store,
  render: h => h(App)
});
