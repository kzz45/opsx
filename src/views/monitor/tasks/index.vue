<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-tabs
        v-model="active_tab_name"
        @tab-click="active_tab_click"
      >
        <!-- 基础任务管理--------------------------------------------------  -->
        <el-tab-pane
          label="基础任务"
          name="basic_task_setting"
        >
          <el-button
            type="primary"
            size="small"
            icon="el-icon-circle-plus"
            @click="create_basic_task"
          >新增</el-button>
          <el-table
            ref="basic_task_list_table_refs"
            :data="basic_task_list"
            empty-text="啥也没有"
            size="small"
            border
          >
            <el-table-column
              label="任务名称"
              prop="name"
            ></el-table-column>
            <el-table-column label="任务类型">
              <template slot-scope="scoped">
                <el-tooltip
                  class="item"
                  effect="dark"
                  placement="top-start"
                >
                  <div slot="content">
                    {{ scoped.row.scheme + '://\{\{ instance \}\}:' + scoped.row.port + scoped.row.args }}
                  </div>
                  <el-tag size="small">{{ scoped.row.mode__name }}
                  </el-tag>
                </el-tooltip>
              </template>
            </el-table-column>
            <el-table-column
              label="实例类型"
              prop="instance_type__name"
            ></el-table-column>
            <el-table-column
              label="实例数量"
              prop="instances_count"
            ></el-table-column>
            <el-table-column
              label="产品"
              prop="product__name"
            ></el-table-column>
            <el-table-column
              label="操作"
              prop="options"
              width="180px;"
            >
              <!-- 可以考虑做下跳转到实例列表 查看任务下的具体实例 id__in=1,2,3,4 -->
              <template slot-scope="scoped">
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  size="mini"
                  @click="update_basic_task(scoped.row)"
                ></el-button>
                <el-popconfirm
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left: 10px"
                  @confirm="delete_basic_task(scoped.row)"
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
                  content="任务标签"
                  placement="top"
                  style="margin-left: 10px;"
                >
                  <el-popover
                    placement="bottom-end"
                    width="100"
                    trigger="click"
                  >
                    <el-tag
                      v-for="item in JSON.parse(scoped.row.match)"
                      :key="item.id"
                      size="small"
                      style="margin-top: 2px;"
                    >{{ item.name + '=' + item.value }}
                    </el-tag>
                    <el-button
                      slot="reference"
                      type="info"
                      size="mini"
                      icon="el-icon-price-tag"
                    ></el-button>
                  </el-popover>
                </el-tooltip>
              </template>
            </el-table-column>
          </el-table>
          <pagination
            v-show="basic_task_list_total>0"
            :total="basic_task_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_basic_task_list"
          ></pagination>
        </el-tab-pane>
        <!-- 业务任务管理--------------------------------------------------  -->
        <el-tab-pane
          label="业务任务"
          name="business_task_setting"
        >
          <BusinessTaskConfig ref="business_task_setting"></BusinessTaskConfig>
        </el-tab-pane>
        <!-- 探测任务管理--------------------------------------------------  -->
        <el-tab-pane
          label="探测任务"
          name="probe_task_setting"
        >
          <ProbeTaskConfig ref="probe_task_setting"></ProbeTaskConfig>
        </el-tab-pane>
        <!-- 高级任务管理--------------------------------------------------  -->
        <el-tab-pane
          label="高级任务"
          name="advance_task_setting"
        >
          <AdvanceTaskConfig ref="advance_task_setting"></AdvanceTaskConfig>
        </el-tab-pane>
      </el-tabs>
    </el-card>
    <!-- 基础任务管理--------------------------------------------------  -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="basic_task_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="50%"
    >
      <el-form
        ref="basic_task_formRef"
        :model="basic_task_form"
        :rules="basic_task_form_rules"
        size="small"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="任务名称"
              prop="name"
            >
              <el-input
                v-model="basic_task_form.name"
                placeholder="请输入任务名称"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="实例类型"
              prop="instance_type"
            >
              <el-select
                v-model="basic_task_form.instance_type"
                placeholder="请选择实例类型"
              >
                <el-option
                  v-for="item in instance_type_list"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="间隔时间"
              prop="interval"
            >
              <el-input-number
                v-model="basic_task_form.interval"
                placeholder="间隔时间"
              >
              </el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="超时时间"
              prop="timeout"
            >
              <el-input-number
                v-model="basic_task_form.timeout"
                placeholder="间隔时间"
              >
              </el-input-number>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="标签过滤"
              prop="labels_name"
            >
              <el-select
                v-model="basic_task_form.labels_name"
                clearable
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
                v-model="basic_task_form.labels_value"
                clearable
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
            <el-form-item v-if="match_label_value_list.length > 0">
              <el-tag
                v-for="(item, index) in match_label_value_list"
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
              label="产品"
              prop="product"
            >
              <el-select
                v-model="basic_task_form.product"
                placeholder="产品"
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
              label="任务类型"
              prop="mode"
            >
              <el-select
                v-model="basic_task_form.mode"
                placeholder="请选择任务类型"
                @change="select_task_mode"
              >
                <el-option
                  v-for="(item, index) in task_mode_list"
                  :key="index"
                  :label="item.name"
                  :value="item.id"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="任务协议"
              prop="scheme"
            >
              <el-radio-group v-model="basic_task_form.scheme">
                <el-radio label="http">http</el-radio>
                <el-radio label="https">https</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="任务端口"
              prop="port"
            >
              <el-input-number
                v-model="basic_task_form.port"
                placeholder="任务端口"
              >
              </el-input-number>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="任务参数"
              prop="args"
            >
              <el-input
                v-if="basic_task_form.task_type === 'basic'"
                v-model="basic_task_form.args"
                placeholder="/exporter/?name=base"
              ></el-input>
              <el-input
                v-else-if="basic_task_form.task_type === 'k8s'"
                v-model="basic_task_form.args"
                placeholder="/federate?match[]={job=~'.*'}"
              ></el-input>
              <el-input
                v-else-if="basic_task_form.task_type === 'port'"
                v-model="basic_task_form.args"
                placeholder="/port/?port=22,80"
              ></el-input>
              <el-input
                v-else-if="basic_task_form.task_type === 'process'"
                v-model="basic_task_form.args"
                placeholder="/process/?list=sshd,sshd"
              ></el-input>
              <el-input
                v-else
                v-model="basic_task_form.args"
                placeholder=""
              ></el-input>
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
          @click="basic_task_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_basic_task"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"
