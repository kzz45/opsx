/* eslint-disable */

import { login, social_login, idass_login, logout, getInfo } from "@/api/user";
import { getUserRoleGroup } from "@/views/cmdb/api/user_group";
import {
  getToken,
  getIdToken,
  setToken,
  setIdToken,
  removeToken,
  removeIdToken,
  getUserID,
  setUserID
} from "@/utils/auth";

const getDefaultState = () => {
  return {
    token: getToken(),
    name: "",
    first_name: "",
    user_id: getUserID(),
    is_superuser: false,
    avatar: "",
    id_token: getIdToken(),
    roles: [],
    groups: [],
    is_ops: false,
    is_finance: false,
    is_qa: false,
    is_readonly: false,
    is_dev: false,
    is_security: false
  };
};

const state = getDefaultState();

const mutations = {
  RESET_STATE: state => {
    Object.assign(state, getDefaultState());
  },
  SET_TOKEN: (state, token) => {
    state.token = token;
  },
  SET_IDTOKEN: (state, id_token) => {
    state.id_token = id_token;
  },
  SET_NAME: (state, name) => {
    state.name = name;
  },
  SET_FIRST_NAME: (state, first_name) => {
    state.name = first_name;
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
  SET_GROUPS: (state, groups) => {
    state.groups = groups;
  },
  SET_GROUP_ROLES: (state, group_roles) => {
    state.group_roles = group_roles;
  },
  SET_OPS: (state, ops) => {
    state.is_ops = ops;
  },
  SET_FINANCE: (state, finance) => {
    state.is_finance = finance;
  },
  SET_QA: (state, qa) => {
    state.is_qa = qa;
  },
  SET_DEV: (state, dev) => {
    state.is_dev = dev;
  },
  SET_READONLY: (state, readonly) => {
    state.is_readonly = readonly;
  },
  SET_SECURITY: (state, security) => {
    state.is_security = security;
  },
  SET_AVATAR: (state, avatar) => {
    state.avatar = avatar;
  }
};

const actions = {
  // user login
  login({ commit }, userInfo) {
    const username = userInfo.username.trim();
    return new Promise((resolve, reject) => {
      login(username, userInfo.password)
        .then(response => {
          const { data } = response;
          // console.log('login response', data)
          commit("SET_TOKEN", data.token);
          commit("SET_USERID", data.user_id);
          setToken(data.token);
          setUserID(data.user_id);
          resolve();
        })
        .catch(error => {
          reject(error);
        });
    });
  },
  getUserRoleGroup({ commit, state }) {
    return new Promise((resolve, reject) => {
      getUserRoleGroup({ user_id: state.user_id, limit: 999 })
        .then(response => {
          const groupList = response.data.results;
          // console.log("getUserGroup", groupList)
          const groups = [];
          const groupRoles = {};
          for (let i = 0; i < groupList.length; i++) {
            const groupName = groupList[i].group__name;
            const role = groupList[i].role__name;
            groups.push(groupName);
            groupRoles[groupName] = role;
          }
          for (var group_role in groupRoles) {
            if (groupRoles[group_role] == "运维") {
              commit("SET_OPS", true);
            }
            if (groupRoles[group_role] == "财务") {
              commit("SET_FINANCE", true);
            }
            if (groupRoles[group_role] == "研发") {
              commit("SET_DEV", true);
            }
            if (groupRoles[group_role] == "测试") {
              commit("SET_QA", true);
            }
            if (groupRoles[group_role] == "只读") {
              commit("SET_READONLY", true);
            }
            if (groupRoles[group_role] == "安全") {
              commit("SET_SECURITY", true);
            }
          }
          commit("SET_GROUPS", groups);
          commit("SET_GROUP_ROLES", groupRoles);
          resolve(response);
        })
        .catch(error => {
          reject(error);
        });
    });
  },
  // get user info
  getInfo({ commit, state }) {
    return new Promise((resolve, reject) => {
      getInfo({
        id: state.user_id
      })
        .then(response => {
          const { data } = response;
          // console.log("data.results[0]", data.results[0])
          if (!data) {
            return reject("Verification failed, please Login again.");
          }
          const {
            id,
            username,
            first_name,
            is_superuser,
            roles
          } = data.results[0];
          // console.log('get user info:', username, first_name, id, is_superuser, roles)
          if (state.is_finance) {
            roles.push("finance");
          }
          if (state.is_ops) {
            roles.push("ops");
          }
          if (state.is_qa) {
            roles.push("qa");
          }
          if (state.is_dev) {
            roles.push("dev");
          }
          if (state.is_readonly) {
            roles.push("readonly");
          }
          if (state.is_security) {
            roles.push("security");
          }
          commit("SET_NAME", username);
          commit("SET_FIRST_NAME", first_name);
          commit("SET_USERID", id);
          commit("SET_SUPERUSER", is_superuser);
          commit("SET_ROLES", roles);
          resolve(data);
        })
        .catch(error => {
          reject(error);
        });
    });
  },

  // user logout
  logout({ commit, state }) {
    return new Promise((resolve, reject) => {
      logout(state.token)
        .then(() => {
          removeToken();
          commit("RESET_STATE");
          resolve();
        })
        .catch(error => {
          reject(error);
        });
    });
  },

  // remove token
  resetToken({ commit }) {
    return new Promise(resolve => {
      removeToken();
      commit("RESET_STATE");
      commit("SET_ROLES", []);
      resolve();
    });
  }
};

export default {
  namespaced: true,
  state,
  mutations,
  actions
};
