<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-tabs
        v-model="active_tab_name"
        @tab-click="active_tab_click"
      >
        <!-- 产品管理--------------------------------------------------  -->
        <el-tab-pane
          label="产品管理"
          name="product_settings"
        >
          <el-button
            type="primary"
            size="small"
            icon="el-icon-circle-plus"
            @click="create_product"
          >新增</el-button>
          <el-table
            ref="product_list_table_refs"
            :data="product_list"
            empty-text="啥也没有"
            size="small"
            border
          >
            <el-table-column
              label="产品名称"
              prop="name"
            >
            </el-table-column>
            <el-table-column
              label="产品描述"
              prop="desc"
            >
            </el-table-column>
            <el-table-column
              label="用户组"
              prop="user_group__name"
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
                  @click="update_product(scoped.row)"
                ></el-button>
                <el-popconfirm
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left: 10px"
                  @confirm="delete_product(scoped.row)"
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
            v-show="product_list_total>0"
            :total="product_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_product_list"
          ></pagination>
        </el-tab-pane>
        <!-- 项目管理--------------------------------------------------  -->
        <el-tab-pane
          label="项目管理"
          name="project_settings"
        >
          <el-button
            type="primary"
            size="small"
            icon="el-icon-circle-plus"
            @click="create_project"
          >新增</el-button>
          <el-table
            ref="project_list_table_refs"
            :data="project_list"
            empty-text="啥也没有"
            size="small"
            border
          >
            <el-table-column
              label="项目名称"
              prop="name"
            >
            </el-table-column>
            <el-table-column
              label="项目描述"
              prop="desc"
            >
            </el-table-column>
            <el-table-column
              label="所属产品"
              prop="product__name"
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
                  @click="update_project(scoped.row)"
                ></el-button>
                <el-popconfirm
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left: 10px"
                  @confirm="delete_project(scoped.row)"
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
            v-show="project_list_total>0"
            :total="project_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_project_list"
          ></pagination>
        </el-tab-pane>
        <!-- Jenkins管理--------------------------------------------------  -->
        <!-- v-permission="['admin']" -->
        <!-- <el-tab-pane
          v-if="checkPermission(['admin'])"
          label="Jenkins管理"
          name="jenkins_settings"
        >
          <el-button
            type="primary"
            size="small"
            icon="el-icon-circle-plus"
            @click="create_jenkins"
          >新增</el-button>
          <el-table
            ref="jenkins_list_table_refs"
            :data="jenkins_list"
            empty-text="啥也没有"
            size="small"
            border
          >
            <el-table-column
              label="名称"
              prop="name"
            >
            </el-table-column>
            <el-table-column
              label="地址"
              prop="addr"
            >
            </el-table-column>
            <el-table-column
              label="操作"
              width="180px"
            >
              <template slot-scope="scoped">
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  size="mini"
                  @click="update_jenkins(scoped.row)"
                ></el-button>
                <el-popconfirm
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left: 10px"
                  @confirm="delete_jenkins(scoped.row)"
                  @cancel="cancel_delete"
                >
                  <el-button
                    slot="reference"
                    type="danger"
                    icon="el-icon-delete"
                    size="mini"
                  ></el-button>
                </el-popconfirm>
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="去看看"
                  placement="top"
                >
                  <el-button
                    type="success"
                    icon="el-icon-s-promotion"
                    size="mini"
                    style="margin-left: 10px;"
                    @click="goto_jenkins(scoped.row)"
                  ></el-button>
                </el-tooltip>
              </template>
            </el-table-column>
          </el-table>
          <pagination
            v-show="jenkins_list_total>0"
            :total="jenkins_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_jenkins_list"
          ></pagination>
        </el-tab-pane> -->
        <!-- Gitlab管理--------------------------------------------------  -->
        <!-- <el-tab-pane
          name="gitlab_settings"
          label="Gitlab管理"
        >
          <el-button
            type="primary"
            size="small"
            icon="el-icon-circle-plus"
            @click="create_gitlab"
          >新增</el-button>
          <el-table
            ref="gitlab_list_table_refs"
            :data="gitlab_list"
            empty-text="啥也没有"
            size="small"
            border
          >
            <el-table-column
              label="项目ID"
              prop="uuid"
            >
            </el-table-column>
            <el-table-column
              label="项目名称"
              prop="name"
            >
            </el-table-column>
            <el-table-column
              label="地址"
              prop="addr"
            >
            </el-table-column>
            <el-table-column
              label="所属产品"
              prop="product__name"
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
                  @click="update_gitlab(scoped.row)"
                ></el-button>
                <el-popconfirm
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left: 10px"
                  @confirm="delete_gitlab(scoped.row)"
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
            v-show="gitlab_list_total>0"
            :total="gitlab_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_gitlab_list"
          ></pagination>
        </el-tab-pane> -->
      </el-tabs>
    </el-card>
    <!-- 产品管理dialog--------------------------------------------------  -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="product_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="60%"
    >
      <el-form
        ref="product_formRef"
        :model="product_form"
        :rules="product_form_rules"
        size="small"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="产品名称"
              prop="name"
            >
              <el-input v-model="product_form.name"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="产品描述"
              prop="desc"
            >
              <el-input v-model="product_form.desc"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="用户组"
              prop="user_group"
            >
              <el-select
                v-model="product_form.user_group"
                placeholder="请选择用户组"
                clearable
                filterable
              >
                <el-option
                  v-for="(item, index) in user_group_list"
                  :key="index"
                  :label="item.name"
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
          @click="product_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_product"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 项目管理dialog--------------------------------------------------  -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="project_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="60%"
    >
      <el-form
        ref="project_formRef"
        :model="project_form"
        :rules="project_form_rules"
        size="small"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="项目名称"
              prop="name"
            >
              <el-input v-model="project_form.name"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="项目描述"
              prop="desc"
            >
              <el-input v-model="project_form.desc"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="所属产品"
              prop="product"
            >
              <el-select
                v-model="project_form.product"
                placeholder="请选择产品"
                clearable
                filterable
              >
                <el-option
                  v-for="(item, index) in product_list"
                  :key="index"
                  :label="item.name"
                  :value="item.id"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12"></el-col>
        </el-row>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="project_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_project"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- Jenkins管理dialog--------------------------------------------------  -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="jenkins_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="60%"
    >
      <el-form
        ref="jenkins_formRef"
        :model="jenkins_form"
        :rules="jenkins_form_rules"
        size="small"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="名称"
              prop="name"
            >
              <el-input v-model="jenkins_form.name"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="地址"
              prop="addr"
            >
              <el-input v-model="jenkins_form.addr"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="用户名"
              prop="username"
            >
              <el-input v-model="jenkins_form.username"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="密码"
              prop="password"
            >
              <el-input v-model="jenkins_form.password"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="21">
            <el-form-item
              label="默认配置"
              prop="config"
            >
              <codemirror
                v-model="jenkins_form.config"
                :options="code_mirror_options"
                class="code-mirror"
                style="width: 610px"
              ></codemirror>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="21">
            <el-form-item
              label="Jenkinsfile"
              prop="jenkins_file"
            >
              <codemirror
                v-model="jenkins_form.jenkins_file"
                :options="code_mirror_options"
                class="code-mirror"
                style="width: 610px"
              ></codemirror>
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
          @click="jenkins_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_jenkins"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- Gitlab管理dialog--------------------------------------------------  -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="gitlab_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="60%"
    >
      <el-form
        ref="gitlab_formRef"
        :model="gitlab_form"
        :rules="gitlab_form_rules"
        size="small"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="项目名称"
              prop="name"
            >
              <el-input v-model="gitlab_form.name"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="项目描述"
              prop="desc"
            >
              <el-input v-model="gitlab_form.desc"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="项目ID"
              prop="uuid"
            >
              <el-input v-model="gitlab_form.uuid"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="项目地址"
              prop="addr"
            >
              <el-input v-model="gitlab_form.addr"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-col :span="12">
              <el-form-item
                label="项目Token"
                prop="token"
              >
                <el-input v-model="gitlab_form.token"></el-input>
              </el-form-item>
            </el-col>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="所属产品"
              prop="product"
            >
              <el-select
                v-model="gitlab_form.product"
                placeholder="请选择产品"
                clearable
                filterable
              >
                <el-option
                  v-for="(item, index) in product_list"
                  :key="index"
                  :label="item.name"
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
          @click="gitlab_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_gitlab"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"
