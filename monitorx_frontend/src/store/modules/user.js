/* eslint-disable */

import { login, logout, getInfo } from "@/api/user";
import {
  getToken,
  setToken,
  removeToken,
  getUserID,
  setUserID,
} from "@/utils/auth";
import { resetRouter } from "@/router";

const getDefaultState = () => {
  return {
    token: getToken(),
    name: "",
    avatar: "",
    user_id: getUserID(),
    is_superuser: false,
    roles: [],
  };
};

const state = getDefaultState();

const mutations = {
  RESET_STATE: (state) => {
    Object.assign(state, getDefaultState());
  },
  SET_TOKEN: (state, token) => {
    state.token = token;
  },
  SET_NAME: (state, name) => {
    state.name = name;
  },
  SET_USERID: (state, user_id) => {
    state.user_id = user_id;
  },
  SET_SUPERUSER: (state, is_superuser) => {
    state.is_superuser = is_superuser;
  },
  SET_ROLES: (state, roles) => {
    state.roles = roles;
  },
  SET_AVATAR: (state, avatar) => {
    state.avatar = avatar;
  },
};

const actions = {
  // user login
  login({ commit }, userInfo) {
    const username = userInfo.username.trim();
    return new Promise((resolve, reject) => {
      login(username, userInfo.password)
        .then((response) => {
          const { data } = response;
          console.log("login response", data);
          commit("SET_TOKEN", data.token);
          commit("SET_USERID", data.user_id);
          setToken(data.token);
          setUserID(data.user_id);
          resolve();
        })
        .catch((error) => {
          reject(error);
        });
    });
  },

  // get user info
  getInfo({ commit, state }) {
    return new Promise((resolve, reject) => {
      getInfo({
        id: state.user_id,
      })
        .then((response) => {
          const { data } = response;
          if (!data) {
            return reject("Verification failed, please Login again.");
          }
          console.log(data.results[0], "=====");
          const { id, username, first_name, is_superuser, roles } =
            data.results[0];
          console.log(
            "get user info:",
            username,
            first_name,
            id,
            is_superuser,
            roles
          );
          commit("SET_NAME", username);
          commit("SET_USERID", id);
          commit("SET_SUPERUSER", is_superuser);
          commit("SET_ROLES", roles);
          resolve(data.results[0]);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },

  // user logout
  logout({ commit, state }) {
    return new Promise((resolve, reject) => {
      logout(state.token)
        .then(() => {
          removeToken(); // must remove  token  first
          resetRouter();
          commit("RESET_STATE");
          resolve();
        })
        .catch((error) => {
          reject(error);
        });
    });
  },

  // remove token
  resetToken({ commit }) {
    return new Promise((resolve) => {
      removeToken(); // must remove  token  first
      commit("RESET_STATE");
      commit("SET_ROLES", []);
      resolve();
    });
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
};
