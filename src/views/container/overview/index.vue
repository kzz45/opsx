<template>
  <div class="app-container">
    <el-card class="box-card">
      <div>
        <el-button
          type="primary"
          size="small"
          icon="el-icon-circle-plus"
          @click="create_app"
        >新建应用</el-button>
      </div>
      <!-- 应用管理--------------------------------------------------  -->
      <el-table
        ref="app_list_table_refs"
        :data="app_list"
        empty-text="啥也没有"
        size="small"
        border
      >
        <el-table-column
          label="应用名称"
          prop="name"
        ></el-table-column>
        <el-table-column
          label="类型"
          prop="types"
        >
          <template slot-scope="scoped">
            <el-tag
              v-if="scoped.row.types === 0"
              type="primary"
              size="small"
            >Deployment</el-tag>
            <el-tag
              v-if="scoped.row.types === 1"
              type="primary"
              size="small"
            >Statefulset</el-tag>
            <el-tag
              v-if="scoped.row.types === 2"
              type="primary"
              size="small"
            >Daemonset</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          label="状态"
          prop="status"
        >
          <template slot-scope="scoped">
            <el-tag
              v-if="scoped.row.status === 0"
              type="info"
              size="small"
            >部署中</el-tag>
            <el-tag
              v-if="scoped.row.status === 1"
              type="success"
              size="small"
            >已部署</el-tag>
            <el-tag
              v-if="scoped.row.status === 2"
              type="danger"
              size="small"
            >已卸载</el-tag>
            <el-tag
              v-if="scoped.row.status === 3"
              type="warning"
              size="small"
            >更新中</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          label="所在集群"
          prop="cluster__name"
        ></el-table-column>
        <el-table-column
          label="更新时间"
          prop="update_at"
        >
          <template slot-scope="scoped">{{ scoped.row.update_at | parseTime('{y}-{m}-{d} {h}:{i}:{s}') }}</template>
        </el-table-column>
        <el-table-column
          label="操作"
          width="180px;"
        >
          <template slot-scope="scoped">
            <el-tooltip
              class="item"
              effect="dark"
              content="应用详情"
              placement="top"
            >
              <el-button
                type="info"
                icon="el-icon-info"
                size="mini"
                @click="view_app_info(scoped.row)"
              ></el-button>
            </el-tooltip>
            <el-popconfirm
              title="确定删除吗？"
              confirm-button-text="确定"
              cancel-button-text="不了"
              style="margin-left: 10px"
              @confirm="delete_app(scoped.row)"
              @cancel="cancel_delete"
            >
              <el-button
                slot="reference"
                type="danger"
                icon="el-icon-delete"
                size="mini"
              ></el-button>
            </el-popconfirm>
            <el-dropdown
              trigger="click"
              style="margin-left: 10px;"
            >
              <el-button
                type="primary"
                icon="el-icon-menu"
                size="mini"
              >
              </el-button>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item
                  icon="el-icon-edit"
                  style="color: #409EFF;"
                  @click.native="update_app(scoped.row)"
                >调整副本</el-dropdown-item>
                <el-dropdown-item
                  icon="el-icon-setting"
                  style="color: #909399;"
                  @click.native="view_app_config(scoped.row)"
                >配置文件</el-dropdown-item>
                <el-dropdown-item
                  icon="el-icon-refresh-left"
                  style="color: #E6A23C;"
                  @click.native="redeploy_app(scoped.row)"
                >重新部署</el-dropdown-item>
                <el-dropdown-item
                  icon="el-icon-data-analysis"
                  style="color: #303133;"
                  @click.native="view_app_log(scoped.row)"
                >查看日志</el-dropdown-item>
                <el-dropdown-item
                  icon="el-icon-view"
                  style="color: #67C23A;"
                  @click.native="view_app_monitor(scoped.row)"
                >查看监控</el-dropdown-item>
                <el-dropdown-item
                  icon="el-icon-copy-document"
                  style="color: #303133;"
                  @click.native="change_app_version(scoped.row)"
                >历史版本</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>
      <pagination
        v-show="app_list_total>0"
        :total="app_list_total"
        :page.sync="list_query.page"
        :limit.sync="list_query.limit"
        @pagination="get_app_list"
      ></pagination>
    </el-card>
    <!-- 应用管理dialog--------------------------------------------------  -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="app_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      top="10vh"
      width="60%"
    >
      <el-tabs
        v-model="dialog_active_tab_name"
        tab-position="left"
      >
        <!-- 前置条件配置--------------------------------------------------  -->
        <el-tab-pane
          name="requirement_config"
          label="前置配置"
          :disabled="requirement_config_disable"
        >
          <el-form
            ref="requirement_config_formRef"
            :model="requirement_config_form"
            :rules="requirement_config_form_rules"
            label-width="100px"
            size="small"
          >
            <el-row>
              <el-col :span="24">
                <el-form-item label="说明">
                  <el-tag type="warning">创建Jenkins目录, 创建Jenkins中Item, 并去构建版本</el-tag>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="12">
                <el-col :span="12">
                  <el-form-item
                    label="应用环境"
                    prop="environ"
                  >
                    <el-select
                      v-model="requirement_config_form.environ"
                      placeholder="请选择应用环境"
                      clearable
                      filterable
                      size="small"
                      @change="select_environ"
                    >
                      <el-option
                        v-for="(item, index) in environ_list"
                        :key="index"
                        :label="item.name"
                        :value="item.id"
                        size="small"
                      ></el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-col>
              <el-col :span="12"></el-col>
            </el-row>
            <el-row>
              <el-col :span="12">
                <el-form-item
                  label="所属产品"
                  prop="product"
                >
                  <el-select
                    v-model="requirement_config_form.product"
                    placeholder="请选择产品"
                    clearable
                    filterable
                    size="small"
                    @change="select_product"
                  >
                    <el-option
                      v-for="(item, index) in product_list"
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
                  label="所属项目"
                  prop="gitlab"
                >
                  <el-select
                    v-model="requirement_config_form.gitlab"
                    placeholder="请选择项目"
                    clearable
                    filterable
                    size="small"
                    @change="select_project"
                  >
                    <el-option
                      v-for="(item, index) in gitlab_list"
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
                  label="Jenkins目录"
                  prop="jenkins_folder"
                >
                  <el-input
                    v-model="requirement_config_form.jenkins_folder"
                    placeholder="Jenkins目录"
                    size="small"
                  ></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item
                  label="Jenkins"
                  prop="jenkins"
                >
                  <el-select
                    v-model="requirement_config_form.jenkins"
                    placeholder="请选择Jenkins"
                    clearable
                    filterable
                    size="small"
                  >
                    <el-option
                      v-for="(item, index) in jenkins_list"
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
              <!-- <el-col :span="12">
                <el-form-item
                  label="Git项目"
                  prop="gitlab"
                >
                  <el-select
                    v-model="requirement_config_form.gitlab"
                    placeholder="请选择Git项目"
                    clearable
                    filterable
                    size="small"
                  >
                    <el-option
                      v-for="(item, index) in gitlab_list"
                      :key="index"
                      :label="item.name"
                      :value="item.id"
                      size="small"
                    ></el-option>
                  </el-select>
                </el-form-item>
              </el-col> -->
            </el-row>
            <el-row style="margin-top: 10px;">
              <el-col :span="8">
                <el-form-item label="创建目录">
                  <el-button
                    type="info"
                    icon="el-icon-folder-add"
                    size="small"
                    style="vertical-align:middle;"
                    @click="create_jenkins_folder"
                  ></el-button>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="创建Item">
                  <el-button
                    type="primary"
                    icon="el-icon-circle-plus"
                    size="small"
                    style="vertical-align:middle;"
                    @click="create_jenkins_item"
                  ></el-button>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="构建Job">
                  <el-button
                    type="success"
                    icon="el-icon-s-promotion"
                    size="small"
                    style="vertical-align:middle;"
                    @click="goto_jenkins"
                  ></el-button>
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>
          <div style="float: right; margin-top: 60px;">
            <el-button
              round
              size="small"
              @click="cancel_create_app"
            >取消</el-button>
            <el-button
              round
              type="primary"
              size="small"
              @click="step_to_basic_config"
            >下一步</el-button>
          </div>
        </el-tab-pane>
        <!-- 应用基础配置--------------------------------------------------  -->
        <el-tab-pane
          name="basic_config"
          label="基础配置"
          :disabled="basic_config_disable"
        >
          <el-form
            ref="basic_config_formRef"
            :model="basic_config_form"
            :rules="basic_config_form_rules"
            label-width="100px"
            size="small"
          >
            <el-row>
              <el-col :span="24">
                <el-form-item label="说明">
                  <el-tag type="warning">选择镜像和镜像版本, 是否开启监控, 是否有环境变量</el-tag>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="12">
                <el-form-item
                  label="应用类型"
                  prop="types"
                >
                  <el-select
                    v-model="basic_config_form.types"
                    placeholder="请选择应用类型"
                    clearable
                    filterable
                    size="small"
                  >
                    <el-option
                      v-for="(item, index) in app_types_list"
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
                  label="镜像仓库"
                  prop="registry"
                >
                  <el-select
                    v-model="basic_config_form.registry"
                    placeholder="请选择镜像仓库"
                    clearable
                    filterable
                    size="small"
                    @change="select_registry_image"
                  >
                    <el-option
                      v-for="(item, index) in registry_list"
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
                  label="镜像名称"
                  prop="image"
                >
                  <el-select
                    v-model="basic_config_form.image"
                    placeholder="请选择镜像"
                    clearable
                    filterable
                    size="small"
                    @change="select_image_tag"
                  >
                    <el-option
                      v-for="(item, index) in image_list"
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
                  label="镜像版本"
                  prop="image_version"
                >
                  <el-select
                    v-model="basic_config_form.image_version"
                    placeholder="请选择镜像版本"
                    clearable
                    filterable
                    size="small"
                  >
                    <el-option
                      v-for="(item, index) in image_tag_list"
                      :key="index"
                      :label="item.version"
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
                  label="开启监控"
                  prop="monitor"
                >
                  <el-switch
                    v-model="basic_config_form.monitor"
                    active-color="#13ce66"
                    inactive-color="#ff4949"
                    :active-value="true"
                    :inactive-value="false"
                  >
                  </el-switch>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item
                  label="额外参数"
                  prop="args"
                >
                  <el-switch
                    v-model="basic_config_form.args"
                    active-color="#13ce66"
                    inactive-color="#ff4949"
                    :active-value="true"
                    :inactive-value="false"
                  >
                  </el-switch>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="12">
                <el-form-item
                  v-if="basic_config_form.monitor"
                  label="监控路径"
                  prop="monitor_path"
                >
                  <el-input
                    v-model="basic_config_form.monitor_path"
                    placeholder="请输入监控路径"
                    size="small"
                  ></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item
                  v-if="basic_config_form.monitor"
                  label="监控端口"
                  prop="monitor_port"
                >
                  <el-input
                    v-model="basic_config_form.monitor_port"
                    placeholder="请输入监控端口"
                    size="small"
                  ></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="24">
                <el-form-item
                  v-if="basic_config_form.args"
                  label="环境变量"
                  prop="args_content"
                >
                  <el-input
                    v-model="basic_config_form.args_content"
                    type="textarea"
                    :autosize="{ minRows: 2, maxRows: 4}"
                    placeholder="请输入环境变量"
                    style="width: 540px;"
                  >
                  </el-input>
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>
          <div style="float: right; margin-top: 60px;">
            <el-button
              round
              size="small"
              @click="cancel_create_app"
            >取消</el-button>
            <el-button
              round
              type="info"
              size="small"
              @click="step_to_requirement_config"
            >上一步</el-button>
            <el-button
              round
              type="primary"
              size="small"
              @click="step_to_overview_config"
            >下一步</el-button>
          </div>
        </el-tab-pane>
        <!-- 配置概览-------------------------------------------------- -->
        <el-tab-pane
          name="overview_config"
          label="配置概览"
          :disabled="overview_config_disable"
        >
          <el-form
            ref="overview_config_formRef"
            :model="overview_config_form"
            :rules="overview_config_form_rules"
            label-width="100px"
            size="small"
          >
            <el-row>
              <el-col :span="24">
                <el-form-item label="说明">
                  <el-tag type="warning">预览配置, 必要时可调整配置</el-tag>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="24">
                <el-form-item
                  label="配置文件"
                  prop="config"
                >
                  <codemirror
                    v-model="overview_config_form.config"
                    :options="code_mirror_options"
                    class="code-mirror"
                  ></codemirror>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="24">
                <el-form-item label="操作">
                  <el-button
                    type="warning"
                    icon="el-icon-circle-check"
                    size="small"
                    @click="update_release_config"
                  ></el-button>
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>
          <div style="float: right; margin-top: 60px;">
            <el-button
              round
              size="small"
              @click="cancel_create_app"
            >取消</el-button>
            <el-button
              round
              type="info"
              size="small"
              @click="step_to_basic_config"
            >上一步</el-button>
            <el-button
              round
              type="primary"
              size="small"
              @click="step_to_target_config"
            >下一步</el-button>
          </div>
        </el-tab-pane>
        <!-- 安装应用-------------------------------------------------- -->
        <el-tab-pane
          name="target_config"
          label="安装应用"
          :disabled="target_config_disable"
        >
          <el-form
            ref="target_config_formRef"
            :model="target_config_form"
            :rules="target_config_form_rules"
            label-width="100px"
            size="small"
          >
            <el-row>
              <el-col :span="24">
                <el-form-item label="说明">
                  <el-tag type="warning">选择应用安装在哪里</el-tag>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="12">
                <el-form-item
                  label="集群名称"
                  prop="cluster"
                >
                  <el-select
                    v-model="target_config_form.cluster"
                    placeholder="请选择部署集群"
                    clearable
                    filterable
                    size="small"
                    @change="select_cluster_ns"
                  >
                    <el-option
                      v-for="(item, index) in cluster_list"
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
                  label="命名空间"
                  prop="namespace"
                >
                  <el-select
                    v-model="target_config_form.namespace"
                    placeholder="请选择集群命名空间"
                    clearable
                    filterable
                    size="small"
                  >
                    <el-option
                      v-for="(item, index) in cluster_ns_list"
                      :key="index"
                      :label="item.name"
                      :value="item.id"
                      size="small"
                    ></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>
          <div style="float: right; margin-top: 60px;">
            <el-button
              round
              size="small"
              @click="cancel_create_app"
            >取消</el-button>
            <el-button
              round
              type="info"
              size="small"
              @click="step_to_overview_config"
            >上一步</el-button>
            <el-button
              round
              type="primary"
              size="small"
              @click="submit_app"
            >安装应用</el-button>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-dialog>
    <!-- 历史版本dialog--------------------------------------------------  -->
    <!-- 配置文件dialog--------------------------------------------------  -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="view_app_dialog"
      :show-close="false"
      top="10vh"
      width="60%"
    >
      <el-form
        ref="view_app_config_formRef"
        :model="view_app_config_form"
        :rules="view_app_config_form_rules"
        label-width="100px"
        size="small"
      >
        <el-row>
          <el-col :span="24">
            <el-form-item label="说明">
              <el-tag type="warning">你最好不要瞎改</el-tag>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <el-form-item
              label="配置文件"
              prop="value_config"
            >
              <codemirror
                v-model="view_app_config_form.value_config"
                :options="code_mirror_options"
                class="code-mirror"
              ></codemirror>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <div style="float: right; margin-top: 60px;">
              <el-button
                round
                size="small"
              >取消</el-button>
              <el-button
                round
                type="primary"
                size="small"
              >更新应用</el-button>
            </div>
          </el-col>
        </el-row>
      </el-form>
    </el-dialog>
    <!-- 查看日志dialog--------------------------------------------------  -->
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination'
import "codemirror/mode/yaml/yaml.js"
import "codemirror/theme/solarized.css"
import { codemirror } from "vue-codemirror"
import { getGitlabList } from '@/views/container/apis/gitlab'
import {
  getJenkinsList,
  createJenkinsFolders,
  createJenkinsItem,
  getJenkinsJobURL
} from '@/views/container/apis/jenkins'
import { getProductList } from '@/views/container/apis/product'
import { getEnvironList } from '@/views/container/apis/environ'
import { getRegistryList } from '@/views/container/apis/registry'
import { getChartList, getChartTagList } from '@/views/container/apis/chart'
import { getImageList, getImageTagList } from '@/views/container/apis/image'
import { getClusterList, getClusterNsList } from '@/views/container/apis/cluster'
import {
  getReleaseList,
  createRelease,
  createReleaseConfig,
  updateReleaseConfig,
  createReleaseHelmPackage,
  installRelease
} from '@/views/container/apis/release'