import permission from "@/directive/permission/index.js"
import checkPermission from '@/utils/permission'
import "codemirror/mode/groovy/groovy.js"
import "codemirror/theme/solarized.css"
import { codemirror } from "vue-codemirror"
import { mapGetters } from "vuex"

import { createGitlab, getGitlabList, updateGitlab } from "@/views/settings/apis/gitlab"
import { getGroupList } from "@/views/settings/apis/group"
import {
  createJenkins,
  getJenkinsList,
  updateJenkins
} from "@/views/settings/apis/jenkins"
import { getPermList } from "@/views/settings/apis/perm"
import {
  createProduct,
  getProductList,
  updateProduct
} from "@/views/settings/apis/product"
import {
  createProject,
  getProjectList,
  updateProject
} from "@/views/settings/apis/project"
import { getUserGroupList } from "@/views/settings/apis/user_group"

export default {
  name: "SettingsProduct",
  components: {
    Pagination,
    codemirror
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
      active_tab_name: "product_settings",
      dialog_map: {
        create_product: "新增产品",
        update_product: "编辑产品",
        create_project: "新增项目",
        update_project: "编辑项目",
        create_jenkins: "新增Jenkins",
        update_jenkins: "编辑Jenkins",
        create_gitlab: "新增Gitlab",
        update_gitlab: "编辑Gitlab"
      },
      dialog_status: "",
      code_mirror_options: {
        tabSize: 4,
        cursorHeight: 0.8,
        mode: "groovy",
        theme: "solarized dark",
        line: true,
        lineNumbers: true
      },
      // 产品管理--------------------------------------------------
      product_list: [],
      product_list_total: 0,
      product_dialog: false,
      product_form: {
        id: null,
        name: null,
        desc: null,
        user_group: null,
        jenkins: null,
        create_folder: false
      },
      product_form_rules: {
        name: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        desc: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        user_group: [{ required: true, message: '不能为空', trigger: ['blur', 'change'] }]
      },
      // 项目管理--------------------------------------------------
      project_list: [],
      project_list_total: 0,
      project_dialog: false,
      project_form: {
        id: null,
        name: null,
        desc: null,
        product: null
      },
      project_form_rules: {
        name: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        desc: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        product: [{ required: true, message: '不能为空', trigger: ['blur', 'change'] }]
      },
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
      },
      // Jenkins管理--------------------------------------------------
      jenkins_list: [],
      jenkins_list_total: 0,
      jenkins_dialog: false,
      jenkins_form: {
        id: null,
        name: null,
        addr: null,
        username: null,
        password: null,
        config: null,
        jenkins_file: null
      },
      jenkins_form_rules: {
        name: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        addr: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        username: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        password: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        config: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        jenkins_file: [{ required: true, message: '不能为空', trigger: ['blur'] }]
      },
      // Gitlab管理--------------------------------------------------
      gitlab_list: [],
      gitlab_list_total: 0,
      gitlab_dialog: false,
      gitlab_form: {
        id: null,
        name: null,
        desc: null,
        uuid: null,
        addr: null,
        token: null,
        product: null
      },
      gitlab_form_rules: {
        name: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        desc: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        uuid: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        addr: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        token: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        product: [{ required: true, message: '不能为空', trigger: ['blur', 'change'] }]
      }
    }
  },
  computed: {
    ...mapGetters(["user_id", "is_superuser"])
  },
  created() {
    this.get_product_list()
  },
  methods: {
    checkPermission,
    active_tab_click(tab) {
      if (tab.name === "product_settings") {
        this.get_product_list()
      } else if (tab.name === "project_settings") {
        this.get_project_list()
      } else if (tab.name === "jenkins_settings") {
        this.get_jenkins_list()
      } else if (tab.name === "gitlab_settings") {
        this.get_gitlab_list()
      }
    },
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
    // 产品管理--------------------------------------------------
    create_product() {
      this.dialog_status = "create_product"
      this.product_dialog = true
      this.product_form.name = null
      this.product_form.desc = null
      this.product_form.user_group = null
      this.product_form.jenkins = null
      this.product_form.create_folder = false
      this.get_user_group_list()
      this.get_jenkins_list()
    },
    update_product(row) {
      this.dialog_status = "update_product"
      this.product_dialog = true
      this.product_form = Object.assign({}, row)
      this.get_user_group_list()
      this.get_jenkins_list()
    },
    delete_product() { },
    submit_product() {
      if (this.dialog_status === "create_product") {
        createProduct(this.product_form)
          .then((resp) => {
            this.$message({
              type: "success",
              message: "新增产品【" + this.product_form.name + "】成功"
            })
            this.product_dialog = false
            this.get_product_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.product_dialog = false
            this.get_product_list()
          })
      } else if (this.dialog_status === "update_product") {
        updateProduct(this.product_form.id, this.product_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新产品【" + this.product_form.name + "】成功"
            })
            this.product_dialog = false
            this.get_product_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.product_dialog = false
            this.get_product_list()
          })
      }
    },
    get_product_list() {
      getProductList(this.list_query)
        .then((resp) => {
          this.product_list = resp.data.results
          this.product_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 项目管理--------------------------------------------------
    create_project() {
      this.dialog_status = "create_project"
      this.project_dialog = true
      this.project_form.name = null
      this.project_form.desc = null
      this.project_form.product = null
      this.get_product_list()
    },
    update_project(row) {
      this.dialog_status = "update_project"
      this.project_dialog = true
      this.project_form = Object.assign({}, row)
      this.get_product_list()
    },
    delete_project() { },
    submit_project() {
      if (this.dialog_status === "create_project") {
        createProject(this.project_form)
          .then((resp) => {
            this.$message({
              type: "success",
              message: "新增项目【" + this.project_form.name + "】成功"
            })
            this.project_dialog = false
            this.get_project_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.project_dialog = false
            this.get_project_list()
          })
      } else if (this.dialog_status === "update_project") {
        updateProject(this.project_form.id, this.project_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新项目【" + this.project_form.name + "】成功"
            })
            this.project_dialog = false
            this.get_project_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.project_dialog = false
            this.get_project_list()
          })
      }
    },
    get_project_list() {
      getProjectList(this.list_query)
        .then((resp) => {
          this.project_list = resp.data.results
          this.project_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
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
    // Jenkins管理--------------------------------------------------
    create_jenkins() {
      this.dialog_status = "create_jenkins"
      this.jenkins_dialog = true
      this.jenkins_form.name = null
      this.jenkins_form.addr = null
      this.jenkins_form.username = null
      this.jenkins_form.password = null
      this.jenkins_form.config = null
      this.jenkins_form.jenkins_file = null
    },
    update_jenkins(row) {
      this.dialog_status = "update_jenkins"
      this.jenkins_dialog = true
      this.jenkins_form = Object.assign({}, row)
    },
    delete_jenkins(row) { },
    goto_jenkins(row) {
      var job_url = row.addr
      window.open(job_url, "_blank")
    },
    submit_jenkins() {
      if (this.dialog_status === "create_jenkins") {
        createJenkins(this.jenkins_form)
          .then((resp) => {
            this.$message({
              type: "success",
              message: "新增【" + this.jenkins_form.name + "】成功"
            })
            this.jenkins_dialog = false
            this.get_jenkins_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.jenkins_dialog = false
            this.get_jenkins_list()
          })
      } else if (this.dialog_status === "update_jenkins") {
        updateJenkins(this.jenkins_form.id, this.jenkins_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新【" + this.jenkins_form.name + "】成功"
            })
            this.jenkins_dialog = false
            this.get_jenkins_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.jenkins_dialog = false
            this.get_jenkins_list()
          })
      }
    },
    get_jenkins_list() {
      getJenkinsList(this.list_query)
        .then((resp) => {
          this.jenkins_list = resp.data.results
          this.jenkins_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // Gitlab管理--------------------------------------------------
    create_gitlab() {
      this.dialog_status = "create_gitlab"
      this.gitlab_dialog = true
      this.gitlab_form.name = null
      this.gitlab_form.desc = null
      this.gitlab_form.uuid = null
      this.gitlab_form.addr = null
      this.gitlab_form.token = null
      this.gitlab_form.product = null
      this.get_product_list()
    },
    update_gitlab(row) {
      this.dialog_status = "update_gitlab"
      this.gitlab_dialog = true
      this.gitlab_form = Object.assign({}, row)
      this.get_product_list()
    },
    delete_gitlab() { },
    submit_gitlab() {
      if (this.dialog_status === "create_gitlab") {
        createGitlab(this.gitlab_form)
          .then((resp) => {
            this.$message({
              type: "success",
              message: "新增【" + this.gitlab_form.name + "】成功"
            })
            this.gitlab_dialog = false
            this.get_gitlab_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.gitlab_dialog = false
            this.get_gitlab_list()
          })
      } else if (this.dialog_status === "update_gitlab") {
        updateGitlab(this.gitlab_form.id, this.gitlab_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新【" + this.gitlab_form.name + "】成功"
            })
            this.gitlab_dialog = false
            this.get_gitlab_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.gitlab_dialog = false
            this.get_gitlab_list()
          })
      }
    },
    get_gitlab_list() {
      getGitlabList(this.list_query)
        .then((resp) => {
          this.gitlab_list = resp.data.results
          this.gitlab_list_total = resp.data.count
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
