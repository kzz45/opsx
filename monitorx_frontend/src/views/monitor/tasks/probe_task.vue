<template>
  <div>
    <el-button
      type="primary"
      size="small"
      icon="el-icon-circle-plus"
      @click="create_probe_task"
    >新增</el-button>
    <el-table
      ref="probe_task_list_table_refs"
      :data="probe_task_list"
      empty-text="啥也没有"
      size="small"
      border
    >
      <el-table-column
        label="名称"
        prop="name"
      ></el-table-column>
      <el-table-column
        label="探测对象"
        prop="target"
      ></el-table-column>
      <el-table-column
        label="探测类型"
        prop="mode"
      ></el-table-column>
      <el-table-column
        label="产品"
        prop="product__name"
      ></el-table-column>
      <el-table-column
        label="探测点"
        prop="probe__name"
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
            @click="update_probe_task(scoped.row)"
          ></el-button>
          <el-popconfirm
            title="确定删除吗？"
            confirm-button-text="确定"
            cancel-button-text="不了"
            style="margin-left: 10px"
            @confirm="delete_probe_task(scoped.row)"
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
      v-show="probe_task_list_total>0"
      :total="probe_task_list_total"
      :page.sync="list_query.page"
      :limit.sync="list_query.limit"
      @pagination="get_probe_task_list"
    ></pagination>
    <!-- 探测任务管理--------------------------------------------------  -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="probe_task_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="50%"
    >
      <el-form
        ref="probe_task_formRef"
        :model="probe_task_form"
        :rules="probe_task_form_rules"
        size="small"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="任务名称"
              prop="name"
            >
              <el-input v-model="probe_task_form.name"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="产品"
              prop="product"
            >
              <el-select
                v-model="probe_task_form.product"
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
                v-model="probe_task_form.interval"
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
                v-model="probe_task_form.timeout"
                placeholder="间隔时间"
              >
              </el-input-number>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="探测对象"
              prop="target"
            >
              <el-input v-model="probe_task_form.target"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="探测节点"
              prop="probe"
            >
              <el-select
                v-model="probe_task_form.probe"
                placeholder="挂载节点"
              >
                <el-option
                  v-for="(item) in probe_list"
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
          @click="probe_task_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_probe_task"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"
import { getProductList } from '@/views/monitor/apis/product'
import { getProbeList } from '@/views/monitor/apis/probe'
import { getProbeTaskList, createProbeTask, updateProbeTask, deleteProbeTask } from '@/views/monitor/apis/probe_task'

export default {
  name: "ProbeTaskConfig",
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
        create_probe_task: "新增探测任务",
        update_probe_task: "编辑探测任务"
      },
      dialog_status: "",
      // 探测任务管理--------------------------------------------------
      probe_task_list: [],
      probe_task_list_total: 0,
      probe_task_dialog: false,
      probe_task_form: {
        id: null,
        name: null,
        product: null,
        interval: 60,
        timeout: 50,
        url: null,
        server: null
      },
      probe_task_form_rules: {
        name: [{ required: true, message: "该项不能为空", trigger: blur }],
        product: [{ required: true, message: "该项不能为空", trigger: blur }],
        interval: [{ required: true, message: "该项不能为空", trigger: blur }],
        timeout: [{ required: true, message: "该项不能为空", trigger: blur }],
        target: [{ required: true, message: "该项不能为空", trigger: blur }],
        probe: [{ required: true, message: "该项不能为空", trigger: blur }]
      },
      probe_list: [],
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
    get_probe_list() {
      getProbeList({ limit: 100 })
        .then(resp => {
          this.probe_list = resp.data.results
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 探测任务管理--------------------------------------------------
    create_probe_task() {
      this.dialog_status = "create_probe_task"
      this.probe_task_dialog = true
      this.get_probe_list()
      this.get_product_list()
    },
    update_probe_task(row) {
      this.dialog_status = "update_probe_task"
      this.probe_task_dialog = true
      this.probe_task_form = Object.assign({}, row)
      this.get_probe_list()
      this.get_product_list()
    },
    delete_probe_task(row) {
      deleteProbeTask(row.id)
        .then(resp => {
          this.$message({
            type: "success",
            message: "删除成功"
          })
          this.get_probe_task_list()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
          this.get_probe_task_list()
        })
    },
    submit_probe_task() {
      if (this.dialog_status === "create_probe_task") {
        this.$refs.probe_task_formRef.validate((valid) => {
          if (valid) {
            createProbeTask(this.probe_task_form)
              .then((resp) => {
                this.$message({
                  type: "success",
                  message: "新增成功"
                })
                this.probe_task_dialog = false
                this.get_probe_task_list()
              })
              .catch((err) => {
                this.$message({
                  type: "error",
                  message: err
                })
                this.probe_task_dialog = false
                this.get_probe_task_list()
              })
          }
        })
      } else if (this.dialog_status === "update_probe_task") {
        updateProbeTask(this.probe_task_form.id, this.probe_task_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新成功"
            })
            this.probe_task_dialog = false
            this.get_probe_task_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.probe_task_dialog = false
            this.get_probe_task_list()
          })
      }
    },
    get_probe_task_list() {
      getProbeTaskList(this.list_query)
        .then(resp => {
          this.probe_task_list = resp.data.results
          this.probe_task_list_total = resp.data.count
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
