<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-tabs
        v-model="active_tab_name"
        @tab-click="active_tab_click"
      >
        <!-- 集群管理--------------------------------------------------  -->
        <el-tab-pane
          label="集群管理"
          name="cluster_settings"
        >
          <el-button
            v-if="checkPermission(['admin'])"
            type="primary"
            size="small"
            icon="el-icon-circle-plus"
            @click="create_cluster"
          >新增</el-button>
          <el-table
            ref="cluster_list_table_refs"
            :data="cluster_list"
            empty-text="啥也没有"
            size="small"
            border
          >
            <el-table-column
              label="集群名称"
              prop="name"
            > </el-table-column>
            <el-table-column
              label="集群描述"
              prop="desc"
            > </el-table-column>
            <el-table-column
              label="集群ID"
              prop="uuid"
            > </el-table-column>
            <el-table-column
              label="集群地址"
              prop="addr"
            > </el-table-column>
            <el-table-column
              label="用户组"
              prop="user_group__name"
            >
            </el-table-column>
            <el-table-column
              label="操作"
              width="180px;"
            >
              <template slot-scope="scoped">
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  size="mini"
                  :disabled="checkPermission(['viewer'])"
                  @click="update_cluster(scoped.row)"
                >
                </el-button>
                <el-popconfirm
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left: 10px"
                  :disabled="checkPermission(['viewer'])"
                  @confirm="delete_cluster(scoped.row)"
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
                  content="集群空间"
                  placement="top"
                >
                  <el-button
                    type="info"
                    icon="el-icon-folder"
                    size="mini"
                    style="margin-left: 10px"
                    @click="view_cluster_ns(scoped.row)"
                  ></el-button>
                </el-tooltip>
              </template>
            </el-table-column>
          </el-table>
          <pagination
            v-show="cluster_list_total > 0"
            :total="cluster_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_cluster_list"
          ></pagination>
        </el-tab-pane>
        <!-- 仓库管理--------------------------------------------------  -->
        <el-tab-pane
          label="仓库管理"
          name="registry_settings"
        >
          <el-button
            type="primary"
            size="small"
            icon="el-icon-circle-plus"
            @click="create_registry"
          >新增</el-button>
          <el-table
            ref="registry_list_table_refs"
            :data="registry_list"
            empty-text="啥也没有"
            size="small"
            border
          >
            <el-table-column
              label="仓库名称"
              prop="name"
            > </el-table-column>
            <el-table-column
              label="仓库地址"
              prop="private_addr"
            >
              <template slot-scope="scoped">
                <el-tooltip
                  class="item"
                  effect="dark"
                  placement="top-start"
                >
                  <div slot="content">
                    公网地址 {{ scoped.row.image_public_addr }}<br>内网地址
                    {{ scoped.row.image_private_addr }}
                  </div>
                  <el-tag
                    v-if="scoped.row.image_private_addr"
                    size="small"
                    style="vertical-align: middle"
                  >Image
                  </el-tag>
                </el-tooltip>
                <el-tooltip
                  class="item"
                  effect="dark"
                  placement="top-start"
                >
                  <div slot="content">
                    公网地址 {{ scoped.row.chart_public_addr }}<br>内网地址
                    {{ scoped.row.chart_private_addr }}
                  </div>
                  <el-tag
                    v-if="scoped.row.chart_private_addr"
                    size="small"
                    style="vertical-align: middle; margin-left: 10px"
                  >Chart</el-tag>
                </el-tooltip>
              </template>
            </el-table-column>
            <el-table-column
              label="云厂商"
              prop="factory__name"
            >
            </el-table-column>
            <el-table-column
              label="操作"
              width="180px;"
            >
              <template slot-scope="scoped">
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  size="mini"
                  @click="update_registry(scoped.row)"
                >
                </el-button>
                <el-popconfirm
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left: 10px"
                  @confirm="delete_registry(scoped.row)"
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
                  content="仓库空间"
                  placement="top"
                >
                  <el-button
                    type="info"
                    icon="el-icon-folder"
                    size="mini"
                    style="margin-left: 10px"
                    @click="view_registry_ns(scoped.row)"
                  ></el-button>
                </el-tooltip>
              </template>
            </el-table-column>
          </el-table>
          <pagination
            v-show="registry_list_total > 0"
            :total="registry_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_registry_list"
          ></pagination>
        </el-tab-pane>
        <!-- 环境管理--------------------------------------------------  -->
        <el-tab-pane
          label="环境管理"
          name="environ_settings"
        >
          <el-button
            type="primary"
            size="small"
            icon="el-icon-circle-plus"
            @click="create_environ"
          >新增</el-button>
          <el-table
            ref="environ_list_table_refs"
            :data="environ_list"
            empty-text="啥也没有"
            size="small"
            border
          >
            <el-table-column
              label="环境名称"
              prop="name"
            > </el-table-column>
            <el-table-column
              label="环境描述"
              prop="desc"
            > </el-table-column>
            <el-table-column
              label="操作"
              width="120px;"
            >
              <template slot-scope="scoped">
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  size="mini"
                  @click="update_environ(scoped.row)"
                >
                </el-button>
                <el-popconfirm
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left: 10px"
                  @confirm="delete_environ(scoped.row)"
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
            v-show="environ_list_total > 0"
            :total="environ_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_environ_list"
          ></pagination>
        </el-tab-pane>
        <!-- 配置文件管理--------------------------------------------------  -->
        <el-tab-pane
          label="Helm配置"
          name="helm_config_settings"
        >
          <el-button
            type="primary"
            size="small"
            icon="el-icon-circle-plus"
            @click="create_helm_config"
          >新增</el-button>
          <el-table
            ref="helm_config_list_table_refs"
            :data="helm_config_list"
            empty-text="啥也没有"
            size="small"
            border
          >
            <el-table-column
              label="名称"
              prop="name"
            ></el-table-column>
            <el-table-column
              label="操作"
              width="120px;"
            >
              <template slot-scope="scoped">
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  size="mini"
                  @click="update_helm_config(scoped.row)"
                >
                </el-button>
                <el-popconfirm
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left: 10px"
                  @confirm="delete_helm_config(scoped.row)"
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
            v-show="helm_config_list_total > 0"
            :total="helm_config_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_helm_config_list"
          ></pagination>
        </el-tab-pane>
      </el-tabs>
    </el-card>
    <!-- 集群管理dialog--------------------------------------------------  -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="cluster_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="60%"
    >
      <el-form
        ref="cluster_formRef"
        :model="cluster_form"
        :rules="cluster_form_rules"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="集群名称"
              prop="name"
            >
              <el-input
                v-model="cluster_form.name"
                placeholder="集群名称"
                size="small"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="集群描述"
              prop="desc"
            >
              <el-input
                v-model="cluster_form.desc"
                placeholder="集群描述"
                size="small"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="集群ID"
              prop="uuid"
            >
              <el-input
                v-model="cluster_form.uuid"
                placeholder="集群唯一ID"
                size="small"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="集群地址"
              prop="addr"
            >
              <el-input
                v-model="cluster_form.addr"
                placeholder="集群地址"
                size="small"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="集群厂商"
              prop="factory"
            >
              <el-select
                v-model="cluster_form.factory"
                placeholder="请选择厂商"
                clearable
                filterable
                size="small"
              >
                <el-option
                  v-for="(item, index) in factory_list"
                  :key="index"
                  :label="item.name"
                  :value="item.id"
                  size="small"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="用户组"
              prop="user_group"
            >
              <el-select
                v-model="cluster_form.user_group"
                placeholder="请选择用户组"
                clearable
                filterable
                size="small"
              >
                <el-option
                  v-for="(item, index) in user_group_list"
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
            <el-form-item
              label="集群Token"
              prop="token"
            >
              <el-input
                v-model="cluster_form.token"
                placeholder="请输入集群Token"
                type="textarea"
                :rows="2"
                style="width: 200px"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="集群凭证"
              prop="config"
            >
              <el-input
                v-model="cluster_form.config"
                placeholder="请输入集群凭证"
                type="textarea"
                :rows="2"
                style="width: 200px"
              ></el-input>
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
          @click="cluster_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_cluster"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 仓库管理dialog--------------------------------------------------  -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="registry_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="60%"
    >
      <el-form
        ref="registry_formRef"
        :model="registry_form"
        :rules="registry_form_rules"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="仓库名称"
              prop="name"
            >
              <el-input
                v-model="registry_form.name"
                size="small"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="仓库厂商"
              prop="factory"
            >
              <el-select
                v-model="registry_form.factory"
                placeholder="请选择厂商"
                clearable
                filterable
                size="small"
              >
                <el-option
                  v-for="(item, index) in factory_list"
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
            <el-form-item
              label="Image(外)"
              prop="image_public_addr"
            >
              <el-input
                v-model="registry_form.image_public_addr"
                size="small"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="Image(内)"
              prop="image_private_addr"
            >
              <el-input
                v-model="registry_form.image_private_addr"
                size="small"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="Chart(外)"
              prop="chart_public_addr"
            >
              <el-input
                v-model="registry_form.chart_public_addr"
                size="small"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="Chart(内)"
              prop="chart_private_addr"
            >
              <el-input
                v-model="registry_form.chart_private_addr"
                size="small"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="用户名"
              prop="username"
            >
              <el-input
                v-model="registry_form.username"
                size="small"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="密码"
              prop="password"
            >
              <el-input
                v-model="registry_form.password"
                size="small"
              ></el-input>
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
          @click="registry_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_registry"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 环境管理dialog--------------------------------------------------  -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="environ_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="60%"
    >
      <el-form
        ref="environ_formRef"
        :model="environ_form"
        :rules="environ_form_rules"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="环境名称"
              prop="name"
            >
              <el-input
                v-model="environ_form.name"
                size="small"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="环境描述"
              prop="desc"
            >
              <el-input
                v-model="environ_form.desc"
                size="small"
              ></el-input>
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
          @click="environ_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_environ"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 配置文件管理dialog--------------------------------------------------  -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="helm_config_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="60%"
    >
      <el-form
        ref="helm_config_formRef"
        :model="helm_config_form"
        :rules="helm_config_form_rules"
        label-width="100px"
      >
        <el-form-item
          label="配置名称"
          prop="name"
        >
          <el-input
            v-model="helm_config_form.name"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="Chart"
          prop="chart_config"
        >
          <codemirror
            v-model="helm_config_form.chart_config"
            :options="code_mirror_options"
            class="code-mirror"
            style="width: 610px;"
          ></codemirror>
        </el-form-item>
        <el-form-item
          label="Value"
          prop="value_config"
        >
          <codemirror
            v-model="helm_config_form.value_config"
            :options="code_mirror_options"
            class="code-mirror"
            style="width: 610px;"
          ></codemirror>
        </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="helm_config_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_helm_config"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import "codemirror/mode/groovy/groovy.js"
