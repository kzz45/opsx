<template>
  <div>
    <el-button
      type="primary"
      size="small"
      icon="el-icon-circle-plus"
      @click="create_alert_route"
    >新增</el-button>
    <!-- 告警路由列表--------------------------------------------------  -->
    <el-table
      ref="alert_route_list_table_refs"
      :data="alert_route_list"
      empty-text="啥也没有"
      size="small"
      border
      @expand-change="get_child_route"
    >
      <el-table-column
        label="名称"
        prop="name"
      ></el-table-column>
      <el-table-column
        label="接收者"
        prop="receiver__list"
      >
        <template slot-scope="scoped">
          <el-tag
            v-for="(item, index) in scoped.row.receiver__list"
            :key="index"
          >{{ item }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column
        label="重复告警"
        prop="repeat_interval"
      >
        <template slot-scope="scoped">
          <el-tag>{{ scoped.row.repeat_interval / 60 }}分钟</el-tag>
        </template>
      </el-table-column>
      <el-table-column
        label="匹配标签"
        prop="match"
      >
        <template slot-scope="scoped">
          <el-tag
            v-for="(item, index) in (JSON.parse(scoped.row.match)).label"
            :key="index"
          >{{ item.name + '=' + item.value }}</el-tag>
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
        width="240px;"
      >
        <template slot-scope="scoped">
          <el-button
            type="primary"
            icon="el-icon-edit"
            size="mini"
            @click="update_alert_route(scoped.row)"
          ></el-button>
          <el-tooltip
            class="item"
            effect="dark"
            content="查看子路由"
            placement="top"
          >
            <el-button
              type="info"
              icon="el-icon-arrow-down"
              size="mini"
              @click="view_child_route(scoped.row)"
            ></el-button>
          </el-tooltip>
          <el-tooltip
            class="item"
            effect="dark"
            content="添加子路由"
            placement="top"
          >
            <el-button
              type="success"
              icon="el-icon-plus"
              size="mini"
              @click="create_child_route(scoped.row)"
            ></el-button>
          </el-tooltip>
          <el-popconfirm
            title="确定删除吗？"
            confirm-button-text="确定"
            cancel-button-text="不了"
            style="margin-left: 10px"
            @confirm="delete_alert_route(scoped.row)"
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
            ref="child_route_list_table_refs"
            :data="scoped.row.child_routes"
            empty-text="没有子路由"
            border
            size="small"
          >
            <el-table-column
              label="名称"
              prop="name"
            ></el-table-column>
            <el-table-column
              label="接收者"
              prop="receiver__list"
            >
              <template slot-scope="scope">
                <el-tag
                  v-for="(item, index) in scope.row.receiver__list"
                  :key="index"
                >{{ item }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column
              label="重复告警"
              prop="repeat_interval"
            >
              <template slot-scope="scope">
                <el-tag>{{ scope.row.repeat_interval / 60 }}分钟</el-tag>
              </template>
            </el-table-column>
            <el-table-column
              label="标签"
              prop="match"
            >
              <template slot-scope="scope">
                <el-tag
                  v-for="(item, index) in (JSON.parse(scope.row.match)).label"
                  :key="index"
                >{{ item.name + '=' + item.value }}</el-tag>
              </template>
            </el-table-column>

            <el-table-column
              label="产品"
              prop="product__name"
            ></el-table-column>
            <el-table-column
              label="是否继续"
              prop="is_raise"
            >
              <template slot-scope="scope">
                <el-tag
                  v-if="scope.row.is_raise == 0"
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
              label="操作"
              width="120px;"
            >
              <template slot-scope="scope">
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  size="mini"
                  @click="update_child_route(scope.row)"
                ></el-button>
                <el-popconfirm
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left: 10px"
                  @confirm="delete_child_route(scope.row)"
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
      v-show="alert_route_list_total>0"
      :total="alert_route_list_total"
      :page.sync="list_query.page"
      :limit.sync="list_query.limit"
      @pagination="get_alert_route_list"
    ></pagination>
    <!-- 告警路由管理Dialog--------------------------------------------------  -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="alert_route_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="50%"
    >
      <el-form
        ref="alert_route_formRef"
        :model="alert_route_form"
        :rules="alert_route_form_rules"
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
                v-model="alert_route_form.name"
                clearable
                placeholder="告警路由名称"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="接收者"
              prop="receiver"
            >
              <el-select
                v-model="alert_route_form.receiver"
                clearable
                filterable
                multiple
                autocomplete="on"
                placeholder="请选择接收者"
              >
                <el-option
                  v-for="(item) in receiver_list"
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
              label="是否继续"
              prop="is_raise"
            >
              <el-radio-group v-model="alert_route_form.is_raise">
                <el-radio :label="0">是</el-radio>
                <el-radio :label="1">否</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="路由正则"
              prop="match_re"
            >
              <el-radio-group v-model="alert_route_form.match_re">
                <el-radio :label="false">否</el-radio>
                <el-radio :label="true">是</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="匹配标签"
              prop="labels_name"
            >
              <el-select
                v-model="alert_route_form.labels_name"
                clearable
                filterable
                allow-create
                placeholder="标签名"
                @change="select_label_value"
              >
                <el-option
                  v-for="(item) in labels_name_list"
                  :key="item"
                  :value="item"
                  :label="item"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="标签值"
              prop="labels_value"
            >
              <el-select
                v-model="alert_route_form.labels_value"
                clearable
                filterable
                allow-create
                placeholder="标签值"
                style="width: 150px;"
              >
                <el-option
                  v-for="(item) in labels_value_list"
                  :key="item.id"
                  :value="item.value"
                  :label="item.value"
                ></el-option>
              </el-select>
              <el-button
                type="primary"
                icon="el-icon-plus"
                size="small"
                style="margin-left: 10px;"
                @click="add_labels_condition"
              ></el-button>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <el-form-item v-if="label_value_list.length > 0">
              <el-tag
                v-for="(item, index) in label_value_list"
                :key="index"
                closable
                :disable-transitions="false"
                style="margin-left: 2px;"
                @close="delete_labels_condition(item.value)"
              >{{ item.name }}={{ item.value }}</el-tag>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="聚合时间"
              prop="group_wait"
            >
              <el-input-number
                v-model="alert_route_form.group_wait"
                :step="60"
                clearable
                placeholder="聚合时间"
              ></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="重复聚合"
              prop="group_interval"
            >
              <el-input-number
                v-model="alert_route_form.group_interval"
                :step="60"
                clearable
                placeholder="重复聚合时间"
              ></el-input-number>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="重复发送"
              prop="repeat_interval"
            >
              <el-input-number
                v-model="alert_route_form.repeat_interval"
                :step="60"
                clearable
                placeholder="重复发送时间"
              ></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="关联产品"
              prop="product"
            >
              <el-select
                v-model="alert_route_form.product"
                placeholder="请选择产品"
                clearable
                filterable
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
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="聚合条件"
              prop="group_by"
            >
              <el-select
                v-model="alert_route_form.group_by"
                placeholder="请选择聚合条件"
                multiple
                filterable
              >
                <el-option
                  v-for="item in conditionData"
                  :key="item.value"
                  :label="item.name"
                  :value="item.value"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="启用"
              prop="enable"
            >
              <el-radio-group v-model="alert_route_form.enable">
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
          @click="alert_route_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_alert_route"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 告警子路由管理Dialog--------------------------------------------------  -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="child_route_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="50%"
    >
      <el-form
        ref="child_route_formRef"
        :model="child_route_form"
        :rules="child_route_form_rules"
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
                v-model="child_route_form.name"
                clearable
                placeholder="告警路由名称"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="接收者"
              prop="receiver"
            >
              <el-select
                v-model="child_route_form.receiver"
                clearable
                filterable
                multiple
                autocomplete="on"
                placeholder="请选择接收者"
              >
                <el-option
                  v-for="(item) in receiver_list"
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
              label="是否继续"
              prop="is_raise"
            >
              <el-radio-group v-model="child_route_form.is_raise">
                <el-radio :label="0">是</el-radio>
                <el-radio :label="1">否</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="路由正则"
              prop="match_re"
            >
              <el-radio-group v-model="child_route_form.match_re">
                <el-radio :label="false">否</el-radio>
                <el-radio :label="true">是</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="匹配标签"
              prop="labels_name"
            >
              <el-select
                v-model="child_route_form.labels_name"
                clearable
                filterable
                allow-create
                placeholder="标签名"
                @change="select_label_value"
              >
                <el-option
                  v-for="(item) in labels_name_list"
                  :key="item"
                  :value="item"
                  :label="item"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="标签值"
              prop="labels_value"
            >
              <el-select
                v-model="child_route_form.labels_value"
                clearable
                filterable
                allow-create
                placeholder="标签值"
                style="width: 150px;"
              >
                <el-option
                  v-for="(item) in labels_value_list"
                  :key="item.id"
                  :value="item.value"
                  :label="item.value"
                ></el-option>
              </el-select>
              <el-button
                type="primary"
                icon="el-icon-plus"
                size="small"
                style="margin-left: 10px;"
                @click="add_child_labels_condition"
              ></el-button>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <el-form-item v-if="child_label_value_list.length > 0">
              <el-tag
                v-for="(item, index) in child_label_value_list"
                :key="index"
                closable
                :disable-transitions="false"
                style="margin-left: 2px;"
                @close="delete_child_labels_condition(item.value)"
              >{{ item.name }}={{ item.value }}</el-tag>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="聚合时间"
              prop="group_wait"
            >
              <el-input-number
                v-model="child_route_form.group_wait"
                :step="60"
                clearable
                placeholder="聚合时间"
              ></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="重复聚合"
              prop="group_interval"
            >
              <el-input-number
                v-model="child_route_form.group_interval"
                :step="60"
                clearable
                placeholder="重复聚合时间"
              ></el-input-number>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="重复发送"
              prop="repeat_interval"
            >
              <el-input-number
                v-model="child_route_form.repeat_interval"
                :step="60"
                clearable
                placeholder="重复发送时间"
              ></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="关联产品"
              prop="product"
            >
              <el-select
                v-model="child_route_form.product"
                placeholder="请选择产品"
                clearable
                filterable
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
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="启用"
              prop="enable"
            >
              <el-radio-group v-model="child_route_form.enable">
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
          @click="child_route_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_child_route"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"
import { getLabelsList } from '@/views/monitor/apis/labels'
import { getProductList } from '@/views/monitor/apis/product'
import { getReceiverList } from '@/views/monitor/apis/receiver'
import { createAlertRoute, updateAlertRoute, deleteAlertRoute, getAlertRouteList } from '@/views/monitor/apis/alert_route'
import { getAlertRouteChildList, createAlertRouteChild, updateAlertRouteChild, deleteAlertRouteChild } from '@/views/monitor/apis/child_route'

export default {
  name: "AlertRouteConfig",
  components: {
    Pagination
  },
  data() {
    return {
      list_query: {
        page: 1,
        limit: 15
      },
      dialog_map: {
        create_alert_route: "新增告警路由",
        update_alert_route: "编辑告警路由",
        create_child_route: "新增子路由",
        update_child_route: "编辑子路由"
      },
      dialog_status: "",
      instance_type_list: [],
      labels_name_list: [],
      labels_value_list: [],
      product_list: [],
      receiver_list: [],
      // 告警路由管理--------------------------------------------------
      alert_route_list: [],
      alert_route_list_total: 0,
      alert_route_dialog: false,
      label_value_list: [],
      alert_route_form: {
        id: null,
        name: null,
        receiver: [],
        match: null,
        group_by: ["alertname", "level", "_product_id"],
        group_wait: 60,
        group_interval: 60,
        repeat_interval: 3600,
        labels_name: null,
        labels_value: null,
        product: null,
        is_raise: 0,
        match_re: false,
        enable: true
      },
      alert_route_form_rules: {
        name: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        receiver: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        group_wait: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        group_interval: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        repeat_interval: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        product: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        is_raise: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        match: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        match_re: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        enable: [{ required: true, message: "该项不能为空", trigger: "blur" }]
      },
      // 告警路由聚合条件
      conditionData: [
        { name: 'alertname', value: 'alertname' },
        { name: 'level', value: 'level' },
        { name: ' _product_id', value: '_product_id' }
      ],
      child_route_dialog: false,
      child_label_value_list: [],
      child_route_form: {
        id: null,
        is_raise: 0,
        receiver: [],
        match: null,
        match_re: false,
        labels_name: null,
        labels_value: null,
        group_wait: 60,
        group_interval: 60,
        repeat_interval: 3600,
        product: null,
        enable: true,
        alert_route: null
      },
      child_route_form_rules: {
        name: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        receiver: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        group_wait: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        group_interval: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        repeat_interval: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        product: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        is_raise: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        match: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        match_re: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        enable: [{ required: true, message: "该项不能为空", trigger: "blur" }]
      }
    }
  },
  methods: {
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
    get_receiver_list() {
      getReceiverList({ limit: 100 })
        .then(resp => {
          this.receiver_list = resp.data.results
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
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
      if (this.alert_route_form.labels_name === "" || this.alert_route_form.labels_value === "") {
        return
      }
      this.label_value_list.push({
        name: this.alert_route_form.labels_name,
        value: this.alert_route_form.labels_value
      })
      this.alert_route_form.labels_name = null
      this.alert_route_form.labels_value = null
    },
    add_child_labels_condition() {
      if (this.child_route_form.labels_name === "" || this.child_route_form.labels_value === "") {
        return
      }
      this.child_label_value_list.push({
        name: this.child_route_form.labels_name,
        value: this.child_route_form.labels_value
      })
      this.child_route_form.labels_name = null
      this.child_route_form.labels_value = null
    },
    delete_labels_condition(tag) {
      this.label_value_list.map((item, index) => {
        if (item.value === tag) {
          this.label_value_list.splice(index, 1)
        }
      })
    },
    delete_child_labels_condition(tag) {
      this.child_label_value_list.map((item, index) => {
        if (item.value === tag) {
          this.child_label_value_list.splice(index, 1)
        }
      })
    },
    // 告警路由管理--------------------------------------------------
    create_alert_route() {
      this.dialog_status = "create_alert_route"
      this.alert_route_dialog = true
      this.get_product_list()
      this.get_receiver_list()
      this.get_label_name_list()
    },
    update_alert_route(row) {
      this.dialog_status = "update_alert_route"
      this.alert_route_dialog = true
      this.alert_route_form = Object.assign({}, row)
      this.alert_route_form.receiver = row.receiver
      this.alert_route_form.group_by = JSON.parse(row.group_by)
      this.label_value_list = JSON.parse(row.match).label
      this.get_product_list()
      this.get_receiver_list()
      this.get_label_name_list()
    },
    delete_alert_route(row) {
      deleteAlertRoute(row.id)
        .then((resp) => {
          this.$message({
            type: "success",
            message: "删除成功"
          })
          this.get_alert_route_list()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
          this.get_alert_route_list()
        })
    },
    submit_alert_route() {
      if (this.dialog_status === "create_alert_route") {
        this.$refs.alert_route_formRef.validate((valid) => {
          if (valid) {
            var create_data = Object.assign({}, this.alert_route_form)
            create_data.group_by = JSON.stringify(this.alert_route_form.group_by)
            var param = { label: this.label_value_list }
            create_data.match = JSON.stringify(param)

            createAlertRoute(create_data)
              .then((resp) => {
                this.$message({
                  type: "success",
                  message: "新增成功"
                })
                this.alert_route_dialog = false
                this.get_alert_route_list()
              })
              .catch((err) => {
                this.$message({
                  type: "error",
                  message: err
                })
                this.alert_route_dialog = false
                this.get_alert_route_list()
              })
          }
        })
      } else if (this.dialog_status === "update_alert_route") {
        var post_data = Object.assign({}, this.alert_route_form)
        post_data.group_by = JSON.stringify(this.alert_route_form.group_by)
        const param = { label: this.label_value_list }
        post_data.match = JSON.stringify(param)
        updateAlertRoute(post_data.id, post_data)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新成功"
            })
            this.alert_route_dialog = false
            this.get_alert_route_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.alert_route_dialog = false
            this.get_alert_route_list()
          })
      }
    },
    get_alert_route_list() {
      getAlertRouteList(this.list_query)
        .then(resp => {
          this.alert_route_list = resp.data.results.map(item => {
            item.child_routes = []
            return item
          })
          this.alert_route_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    view_child_route(row) {
      const $table = this.$refs.alert_route_list_table_refs
      this.alert_route_list.map((item) => {
        if (row.id !== item.id) {
          $table.toggleRowExpansion(item, false)
        }
      })
      $table.toggleRowExpansion(row)
    },
    create_child_route(row) {
      this.dialog_status = "create_child_route"
      this.child_route_dialog = true
      this.child_route_form.alert_route = row.id
      this.get_product_list()
      this.get_receiver_list()
      this.get_label_name_list()
    },
    update_child_route(row) {
      this.dialog_status = "update_child_route"
      this.child_route_dialog = true
      this.child_route_form = Object.assign({}, row)
      this.child_route_form.receiver = row.receiver
      this.child_label_value_list = JSON.parse(row.match).label
      this.get_product_list()
      this.get_receiver_list()
      this.get_label_name_list()
    },
    delete_child_route(row) {
      deleteAlertRouteChild(row.id)
        .then((resp) => {
          this.$message({
            type: "success",
            message: "删除成功"
          })
          this.get_alert_route_list()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
          this.get_alert_route_list()
        })
    },
    submit_child_route() {
      if (this.dialog_status === "create_child_route") {
        this.$refs.child_route_formRef.validate((valid) => {
          if (valid) {
            var create_data = Object.assign({}, this.child_route_form)
            var param = { label: this.child_label_value_list }
            create_data.match = JSON.stringify(param)
            createAlertRouteChild(create_data)
              .then((resp) => {
                this.$message({
                  type: "success",
                  message: "新增成功"
                })
                this.child_route_dialog = false
                this.get_alert_route_list()
              })
              .catch((err) => {
                this.$message({
                  type: "error",
                  message: err
                })
                this.child_route_dialog = false
                this.get_alert_route_list()
              })
          }
        })
      } else if (this.dialog_status === "update_child_route") {
        var post_data = Object.assign({}, this.child_route_form)
        const param = { label: this.child_label_value_list }
        post_data.match = JSON.stringify(param)
        updateAlertRouteChild(post_data.id, post_data)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新成功"
            })
            this.child_route_dialog = false
            this.get_alert_route_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.child_route_dialog = false
            this.get_alert_route_list()
          })
      }
    },
    get_child_route(row) {
      getAlertRouteChildList({ alert_route: row.id })
        .then(resp => {
          row.child_routes = resp.data.results
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
.el-button {
  vertical-align: top;
}
.el-table {
  width: 100%;
  margin-top: 10px;
}
</style>
