<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-tabs
        v-model="active_tab_name"
        @tab-click="active_tab_click"
      >
        <!-- 用户管理--------------------------------------------------  -->
        <el-tab-pane
          label="用户管理"
          name="user_settting"
        >
          <el-input
            v-model="input_content"
            placeholder="搜索用户"
            size="small"
            style="width: 400px"
            clearable
            @keyup.enter.native="search_user"
          >
            <el-select
              slot="prepend"
              v-model="select_content"
              size="small"
              style="width: 100px"
              placeholder="请选择"
            >
              <el-option
                label="用户名"
                value="username"
              ></el-option>
              <el-option
                label="用户别名"
                value="first_name"
              ></el-option>
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
          >新增</el-button>
          <el-table
            ref="user_list_table_refs"
            :data="user_list"
            empty-text="啥也没有"
            size="small"
            border
          >
            <el-table-column
              prop="username"
              label="用户名"
            >
            </el-table-column>
            <el-table-column
              prop="first_name"
              label="别名"
            >
            </el-table-column>
            <el-table-column
              label="邮箱"
              prop="email"
            >
            </el-table-column>
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
            <el-table-column
              prop="groups"
              label="权限组"
            >
              <template slot-scope="scoped">
                <el-tag
                  v-for="(item, index) in scoped.row.groups"
                  :key="index"
                >
                  {{ item.name }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column
              label="操作"
              width="120px"
            >
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
          <pagination
            v-show="user_list_total>0"
            :total="user_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_user_list"
          ></pagination>
        </el-tab-pane>
        <!-- 权限分组管理--------------------------------------------------  -->
        <el-tab-pane
          v-if="checkPermission(['admin'])"
          label="权限分组"
          name="perm_group_settting"
        >
          <el-button
            type="primary"
            size="small"
            icon="el-icon-circle-plus"
            @click="create_perm_group"
          >新增</el-button>
          <el-table
            ref="group_list_table_refs"
            :data="group_list"
            empty-text="啥也没有"
            size="small"
            border
          >
            <el-table-column
              label="组名"
              prop="name"
            >
            </el-table-column>
            <el-table-column
              label="操作"
              width="120px"
            >
              <template slot-scope="scoped">
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  size="mini"
                  @click="update_perm_group(scoped.row)"
                ></el-button>
                <el-popconfirm
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left: 10px"
                  @confirm="delete_perm_group(scoped.row)"
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
            v-show="group_list_total>0"
            :total="group_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_perm_group_list"
          ></pagination>
        </el-tab-pane>
        <!-- 用户分组管理--------------------------------------------------  -->
        <el-tab-pane
          label="用户分组"
          name="user_group_settings"
        >
          <el-button
            type="primary"
            size="small"
            icon="el-icon-circle-plus"
            @click="create_user_group"
          >新增</el-button>
          <el-table
            ref="user_group_list_table_refs"
            :data="user_group_list"
            empty-text="啥也没有"
            size="small"
            border
          >
            <el-table-column
              label="分组名称"
              prop="name"
            >
            </el-table-column>
            <el-table-column
              label="管理员"
              prop="admin__first_name"
            >
            </el-table-column>
            <el-table-column
              label="操作"
              width="120px"
            >
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
            v-show="user_group_list_total>0"
            :total="user_group_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_user_group_list"
          ></pagination>
        </el-tab-pane>
      </el-tabs>
    </el-card>
    <!-- 用户管理dialog--------------------------------------------------  -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="user_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="50%"
    >
      <el-form
        ref="user_formRef"
        :model="user_form"
        :rules="user_form_rules"
        size="small"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="用户名称"
              prop="username"
            >
              <el-input v-model="user_form.username"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="用户别名"
              prop="first_name"
            >
              <el-input v-model="user_form.first_name"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="用户分组"
              prop="groups"
            >
              <el-select
                v-model="user_form.groups"
                placeholder="请选择用户分组"
                clearable
                filterable
              >
                <el-option
                  v-for="(item, index) in group_list"
                  :key="index"
                  :label="item.name"
                  :value="item.id"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="用户密码"
              prop="password"
            >
              <el-input
                v-model="user_form.password"
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
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="用户邮箱"
              prop="email"
            >
              <el-input v-model="user_form.email"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="是否活跃"
              prop="is_active"
            >
              <el-radio-group v-model="user_form.is_active">
                <el-radio :label="true">是</el-radio>
                <el-radio :label="false">否</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="是否超管"
              prop="is_superuser"
            >
              <el-radio-group v-model="user_form.is_superuser">
                <el-radio :label="true">是</el-radio>
                <el-radio :label="false">否</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="user_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_user"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 权限分组管理dialog--------------------------------------------------  -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="group_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="60%"
    >
      <el-form
        ref="group_formRef"
        :model="group_form"
        :rules="group_form_rules"
        size="small"
        label-width="100px"
      >
        <el-form-item
          label="用户组名"
          prop="name"
        >
          <el-input v-model="group_form.name"></el-input>
        </el-form-item>
        <el-form-item
          label="权限"
          prop="permissions"
        >
          <el-transfer
            v-model="target_perm_list"
            :right-default-checked="target_perm_list"
            :data="source_perm_list"
            :titles="['可用 权限', '选中 权限']"
            filter-placeholder="请输入权限名称"
            :format="{noChecked: '${total}',hasChecked: '${checked}/${total}'}"
            filterable
          ></el-transfer>
        </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="group_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_perm_group"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 用户分组dialog--------------------------------------------------  -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="user_group_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="60%"
    >
      <el-form
        ref="user_group_formRef"
        :model="user_group_form"
        :rules="user_group_form_rules"
        size="small"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="分组名称"
              prop="name"
            >
              <el-input v-model="user_group_form.name"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="分组描述"
              prop="desc"
            >
              <el-input v-model="user_group_form.desc"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="管理员"
              prop="admin"
            >
              <el-select
                v-model="user_group_form.admin"
                placeholder="请选择管理员"
                clearable
                filterable
              >
                <el-option
                  v-for="(item, index) in user_list"
                  :key="index"
                  :label="item.first_name"
                  :value="item.id"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="分组成员"
              prop="users"
            >
              <el-select
                v-model="user_group_form.users"
                placeholder="请选择成员"
                multiple
                filterable
              >
                <el-option
                  v-for="(item, index) in user_list"
                  :key="index"
                  :label="item.first_name"
                  :value="item.id"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="user_group_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_user_group"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"
import permission from "@/directive/permission/index.js"
import checkPermission from '@/utils/permission'
import { mapGetters } from "vuex"

import { createGroup, getGroupList, updateGroup } from "@/views/settings/apis/group"
import { getPermList } from "@/views/settings/apis/perm"
import { createUser, deleteUser, getUserList, updateUser } from "@/views/settings/apis/user"
import { createUserGroup, getUserGroupList, updateUserGroup } from "@/views/settings/apis/user_group"

export default {
  name: "SettingsRBAC",
  components: {
    Pagination
  },
  directives: {
    permission
  },
  data() {
    return {
      list_query: {
        page: 1,
        limit: 15
      },
      active_tab_name: "user_settting",
      dialog_map: {
        create_user: "新增用户",
        update_user: "编辑用户",
        create_perm_group: "新增权限分组",
        update_perm_group: "编辑权限分组",
        create_perm: "新增权限",
        update_perm: "编辑权限",
        create_user_group: "新增用户分组",
        update_user_group: "编辑用户分组"
      },
      dialog_status: "",
      // 用户管理--------------------------------------------------
      input_content: "",
      select_content: "username",
      user_list: [],
      user_list_total: 0,
      user_dialog: false,
      user_form: {
        id: null,
        username: null,
        password: null,
        first_name: null,
        email: null,
        is_active: true,
        is_superuser: false,
        groups: []
      },
      password_disable: true,
      user_form_rules: {
        username: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        password: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        email: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        first_name: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        groups: [{ required: true, message: '不能为空', trigger: ['blur', 'change'] }],
        is_active: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        is_superuser: [{ required: true, message: '不能为空', trigger: ['blur'] }]
      },
      format_user_active: function (row, column, cellValue) {
        var ret = ""
        if (cellValue) {
          ret = "活跃"
        } else {
          ret = "禁止"
        }
        return ret
      },
      format_user_super: function (row, column, cellValue) {
        var ret = ""
        if (cellValue) {
          ret = "是"
        } else {
          ret = "否"
        }
        return ret
      },
      // 权限分组--------------------------------------------------
      group_list: [],
      group_list_total: 0,
      group_dialog: false,
      group_form: {
        id: null,
        name: null,
        permissions: []
      },
      group_form_rules: {
        name: [{ required: true, message: '不能为空', trigger: ['blur'] }]
      },
      source_perm_list: [],
      source_perm_total: 0,
      target_perm_list: [],
      // 权限管理--------------------------------------------------
      perm_list: [],
      perm_list_total: 0,
      perm_dialog: false,
      perm_form: {},
      perm_form_rules: {},
      // 用户分组管理--------------------------------------------------
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
        name: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        desc: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        admin: [{ required: true, message: '不能为空', trigger: ['blur', 'change'] }],
        users: [{ required: true, message: '不能为空', trigger: ['blur', 'change'] }]
      }
    }
  },
  computed: {
    ...mapGetters(["user_id", "is_superuser"])
  },
  created() {
    this.get_user_list()
  },
  methods: {
    checkPermission,
    active_tab_click(tab) {
      if (tab.name === "user_settting") {
        this.get_user_list()
      } else if (tab.name === "perm_group_settting") {
        this.get_perm_group_list()
      } else if (tab.name === "user_group_settings") {
        this.get_user_group_list()
      }
    },
    // 用户管理--------------------------------------------------
    random_password() {
      const chars = "ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz123456789"
      var pwd = ""
      for (let i = 0; i < 20; i++) {
        pwd += chars.charAt(Math.floor(Math.random() * chars.length))
      }
      this.user_form.password = pwd
    },
    create_user() {
      this.dialog_status = "create_user"
      this.user_dialog = true
      this.user_form.username = null
      this.user_form.first_name = null
      this.user_form.password = null
      this.user_form.email = null
      this.user_form.is_active = true
      this.user_form.is_superuser = false
      this.user_form.groups = null
      this.password_disable = false
      this.get_perm_group_list()
    },
    update_user(row) {
      this.dialog_status = "update_user"
      this.user_dialog = true
      this.user_form = Object.assign({}, row)
      // this.user_form.id = row.id
      // this.user_form.username = row.username
      // this.user_form.first_name = row.first_name
      // this.user_form.password = row.password
      // this.user_form.is_active = row.is_active
      // this.user_form.is_superuser = row.is_superuser
      console.log(this.user_form)
      this.get_perm_group_list()
      for (let index = 0; index < row.groups.length; index++) {
        const element = row.groups[index]
        this.user_form.groups = element.id
      }
      if (row.id === this.user_id) {
        this.password_disable = false
      } else if (this.is_superuser) {
        this.password_disable = false
      } else {
        this.password_disable = true
      }
    },
    search_user() {
      const params = this.select_content + "__contains"
      this.list_query[params] = this.input_content
      getUserList(this.list_query)
        .then((resp) => {
          this.user_list = resp.data.results
          this.user_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    submit_user() {
      if (this.dialog_status === "create_user") {
        delete this.user_form.id
        createUser(this.user_form)
          .then((resp) => {
            this.$message({
              type: "success",
              message: "新增成功"
            })
            this.user_dialog = false
            this.get_user_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.user_dialog = false
            this.get_user_list()
          })
      } else if (this.dialog_status === "update_user") {
        updateUser(this.user_form.id, this.user_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新成功"
            })
            this.user_dialog = false
            this.get_user_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.user_dialog = false
            this.get_user_list()
          })
      }
    },
    delete_user(row) {
      deleteUser(row.id)
        .then(() => {
          this.$message({
            type: "success",
            message: "删除用户【" + row.username + "】成功"
          })
          this.get_user_list()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
          this.get_user_list()
        })
    },
    get_user_list() {
      getUserList(this.list_query)
        .then((resp) => {
          this.user_list = resp.data.results
          this.user_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 分组管理--------------------------------------------------
    create_perm_group() {
      this.dialog_status = "create_perm_group"
      this.group_dialog = true
      this.group_form.name = null
      this.target_perm_list = []
      this.get_perm_list()
    },
    update_perm_group(row) {
      this.get_perm_list()
      this.dialog_status = "update_perm_group"
      this.group_dialog = true
      this.group_form = Object.assign({}, row)
      this.target_perm_temp_list = Object.keys(row.permissions).map(function (
        key
      ) {
        return row.permissions[key]["id"]
      })
      this.target_perm_list = this.target_perm_temp_list
    },
    submit_perm_group() {
      if (this.dialog_status === "create_perm_group") {
        createGroup(this.group_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "新增权限组成功"
            })
            this.group_dialog = false
            this.get_perm_group_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.group_dialog = false
            this.get_perm_group_list()
          })
      } else if (this.dialog_status === "update_perm_group") {
        this.group_form.permissions = this.target_perm_list
        updateGroup(this.group_form.id, this.group_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新权限组成功"
            })
            this.group_dialog = false
            this.get_perm_group_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.group_dialog = false
            this.get_perm_group_list()
          })
      }
    },
    delete_perm_group() { },
    get_perm_group_list() {
      getGroupList(this.list_query)
        .then((resp) => {
          this.group_list = resp.data.results
          this.group_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 权限管理--------------------------------------------------
    create_perm() { },
    update_perm() { },
    delete_perm() { },
    get_perm_list() {
      getPermList({ limit: 999 })
        .then((resp) => {
          this.source_perm_temp_list = Object.keys(resp.data.results).map(
            function (key) {
              return {
                key: resp.data.results[key]["id"],
                label: resp.data.results[key]["name"]
              }
            }
          )
          this.source_perm_total = resp.data.count
          this.source_perm_list = this.source_perm_temp_list
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 用户分组管理--------------------------------------------------
    create_user_group() {
      this.dialog_status = "create_user_group"
      this.user_group_dialog = true
      this.user_group_form.name = null
      this.user_group_form.desc = null
      this.user_group_form.admin = null
      this.user_group_form.users = []
      this.get_user_list()
    },
    update_user_group(row) {
      this.dialog_status = "update_user_group"
      this.user_group_dialog = true
      this.user_group_form = Object.assign({}, row)
      this.get_user_list()
    },
    delete_user_group() { },
    submit_user_group() {
      if (this.dialog_status === "create_user_group") {
        createUserGroup(this.user_group_form)
          .then((resp) => {
            this.$message({
              type: "success",
              message: "新增分组【" + this.user_group_form.name + "】成功"
            })
            this.user_group_dialog = false
            this.get_user_group_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.user_group_dialog = false
            this.get_user_group_list()
          })
      } else if (this.dialog_status === "update_user_group") {
        updateUserGroup(this.user_group_form.id, this.user_group_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新分组【" + this.user_group_form.name + "】成功"
            })
            this.user_group_dialog = false
            this.get_user_group_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.user_group_dialog = false
            this.get_user_group_list()
          })
      }
    },
    get_user_group_list() {
      getUserGroupList(this.list_query)
        .then((resp) => {
          this.user_group_list = resp.data.results
          this.user_group_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    cancel_delete() {
      this.$message({
        type: "warning",
        message: "你考虑的很全面"
      })
    }
  }
}
</script>

<style scoped>
.el-input {
  width: 200px;
}
.el-select {
  width: 200px;
}
.el-button {
  vertical-align: top;
}
.el-table {
  width: 100%;
  margin-top: 10px;
}
</style>