import { getLabelsList } from '@/views/monitor/apis/labels'
import { getProductList } from '@/views/monitor/apis/product'
import { getTaskModeList } from '@/views/monitor/apis/task_mode'
import { getInstanceTypeList } from '@/views/monitor/apis/instance_type'
import ProbeTaskConfig from '@/views/monitor/tasks/probe_task.vue'
import AdvanceTaskConfig from '@/views/monitor/tasks/advance_task.vue'
import BusinessTaskConfig from '@/views/monitor/tasks/business_task.vue'
import { createTargetTask, updateTargetTask, getTargetTaskList } from '@/views/monitor/apis/target_task'

export default {
  name: "MonitorAlertConfig",
  components: {
    Pagination,
    ProbeTaskConfig,
    AdvanceTaskConfig,
    BusinessTaskConfig
  },
  data() {
    return {
      list_query: {
        page: 1,
        limit: 15
      },
      dialog_map: {
        create_basic_task: "新增基础任务",
        update_basic_task: "编辑基础任务"
      },
      dialog_status: "",
      active_tab_name: "basic_task_setting",
      // 基础任务管理--------------------------------------------------
      task_mode_list: [
        { name: "basic", value: "基础任务" },
        { name: "k8s", value: "集群任务" },
        { name: "port", value: "端口任务" },
        { name: "process", value: "进程任务" }
      ],
      basic_task_list: [],
      basic_task_list_total: 0,
      basic_task_dialog: false,
      basic_task_form: {
        id: null,
        mode: null,
        interval: 60,
        timeout: 50,
        match: null,
        scheme: "http",
        port: 2021,
        args: null,
        product: null,
        server: null,
        labels_name: null,
        labels_value: null,
        label_value_list: null
      },
      match_label_value_list: [],
      basic_task_form_rules: {
        name: [{ required: true, message: "该项不能为空", trigger: blur }],
        instance_type: [{ required: true, message: "该项不能为空", trigger: blur }],
        interval: [{ required: true, message: "该项不能为空", trigger: blur }],
        timeout: [{ required: true, message: "该项不能为空", trigger: blur }],
        product: [{ required: true, message: "该项不能为空", trigger: blur }],
        mode: [{ required: true, message: "该项不能为空", trigger: blur }],
        scheme: [{ required: true, message: "该项不能为空", trigger: blur }],
        port: [{ required: true, message: "该项不能为空", trigger: blur }],
        args: [{ required: true, message: "该项不能为空", trigger: blur }]
      },
      instance_type_list: [],
      labels_name_list: [],
      labels_value_list: [],
      product_list: []
    }
  },
  created() {
    this.get_basic_task_list()
  },
  methods: {
    active_tab_click(tab) {
      if (tab.name === "basic_task_setting") {
        this.get_basic_task_list()
      } else if (tab.name === "probe_task_setting") {
        this.$refs.probe_task_setting.get_probe_task_list()
      } else if (tab.name === "business_task_setting") {
        this.$refs.business_task_setting.get_business_task_list()
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
    get_instance_type_list() {
      getInstanceTypeList({ limit: 100 })
        .then(resp => {
          this.instance_type_list = resp.data.results
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    get_task_mode_list() {
      getTaskModeList({ limit: 100 })
        .then(resp => {
          this.task_mode_list = resp.data.results
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
      if (this.basic_task_form.labels_name === "" || this.basic_task_form.labels_value === "") {
        return
      }
      this.match_label_value_list.push({
        name: this.basic_task_form.labels_name,
        value: this.basic_task_form.labels_value
      })
      this.basic_task_form.labels_name = null
      this.basic_task_form.labels_value = null
    },
    delete_labels_condition(tag) {
      this.match_label_value_list.map((item, index) => {
        if (item.value === tag) {
          this.match_label_value_list.splice(index, 1)
        }
      })
    },
    select_task_mode(val) {
      getTaskModeList({ id: val })
        .then(resp => {
          this.basic_task_form.args = resp.data.results[0].args
        })
    },
    // 基础任务管理--------------------------------------------------
    create_basic_task() {
      this.dialog_status = "create_basic_task"
      this.basic_task_dialog = true
      this.get_product_list()
      this.get_task_mode_list()
      this.get_label_name_list()
      this.get_instance_type_list()
    },
    view_basic_task(row) {
      console.log(row.scheme + '://\{\{ instance \}\}:' + row.port + row.args)
    },
    update_basic_task(row) {
      this.dialog_status = "update_basic_task"
      this.basic_task_dialog = true
      this.basic_task_form = Object.assign({}, row)
      this.get_product_list()
      this.get_task_mode_list()
      this.get_label_name_list()
      this.get_instance_type_list()
      this.$nextTick(() => {
        this.match_label_value_list = JSON.parse(row.match)
      })
    },
    delete_basic_task(row) { },
    submit_basic_task() {
      if (this.dialog_status === "create_basic_task") {
        this.$refs.basic_task_formRef.validate((valid) => {
          if (valid) {
            var post_data = Object.assign({}, this.basic_task_form)
            post_data.match = JSON.stringify(this.match_label_value_list)
            console.log(post_data)
            createTargetTask(post_data)
              .then((resp) => {
                this.$message({
                  type: "success",
                  message: "新增成功"
                })
                this.basic_task_dialog = false
                this.get_basic_task_list()
              })
              .catch((err) => {
                this.$message({
                  type: "error",
                  message: err
                })
                this.basic_task_dialog = false
                this.get_basic_task_list()
              })
          }
        })
      } else if (this.dialog_status === "update_basic_task") {
        var update_data = Object.assign({}, this.basic_task_form)
        update_data.match = JSON.stringify(this.match_label_value_list)
        updateTargetTask(update_data.id, update_data)
          .then((resp) => {
            this.$message({
              type: "success",
              message: "更新成功"
            })
            this.basic_task_dialog = false
            this.get_basic_task_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.basic_task_dialog = false
            this.get_basic_task_list()
          })
      }
    },
    get_basic_task_list() {
      getTargetTaskList(this.list_query)
        .then(resp => {
          this.basic_task_list = resp.data.results
          this.basic_task_list_total = resp.data.count
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
