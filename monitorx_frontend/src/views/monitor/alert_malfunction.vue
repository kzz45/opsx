告警和故障列表页面

<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-tabs
        v-model="active_tab_name"
        @tab-click="active_tab_click"
      >
        <!-- 告警列表-------------------------------------------------- -->
        <el-tab-pane
          label="告警列表"
          name="alert_list"
        >
          <div>
            <el-input
              v-model="search_input_content"
              placeholder="搜点啥"
              size="small"
              clearable
              @keyup.enter.native="search_alert"
            >
              <el-select
                slot="prepend"
                v-model="search_select_input"
                size="small"
              >
                <el-option
                  label="实例"
                  value="endpoint"
                ></el-option>
              </el-select>
              <el-button
                slot="append"
                icon="el-icon-search"
                @click="search_alert"
              ></el-button>
            </el-input>
          </div>
          <el-table
            :data="alert_list"
            empty-text="告警列表 包括当前告警和已经恢复的告警"
            border
            size="small"
          >
            <el-table-column
              label="名称"
              prop="name"
            ></el-table-column>
            <el-table-column
              label="对象"
              prop="instance_name"
            ></el-table-column>
            <el-table-column
              label="消息"
              prop="summary"
            ></el-table-column>
            <el-table-column
              label="等级"
              prop="level"
            >
              <template slot-scope="scoped">
                <el-tag :type="scoped.row.level == 'crit'?'danger':(scoped.row.level == 'warn'?'warning':'success')">{{ scoped.row.level== 'crit'?'严重':(scoped.row.level == 'warn'?'警告':'普通') }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column
              label="开始时间"
              prop="start"
            >
              <template slot-scope="scoped">
                <span>{{ scoped.row.start | parseTime('{y}-{m}-{d} {h}:{i}:{s}') }}</span>
              </template>
            </el-table-column>
            <el-table-column
              label="结束时间"
              prop="end"
            >
              <template slot-scope="scoped">
                <span>{{ scoped.row.end | parseTime('{y}-{m}-{d} {h}:{i}:{s}') }}</span>
              </template>
            </el-table-column>
            <el-table-column
              label="状态"
              prop="state"
            >
              <template slot-scope="scoped">
                <el-tag
                  v-if="scoped.row.state == 'firing'"
                  type="danger"
                >崩盘</el-tag>
                <el-tag
                  v-else
                  type="success"
                >恢复</el-tag>
              </template>
            </el-table-column>
            <el-table-column
              label="产品"
              prop="product__name"
            ></el-table-column>
            <el-table-column
              label="操作"
              width="80px;"
            >
              <template slot-scope="scoped">
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="设置维护"
                  placement="top"
                >
                  <el-button
                    type="warning"
                    icon="el-icon-timer"
                    size="mini"
                    :disabled="scoped.row.state ==='firing'? false: true"
                    @click="create_maintain(scoped.row)"
                  ></el-button>
                </el-tooltip>
              </template>
            </el-table-column>
          </el-table>
          <pagination
            v-show="alert_list_total>0"
            :total="alert_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_alert_list"
          >
          </pagination>
        </el-tab-pane>
        <!-- 事故列表-------------------------------------------------- -->
        <el-tab-pane
          label="事故列表"
          name="adcident_list"
        >
          <div>
            <el-button
              type="primary"
              icon="el-icon-circle-plus-outline"
              size="small"
              @click="create_adcident"
            >
              记录事故
            </el-button>
          </div>
          <el-table
            :data="adcident_list"
            empty-text="记录处理故障"
            border
            size="small"
          >
            <el-table-column
              label="事故标题"
              prop="name"
            ></el-table-column>
            <el-table-column
              label="事故等级"
              prop="level"
            >
              <template slot-scope="scope">
                <el-tag :type="(scope.row.level == '0' || scope.row.level == '1') ? 'danger' : (scope.row.level == '2'?'warning':'success')">
                  {{ scope.row.level == 0? '致命影响': (scope.row.level == 1? 'P'+scope.row.level+': 严重影响': (scope.row.level == 2? 'P'+scope.row.level+': 一般影响':(scope.row.level ==3? 'P'+scope.row.level+': 微弱影响':'P'+scope.row.level+': 既往不咎') )) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column
              label="发生时间"
              prop="start_time"
            >
              <template slot-scope="scoped">
                <span>{{ scoped.row.start_time | parseTime('{y}-{m}-{d} {h}:{i}:{s}') }}</span>
              </template>
            </el-table-column>
            <el-table-column
              label="事故时长"
              prop="duration"
            >
              <template slot-scope="scope">{{ scope.row.duration|format_duration }}</template>
            </el-table-column>
            <el-table-column
              label="处理状态"
              prop="status"
            >
              <template slot-scope="scoped">
                <el-tag :type="(scoped.row.status == '0'? 'danger': (scoped.row.status == '1'? 'warning': 'success'))">
                  {{ scoped.row.status == 0 ?'待解决':(scoped.row.status == 1?'处理中':'已解决') }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column
              label="负责人"
              prop="user__first_name"
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
                  @click="update_adcident(scoped.row)"
                ></el-button>
                <el-popconfirm
                  title="确定删除故障记录吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left: 10px"
                  @confirm="delete_adcident(scoped.row)"
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
            v-show="adcident_list_total>0"
            :total="adcident_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_adcident_list"
          >
          </pagination>
        </el-tab-pane>
        <el-tab-pane
          label="事件列表"
          name="event_list"
        ></el-tab-pane>
      </el-tabs>
    </el-card>
    <!-- 故障记录的Dialog-------------------------------------------------- -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="adcident_dialog"
      width="55%"
    >
      <el-form
        ref="adcident_formRefs"
        :model="adcident_form"
        :rules="adcident_form_rules"
        label-width="100px"
        size="small"
      >
        <el-row :gutter="2">
          <el-col :span="12">
            <el-form-item
              label="故障名称"
              prop="name"
            >
              <el-input
                v-model="adcident_form.name"
                placeholder="请输入此次故障名称"
                style="width: 250px;"
              ></el-input>
            </el-form-item>
            <el-form-item
              label="影响范围"
              prop="scope"
            >
              <el-input
                v-model="adcident_form.scope"
                type="textarea"
                :autosize="{ minRows: 2}"
                placeholder="请输入此次故障影响范围"
                style="width: 250px;"
              ></el-input>
            </el-form-item>
            <el-form-item
              label="负责人"
              prop="people"
            >
              <el-select
                v-model="adcident_form.people"
                clearable
                placeholder="请选择故障负责人"
                style="width: 250px;"
              >
                <el-option
                  v-for="(item, index) in user_list"
                  :key="index"
                  :label="item.first_name"
                  :value="item.id"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item
              label="故障状态"
              prop="status"
            >
              <el-select
                v-model="adcident_form.status"
                placeholder="请选择故障状态"
                style="width: 250px;"
              >
                <el-option
                  v-for="(item, index) in adcident_status_list"
                  :key="index"
                  :label="item.name"
                  :value="item.value"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item
              label="故障等级"
              prop="level"
            >
              <el-select
                v-model="adcident_form.level"
                clearable
                placeholder="请选择故障等级"
                style="width: 250px;"
              >
                <el-option
                  v-for="(item, index) in adcident_level_list"
                  :key="index"
                  :label="item.name"
                  :value="Number(item.value)"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item
              label="故障原因"
              prop="reason"
            >
              <el-input
                v-model="adcident_form.reason"
                type="textarea"
                :autosize="{ minRows: 2}"
                placeholder="请输入故障原因"
                style="width: 250px;"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="发生时间"
              prop="start_time"
            >
              <el-date-picker
                v-model="adcident_form.start_time"
                value-format="timestamp"
                type="datetime"
                placeholder="请填写故障开始时间"
                style="width: 250px;"
              ></el-date-picker>
            </el-form-item>
            <el-form-item
              label="恢复时间"
              prop="recover_time"
            >
              <el-date-picker
                v-model="adcident_form.recover_time"
                value-format="timestamp"
                type="datetime"
                placeholder="请填写故障恢复时间"
                style="width: 250px;"
              ></el-date-picker>
            </el-form-item>
            <el-form-item
              label="解决方式"
              prop="solution"
            >
              <el-input
                v-model="adcident_form.solution"
                type="textarea"
                :autosize="{ minRows: 2}"
                placeholder="请输入故障解决过程方式"
                style="width: 250px;"
              ></el-input>
            </el-form-item>
            <el-form-item
              label="规避方案"
              prop="plan"
            >
              <el-input
                v-model="adcident_form.plan"
                type="textarea"
                :autosize="{ minRows: 6}"
                placeholder="请输入故障后续的规避方案"
                style="width: 250px;"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <div slot="footer">
        <el-button
          size="small"
          @click="adcident_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_adcident"
        >确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { parseTime } from '@/utils'
import Pagination from "@/components/Pagination"
import { getUserList } from '@/api/user'
import { getAlertList } from '@/views/monitor/api/alert'
import { getAdCidentList, createAdCident, updateAdCidentByID, deleteAdCidentByID } from '@/views/monitor/api/adcident'

export default {
  name: "Malfunction",
  components: {
    Pagination
  },
  filters: {
    parseTime(time, cFormat) {
      return parseTime(time, cFormat)
    },
    format_duration(mss) {
      var days = parseInt(mss / (60 * 60 * 24))
      var hours = parseInt((mss % (60 * 60 * 24)) / (60 * 60))
      var minutes = parseInt((mss % (60 * 60)) / 60)
      return days + ' 天 ' + hours + ' 小时 ' + minutes + ' 分钟 '
    }
  },
  data() {
    return {
      list_query: {
        page: 1,
        limit: 15
      },
      dialog_map: {
        create_adcident: "新增事故",
        update_adcident: "编辑事故"
      },
      dialog_status: "",
      adcident_dialog: false,
      active_tab_name: "alert_list",
      search_input_content: "",
      search_select_input: "endpoint",
      alert_list: [],
      alert_list_total: 0,
      alert_state_list: [{ text: "崩盘", value: 'firing' }, { text: "恢复", value: "resolved" }],
      adcident_list: [],
      adcident_list_total: 0,
      adcident_form: {
        id: null
      },
      adcident_form_rules: {
        name: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        start_time: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        status: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        scope: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        level: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        people: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        reason: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        solution: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        plan: [{ required: true, message: "该项不能为空", trigger: "blur" }]
      },
      user_list: [],
      adcident_status_list: [
        {
          name: '待解决',
          value: 0
        }, {
          name: '处理中',
          value: 1
        }, {
          name: '已解决',
          value: 2
        }],
      adcident_level_list: [
        {
          name: 'P0(致命影响)',
          value: '0'
        }, {
          name: 'P1(严重影响)',
          value: '1'
        }, {
          name: 'P2(一般影响)',
          value: '2'
        }, {
          name: 'P3(微弱影响)',
          value: '3'
        }, {
          name: 'P4(既往不咎)',
          value: '4'
        }
      ]
    }
  },
  computed: {
    ...mapGetters(['current_select_product_id', 'current_select_product_name'])
  },
  watch: {
    // 全局组件global-product选择变化时 自动刷新表格
    current_select_product_id: function () {
      this.get_alert_list()
    }
  },
  created() {
    this.get_alert_list()
  },
  methods: {
    active_tab_click(tab) {
      if (tab.name === "alert_list") {
        this.get_alert_list()
      } else if (tab.name === "adcident_list") {
        this.get_user_list()
        this.get_adcident_list()
      }
    },
    // 获取用户列表
    get_user_list() {
      getUserList(this.list_query)
        .then(resp => {
          this.user_list = resp.data.results
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    get_alert_list() {
      const params = "product__id__in"
      const params2 = "state__contains"
      this.list_query[params] = this.current_select_product_id
      this.list_query[params2] = "firing"
      // 如果是选择的产品是全部【0】就展示全部
      if (this.current_select_product_id === 0) {
        this.list_query[params] = ""
      } else {
        this.list_query[params] = this.current_select_product_id
      }
      getAlertList(this.list_query)
        .then(resp => {
          this.alert_list = resp.data.results
          this.alert_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    filter_alert_state(value, row) {
      return row.state === value
    },
    search_alert() {
      var params = this.search_select_input + "__contains"
      this.list_query[params] = this.search_input_content
      this.get_alert_list()
    },
    get_adcident_list() {
      getAdCidentList(this.list_query)
        .then(resp => {
          this.adcident_list = resp.data.results
          this.adcident_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    create_maintain() { },
    create_adcident() {
      this.adcident_dialog = true
      this.dialog_status = "create_adcident"
      if (this.$refs.adcident_formRefs) {
        this.$refs.adcident_formRefs.resetFields()
      }
    },
    update_adcident(row) {
      this.adcident_dialog = true
      this.dialog_status = "update_adcident"
      this.adcident_form = Object.assign({}, row)
      this.adcident_form.start_time = this.adcident_form.start_time * 1000
      this.adcident_form.recover_time = this.adcident_form.recover_time * 1000
      console.log(this.adcident_form, '===')
    },
    submit_adcident() {
      if (this.dialog_status === "create_adcident") {
        var post_data = Object.assign({}, this.adcident_form)
        post_data.start_time = post_data.start_time.valueOf() / 1000
        post_data.recover_time = post_data.recover_time.valueOf() / 1000
        createAdCident(post_data)
          .then(resp => {
            this.$message({
              type: "success",
              message: "新增故障记录成功"
            })
            this.adcident_dialog = false
            this.get_adcident_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.adcident_dialog = false
            this.get_adcident_list()
          })
      } else if (this.dialog_status === "update_adcident") {
        var update_data = Object.assign({}, this.adcident_form)
        update_data.start_time = update_data.start_time.valueOf() / 1000
        update_data.recover_time = update_data.recover_time.valueOf() / 1000
        console.log(update_data, '===')
        updateAdCidentByID(update_data.id, update_data)
          .then(resp => {
            this.$message({
              type: "success",
              message: "更新故障记录成功"
            })
            this.adcident_dialog = false
            this.get_adcident_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.adcident_dialog = false
            this.get_adcident_list()
          })
      }
    },
    delete_adcident(row) {
      deleteAdCidentByID(row.id)
        .then(resp => {
          this.$message({
            type: "success",
            message: "删除故障记录成功"
          })
          this.get_adcident_list()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
          this.get_adcident_list()
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
.el-table {
  width: 100%;
  margin-top: 10px;
}
.el-select {
  width: 120px;
}
.el-input {
  width: 400px;
}
.el-button {
  vertical-align: top;
}
.el-dropdown {
  vertical-align: top;
}
</style>
