<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-tabs
        v-model="active_tab_name"
        @tab-click="active_tab_click"
      >
        <!-- 告警规则管理--------------------------------------------------  -->
        <el-tab-pane
          label="告警规则"
          name="alert_rule_setting"
        >
          <el-button
            type="primary"
            size="small"
            icon="el-icon-circle-plus"
            @click="create_alert_rule"
          >新增</el-button>
          <el-table
            ref="alert_rule_list_table_refs"
            :data="alert_rule_list"
            empty-text="啥也没有"
            size="small"
            border
            @expand-change="get_child_rule_list"
          >
            <el-table-column
              label="名称"
              prop="name"
            ></el-table-column>
            <el-table-column
              label="规则"
              prop="expression"
            >
              <template slot-scope="scoped">
                {{ scoped.row.expression }} {{ scoped.row.op }} {{ scoped.row.value }}
              </template>
            </el-table-column>
            <el-table-column
              label="等级"
              prop="alert_rule_level__name"
            ></el-table-column>
            <el-table-column
              label="消息"
              prop="summary"
            ></el-table-column>
            <el-table-column
              label="产品"
              prop="product__name"
            ></el-table-column>
            <el-table-column
              label="启用"
              prop="enable"
            >
              <template slot-scope="scoped">
                <el-tag
                  v-if="scoped.row.enable == 1"
                  type="success"
                >是</el-tag>
                <el-tag
                  v-else
                  type="danger"
                >否</el-tag>
              </template>
            </el-table-column>
            <el-table-column
              label="操作"
              probe="options"
              width="240px"
            >
              <template slot-scope="scoped">
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  size="mini"
                  @click="update_alert_rule(scoped.row)"
                ></el-button>
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="查看子规则"
                  placement="top"
                >
                  <el-button
                    type="info"
                    icon="el-icon-arrow-down"
                    size="mini"
                    @click="view_child_rule(scoped.row)"
                  ></el-button>
                </el-tooltip>
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="添加子规则"
                  placement="top"
                >
                  <el-button
                    type="success"
                    icon="el-icon-plus"
                    size="mini"
                    @click="create_child_rule(scoped.row)"
                  ></el-button>
                </el-tooltip>
                <el-popconfirm
                  title="确定删除这条规则吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left: 10px"
                  @confirm="delete_alert_rule(scoped.row)"
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
            <el-table-column
              type="expand"
              width="1"
            >
              <template slot-scope="scoped">
                <el-table
                  ref="child_rule_list_table_refs"
                  :data="scoped.row.child_rules"
                  empty-text="没有子规则"
                  border
                  size="small"
                >
                  <el-table-column
                    label="规则"
                    prop="expression"
                  >
                    <template slot-scope="scope">
                      {{ scope.row.expression }} {{ scope.row.op }} {{ scope.row.value }}
                    </template>
                  </el-table-column>
                  <el-table-column
                    label="覆盖"
                    prop="is_cover"
                  >
                    <template slot-scope="scope">
                      {{ scope.row.is_cover == 1?'是':'否' }}
                    </template>
                  </el-table-column>
                  <el-table-column
                    label="产品"
                    prop="product__name"
                  ></el-table-column>
                  <el-table-column
                    label="启用"
                    prop="enable"
                  >
                    <template slot-scope="scope">
                      <el-tag
                        v-if="scope.row.enable == 1"
                        type="success"
                      >是</el-tag>
                      <el-tag
                        v-else
                        type="danger"
                      >否</el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column
                    label="添加者"
                    prop="user__first_name"
                  ></el-table-column>
                  <el-table-column
                    label="操作"
                    width="120px;"
                  >
                    <template slot-scope="scope">
                      <el-button
                        type="primary"
                        icon="el-icon-edit"
                        size="mini"
                        @click="update_child_rule(scope.row)"
                      ></el-button>
                      <el-popconfirm
                        title="确定删除这条子规则吗？"
                        confirm-button-text="确定"
                        cancel-button-text="不了"
                        style="margin-left: 10px"
                        @confirm="delete_child_rule(scope.row)"
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
              </template>
            </el-table-column>
          </el-table>
          <pagination
            v-show="alert_rule_list_total>0"
            :total="alert_rule_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_alert_rule_list"
          ></pagination>
          <!-- <AlertRuleSetting ref="alert_rule_setting"></AlertRuleSetting> -->
        </el-tab-pane>
        <!-- 告警路由管理--------------------------------------------------  -->
        <el-tab-pane
          label="告警路由"
          name="alert_route_setting"
        >
          <AlertRouteConfig ref="alert_route_setting"></AlertRouteConfig>
        </el-tab-pane>
        <!-- 告警接收--------------------------------------------------  -->
        <el-tab-pane
          label="告警接收"
          name="receiver_setting"
        >
          <ReceiverConfig ref="receiver_setting"></ReceiverConfig>
        </el-tab-pane>
        <!-- 告警回调--------------------------------------------------  -->
        <el-tab-pane
          label="告警回调"
          name="callback_setting"
        >
          <CallbackConfig ref="callback_setting"></CallbackConfig>
        </el-tab-pane>
      </el-tabs>
    </el-card>
    <!-- 告警规则管理Dialog--------------------------------------------------  -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="alert_rule_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="50%"
    >
      <el-form
        ref="alert_rule_formRef"
        :model="alert_rule_form"
        :rules="alert_rule_form_rules"
        size="small"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="名称"
              prop="name"
            >
              <el-input
                v-model="alert_rule_form.name"
                placeholder="告警规则名称"
                clearable
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="等级"
              prop="alert_rule_level"
            >
              <el-select
                v-model="alert_rule_form.alert_rule_level"
                clearable
                placeholder="请选择告警等级"
              >
                <el-option
                  v-for="item in alert_rule_level_list"
                  :key="item.id"
                  :value="item.id"
                  :label="item.name"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="类型"
              prop="alert_rule_type"
            >
              <el-select
                v-model="alert_rule_form.alert_rule_type"
                clearable
                placeholder="请选择告警规则类型"
              >
                <el-option
                  v-for="item in alert_rule_type_list"
                  :key="item.id"
                  :value="item.id"
                  :label="item.name"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="持续时间"
              prop="interval"
            >
              <el-input-number
                v-model="alert_rule_form.interval"
                placeholder="告警持续时间"
              ></el-input-number>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="表达式"
              prop="expression"
            >
              <el-input
                v-model="alert_rule_form.expression"
                :autosize="{ minRows:2, maxRows: 4 }"
                type="textarea"
                placeholder="告警规则内容"
                style="width: 540px;"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="告警概述"
              prop="summary"
            >
              <el-input
                v-model="alert_rule_form.summary"
                :autosize="{ minRows:2, maxRows: 4 }"
                type="textarea"
                placeholder="告警概述消息"
                style="width: 200px;"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="告警描述"
              prop="description"
            >
              <el-input
                v-model="alert_rule_form.description"
                :autosize="{ minRows:2, maxRows: 4 }"
                type="textarea"
                placeholder="告警描述消息"
                style="width: 200px;"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="操作符"
              prop="op"
            >
              <el-select
                v-model="alert_rule_form.op"
                filterable
                clearable
                placeholder="操作符"
              >
                <el-option
                  v-for="item in op_item_list"
                  :key="item.id"
                  :value="item.id"
                  :label="item.name"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="阈值"
              prop="value"
            >
              <el-input-number
                v-model="alert_rule_form.value"
                placeholder="阈值"
              ></el-input-number>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="记录值"
              prop="record"
            >
              <el-input
                v-model="alert_rule_form.record"
                :autosize="{ minRows:2, maxRows: 4 }"
                type="textarea"
                placeholder="告警记录规则内容"
                style="width: 540px;"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="关联产品"
              prop="product"
            >
              <el-select
                v-model="alert_rule_form.product"
                placeholder="请选择产品"
              >
                <el-option
                  v-for="(item) in product_list"
                  :key="item.id"
                  :value="item.id"
                  :label="item.name"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="状态"
              prop="enable"
            >
              <!-- <el-switch
                v-model="alert_rule_form.enable"
                active-color="#13ce66"
                inactive-color="#ff4949"
                active-text="启用"
                inactive-text="禁用"
                :active-value="true"
                :inactive-value="false"
              >
              </el-switch> -->
              <el-radio-group v-model="alert_rule_form.enable">
                <el-radio :label="true">启用</el-radio>
                <el-radio :label="false">禁用</el-radio>
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
          @click="alert_rule_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_alert_rule"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 告警子规则管理Dialog--------------------------------------------------  -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="child_rule_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="50%"
    >
      <el-form
        ref="child_rule_formRef"
        :model="child_rule_form"
        :rules="child_rule_form_rules"
        size="small"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="名称"
              prop="name"
            >
              <el-input
                v-model="child_rule_form.name"
                placeholder="子规则名称"
                clearable
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="表达式"
              prop="expression"
            >
              <el-input
                v-model="child_rule_form.expression"
                :autosize="{ minRows:2, maxRows: 4 }"
                type="textarea"
                placeholder="子规则内容"
                style="width: 540px;"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="记录值"
              prop="record"
            >
              <el-input
                v-model="child_rule_form.record"
                :autosize="{ minRows:2, maxRows: 4 }"
                type="textarea"
                placeholder="告警记录规则内容"
                style="width: 540px;"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="操作符"
              prop="op"
            >
              <el-select
                v-model="child_rule_form.op"
                filterable
                clearable
                placeholder="操作符"
              >
                <el-option
                  v-for="item in op_item_list"
                  :key="item.id"
                  :value="item.id"
                  :label="item.name"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="阈值"
              prop="value"
            >
              <el-input-number
                v-model="child_rule_form.value"
                placeholder="阈值"
              ></el-input-number>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="持续时间"
              prop="interval"
            >
              <el-input-number
                v-model="child_rule_form.interval"
                placeholder="告警持续时间"
              ></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="状态"
              prop="enable"
            >
              <!-- <el-switch
                v-model="child_rule_form.enable"
                active-color="#13ce66"
                inactive-color="#ff4949"
                active-text="启用"
                inactive-text="禁用"
                :active-value="true"
                :inactive-value="false"
              >
              </el-switch> -->
              <el-radio-group v-model="child_rule_form.enable">
                <el-radio :label="true">启用</el-radio>
                <el-radio :label="false">禁用</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="关联产品"
              prop="product"
            >
              <el-select
                v-model="child_rule_form.product"
                placeholder="请选择产品"
              >
                <el-option
                  v-for="(item) in product_list"
                  :key="item.id"
                  :value="item.id"
                  :label="item.name"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="覆盖"
              prop="is_cover"
            >
              <!-- <el-switch
                v-model="child_rule_form.is_cover"
                active-color="#13ce66"
                inactive-color="#ff4949"
                active-text="是"
                inactive-text="否"
                :active-value="true"
                :inactive-value="false"
              >
              </el-switch> -->
              <el-radio-group v-model="child_rule_form.is_cover">
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
          @click="child_rule_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_child_rule"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import ReceiverConfig from '@/views/monitor/alert_config/receiver.vue'
