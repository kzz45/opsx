/* eslint-disable */
// 定义一些全局共享的产品信息
import Cookies from "js-cookie";

function getCurrentSelectProductIDFromCookie() {
  if (Cookies.get("current_select_product_id")) {
    return Number(Cookies.get("current_select_product_id"));
  } else {
    return 0;
  }
}

function getCurrentSelectProductNameFromCookie() {
  if (Cookies.get("current_select_product_name")) {
    return Cookies.get("current_select_product_name");
  } else {
    return "-";
  }
}

const product = {
  // 定义全局共享的产品信息
  state: {
    product_list: [],
    current_select_product_id: getCurrentSelectProductIDFromCookie(),
    current_select_product_name: getCurrentSelectProductNameFromCookie(),
  },
  actions: {
    set_product({ commit }, val) {
      commit("SET_SELECT_PRODUCT", val);
    },
  },
  // 一些异步的操作
  mutations: {
    SET_SELECT_PRODUCT_LIST: (state, playload) => {
      state.product_list = playload.product_list;
    },
    SET_SELECT_PRODUCT: (state, payload) => {
      Cookies.set(
        "current_select_product_id",
        payload.current_select_product_id
      );
      state.current_select_product_id = payload.current_select_product_id;
      Cookies.set(
        "current_select_product_name",
        payload.current_select_product_name
      );
      state.current_select_product_name = payload.current_select_product_name;
    },
  },
};

export default product;
