/* eslint-disable */

import router from "./router";
import store from "./store";
import { Message } from "element-ui";
import NProgress from "nprogress"; // progress bar
import "nprogress/nprogress.css"; // progress bar style
import { getToken } from "@/utils/auth"; // get token from cookie
import getPageTitle from "@/utils/get-page-title";

NProgress.configure({
  showSpinner: false
});

const whiteList = ["/login", "/idass_login", "/unauth", "/idaas"];
// const whiteList = ['/idass_login', '/unauth', '/idaas', '/logout']

router.beforeEach(async (to, from, next) => {
  NProgress.start();
  // console.log(to.path, from.path, to.query, '?????????????')
  document.title = getPageTitle(to.meta.title);

  const hasToken = getToken();
  if (hasToken) {
    if (to.path === "/login") {
      next({
        path: "/"
      });
      NProgress.done();
    } else if (to.path === "/auth-redirect") {
      next({
        path: "/"
      });
      NProgress.done();
    } else {
      const hasGetUserInfo = store.getters.name;
      if (hasGetUserInfo) {
        next();
      } else {
        try {
          await store.dispatch("user/getUserRoleGroup");
          await store.dispatch("user/getInfo");
          next();
        } catch (error) {
          await store.dispatch("user/resetToken");
          next(`/login?redirect=${to.path}`);
          NProgress.done();
        }
      }
    }
  } else {
    if (whiteList.indexOf(to.path) !== -1) {
      next();
    } else {
      // console.log(to.path, '+++++', to.query, 'redirect===========')
      next(`/login`);
      NProgress.done();
    }
  }
});

router.afterEach(() => {
  NProgress.done();
});
