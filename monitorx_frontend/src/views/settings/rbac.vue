<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-tabs v-model="active_tab_name" @tab-click="tab_click">
        <!-- 用户管理--------------------------------------------------  -->
        <el-tab-pane label="用户管理" name="user_settings">
          <el-input
            v-model="input_select_user"
            placeholder="搜索用户"
            size="small"
            style="width: 400px"
            clearable
            @keyup.enter.native="search_user"
          >
            <el-select
              slot="prepend"
              v-model="select_input_user"
              size="small"
              style="width: 100px"
              placeholder="请选择"
            >
              <el-option label="用户名" value="username"></el-option>
              <el-option label="用户别名" value="first_name"></el-option>
            </el-select>
            <el-button
              slot="append"
              icon="el-icon-search"
              @click="search_user"
            ></el-button>
          </el-input>
          <el-button
            type="primary"
            size="small"
            icon="el-icon-circle-plus"
            style="margin-left: 10px"
            @click="create_user"
            >新增</el-button
          >
          <el-table :data="user_list" border size="small">
            <el-table-column prop="username" label="用户名"> </el-table-column>
            <el-table-column prop="first_name" label="别名"> </el-table-column>
            <el-table-column
              prop="is_active"
              label="状态"
              :formatter="format_user_active"
            >
            </el-table-column>
            <el-table-column
              prop="is_superuser"
              label="超管"
              :formatter="format_user_super"
            >
            </el-table-column>
            <el-table-column prop="groups" label="权限组">
              <template slot-scope="scoped">
                <el-tag v-for="(item, index) in scoped.row.groups" :key="index">
                  {{ item.name }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120px;">
              <template slot-scope="scoped">
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  size="mini"
                  @click="update_user(scoped.row)"
                ></el-button>
                <el-popconfirm
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left:10px"
                  @confirm="delete_user(scoped.row)"
                  @cancel="cancel_delete"
                >
                  <el-button
                    slot="reference"
                    type="danger"
                    icon="el-icon-delete"
                    size="mini"
                  ></el-button>
                </el-popconfirm>
              </template>
            </el-table-column>
          </el-table>
          <!-- 分页组件 -->
          <pagination
            v-show="user_list_total > 0"
            :total="user_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_user_list"
          ></pagination>
        </el-tab-pane>
        <!-- 权限分组管理-------------------------------------------------- -->
        <el-tab-pane label="权限分组" name="group_settings">
          <el-button
            type="primary"
            size="small"
            icon="el-icon-circle-plus"
            @click="create_group"
            >新增</el-button
          >
          <el-table :data="group_list" border size="small">
            <template slot="empty">
              <span>不好意思啊</span>
            </template>
            <el-table-column label="组名" prop="name"> </el-table-column>
            <el-table-column label="操作" width="120px;">
              <template slot-scope="scoped">
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  size="mini"
                  @click="update_group(scoped.row)"
                ></el-button>
                <el-popconfirm
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left: 10px"
                  @confirm="delete_group(scoped.row)"
                  @cancel="cancel_delete"
                >
                  <el-button
                    slot="reference"
                    type="danger"
                    icon="el-icon-delete"
                    size="mini"
                  ></el-button>
                </el-popconfirm>
              </template>
            </el-table-column>
          </el-table>
          <pagination
            v-show="group_total > 0"
            :total="group_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_group_list"
          ></pagination>
        </el-tab-pane>
        <!-- 用户分组管理-------------------------------------------------- -->
        <el-tab-pane label="用户分组" name="user_group_settings" disabled>
          <el-button
            type="primary"
            size="small"
            icon="el-icon-circle-plus"
            @click="create_user_group"
            >新增</el-button
          >
          <el-table
            ref="user_group_list_table_refs"
            :data="user_group_list"
            empty-text="啥也没有"
            size="small"
            border
          >
            <el-table-column label="分组名称" prop="name"> </el-table-column>
            <el-table-column label="管理员" prop="admin__first_name">
            </el-table-column>
            <el-table-column label="操作" width="120px;">
              <template slot-scope="scoped">
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  size="mini"
                  @click="update_user_group(scoped.row)"
                ></el-button>
                <el-popconfirm
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left: 10px"
                  @confirm="delete_user_group(scoped.row)"
                  @cancel="cancel_delete"
                >
                  <el-button
                    slot="reference"
                    type="danger"
                    icon="el-icon-delete"
                    size="mini"
                  ></el-button>
                </el-popconfirm>
              </template>
            </el-table-column>
          </el-table>
          <pagination
            v-show="user_group_list_total > 0"
            :total="user_group_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_user_group_list"
          ></pagination>
        </el-tab-pane>
      </el-tabs>
    </el-card>
    <!-- 用户管理Dialog--------------------------------------------------  -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="user_dialog"
      width="50%"
    >
      <el-form
        ref="user_formRef"
        :model="user_form"
        :rules="user_form_rules"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item label="用户名称" prop="username">
              <el-input v-model="user_form.username" size="small"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="用户别名" prop="first_name">
              <el-input v-model="user_form.first_name" size="small"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="密码" prop="password">
              <el-input
                v-model="user_form.password"
                size="small"
                :show-password="password_disable"
                :disabled="password_disable"
              >
                <el-button
                  slot="append"
                  icon="el-icon-lock"
                  @click="random_password"
                ></el-button>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="权限组" prop="groups">
              <el-select
                v-model="user_form.groups"
                placeholder="请选择用户分组"
                clearable
                filterable
                size="small"
              >
                <el-option
                  v-for="(item, index) in group_list"
                  :key="index"
                  :label="item.name"
                  :value="item.id"
                  size="small"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="活跃" prop="is_active">
              <el-switch
                v-model="user_form.is_active"
                active-color="#13ce66"
                inactive-color="#ff4949"
              >
              </el-switch>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="超管" prop="is_superuser">
              <el-switch
                v-model="user_form.is_superuser"
                active-color="#13ce66"
                inactive-color="#ff4949"
              >
              </el-switch>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button size="small" @click="user_dialog = false">取 消</el-button>
        <el-button type="primary" size="small" @click="submit_user"
          >确 定</el-button
        >
      </span>
    </el-dialog>
    <!-- 权限分组管理Dialog--------------------------------------------------  -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="group_dialog"
      width="60%"
    >
      <el-form
        ref="group_formRef"
        :model="group_form"
        :rules="group_form_rules"
        label-width="100px"
      >
        <el-form-item label="用户组名称" prop="name">
          <el-input v-model="group_form.name" size="small"></el-input>
        </el-form-item>
        <el-form-item label="权限" prop="permissions">
          <el-transfer
            v-model="target_perm_list"
            :right-default-checked="target_perm_list"
            :data="source_perm_list"
            :titles="['可用 权限', '选中 权限']"
            filter-placeholder="请输入权限名称"
            :format="{
              noChecked: '${total}',
              hasChecked: '${checked}/${total}'
            }"
            filterable
          ></el-transfer>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button size="small" @click="group_dialog = false">取 消</el-button>
        <el-button type="primary" size="small" @click="submit_group"
          >确 定</el-button
        >
      </span>
    </el-dialog>
    <!-- 用户分组管理Dialog-------------------------------------------------- -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="user_group_dialog"
      :show-close="false"
      width="60%"
    >
      <el-form
        ref="user_group_formRef"
        :model="user_group_form"
        :rules="user_group_form_rules"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item label="分组名称" prop="name">
              <el-input v-model="user_group_form.name" size="small"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="分组描述" prop="desc">
              <el-input v-model="user_group_form.desc" size="small"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="管理员" prop="admin">
              <el-select
                v-model="user_group_form.admin"
                placeholder="请选择管理员"
                clearable
                filterable
                size="small"
              >
                <el-option
                  v-for="(item, index) in all_user_list"
                  :key="index"
                  :label="item.first_name"
                  :value="item.id"
                  size="small"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="分组成员" prop="users">
              <el-select
                v-model="user_group_form.users"
                placeholder="请选择成员"
                clearable
                filterable
                multiple
                size="small"
              >
                <el-option
                  v-for="(item, index) in all_user_list"
                  :key="index"
                  :label="item.first_name"
                  :value="item.id"
                  size="small"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button size="small" @click="user_group_dialog = false"
          >取 消</el-button
        >
        <el-button type="primary" size="small" @click="submit_user_group"
          >确 定</el-button
        >
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import Pagination from "@/components/Pagination";
import checkPermission from "@/utils/permission";
// import permission from '@/directive/permission/index.js'
import { getPermList } from "@/api/perm";
import {
  createUser,
  getUserList,
  updateUserByID,
  deleteUserByID
} from "@/api/user";
import {
  createUserGroups,
  getUserGroups,
  updateUserGroup,
  deleteUserGroup
} from "@/api/user";
import {
  getCmdbUserGroupList,
  createCmdbUserGroup,
  updateCmdbUserGroup,
  deleteCmdbUserGroup
} from "@/views/settings/apis/user_group";
import {
  getRolerList,
  getUserRoleGroup,
  createUserRoleGroup,
  updateUserRoleGroupByID,
  deleteUserRoleGroup
} from "@/views/cmdb/api/user_group";
export default {
  name: "RBAC",
  components: {
    Pagination
  },
  // directives: {
  //   permission
  // },
  data() {
    return {
      list_query: {
        page: 1,
        limit: 15
      },
      active_tab_name: "user_settings",
      dialog_map: {
        create_user: "新增用户",
        update_user: "编辑用户",
        create_group: "新增分组",
        update_group: "编辑分组",
        create_user_group: "新增用户分组",
        update_user_group: "编辑用户分组"
      },
      dialog_status: "",
      // 用户管理--------------------------------------------------
      input_select_user: "",
      select_input_user: "username",
      user_list: [],
      user_list_total: 0,
      all_user_list: [],
      current_user_group_id: 0,
      role_list: [],
      role_list_total: 0,
      user_role_group_list: [],
      user_dialog: false,
      user_form: {
        id: "",
        username: "",
        first_name: "",
        password: "",
        is_active: true,
        is_superuser: false,
        groups: ""
      },
      password_disable: true,
      user_form_rules: {
        username: [{ required: true, message: "不能为空", trigger: "blur" }],
        first_name: [{ required: true, message: "不能为空", trigger: "blur" }],
        password: [{ required: true, message: "不能为空", trigger: "blur" }],
        groups: [
          { required: true, message: "不能为空", trigger: ["blur", "change"] }
        ]
      },
      format_user_active: function(row, column, cellValue) {
        var ret = "";
        if (cellValue) {
          ret = "活跃";
        } else {
          ret = "僵尸";
        }
        return ret;
      },
      format_user_super: function(row, column, cellValue) {
        var ret = "";
        if (cellValue) {
          ret = "是";
        } else {
          ret = "否";
        }
        return ret;
      },
      // 权限管理--------------------------------------------------
      perm_list: [],
      perm_list_total: 0,
      // 权限分组管理--------------------------------------------------
      group_list: [],
      group_total: 0,
      group_dialog: false,
      group_form: {
        id: "",
        name: "",
        permissions: []
      },
      group_form_rules: {
        name: [{ required: true, message: "不能为空", trigger: "blur" }]
      },
      target_perm_list: [],
      target_perm_temp_list: [],
      source_perm_list: [],
      source_perm_total: 0,
      source_perm_temp_list: [],
      user_group_list: [],
      user_group_list_total: 0,
      user_group_dialog: false,
      user_group_form: {
        id: null,
        name: null,
        desc: null,
        admin: null,
        users: []
      },
      user_group_form_rules: {
        name: [{ required: true, message: "不能为空", trigger: "blur" }],
        desc: [{ required: true, message: "不能为空", trigger: "blur" }],
        admin: [{ required: true, message: "不能为空", trigger: "blur" }]
        // users: [{ required: true, message: "不能为空", trigger: "blur" }]
      }
    };
  },
  computed: {
    ...mapGetters(["user_id", "is_superuser"])
  },
  created() {
    this.get_user_list();
    this.get_role_list();
    this.get_all_user();
    this.get_user_group_list();
  },
  methods: {
    checkPermission,
    tab_click(tab) {
      if (tab.name === "user_settings") {
        this.get_user_list();
        this.get_group_list();
      } else if (tab.name === "group_settings") {
        this.get_perm_list();
        this.get_original_perm_list();
        this.get_group_list();
      } else if (tab.name === "user_group_settings") {
        this.get_user_group_list();
      }
    },
    // 用户管理--------------------------------------------------
    random_password() {
      const chars = "ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz123456789";
      var pwd = "";
      for (let i = 0; i < 20; i++) {
        pwd += chars.charAt(Math.floor(Math.random() * chars.length));
      }
      this.user_form.password = pwd;
    },
    create_user() {
      this.dialog_status = "create_user";
      this.user_dialog = true;
      this.user_form.username = null;
      this.user_form.first_name = null;
      this.user_form.password = null;
      this.user_form.groups = null;
      this.password_disable = false;
      this.get_group_list();
    },
    // 编辑用户
    update_user(row) {
      this.dialog_status = "update_user";
      this.user_dialog = true;
      this.user_form = Object.assign({}, row);
      for (let index = 0; index < row.groups.length; index++) {
        const element = row.groups[index];
        this.user_form.groups = element.id;
      }
      // this.user_form.groups = 4;
      if (this.is_superuser || row.id === this.user_id) {
        this.password_disable = false;
      } else {
        this.password_disable = true;
      }
      this.get_group_list();
    },
    // 提交用户Dialog
    submit_user() {
      if (this.dialog_status === "create_user") {
        createUser(this.user_form)
          .then(resp => {
            this.$message({
              type: "success",
              message: "新增用户【" + this.user_form.username + "】成功"
            });
            this.user_dialog = false;
            this.get_user_list();
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            });
            this.user_dialog = false;
            this.get_user_list();
          });
      } else if (this.dialog_status === "update_user") {
        updateUserByID(this.user_form.id, this.user_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新用户【" + this.user_form.username + "】成功"
            });
            this.user_dialog = false;
            this.get_user_list();
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            });
            this.user_dialog = false;
            this.get_user_list();
          });
      }
    },
    // 删除用户
    delete_user(row) {
      deleteUserByID(row.id)
        .then(() => {
          this.$message({
            type: "success",
            message: "删除用户【" + row.username + "】成功"
          });
          this.get_user_list();
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          });
          this.get_user_list();
        });
    },
    // 查找用户
    search_user() {
      const params = this.select_input_user + "__contains";
      this.list_query[params] = this.input_select_user;
      getUserList(this.list_query)
        .then(resp => {
          this.user_list = resp.data.results;
          this.user_list_total = resp.data.count;
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          });
        });
    },
    // 获取用户列表
    get_user_list() {
      getUserList(this.list_query)
        .then(resp => {
          this.user_list = resp.data.results;
          this.user_list_total = resp.data.count;
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          });
        });
    },
    // 获取用户列表
    get_all_user() {
      const req = {
        page: 1,
        limit: 999
      };
      getUserList(req)
        .then(resp => {
          this.all_user_list = resp.data.results;
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          });
        });
    },
    // 获取用户列表
    get_role_list() {
      getRolerList(this.list_query)
        .then(resp => {
          this.role_list = resp.data.results;
          this.role_list_total = resp.data.count;
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          });
        });
    },
    onAddItem() {
      this.user_role_group_list.unshift({
        id: -1,
        user_name: "",
        role__name: ""
      });
    },
    deleteRow(data) {
      deleteUserRoleGroup(data.row.id)
        .then(() => {
          this.$message({
            type: "success",
            message: "删除成功"
          });
          this.user_role_group_list.splice(data.$index, 1);
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          });
        });
    },
    confirmChange(data) {
      const req = {
        group: this.current_user_group_id,
        user: data.row.user,
        role: data.row.role
      };
      if (data.row.id === -1) {
        if (
          typeof data.row.user === "undefined" ||
          typeof data.row.role === "undefined"
        ) {
          this.$message({
            type: "error",
            message: "空的!不能提交!!"
          });
        } else {
          createUserRoleGroup(req)
            .then(resp => {
              this.$message({
                type: "success",
                message: "新增用户角色组成功"
              });
            })
            .catch(err => {
              this.$message({
                type: "error",
                message: err
              });
            });
        }
      } else {
        if (data.row.user === "" || data.row.role === "") {
          this.$message({
            type: "error",
            message: "空的!不能提交!!"
          });
        } else {
          updateUserRoleGroupByID(data.row.id, req)
            .then(resp => {
              this.$message({
                type: "success",
                message: "更新用户角色组成功"
              });
            })
            .catch(err => {
              this.$message({
                type: "error",
                message: err
              });
            });
        }
      }
    },
    // 获取权限列表
    get_perm_list() {
      getPermList({ limit: 999 })
        .then(resp => {
          this.source_perm_temp_list = Object.keys(resp.data.results).map(
            function(key) {
              return {
                key: resp.data.results[key]["id"],
                label: resp.data.results[key]["name"]
              };
            }
          );
          this.source_perm_total = resp.data.count;
          this.source_perm_list = this.source_perm_temp_list;
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          });
        });
      this.list_query = {};
    },
    get_original_perm_list() {
      getPermList({ limit: 999 }).then(resp => {
        this.perm_list = resp.data.results;
        this.perm_list_total = resp.data.count;
      });
    },
    // 获取用户组列表
    get_group_list() {
      getUserGroups(this.listQuery)
        .then(response => {
          this.group_list = response.data.results;
          this.group_total = response.data.count;
          setTimeout(() => {
            this.listLoading = false;
          }, 1.5 * 1000);
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          });
        });
    },
    // 新增用户组
    create_group() {
      this.dialog_status = "create_group";
      this.group_dialog = true;
      this.group_form.name = null;
      this.target_perm_list = [];
      this.target_perm_temp_list = [];
    },
    // 编辑用户组
    update_group(row) {
      this.get_perm_list();
      this.dialog_status = "update_group";
      this.group_dialog = true;
      this.group_form = Object.assign({}, row);
      this.target_perm_temp_list = Object.keys(row.permissions).map(function(
        key
      ) {
        return row.permissions[key]["id"];
      });
      this.target_perm_list = this.target_perm_temp_list;
    },
    // 提交用户组Dialog
    submit_group() {
      if (this.dialog_status === "create_group") {
        createUserGroups(this.group_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "新增用户组成功"
            });
            this.group_dialog = false;
            this.get_group_list();
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            });
            this.group_dialog = false;
            this.get_group_list();
          });
      } else if (this.dialog_status === "update_group") {
        this.group_form.permissions = this.target_perm_list;
        updateUserGroup(this.group_form.id, this.group_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新用户组成功"
            });
            this.group_dialog = false;
            this.get_group_list();
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            });
            this.group_dialog = false;
            this.get_group_list();
          });
      }
    },
    // 删除用户组
    delete_group(row) {
      deleteUserGroup(row.id)
        .then(() => {
          this.$message({
            type: "success",
            message: "删除用户组【" + row.name + "】成功"
          });
          this.get_group_list();
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          });
          this.get_group_list();
        });
    },
    create_user_group() {
      this.dialog_status = "create_user_group";
      this.user_group_dialog = true;
      this.user_group_form.name = null;
      this.user_group_form.desc = null;
      this.user_group_form.admin = null;
      this.user_role_group_list = [];
      this.get_user_list();
    },
    update_user_group(row) {
      // console.log("update_user_group", row)
      this.dialog_status = "update_user_group";
      this.user_group_dialog = true;
      this.user_group_form = Object.assign({}, row);
      const req = {
        limit: 999,
        group_id: row.id
      };
      this.current_user_group_id = row.id;
      getUserRoleGroup(req)
        .then(resp => {
          // console.log("getUserRoleGroup", resp.data.results)
          this.user_role_group_list = resp.data.results;
          // this.user_group_form.users = resp.data.results.map(function(item) {
          //   return item.id
          // })
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          });
        });
      this.get_user_list();
    },
    delete_user_group(row) {
      deleteCmdbUserGroup(row.id)
        .then(resp => {
          this.user_group_list = resp.data.results;
          this.user_group_list_total = resp.data.count;
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          });
        });
    },
    submit_user_group() {
      if (this.dialog_status === "create_user_group") {
        createCmdbUserGroup(this.user_group_form)
          .then(resp => {
            this.$message({
              type: "success",
              message: "新增分组【" + this.user_group_form.name + "】成功"
            });
            this.user_group_dialog = false;
            this.get_user_group_list();
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            });
            this.user_group_dialog = false;
            this.get_user_group_list();
          });
      } else if (this.dialog_status === "update_user_group") {
        // console.log("update_user_group", this.user_group_form)
        updateCmdbUserGroup(this.user_group_form.id, this.user_group_form)
          .then(() => {
            this.$message({
              type: "success",
              message:
                "更新分组【" +
                this.user_group_form.name +
                "】成功, 刷新以更新产品选择器"
            });
            this.user_group_dialog = false;
            this.get_user_group_list();
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            });
            this.user_group_dialog = false;
            this.get_user_group_list();
          });
      }
    },
    get_user_group_list() {
      getCmdbUserGroupList(this.list_query)
        .then(resp => {
          // console.log("listQuery", this.list_query)
          // console.log("resp",)
          this.user_group_list = resp.data.results;
          this.user_group_list_total = resp.data.count;
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          });
        });
    },
    cancel_delete() {
      this.$message({
        type: "warning",
        message: "你考虑的很全面"
      });
    }
  }
};
</script>

<style scoped>
.el-input {
  width: 200px;
}
.el-select {
  width: 200px;
}
.el-table {
  width: 100%;
  margin-top: 10px;
}
.el-button {
  vertical-align: top;
}
</style>
