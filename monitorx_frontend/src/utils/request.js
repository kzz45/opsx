/* eslint-disable */

import axios from "axios";
import {
  // MessageBox,
  Message,
} from "element-ui";
import store from "@/store";
import { getToken } from "@/utils/auth";

// create an axios instance
const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API, // url = base url + request url
  withCredentials: true, // send cookies when cross-domain requests
  timeout: 5000, // request timeout
});

// request interceptor
service.interceptors.request.use(
  (config) => {
    if (store.getters.token) {
      config.headers["Authorization"] = getToken();
    }
    if (!config.headers["Content-Type"]) {
      config.headers["Content-Type"] = "application/json";
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// response interceptor
service.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.log("err" + error); // for debug
    // Message({
    //   message: error.message,
    //   type: "error",
    //   duration: 5 * 1000
    // })
    return Promise.reject(error.response.data);
  }
);

export default service;
