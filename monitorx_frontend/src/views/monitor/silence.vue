告警维护页面

<template>
  <div class="app-container">
    <el-card class="box-card">
      <div>
        <el-button
          type="primary"
          icon="el-icon-circle-plus-outline"
          size="small"
          @click="create_silence"
        >新增策略</el-button>
        <el-button
          type="info"
          size="small"
          :icon="showAll?'el-icon-arrow-up':'el-icon-arrow-down'"
          @click="show_more"
        >
          {{ showAll ? "收起搜索": "更多搜索" }}
        </el-button>
        <el-form
          :model="search_item"
          label-width="100px;"
          style="margin-top: 10px;"
        >
          <el-collapse-transition>
            <div v-show="showAll">
              <el-row>
                <el-col :span="6">
                  <el-form-item label="策略状态">
                    <el-select
                      v-model="search_item.state"
                      clearable
                      placeholder="请选择状态"
                      size="small"
                      @change="change_state($event)"
                    >
                      <el-option
                        label="生效"
                        :value="1"
                      ></el-option>
                      <el-option
                        label="失效"
                        :value="0"
                      ></el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="6">
                  <el-form-item label="维护人">
                    <el-select
                      v-model="search_item.user"
                      placeholder="请选择维护人"
                      clearable
                      size="small"
                      @change="change_user($event)"
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
                <el-col :span="6">
                  <el-form-item label="维护时间">
                    <el-date-picker
                      v-model="search_item.silence_time"
                      type="datetimerange"
                      value-format="timestamp"
                      range-separator="至"
                      start-placeholder="开始时间"
                      end-placeholder="结束时间"
                      align="right"
                      size="small"
                      style="width: 200px;"
                    >
                    </el-date-picker>
                  </el-form-item>
                </el-col>
                <el-col :span="6">
                  <el-form-item label="来源">
                    <el-select
                      v-model="search_item.source"
                      placeholder="请选择来源"
                      clearable
                      size="small"
                      @change="change_source($event)"
                    >
                      <el-option
                        v-for="(item, index) in source_list"
                        :key="index"
                        :label="item.name"
                        :value="item.id"
                      ></el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>
            </div>
          </el-collapse-transition>
        </el-form>
      </div>
      <div>
        <el-table
          :data="silence_list"
          size="small"
          empty-text="针对告警的维护策略"
          border
        >
          <el-table-column
            label="策略"
            prop="describe"
          ></el-table-column>
          <el-table-column
            label="维护时长"
            prop="duration"
          >
            <template slot-scope="scoped">{{ scoped.row.duration | formatDuring }}</template>
          </el-table-column>
          <el-table-column
            label="到期时间"
            prop="end"
          >
            <template slot-scope="scoped">{{ scoped.row.end | parseTime('{y}-{m}-{d} {h}:{i}:{s}') }}</template>
          </el-table-column>
          <el-table-column
            label="状态"
            prop="state"
          >
            <template slot-scope="scoped">
              <el-tag :type="scoped.row.state == 1? 'success' : 'info'">
                {{ scoped.row.state == 1? '生效' : '失效' }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column
            label="来源"
            prop="source"
          >
            <template slot-scope="scope">
              {{ scope.row.source == 0 ? "自定义" : "快速维护" }}
            </template>
          </el-table-column>
          <el-table-column
            label="产品"
            prop="product__name"
          ></el-table-column>
          <el-table-column
            label="维护人"
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
                @click="update_silence(scoped.row)"
              ></el-button>
              <el-popconfirm
                title="确定解除维护吗？"
                confirm-button-text="确定"
                cancel-button-text="不了"
                style="margin-left: 10px"
                @confirm="delete_silence(scoped.row)"
                @cancel="cancel_delete"
              >
                <el-button
                  slot="reference"
                  type="danger"
                  icon="el-icon-setting"
                  size="mini"
                ></el-button>
              </el-popconfirm>
            </template>
          </el-table-column>
        </el-table>
        <pagination
          v-show="silence_list_total>0"
          :total="silence_list_total"
          :page.sync="list_query.page"
          :limit.sync="list_query.limit"
          @pagination="get_silence_list"
        >
        </pagination>
      </div>
    </el-card>
    <!-- 维护策略的Dialog -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="silence_dialog"
      width="50%"
    >
      <el-form
        ref="silence_formRefs"
        :model="silence_form"
        :rules="silence_form_rules"
        label-width="100px"
        size="small"
      >
        <el-form-item
          label="维护范围"
          prop="target"
        >
          <el-radio-group v-model="silence_form.target">
            <el-radio :label="0">局部</el-radio>
            <el-radio
              :label="1"
              disabled
            >全局</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item
          v-if="silence_form.target === 0? true: false"
          label="产品"
          prop="product"
        >
          <el-select
            v-model="silence_form.product"
            placeholder="请选择产品"
            clearable
            size="small"
            style="width: 300px;"
          >
            <el-option
              v-for="(item) in product_list"
              :key="item.id"
              :value="item.id"
              :label="item.name"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          label="维护时长"
          prop="duration"
        >
          <el-input-number
            v-model="silence_form.duration"
            placeholder="请输入持续时间"
            style="width: 200px;"
          ></el-input-number>
          <el-select
            v-model="silence_form.unit"
            placeholder="单位"
            clearable
            style="width: 90px; margin-left: 10px;"
          >
            <el-option
              label="分"
              value="m"
            ></el-option>
            <el-option
              label="时"
              value="h"
            ></el-option>
            <el-option
              label="天"
              value="d"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          label="描述"
          prop="describe"
        >
          <el-input
            v-model="silence_form.describe"
            type="textarea"
            :autosize="{ minRows: 2, maxRows: 4}"
            placeholder="维护策略的说明"
            style="width: 300px;"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="标签"
          prop="lables"
        >
          <labelHandler ref="label_handler"></labelHandler>
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button
          size="small"
          @click="silence_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_silence"
        >确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { parseTime } from '@/utils'
import { getUserList } from '@/api/user'
import Pagination from "@/components/Pagination"
import labelHandler from '@/views/monitor/components/label_handler.vue'
import { getProductList } from '@/api/product'
import { getSilenceList, createSilence, updateSilenceByID } from '@/views/monitor/api/silence'

export default {
  name: "Silence",
  components: {
    Pagination,
    labelHandler
  },
  filters: {
    formatDuring(mss) {
      if (mss) {
        var days = parseInt(mss / (60 * 60 * 24))
        var hours = parseInt((mss % (60 * 60 * 24)) / (60 * 60))
        var minutes = parseInt((mss % (60 * 60)) / 60)
        return days + " 天 " + hours + " 小时 " + minutes + " 分钟 "
      }
    },
    parseTime(time, cFormat) {
      return parseTime(time, cFormat)
    }
  },
  data() {
    return {
      list_query: {
        page: 1,
        limit: 15
      },
      search_item: {},
      showAll: false,
      silence_time: null,
      silence_list: [],
      silence_list_total: 0,
      dialog_map: {
        create_silence: "新增维护策略",
        update_silence: "编辑维护策略"
      },
      dialog_status: "",
      silence_dialog: false,
      silence_form: {
        target: 0,
        product: null,
        duration: null,
        unit: 'm',
        describe: '',
        state: 1,
        user: this.$store.getters.user_id
      },
      silence_form_rules: {
        target: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        product: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        duration: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        describe: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        lables: [{ required: true, message: "该项不能为空", trigger: "blur" }]
      },
      product_list: [],
      user_list: [],
      source_list: [{ name: "自定义", id: 0 }, { name: "快速维护", id: 1 }]
    }
  },
  computed: {
    ...mapGetters(['user_id'])
  },
  created() {
    this.get_user_list()
    this.get_product_list()
    this.get_silence_list()
  },
  methods: {
    show_more() {
      this.showAll = !this.showAll
    },
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
    create_silence() {
      this.silence_dialog = true
      this.dialog_status = "create_silence"
      if (this.$refs.silence_formRefs) {
        this.$refs.silence_formRefs.resetFields()
      }
    },
    update_silence(row) {
      this.silence_dialog = true
      this.dialog_status = "update_silence"
      this.silence_form = Object.assign({}, row)
      this.silence_form.target = 0
      this.silence_form.unit = row.unit
      if (row.unit === 'h') {
        this.silence_form.duration = row.duration / 3600
      } else if (row.unit === 'm') {
        this.silence_form.duration = row.duration / 60
      } else {
        this.silence_form.duration = row.duration / (3600 * 24)
      }
      this.$nextTick(() => {
        this.$refs.label_handler.label_value_list = JSON.parse(row.match)
      })
    },
    submit_silence() {
      if (this.dialog_status === "create_silence") {
        var post_data = Object.assign({}, this.silence_form)
        post_data.start = Math.round(new Date().getTime() / 1000)
        post_data.duration = post_data.duration * (post_data.unit === 'd' ? 86400 : (post_data.unit === 'h' ? 3600 : 60))
        post_data.end = Number(post_data.start) + Number(post_data.duration)
        post_data.match = JSON.stringify(this.$refs.label_handler.label_value_list)
        createSilence(post_data)
          .then(resp => {
            this.$message({
              type: "success",
              message: "新增维护策略成功"
            })
            this.silence_dialog = false
            this.get_silence_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.silence_dialog = false
            this.get_silence_list()
          })
      } else if (this.dialog_status === "update_silence") {
        var update_data = Object.assign({}, this.silence_form)
        update_data.state = 1
        update_data.start = Math.round(new Date().getTime() / 1000)
        update_data.duration = update_data.duration * (update_data.unit === 'd' ? 86400 : (update_data.unit === 'h' ? 3600 : 60))
        update_data.end = Number(update_data.start) + Number(update_data.duration)
        var update_param = this.$refs.label_handler.label_value_list
        update_data.match = JSON.stringify(update_param)
        // console.log(update_data, '=====')
        updateSilenceByID(update_data.id, update_data)
          .then(resp => {
            this.$message({
              type: "success",
              message: "更新维护策略成功"
            })
            this.silence_dialog = false
            this.get_silence_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.silence_dialog = false
            this.get_silence_list()
          })
      }
    },
    delete_silence(row) {
      var data = Object.assign({}, this.silence_form, row)
      if (data.state === 0) {
        this.$message({
          type: "warning",
          message: "当前的维护策略已经解除失效了"
        })
      } else {
        updateSilenceByID(row.id, { state: 0 })
          .then(resp => {
            this.$message({
              type: "success",
              message: "解除维护策略成功"
            })
            this.get_silence_list()
          }
          )
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.get_silence_list()
          })
      }
    },
    cancel_delete() {
      this.$message({
        type: "warning",
        message: "你考虑的很全面"
      })
    },
    get_silence_list() {
      getSilenceList(this.list_query)
        .then(resp => {
          this.silence_list = resp.data.results
          this.silence_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    get_product_list() {
      getProductList(this.list_query)
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
    change_user(val) {
      // console.log(val, 'xxxxxx')
      this.list_query.user__id = val
      this.get_silence_list(this.list_query)
    },
    change_source(val) {
      this.list_query.source = val
      this.get_silence_list(this.list_query)
    },
    change_state(val) {
      this.list_query.state = val
      // console.log('.......', val)
      this.get_silence_list(this.list_query)
    }
  }
}
</script>

<style scoped>
.el-table {
  width: 100%;
  margin-top: 10px;
}
.el-input {
  width: 300px;
}
.el-button {
  vertical-align: top;
}
</style>