import "codemirror/mode/yaml/yaml.js"
import "codemirror/theme/solarized.css"
import { codemirror } from "vue-codemirror"
import checkPermission from '@/utils/permission'
import Pagination from "@/components/Pagination"
import { createCluster, getClusterList, updateCluster } from "@/views/container/apis/cluster"
import { createEnviron, getEnvironList, updateEnviron } from "@/views/container/apis/environ"
import { getFactoryList } from "@/views/container/apis/factory"
import { createRegistry, getRegistryList, updateRegistry } from "@/views/container/apis/registry"
import { getUserGroupList } from "@/views/container/apis/user_group"
import { getHelmConfigList, createHelmConfig, updateHelmConfig } from "@/views/container/apis/helm_config"

export default {
  name: "ClusterSettings",
  components: {
    Pagination,
    codemirror
  },
  data() {
    return {
      list_query: {
        page: 1,
        limit: 15
      },
      active_tab_name: "cluster_settings",
      dialog_map: {
        create_cluster: "新增集群",
        update_cluster: "编辑集群",
        create_environ: "新增环境",
        update_environ: "编辑环境",
        create_registry: "新增仓库",
        update_registry: "编辑仓库",
        create_helm_config: "新增配置文件",
        update_helm_config: "编辑配置文件"
      },
      dialog_status: "",
      code_mirror_options: {
        tabSize: 4,
        cursorHeight: 0.8,
        mode: "yaml",
        theme: "solarized dark",
        line: true,
        lineNumbers: true
      },
      // 集群管理--------------------------------------------------
      cluster_list: [],
      cluster_list_total: 0,
      factory_list: [],
      user_group_list: [],
      cluster_dialog: false,
      cluster_form: {
        id: null,
        name: null,
        desc: null,
        uuid: null,
        user_group: null,
        addr: null,
        token: null,
        config: null,
        factory: null
      },
      cluster_form_rules: {
        name: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        desc: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        uuid: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        user_group: [{ required: true, message: '不能为空', trigger: ['blur', 'change'] }],
        addr: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        token: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        config: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        factory: [{ required: true, message: '不能为空', trigger: ['blur', 'change'] }]
      },
      // 环境管理--------------------------------------------------
      environ_list: [],
      environ_list_total: 0,
      environ_dialog: false,
      environ_form: {
        id: null,
        name: null,
        desc: null
      },
      environ_form_rules: {
        name: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        desc: [{ required: true, message: '不能为空', trigger: ['blur'] }]
      },
      // 仓库管理--------------------------------------------------
      registry_list: [],
      registry_list_total: 0,
      registry_dialog: false,
      registry_form: {
        id: null,
        name: null,
        desc: null,
        types: null,
        image_public_addr: null,
        image_private_addr: null,
        chart_public_addr: null,
        chart_private_addr: null,
        username: null,
        password: null,
        factory: null
      },
      registry_form_rules: {
        name: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        desc: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        factory: [{ required: true, message: '不能为空', trigger: ['blur', 'change'] }],
        image_public_addr: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        image_private_addr: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        chart_public_addr: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        chart_private_addr: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        username: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        password: [{ required: true, message: '不能为空', trigger: ['blur'] }]
      },
      // 构建记录--------------------------------------------------
      helm_config_list: [],
      helm_config_list_total: 0,
      helm_config_dialog: false,
      helm_config_form: {
        id: null,
        name: null,
        chart_config: null,
        value_config: null
      },
      helm_config_form_rules: {
        name: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        chart_config: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        value_config: [{ required: true, message: '不能为空', trigger: ['blur'] }]
      }
    }
  },
  created() {
    this.get_cluster_list()
  },
  methods: {
    checkPermission,
    active_tab_click(tab) {
      if (tab.name === "cluster_settings") {
        this.get_cluster_list()
      } else if (tab.name === "environ_settings") {
        this.get_environ_list()
      } else if (tab.name === "registry_settings") {
        this.get_registry_list()
      } else if (tab.name === "helm_config_settings") {
        this.get_helm_config_list()
      }
    },
    // 集群管理--------------------------------------------------
    create_cluster() {
      this.dialog_status = "create_cluster"
      this.cluster_dialog = true
      this.cluster_form.name = null
      this.cluster_form.desc = null
      this.get_factory_list()
      this.get_user_group_list()
    },
    update_cluster(row) {
      this.dialog_status = "update_cluster"
      this.cluster_dialog = true
      this.cluster_form = Object.assign({}, row)
      this.get_factory_list()
      this.get_user_group_list()
    },
    delete_cluster() { },
    view_cluster_ns(row) {
      const parObj = JSON.stringify(row)
      this.$router.push({
        path: "/container/cluster_ns/",
        query: { cluster_info: parObj }
      })
    },
    submit_cluster() {
      if (this.dialog_status === "create_cluster") {
        createCluster(this.cluster_form)
          .then((resp) => {
            this.$message({
              type: "success",
              message: "新增集群【" + this.cluster_form.name + "】成功"
            })
            this.cluster_dialog = false
            this.get_cluster_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.cluster_dialog = false
            this.get_cluster_list()
          })
      } else if (this.dialog_status === "update_cluster") {
        updateCluster(this.cluster_form.id, this.cluster_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新集群【" + this.cluster_form.name + "】成功"
            })
            this.cluster_dialog = false
            this.get_cluster_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.cluster_dialog = false
            this.get_cluster_list()
          })
      }
    },
    get_cluster_list() {
      getClusterList(this.list_query)
        .then((resp) => {
          this.cluster_list = resp.data.results
          this.cluster_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    get_user_group_list() {
      getUserGroupList({ limit: 999 })
        .then((resp) => {
          this.user_group_list = resp.data.results
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    get_factory_list() {
      getFactoryList({ limit: 999 })
        .then((resp) => {
          this.factory_list = resp.data.results
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 环境管理--------------------------------------------------
    create_environ() {
      this.dialog_status = "create_environ"
      this.environ_dialog = true
      this.environ_form.name = null
      this.environ_form.desc = null
    },
    update_environ(row) {
      this.dialog_status = "update_environ"
      this.environ_dialog = true
      this.environ_form = Object.assign({}, row)
    },
    delete_environ(row) { },
    submit_environ() {
      if (this.dialog_status === "create_environ") {
        createEnviron(this.environ_form)
          .then((resp) => {
            this.$message({
              type: "success",
              message: "新增环境【" + this.environ_form.name + "】成功"
            })
            this.environ_dialog = false
            this.get_environ_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.environ_dialog = false
            this.get_environ_list()
          })
      } else if (this.dialog_status === "update_environ") {
        updateEnviron(this.environ_form.id, this.environ_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新环境【" + this.environ_form.name + "】成功"
            })
            this.environ_dialog = false
            this.get_environ_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.environ_dialog = false
            this.get_environ_list()
          })
      }
    },
    get_environ_list() {
      getEnvironList(this.list_query)
        .then((resp) => {
          this.environ_list = resp.data.results
          this.environ_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 仓库管理--------------------------------------------------
    create_registry() {
      this.dialog_status = "create_registry"
      this.registry_dialog = true
      this.registry_form.name = null
      this.registry_form.desc = null
      this.registry_form.types = null
      this.registry_form.image_public_addr = null
      this.registry_form.image_private_addr = null
      this.registry_form.chart_public_addr = null
      this.registry_form.chart_private_addr = null
      this.registry_form.username = null
      this.registry_form.password = null
      this.get_factory_list()
    },
    update_registry(row) {
      this.dialog_status = "update_registry"
      this.registry_dialog = true
      this.registry_form = Object.assign({}, row)
      this.get_factory_list()
    },
    delete_registry() { },
    view_registry_ns(row) {
      const parObj = JSON.stringify(row)
      this.$router.push({
        path: "/container/registry_ns/",
        query: { registry_info: parObj }
      })
    },
    submit_registry() {
      if (this.dialog_status === "create_registry") {
        createRegistry(this.registry_form)
          .then((resp) => {
            this.$message({
              type: "success",
              message: "新增仓库【" + this.registry_form.name + "】成功"
            })
            this.registry_dialog = false
            this.get_registry_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.registry_dialog = false
            this.get_registry_list()
          })
      } else if (this.dialog_status === "update_registry") {
        updateRegistry(this.registry_form.id, this.registry_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新仓库【" + this.registry_form.name + "】成功"
            })
            this.registry_dialog = false
            this.get_registry_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.registry_dialog = false
            this.get_registry_list()
          })
      }
    },
    get_registry_list() {
      getRegistryList(this.list_query)
        .then((resp) => {
          this.registry_list = resp.data.results
          this.registry_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 配置文件管理--------------------------------------------------
    create_helm_config() {
      this.dialog_status = "create_helm_config"
      this.helm_config_dialog = true
      this.helm_config_form.name = null
      this.helm_config_form.chart_config = null
      this.helm_config_form.value_config = null
    },
    update_helm_config(row) {
      this.dialog_status = "update_helm_config"
      this.helm_config_dialog = true
      this.helm_config_form = Object.assign({}, row)
    },
    delete_helm_config(row) { },
    submit_helm_config() {
      if (this.dialog_status === "create_helm_config") {
        createHelmConfig(this.helm_config_form)
          .then((resp) => {
            this.$message({
              type: "success",
              message: "新增配置【" + this.helm_config_form.name + "】成功"
            })
            this.helm_config_dialog = false
            this.get_helm_config_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.helm_config_dialog = false
            this.get_helm_config_list()
          })
      } else if (this.dialog_status === "update_helm_config") {
        updateHelmConfig(this.helm_config_form.id, this.helm_config_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新配置【" + this.helm_config_form.name + "】成功"
            })
            this.helm_config_dialog = false
            this.get_helm_config_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.helm_config_dialog = false
            this.get_helm_config_list()
          })
      }
    },
    get_helm_config_list() {
      getHelmConfigList(this.list_query)
        .then((resp) => {
          this.helm_config_list = resp.data.results
          this.helm_config_list_total = resp.data.count
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
