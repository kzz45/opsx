<template>
  <div>
    <el-button
      type="primary"
      size="small"
      icon="el-icon-circle-plus"
      @click="create_business_task"
    >新增</el-button>
    <el-table
      ref="business_task_list_table_refs"
      :data="business_task_list"
      empty-text="啥也没有"
      size="small"
      border
    >
      <el-table-column
        label="名称"
        prop="name"
      ></el-table-column>
      <el-table-column
        label="URL"
        prop="url"
      ></el-table-column>
      <el-table-column
        label="产品"
        prop="product__name"
      ></el-table-column>
      <el-table-column
        label="采集点"
        prop="server__name"
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
            @click="update_business_task(scoped.row)"
          ></el-button>
          <el-popconfirm
            title="确定删除吗？"
            confirm-button-text="确定"
            cancel-button-text="不了"
            style="margin-left: 10px"
            @confirm="delete_business_task(scoped.row)"
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
      v-show="business_task_list_total>0"
      :total="business_task_list_total"
      :page.sync="list_query.page"
      :limit.sync="list_query.limit"
      @pagination="get_business_task_list"
    ></pagination>
    <!-- 业务任务管理--------------------------------------------------  -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="business_task_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="50%"
    >
      <el-form
        ref="business_task_formRef"
        :model="business_task_form"
        :rules="business_task_form_rules"
        size="small"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="任务名称"
              prop="name"
            >
              <el-input v-model="business_task_form.name"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="产品"
              prop="product"
            >
              <el-select
                v-model="business_task_form.product"
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
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="间隔时间(s)"
              prop="interval"
            >
              <el-input-number
                v-model="business_task_form.interval"
                placeholder="间隔时间"
              >
              </el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="超时时间(s)"
              prop="timeout"
            >
              <el-input-number
                v-model="business_task_form.timeout"
                placeholder="间隔时间"
              >
              </el-input-number>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="业务URL"
              prop="url"
            >
              <el-input v-model="business_task_form.url"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="挂载节点"
              prop="server"
            >
              <el-select
                v-model="business_task_form.server"
                placeholder="挂载节点"
              >
                <el-option
                  v-for="(item) in server_list"
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
          @click="business_task_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_business_task"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"
import { getProductList } from '@/views/monitor/apis/product'
import { getServerList } from '@/views/monitor/apis/server'
import { getBusinessTaskList, createBusinessTask, updateBusinessTask, deleteBusinessTask } from '@/views/monitor/apis/business_task'

export default {
  name: "BusinessTaskConfig",
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
        create_business_task: "新增业务任务",
        update_business_task: "编辑业务任务"
      },
      dialog_status: "",
      // 业务任务管理--------------------------------------------------
      business_task_list: [],
      business_task_list_total: 0,
      business_task_dialog: false,
      business_task_form: {
        id: null,
        name: null,
        product: null,
        interval: 60,
        timeout: 50,
        url: null,
        server: null
      },
      business_task_form_rules: {
        name: [{ required: true, message: "该项不能为空", trigger: blur }],
        product: [{ required: true, message: "该项不能为空", trigger: blur }],
        interval: [{ required: true, message: "该项不能为空", trigger: blur }],
        timeout: [{ required: true, message: "该项不能为空", trigger: blur }],
        url: [{ required: true, message: "该项不能为空", trigger: blur }],
        server: [{ required: true, message: "该项不能为空", trigger: blur }]
      },
      server_list: [],
      product_list: []
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
    get_server_list() {
      getServerList({ limit: 100 })
        .then(resp => {
          this.server_list = resp.data.results
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 业务任务管理--------------------------------------------------
    create_business_task() {
      this.dialog_status = "create_business_task"
      this.business_task_dialog = true
      this.get_server_list()
      this.get_product_list()
    },
    update_business_task(row) {
      this.dialog_status = "update_business_task"
      this.business_task_dialog = true
      this.business_task_form = Object.assign({}, row)
      this.get_server_list()
      this.get_product_list()
    },
    delete_business_task(row) {
      deleteBusinessTask(row.id)
        .then(resp => {
          this.$message({
            type: "success",
            message: "删除成功"
          })
          this.get_business_task_list()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
          this.get_business_task_list()
        })
    },
    submit_business_task() {
      if (this.dialog_status === "create_business_task") {
        this.$refs.business_task_formRef.validate((valid) => {
          if (valid) {
            createBusinessTask(this.business_task_form)
              .then((resp) => {
                this.$message({
                  type: "success",
                  message: "新增成功"
                })
                this.business_task_dialog = false
                this.get_business_task_list()
              })
              .catch((err) => {
                this.$message({
                  type: "error",
                  message: err
                })
                this.business_task_dialog = false
                this.get_business_task_list()
              })
          }
        })
      } else if (this.dialog_status === "update_business_task") {
        updateBusinessTask(this.business_task_form.id, this.business_task_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新成功"
            })
            this.business_task_dialog = false
            this.get_business_task_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.business_task_dialog = false
            this.get_business_task_list()
          })
      }
    },
    get_business_task_list() {
      getBusinessTaskList(this.list_query)
        .then(resp => {
          this.business_task_list = resp.data.results
          this.business_task_list_total = resp.data.count
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
