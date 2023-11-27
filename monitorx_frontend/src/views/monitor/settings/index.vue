<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-tabs
        v-model="active_tab_name"
        @tab-click="active_tab_click"
      >
        <!-- 采集节点管理--------------------------------------------------  -->
        <el-tab-pane
          label="采集节点"
          name="server_setting"
        >
          <el-button
            type="primary"
            size="small"
            icon="el-icon-circle-plus"
            @click="create_server"
          >新增</el-button>
          <el-table
            ref="server_list_table_refs"
            :data="server_list"
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
              label="标识"
              prop="code"
            >
            </el-table-column>
            <el-table-column
              label="地址"
              prop="ipaddr"
            >
            </el-table-column>
            <el-table-column
              label="唯一ID"
              prop="uuid"
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
                  @click="update_server(scoped.row)"
                ></el-button>
                <el-popconfirm
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left: 10px"
                  @confirm="delete_server(scoped.row)"
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
            v-show="server_list_total>0"
            :total="server_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_server_list"
          ></pagination>
        </el-tab-pane>
        <!-- 探测节点管理--------------------------------------------------  -->
        <el-tab-pane
          label="探测节点"
          name="probe_setting"
        >
          <probe-setting ref="probe_setting"></probe-setting>
        </el-tab-pane>
        <!-- 告警模板--------------------------------------------------  -->
        <el-tab-pane
          v-if="checkPermission(['admin'])"
          label="模板管理"
          name="tmpl_setting"
        >
          <TmplConfig ref="tmpl_setting"></TmplConfig>
        </el-tab-pane>
        <!-- 标签管理--------------------------------------------------  -->
        <el-tab-pane
          label="标签管理"
          name="labels_setting"
        >
          <labels-setting ref="labels_setting"></labels-setting>
        </el-tab-pane>
        <!-- 任务模式管理--------------------------------------------------  -->
        <el-tab-pane
          v-if="checkPermission(['admin'])"
          label="任务模式"
          name="task_mode_setting"
        >
          <TaskModeSetting ref="task_mode_setting"></TaskModeSetting>
        </el-tab-pane>
        <!-- 实例类型--------------------------------------------------  -->
        <el-tab-pane
          label="实例类型"
          name="instance_type_setting"
        >
          <InstanceTypeSetting ref="instance_type_setting"></InstanceTypeSetting>
        </el-tab-pane>
        <!-- 规则类型--------------------------------------------------  -->
        <el-tab-pane
          label="规则类型"
          name="alert_rule_type_setting"
        >
          <AlertRuleTypeSetting ref="alert_rule_type_setting"></AlertRuleTypeSetting>
        </el-tab-pane>
        <!-- 告警等级--------------------------------------------------  -->
        <el-tab-pane
          label="告警等级"
          name="alert_rule_level_setting"
        >
          <AlertRuleLevelSetting ref="alert_rule_level_setting"></AlertRuleLevelSetting>
        </el-tab-pane>
        <!-- 大盘管理--------------------------------------------------  -->
        <el-tab-pane
          v-if="checkPermission(['admin'])"
          label="大盘管理"
          name="dashboard_setting"
        >
          <DashboardSetting ref="dashboard_setting"></DashboardSetting>
        </el-tab-pane>
      </el-tabs>
    </el-card>
    <!-- 采集节点管理--------------------------------------------------  -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="server_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="50%"
    >
      <el-form
        ref="server_formRef"
        :model="server_form"
        :rules="server_form_rules"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="名称"
              prop="name"
            >
              <el-input
                v-model="server_form.name"
                size="small"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="标识"
              prop="code"
            >
              <el-input
                v-model="server_form.code"
                size="small"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="唯一ID"
              prop="uuid"
            >
              <el-input
                v-model="server_form.uuid"
                size="small"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="地址"
              prop="ipaddr"
            >
              <el-input
                v-model="server_form.ipaddr"
                size="small"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="告警地址"
              prop="alertmanager"
            >
              <el-input
                v-model="server_form.alertmanager"
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
          @click="server_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_server"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"