import CallbackConfig from '@/views/monitor/alert_config/callback.vue'
import AlertRouteConfig from '@/views/monitor/alert_config/alert_route.vue'
import Pagination from "@/components/Pagination"
import { getLabelsList } from '@/views/monitor/apis/labels'
import { getProductList } from '@/views/monitor/apis/product'
import { getAlertRuleTypeList } from '@/views/monitor/apis/alert_rule_type'
import { getAlertRuleLevelList } from '@/views/monitor/apis/alert_rule_level'
import { getAlertRuleList, createAlertRule, updateAlertRule, deleteAlertRule } from '@/views/monitor/apis/alert_rule'
import { getAlertRuleChildList, createAlertRuleChild, updateAlertRuleChild, deleteAlertRuleChild } from '@/views/monitor/apis/child_rule'

export default {
  name: "MonitorAlertConfig",
  components: {
    Pagination,
    CallbackConfig,
    ReceiverConfig,
    AlertRouteConfig
  },
  data() {
    return {
      list_query: {
        page: 1,
        limit: 15
      },
      active_tab_name: "alert_rule_setting",
      dialog_map: {
        create_alert_rule: "新增告警规则",
        update_alert_rule: "编辑告警规则",
        create_child_rule: "新增告警子规则",
        update_child_rule: "编辑告警子规则"
      },
      dialog_status: "",
      product_list: [],
      // 告警规则管理--------------------------------------------------
      alert_rule_list: [],
      alert_rule_list_total: 0,
      alert_rule_dialog: false,
      alert_rule_form: {
        id: null,
        name: null,
        alert_rule_level: null,
        alert_rule_type: null,
        interval: 180,
        expression: null,
        op: null,
        value: null,
        summary: null,
        description: null,
        product: null,
        enable: true
      },
      alert_rule_form_rules: {
        name: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        alert_rule_level: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        alert_rule_type: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        interval: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        expression: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        op: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        value: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        summary: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        description: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        product: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        enable: [{ required: true, message: "该项不能为空", trigger: "blur" }]
      },
      alert_rule_level_list: [],
      alert_rule_type_list: [],
      op_item_list: [
        { id: '==', name: '==' },
        { id: '!=', name: '!=' },
        { id: '>', name: '>' },
        { id: '>=', name: '>=' },
        { id: '<', name: '<' },
        { id: '<=', name: '<=' }
      ],
      labels_name_list: [],
      labels_value_list: [],
      label_value_list: [],
      child_rule_dialog: false,
      child_rule_form: {
        id: null,
        name: null,
        interval: 180,
        expression: null,
        op: null,
        value: null,
        labels_name: "",
        labels_value: "",
        product: null,
        enable: true,
        is_cover: false,
        alert_rule: null
      },
      child_rule_form_rules: {
        name: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        interval: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        expression: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        op: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        value: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        product: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        is_cover: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        enable: [{ required: true, message: "该项不能为空", trigger: "blur" }]
      }
    }
  },
  created() {
    this.get_alert_rule_list()
  },
  methods: {
    active_tab_click(tab) {
      if (tab.name === "alert_rule_setting") {
        this.get_alert_rule_list()
      } else if (tab.name === "alert_route_setting") {
        this.$refs.alert_route_setting.get_alert_route_list()
      } else if (tab.name === "receiver_setting") {
        this.$refs.receiver_setting.get_receiver_list()
      } else if (tab.name === "callback_setting") {
        this.$refs.callback_setting.get_callback_list()
      }
    },
    get_product_list() {
      getProductList({ limit: 100 })
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
    // 告警规则管理--------------------------------------------------
    create_alert_rule() {
      this.dialog_status = "create_alert_rule"
      this.alert_rule_dialog = true
      this.alert_rule_form.name = null
      this.alert_rule_form.alert_rule_level = null
      this.alert_rule_form.alert_rule_type = null
      this.alert_rule_form.expression = null
      this.alert_rule_form.summary = null
      this.alert_rule_form.description = null
      this.alert_rule_form.op = null
      this.alert_rule_form.value = null
      this.alert_rule_form.product = null
      this.get_product_list()
      this.get_alert_rule_type_list()
      this.get_alert_rule_level_list()
    },
    update_alert_rule(row) {
      this.dialog_status = "update_alert_rule"
      this.alert_rule_dialog = true
      this.alert_rule_form = Object.assign({}, row)
      this.get_product_list()
      this.get_alert_rule_type_list()
      this.get_alert_rule_level_list()
    },
    delete_alert_rule(row) {
      deleteAlertRule(row.id)
        .then(resp => {
          this.$message({
            type: "success",
            message: "删除成功"
          })
          this.get_alert_rule_list()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
          this.get_alert_rule_list()
        })
    },
    submit_alert_rule() {
      if (this.dialog_status === "create_alert_rule") {
        this.$refs.alert_rule_formRef.validate((valid) => {
          if (valid) {
            createAlertRule(this.alert_rule_form)
              .then((resp) => {
                this.$message({
                  type: "success",
                  message: "新增成功"
                })
                this.alert_rule_dialog = false
                this.get_alert_rule_list()
              })
              .catch((err) => {
                this.$message({
                  type: "error",
                  message: err
                })
                this.alert_rule_dialog = false
                this.get_alert_rule_list()
              })
          }
        })
      } else if (this.dialog_status === "update_alert_rule") {
        updateAlertRule(this.alert_rule_form.id, this.alert_rule_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新成功"
            })
            this.alert_rule_dialog = false
            this.get_alert_rule_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.alert_rule_dialog = false
            this.get_alert_rule_list()
          })
      }
    },
    get_alert_rule_list() {
      getAlertRuleList(this.list_query)
        .then(resp => {
          this.alert_rule_list = resp.data.results.map(item => {
            item.child_rules = []
            return item
          })
          this.alert_rule_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    get_alert_rule_level_list() {
      getAlertRuleLevelList({ limit: 100 })
        .then(resp => {
          this.alert_rule_level_list = resp.data.results
        })
    },
    get_alert_rule_type_list() {
      getAlertRuleTypeList({ limit: 100 })
        .then(resp => {
          this.alert_rule_type_list = resp.data.results
        })
    },
    view_child_rule(row) {
      const $table = this.$refs.alert_rule_list_table_refs
      this.alert_rule_list.map((item) => {
        if (row.id !== item.id) {
          $table.toggleRowExpansion(item, false)
        }
      })
      $table.toggleRowExpansion(row)
    },
    get_label_name_list() {
      getLabelsList({ limit: 1000 })
        .then(resp => {
          resp.data.results.forEach(element => {
            if (!this.labels_name_list.includes(element.name)) {
              this.labels_name_list.push(element.name)
            }
          })
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    select_label_value(val) {
      getLabelsList({ name: val }).then(resp => {
        this.labels_value_list = resp.data.results
      })
    },
    add_labels_condition() {
      if (this.child_rule_form.labels_name === "" || this.child_rule_form.labels_value === "") {
        return
      }
      this.label_value_list.push({
        name: this.child_rule_form.labels_name,
        value: this.child_rule_form.labels_value
      })
      this.child_rule_form.labels_name = null
      this.child_rule_form.labels_value = null
    },
    delete_labels_condition(tag) {
      this.label_value_list.map((item, index) => {
        if (item.value === tag) {
          this.label_value_list.splice(index, 1)
        }
      })
    },
    create_child_rule(row) {
      this.dialog_status = "create_child_rule"
      this.child_rule_dialog = true
      this.child_rule_form.alert_rule = row.id
      this.child_rule_form.expression = row.expression
      this.child_rule_form.name = null
      this.child_rule_form.op = null
      this.child_rule_form.value = null
      this.child_rule_form.product = null
      this.get_product_list()
      this.get_label_name_list()
    },
    update_child_rule(row) {
      this.dialog_status = "update_child_rule"
      this.child_rule_dialog = true
      this.child_rule_form = Object.assign({}, row)
      this.get_product_list()
    },
    delete_child_rule(row) {
      deleteAlertRuleChild(row.id)
        .then(resp => {
          this.$message({
            type: "success",
            message: "删除成功"
          })
          this.get_alert_rule_list()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
          this.get_alert_rule_list()
        })
    },
    submit_child_rule() {
      if (this.dialog_status === "create_child_rule") {
        this.$refs.child_rule_formRef.validate((valid) => {
          if (valid) {
            createAlertRuleChild(this.child_rule_form)
              .then((resp) => {
                this.$message({
                  type: "success",
                  message: "新增成功"
                })
                this.child_rule_dialog = false
                this.get_alert_rule_list()
              })
              .catch((err) => {
                this.$message({
                  type: "error",
                  message: err
                })
                this.child_rule_dialog = false
                this.get_alert_rule_list()
              })
          }
        })
      } else if (this.dialog_status === "update_child_rule") {
        updateAlertRuleChild(this.child_rule_form.id, this.child_rule_form)
          .then((resp) => {
            this.$message({
              type: "success",
              message: "更新成功"
            })
            this.child_rule_dialog = false
            this.get_alert_rule_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.child_rule_dialog = false
            this.get_alert_rule_list()
          })
      }
    },
    get_child_rule_list(row) {
      getAlertRuleChildList({ alert_rule: row.id })
        .then(resp => {
          row.child_rules = resp.data.results
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
.el-input-number {
  width: 200px;
}
.el-tag {
  vertical-align: middle;
}
.el-button {
  vertical-align: top;
}
.el-table {
  width: 100%;
  margin-top: 10px;
}
</style>