export default {
  filters: {
    parseTime(time, cFormat) {
      return parseTime(time, cFormat)
    }
  },
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
      app_list: [],
      app_list_total: 0,
      dialog_map: {
        create_app: "新增应用",
        update_app: "编辑应用",
        view_app_config: "应用配置文件"
      },
      dialog_status: "",
      app_dialog: false,
      code_mirror_options: {
        tabSize: 2,
        cursorHeight: 0.8,
        mode: "yaml",
        theme: "solarized dark",
        line: true,
        lineNumbers: true
      },
      dialog_active_tab_name: "requirement_config",
      // 前置配置--------------------------------------------------
      requirement_config_disable: false,
      requirement_config_form: {
        environ: null,
        environ_name: null,
        product: null,
        product_name: null,
        project: null,
        project_name: null,
        gitlab: null,
        jenkins_folder: null,
        jenkins: null
      },
      requirement_config_form_rules: {
        environ: [{ required: true, message: '不能为空', trigger: ['blur', 'change'] }],
        product: [{ required: true, message: '不能为空', trigger: ['blur', 'change'] }],
        project: [{ required: true, message: '不能为空', trigger: ['blur', 'change'] }],
        gitlab: [{ required: true, message: '不能为空', trigger: ['blur', 'change'] }],
        jenkins: [{ required: true, message: '不能为空', trigger: ['blur', 'change'] }]
      },
      gitlab_list: [],
      jenkins_list: [],
      environ_list: [],
      product_list: [],
      project_list: [],
      // 基础配置--------------------------------------------------
      basic_config_disable: true,
      basic_config_form: {
        chart: null,
        version: null,
        types: 0,
        registry: null,
        image: null,
        image_version: null,
        monitor: false,
        monitor_path: "/metrics",
        monitor_port: null,
        args: false,
        args_content: null
      },
      basic_config_form_rules: {
        types: [{ required: true, message: '不能为空', trigger: ['blur', 'change'] }],
        registry: [{ required: true, message: '不能为空', trigger: ['blur', 'change'] }],
        image: [{ required: true, message: '不能为空', trigger: ['blur', 'change'] }],
        image_version: [{ required: true, message: '不能为空', trigger: ['blur', 'change'] }]
      },
      registry_list: [],
      app_types_list: [
        { id: 0, name: "deployment" },
        { id: 1, name: "statefulset" },
        { id: 2, name: "daemonset" }
      ],
      image_list: [],
      image_tag_list: [],
      chart_list: [],
      chart_tag_list: [],
      cluster_list: [],
      cluster_ns_list: [],
      // 配置概览--------------------------------------------------
      overview_config_disable: true,
      overview_config_form: {
        id: null,
        name: null,
        config: null
      },
      overview_config_form_rules: {
        name: [{ required: true, message: '不能为空', trigger: ['blur', 'change'] }],
        config: [{ required: true, message: '不能为空', trigger: ['blur', 'change'] }]
      },
      // 安装应用--------------------------------------------------
      target_config_disable: true,
      target_config_form: {
        cluster: null,
        namespace: null,
        cluster_name: null
      },
      target_config_form_rules: {
        cluster: [{ required: true, message: '不能为空', trigger: ['blur', 'change'] }],
        namespace: [{ required: true, message: '不能为空', trigger: ['blur', 'change'] }]
      },
      // 查看应用配置文件--------------------------------------------------
      view_app_dialog: false,
      view_app_config_form: {
        id: null,
        name: null,
        chart_config: null,
        value_config: null
      },
      view_app_config_form_rules: {}
    }
  },
  computed: {
    ...mapGetters(['user_id'])
  },
  created() {
    this.get_app_list()
  },
  methods: {
    create_app() {
      this.dialog_status = "create_app"
      this.app_dialog = true
      this.requirement_config_disable = false
      this.basic_config_disable = true
      this.overview_config_disable = true
      this.get_environ_list()
      this.get_product_list()
      this.get_jenkins_list()
    },
    cancel_create_app() {
      this.dialog_status = "create_app"
      this.app_dialog = false
      this.dialog_active_tab_name = "requirement_config"
      this.requirement_config_disable = false
      this.$refs.requirement_config_formRef.resetFields()
      this.basic_config_disable = true
      this.$refs.basic_config_formRef.resetFields()
      this.overview_config_disable = true
      this.target_config_disable = true
      this.$refs.target_config_formRef.resetFields()
    },
    // 前置配置--------------------------------------------------
    get_environ_list() {
      getEnvironList({ limit: 999 })
        .then(resp => {
          this.environ_list = resp.data.results
        })
    },
    step_to_requirement_config() {
      this.dialog_active_tab_name = "requirement_config"
      this.requirement_config_disable = false
      this.basic_config_disable = true
      this.overview_config_disable = true
    },
    create_jenkins_folder() {
      createJenkinsFolders({
        "jenkins": this.requirement_config_form.jenkins,
        "jenkins_folder": this.requirement_config_form.jenkins_folder
      })
        .then(resp => {
          var msg = resp.data.msg
          var status = resp.data.status
          if (status) {
            this.$message({
              type: "success",
              message: msg
            })
          }
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    create_jenkins_item() {
      createJenkinsItem({
        "gitlab": this.requirement_config_form.gitlab,
        "jenkins": this.requirement_config_form.jenkins,
        "jenkins_folder": this.requirement_config_form.jenkins_folder
      })
        .then(resp => {
          var msg = resp.data.msg
          var status = resp.data.status
          if (status) {
            this.$message({
              type: "success",
              message: msg
            })
          }
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    goto_jenkins() {
      var job_url = ""
      getJenkinsJobURL({
        "jenkins": this.requirement_config_form.jenkins,
        "jenkins_folder": this.requirement_config_form.jenkins_folder
      })
        .then(resp => {
          job_url = resp.data
          window.open(job_url, "_blank")
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 基础配置--------------------------------------------------
    step_to_basic_config() {
      this.dialog_active_tab_name = "basic_config"
      this.requirement_config_disable = true
      this.basic_config_disable = false
      this.overview_config_disable = true
      this.get_registry_list()
      // this.get_chart_list()
      // this.get_cluster_list()
      // this.$refs.requirement_config_formRef.validate((valid) => {
      //   if (valid) {
      //     this.dialog_active_tab_name = "basic_config"
      //     this.requirement_config_disable = true
      //     this.basic_config_disable = false
      //     this.overview_config_disable = true
      //     this.get_registry_list()
      //     this.get_chart_list()
      //     this.get_cluster_list()
      //   } else {
      //     this.$message({
      //       type: "warning",
      //       message: "你一定在考虑什么"
      //     })
      //     return false
      //   }
      // })
    },
    // 生成配置并预览
    create_release_config() {
      var create_data = Object.assign({})
      // create_data.types = this.basic_config_form.types
      create_data.types = "deployment"
      create_data.name = this.requirement_config_form.project_name
      create_data.image_version = this.basic_config_form.image_version
      createReleaseConfig(create_data)
        .then(resp => {
          // console.log(resp, '========')
          this.overview_config_form.id = resp.data.id
          this.overview_config_form.name = resp.data.name
          this.overview_config_form.config = resp.data.msg
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 基础概览--------------------------------------------------
    step_to_overview_config() {
      this.dialog_active_tab_name = "overview_config"
      this.basic_config_disable = true
      this.overview_config_disable = false
      this.target_config_disable = true
      this.create_release_config()
    },
    update_release_config() {
      // console.log(this.overview_config_form)
      var update_data = Object.assign({})
      update_data.name = this.requirement_config_form.project_name
      update_data.config = this.overview_config_form.config
      updateReleaseConfig(update_data)
        .then(resp => {
          this.overview_config_form.id = resp.data.id
          this.overview_config_form.name = resp.data.name
          this.overview_config_form.config = resp.data.msg
          this.$message({
            type: "success",
            message: "更新配置成功"
          })
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    create_helm_package() {
      var create_data = Object.assign({})
      create_data.release_name = this.requirement_config_form.project_name
      createReleaseHelmPackage(create_data)
        .then(resp => {
          console.log(resp.data.msg, '========')
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    step_to_target_config() {
      this.dialog_active_tab_name = "target_config"
      this.basic_config_disable = true
      this.overview_config_disable = true
      this.target_config_disable = false
      this.create_helm_package()
      this.get_cluster_list()
    },
    update_app() { },
    delete_app() { },
    view_app_config(row) {
      this.view_app_dialog = true
      this.dialog_status = "view_app_config"
      this.view_app_config_form.name = row.name
      this.view_app_config_form.chart_config = row.config__chart_config
      this.view_app_config_form.value_config = row.config__value_config
    },
    redeploy_app() { },
    view_app_log() { },
    view_app_monitor() { },
    change_app_version() { },
    submit_app() {
      if (this.dialog_status === "create_app") {
        var requirement_data = Object.assign({}, this.requirement_config_form)
        var basic_data = Object.assign({}, this.basic_config_form)
        var overview_data = Object.assign({}, this.overview_config_form)
        var target_data = Object.assign({}, this.target_config_form)
        var create_data = Object.assign({})
        create_data.name = requirement_data.project_name
        create_data.user = this.$store.getters.user_id
        create_data.environ = requirement_data.environ
        create_data.types = basic_data.types
        create_data.registry = basic_data.registry
        create_data.image = basic_data.image_version
        create_data.cluster = target_data.cluster
        create_data.cluster_name = target_data.cluster_name
        create_data.namespace = target_data.namespace
        create_data.gitlab = requirement_data.gitlab
        create_data.config = overview_data.id
        console.log(create_data, '=====')
        var install_data = Object.assign({})
        install_data.cluster_name = target_data.cluster_name
        install_data.release_name = requirement_data.project_name
        installRelease(install_data)
        createRelease(create_data)
          .then(resp => {
            this.$message({
              type: "success",
              message: "新增应用【" + requirement_data.project_name + "】成功"
            })
            this.cancel_create_app()
            this.get_app_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.cancel_create_app()
            this.get_app_list()
          })
      } else if (this.dialog_status === "update_app") {
        //
      }
    },
    view_app_info(row) {
      const parObj = JSON.stringify(row)
      this.$router.push({
        path: "/container/app_info/",
        query: { app_info: parObj }
      })
    },
    get_app_list() {
      getReleaseList(this.list_query)
        .then(resp => {
          this.app_list = resp.data.results
          this.app_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    get_product_list() {
      getProductList({ limit: 999 })
        .then(resp => {
          this.product_list = resp.data.results
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    get_gitlab_list() {
      getGitlabList({ limit: 999 })
        .then(resp => {
          this.gitlab_list = resp.data.results
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    get_jenkins_list() {
      getJenkinsList({ limit: 999 })
        .then(resp => {
          this.jenkins_list = resp.data.results
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    select_environ(environ_id) {
      getEnvironList({ id: environ_id })
        .then(resp => {
          this.requirement_config_form.environ_name = resp.data.results[0]["name"]
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 选择当前产品下的项目和gitlab项目
    select_product(product_id) {
      // getProjectList({ product: product_id })
      //   .then(resp => {
      //     this.project_list = resp.data.results
      //   })
      getGitlabList({ product: product_id })
        .then(resp => {
          this.gitlab_list = resp.data.results
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 选择完项目之后 在Jenkins中的项目目录其实已经定好了
    select_project(project_id) {
      getGitlabList({ id: project_id })
        .then(resp => {
          this.requirement_config_form.project_name = resp.data.results[0]["name"]
          this.requirement_config_form.product_name = resp.data.results[0]["product__name"]
          this.requirement_config_form.jenkins_folder = this.requirement_config_form.product_name +
            "/" + this.requirement_config_form.project_name +
            "/" + this.requirement_config_form.environ_name
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    get_registry_list() {
      getRegistryList({ limit: 999 })
        .then(resp => {
          this.registry_list = resp.data.results
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    get_chart_list() {
      getChartList({ limit: 999 })
        .then(resp => {
          this.chart_list = resp.data.results
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    get_image_list() {
      getImageList()
    },
    select_registry_image(registry_id) {
      getImageList({ namespace__name: this.requirement_config_form.project_name })
        .then(resp => {
          this.image_list = resp.data.results
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    select_image_tag(image_id) {
      getImageTagList({ image: image_id })
        .then(resp => {
          this.image_tag_list = resp.data.results
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    select_chart_tag(chart_id) {
      getChartTagList({ chart: chart_id })
        .then(resp => {
          this.chart_tag_list = resp.data.results
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    select_cluster_ns(cluster_id) {
      getClusterNsList({ cluster: cluster_id })
        .then(resp => {
          this.target_config_form.cluster_name = resp.data.results[0]["cluster__name"]
          this.cluster_ns_list = resp.data.results
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    get_cluster_list() {
      getClusterList({ limit: 999 })
        .then(resp => {
          this.cluster_list = resp.data.results
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
.el-form {
  margin-top: 10px;
}
.el-table {
  width: 100%;
  margin-top: 10px;
}
</style>