import checkPermission from '@/utils/permission'
import ProbeSetting from '@/views/monitor/settings/probe.vue'
import LabelsSetting from '@/views/monitor/settings/labels.vue'
import TmplConfig from '@/views/monitor/settings/tmpl.vue'
import TaskModeSetting from '@/views/monitor/settings/task_mode.vue'
import DashboardSetting from '@/views/monitor/settings/dashboard.vue'
import InstanceTypeSetting from '@/views/monitor/settings/instance_type.vue'
import AlertRuleTypeSetting from '@/views/monitor/settings/alert_rule_type.vue'
import AlertRuleLevelSetting from '@/views/monitor/settings/alert_rule_level.vue'
import { createServer, updateServer, deleteServer, getServerList } from '@/views/monitor/apis/server'

export default {
  name: "MonitorSettings",
  components: {
    Pagination,
    TmplConfig,
    ProbeSetting,
    LabelsSetting,
    TaskModeSetting,
    DashboardSetting,
    InstanceTypeSetting,
    AlertRuleTypeSetting,
    AlertRuleLevelSetting
  },
  data() {
    return {
      list_query: {
        page: 1,
        limit: 15
      },
      active_tab_name: "server_setting",
      dialog_map: {
        create_server: "新增采集点",
        update_server: "编辑采集点"
      },
      dialog_status: "",
      // 采集节点管理--------------------------------------------------
      server_list: [],
      server_list_total: 0,
      server_dialog: false,
      server_form: {
        id: null,
        name: null,
        desc: null,
        code: null,
        uuid: null,
        ipaddr: null,
        alertmanager: null
      },
      server_form_rules: {
        name: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        desc: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        code: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        uuid: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        ipaddr: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        alertmanager: [{ required: true, message: "该项不能为空", trigger: "blur" }]
      }
    }
  },
  created() {
    this.get_server_list()
  },
  methods: {
    checkPermission,
    active_tab_click(tab) {
      if (tab.name === "server_setting") {
        this.get_server_list()
      } else if (tab.name === "labels_setting") {
        this.$refs.labels_setting.get_labels_list()
      } else if (tab.name === "probe_setting") {
        this.$refs.probe_setting.get_probe_list()
      } else if (tab.name === "tmpl_setting") {
        this.$refs.tmpl_setting.get_tmpl_list()
      } else if (tab.name === "task_mode_setting") {
        this.$refs.task_mode_setting.get_task_mode_list()
      } else if (tab.name === "dashboard_setting") {
        this.$refs.dashboard_setting.get_dashboard_list()
      } else if (tab.name === "instance_type_setting") {
        this.$refs.instance_type_setting.get_instance_type_list()
      } else if (tab.name === "alert_rule_type_setting") {
        this.$refs.alert_rule_type_setting.get_alert_rule_type_list()
      } else if (tab.name === "alert_rule_level_setting") {
        this.$refs.alert_rule_level_setting.get_alert_rule_level_list()
      }
    },
    // 采集节点管理--------------------------------------------------
    create_server() {
      this.dialog_status = "create_server"
      this.server_dialog = true
      this.server_form.name = null
      this.server_form.desc = null
      this.server_form.uuid = null
      this.server_form.code = null
      this.server_form.ipaddr = null
    },
    update_server(row) {
      this.dialog_status = "update_server"
      this.server_dialog = true
      this.server_form = Object.assign({}, row)
    },
    delete_server(row) {
      deleteServer(row.id)
        .then(resp => {
          this.$message({
            type: "success",
            message: "删除成功"
          })
          this.get_server_list()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
          this.get_server_list()
        })
    },
    submit_server() {
      if (this.dialog_status === "create_server") {
        this.$refs.server_formRef.validate((valid) => {
          if (valid) {
            createServer(this.server_form)
              .then((resp) => {
                this.$message({
                  type: "success",
                  message: "新增成功"
                })
                this.server_dialog = false
                this.get_server_list()
              })
              .catch((err) => {
                this.$message({
                  type: "error",
                  message: err
                })
                this.server_dialog = false
                this.get_server_list()
              })
          }
        })
      } else if (this.dialog_status === "update_server") {
        updateServer(this.server_form.id, this.server_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新成功"
            })
            this.server_dialog = false
            this.get_server_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.server_dialog = false
            this.get_server_list()
          })
      }
    },
    get_server_list() {
      getServerList(this.list_query)
        .then(resp => {
          this.server_list = resp.data.results
          this.server_list_total = resp.data.count
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
