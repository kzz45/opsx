<template>
  <div>
    <el-button
      type="primary"
      size="small"
      icon="el-icon-circle-plus"
      @click="create_callback"
    >新增</el-button>
    <el-table
      ref="callback_list_table_refs"
      :data="callback_list"
      empty-text="啥也没有"
      size="small"
      border
    >
      <el-table-column
        label="名称"
        prop="name"
      ></el-table-column>
      <el-table-column
        label="Robot"
        prop="robot"
      ></el-table-column>
      <el-table-column
        label="产品"
        prop="product__name"
      ></el-table-column>
      <el-table-column
        label="厂商"
        prop="factory__name"
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
            @click="update_callback(scoped.row)"
          ></el-button>
          <el-popconfirm
            title="确定删除吗？"
            confirm-button-text="确定"
            cancel-button-text="不了"
            style="margin-left: 10px"
            @confirm="delete_callback(scoped.row)"
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
      v-show="callback_list_total>0"
      :total="callback_list_total"
      :page.sync="list_query.page"
      :limit.sync="list_query.limit"
      @pagination="get_callback_list"
    ></pagination>
    <!-- 告警接收管理--------------------------------------------------  -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="callback_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="50%"
    >
      <el-form
        ref="callback_formRef"
        :model="callback_form"
        :rules="callback_form_rules"
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
                v-model="callback_form.name"
                clearable
                placeholder="名称"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="Robot"
              prop="robot"
            >
              <el-input
                v-model="callback_form.robot"
                clearable
                placeholder="机器人"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="检查周期"
              prop="check_duration"
            >
              <el-input-number
                v-model="callback_form.check_duration"
                placeholder=""
              ></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="静默周期"
              prop="silence_duration"
            >
              <el-input-number
                v-model="callback_form.silence_duration"
                placeholder=""
              ></el-input-number>
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
                v-model="callback_form.product"
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
              label="关联云厂"
              prop="factory"
            >
              <el-select
                v-model="callback_form.factory"
                placeholder="请选择产品"
              >
                <el-option
                  v-for="(item) in factory_list"
                  :key="item.id"
                  :value="item.id"
                  :label="item.name"
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
          @click="callback_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_callback"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"
import { getProductList } from '@/views/monitor/apis/product'
import { getFactoryList } from "@/views/settings/apis/factory"
import { createCallBack, updateCallBack, deleteCallBack, getCallBackList } from '@/views/monitor/apis/callback'

export default {
  name: "CallbackConfig",
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
        create_callback: "新增告警回调",
        update_callback: "编辑告警回调"
      },
      dialog_status: "",
      product_list: [],
      factory_list: [],
      // 告警回调--------------------------------------------------
      callback_list: [],
      callback_list_total: 0,
      callback_dialog: false,
      callback_form: {
        id: null,
        name: null,
        robot: null,
        check_duration: 60,
        silence_duration: 600,
        product: null,
        factory: null
      },
      callback_form_rules: {
        name: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        robot: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        check_duration: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        silence_duration: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        product: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        factory: [{ required: true, message: "该项不能为空", trigger: "blur" }]
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
    get_factory_list() {
      getFactoryList({ limit: 100 })
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
    create_callback() {
      this.dialog_status = "create_callback"
      this.callback_dialog = true
      this.callback_form.name = null
      this.callback_form.robot = null
      this.callback_form.product = null
      this.callback_form.factory = null
      this.get_product_list()
      this.get_factory_list()
    },
    update_callback(row) {
      this.dialog_status = "update_callback"
      this.callback_dialog = true
      this.callback_form = Object.assign({}, row)
      this.get_product_list()
      this.get_factory_list()
    },
    delete_callback(row) {
      deleteCallBack(row.id)
        .then(resp => {
          this.$message({
            type: "success",
            message: "删除成功"
          })
          this.get_callback_list()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
          this.get_callback_list()
        })
    },
    submit_callback() {
      if (this.dialog_status === "create_callback") {
        this.$refs.callback_formRef.validate((valid) => {
          if (valid) {
            createCallBack(this.callback_form)
              .then((resp) => {
                this.$message({
                  type: "success",
                  message: "新增成功"
                })
                this.callback_dialog = false
                this.get_callback_list()
              })
              .catch((err) => {
                this.$message({
                  type: "error",
                  message: err
                })
                this.callback_dialog = false
                this.get_callback_list()
              })
          }
        })
      } else if (this.dialog_status === "update_callback") {
        updateCallBack(this.callback_form.id, this.callback_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新成功"
            })
            this.callback_dialog = false
            this.get_callback_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.callback_dialog = false
            this.get_callback_list()
          })
      }
    },
    get_callback_list() {
      getCallBackList(this.list_query)
        .then(resp => {
          this.callback_list = resp.data.results
          this.callback_list_total = resp.data.count
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
