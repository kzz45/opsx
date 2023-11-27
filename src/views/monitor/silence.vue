<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-button
        type="primary"
        size="small"
        icon="el-icon-circle-plus"
        @click="create_silence"
      >新增</el-button>
      <el-table
        ref="silence_list_table_refs"
        :data="silence_list"
        empty-text="啥也没有"
        size="small"
        border
      >
        <el-table-column
          label="维护ID"
          prop="uuid"
        ></el-table-column>
        <el-table-column
          label="维护说明"
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
              :disabled="scoped.row.state == 0"
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
                icon="el-icon-delete"
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
      ></pagination>
    </el-card>
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="silence_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="50%"
    >
      <el-form
        ref="silence_formRef"
        :model="silence_form"
        :rules="silence_form_rules"
        size="small"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="维护产品"
              prop="product"
            >
              <el-select
                v-model="silence_form.product"
                placeholder="请选择产品"
                clearable
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
              label="维护时长"
              prop="duration"
            >
              <el-input-number
                v-model="silence_form.duration"
                placeholder="持续时间"
                style="width: 130px;"
              ></el-input-number>
              <el-select
                v-model="silence_form.unit"
                placeholder="单位"
                clearable
                style="width: 60px; margin-left: 10px;"
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
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="正则"
              prop="is_regex"
            >
              <el-radio-group v-model="silence_form.is_regex">
                <el-radio :label="1">是</el-radio>
                <el-radio :label="0">否</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="生效"
              prop="state"
            >
              <el-radio-group v-model="silence_form.state">
                <el-radio :label="1">是</el-radio>
                <el-radio :label="0">否</el-radio>
              </el-radio-group>
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
                v-model="silence_form.labels_name"
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
                v-model="silence_form.labels_value"
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
              label="描述"
              prop="describe"
            >
              <el-input
                v-model="silence_form.describe"
                type="textarea"
                :autosize="{ minRows: 2, maxRows: 4}"
                placeholder="维护策略的说明"
                style="width: 540px;"
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
          @click="silence_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_silence"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { parseTime } from '@/utils'
import Pagination from "@/components/Pagination"
import { getLabelsList } from '@/views/monitor/apis/labels'
import { getProductList } from '@/views/monitor/apis/product'
import { createSilence, updateSilence, deleteSilence, getSilenceList } from '@/views/monitor/apis/silence'

export default {
  name: "MonitorSilence",
  components: {
    Pagination
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
      dialog_map: {
        create_silence: "新增维护策略",
        update_silence: "编辑维护策略"
      },
      dialog_status: "",
      silence_list: [],
      silence_list_total: 0,
      silence_dialog: false,
      silence_form: {
        id: null,
        uuid: null,
        start: null,
        end: null,
        is_regex: 0,
        state: 1,
        duration: 10,
        unit: 'm',
        match: null,
        product: null,
        describe: null,
        labels_name: null,
        labels_value: null
      },
      silence_form_rules: {
        is_regex: [{ required: true, message: "该项不能为空", trigger: blur }],
        describe: [{ required: true, message: "该项不能为空", trigger: blur }],
        product: [{ required: true, message: "该项不能为空", trigger: blur }],
        duration: [{ required: true, message: "该项不能为空", trigger: blur }]
      },
      label_value_list: [],
      product_list: [],
      labels_name_list: [],
      labels_value_list: []
    }
  },
  created() {
    this.get_silence_list()
  },
  methods: {
    create_silence() {
      this.dialog_status = "create_silence"
      this.silence_dialog = true
      this.silence_form.describe = null
      this.silence_form.product = null
      this.label_value_list = []
      this.get_product_list()
      this.get_label_name_list()
    },
    update_silence(row) {
      this.dialog_status = "update_silence"
      this.silence_dialog = true
      this.silence_form = Object.assign({}, row)
      console.log(this.silence_form)
      if (row.unit === 'h') {
        this.silence_form.duration = row.duration / 3600
      } else if (row.unit === 'm') {
        this.silence_form.duration = row.duration / 60
      } else {
        this.silence_form.duration = row.duration / (3600 * 24)
      }
      this.label_value_list = JSON.parse(this.silence_form.match)
      this.get_product_list()
      this.get_label_name_list()
    },
    delete_silence(row) {
      deleteSilence(row.id)
        .then((resp) => {
          this.$message({
            type: "success",
            message: "删除成功"
          })
          this.get_silence_list()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
          this.get_silence_list()
        })
    },
    submit_silence() {
      if (this.dialog_status === "create_silence") {
        var post_data = Object.assign({}, this.silence_form)
        post_data.start = Math.round(new Date().getTime() / 1000)
        post_data.duration = post_data.duration * (post_data.unit === 'd' ? 86400 : (post_data.unit === 'h' ? 3600 : 60))
        post_data.end = Number(post_data.start) + Number(post_data.duration)
        post_data.match = JSON.stringify(this.label_value_list)
        this.$refs.silence_formRef.validate((valid) => {
          if (valid) {
            createSilence(post_data)
              .then((resp) => {
                this.$message({
                  type: "success",
                  message: "新增成功"
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
        })
      } else if (this.dialog_status === "update_silence") {
        var update_data = Object.assign({}, this.silence_form)
        update_data.start = Math.round(new Date().getTime() / 1000)
        update_data.duration = update_data.duration * (update_data.unit === 'd' ? 86400 : (update_data.unit === 'h' ? 3600 : 60))
        update_data.end = Number(update_data.start) + Number(update_data.duration)
        update_data.match = JSON.stringify(this.label_value_list)
        updateSilence(update_data.id, update_data)
          .then((resp) => {
            this.$message({
              type: "success",
              message: "更新成功"
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
    select_label_value(val) {
      getLabelsList({ name: val }).then(resp => {
        this.labels_value_list = resp.data.results
      })
    },
    add_labels_condition() {
      if (this.silence_form.labels_name === "" || this.silence_form.labels_value === "") {
        return
      }
      this.label_value_list.push({
        name: this.silence_form.labels_name,
        value: this.silence_form.labels_value
      })
      this.silence_form.labels_name = null
      this.silence_form.labels_value = null
    },
    delete_labels_condition(tag) {
      this.label_value_list.map((item, index) => {
        if (item.value === tag) {
          this.label_value_list.splice(index, 1)
        }
      })
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
