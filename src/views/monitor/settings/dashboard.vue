<template>
  <div>
    <el-button
      type="primary"
      size="small"
      icon="el-icon-circle-plus"
      @click="create_dashboard"
    >新增</el-button>
    <el-table
      ref="dashboard_list_table_refs"
      :data="dashboard_list"
      empty-text="啥也没有"
      size="small"
      border
    >
      <el-table-column
        label="名称"
        prop="name"
      ></el-table-column>
      <el-table-column
        label="描述"
        prop="desc"
      ></el-table-column>
      <el-table-column
        label="地址"
        prop="addr"
      ></el-table-column>
      <el-table-column
        label="所属产品"
        prop="product__name"
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
            @click="update_dashboard(scoped.row)"
          ></el-button>
          <el-popconfirm
            title="确定删除吗？"
            confirm-button-text="确定"
            cancel-button-text="不了"
            style="margin-left: 10px"
            @confirm="delete_dashboard(scoped.row)"
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
      v-show="dashboard_list_total>0"
      :total="dashboard_list_total"
      :page.sync="list_query.page"
      :limit.sync="list_query.limit"
      @pagination="get_dashboard_list"
    ></pagination>
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="dashboard_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="50%"
    >
      <el-form
        ref="dashboard_formRefs"
        :model="dashboard_form"
        :rules="dashboard_form_rules"
        label-width="100px"
        size="small"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="名称"
              prop="name"
            >
              <el-input
                v-model="dashboard_form.name"
                size="small"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="描述"
              prop="desc"
            >
              <el-input
                v-model="dashboard_form.desc"
                size="small"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="地址"
              prop="addr"
            >
              <el-input
                v-model="dashboard_form.addr"
                size="small"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="关联产品"
              prop="product"
            >
              <el-select
                v-model="dashboard_form.product"
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
        </el-row>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="dashboard_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_dashboard"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"
import { getProductList } from '@/views/monitor/apis/product'
import { getDashboardList, createDashboard, updateDashboard, deleteDashboard } from '@/views/monitor/apis/dashboard'

export default {
  name: "DashboardSetting",
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
        create_dashboard: "新增大盘",
        update_dashboard: "编辑大盘"
      },
      dialog_status: "",
      product_list: [],
      // 大盘管理--------------------------------------------------
      dashboard_list: [],
      dashboard_list_total: 0,
      dashboard_dialog: false,
      dashboard_form: {
        id: null,
        name: null,
        desc: null,
        addr: null,
        product: null
      },
      dashboard_form_rules: {
        name: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        desc: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        addr: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        product: [{ required: true, message: "该项不能为空", trigger: "blur" }]
      }
    }
  },
  methods: {
    create_dashboard() {
      this.dialog_status = "create_dashboard"
      this.dashboard_dialog = true
      this.dashboard_form.name = null
      this.dashboard_form.desc = null
      this.dashboard_form.addr = null
      this.dashboard_form.product = null
      this.get_product_list()
    },
    update_dashboard(row) {
      this.dialog_status = "update_dashboard"
      this.dashboard_dialog = true
      this.dashboard_form = Object.assign({}, row)
      this.get_product_list()
    },
    delete_dashboard(row) {
      deleteDashboard(row.id)
        .then((resp) => {
          this.$message({
            type: "success",
            message: "删除成功"
          })
          this.get_dashboard_list()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
          this.get_dashboard_list()
        })
    },
    submit_dashboard() {
      if (this.dialog_status === "create_dashboard") {
        this.$refs.dashboard_formRefs.validate((valid) => {
          if (valid) {
            createDashboard(this.dashboard_form)
              .then((resp) => {
                this.$message({
                  type: "success",
                  message: "新增成功"
                })
                this.dashboard_dialog = false
                this.get_dashboard_list()
              })
              .catch((err) => {
                this.$message({
                  type: "error",
                  message: err
                })
                this.dashboard_dialog = false
                this.get_dashboard_list()
              })
          }
        })
      } else if (this.dialog_status === "update_dashboard") {
        updateDashboard(this.dashboard_form.id, this.dashboard_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新成功"
            })
            this.dashboard_dialog = false
            this.get_dashboard_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.dashboard_dialog = false
            this.get_dashboard_list()
          })
      }
    },
    get_dashboard_list() {
      getDashboardList(this.list_query)
        .then(resp => {
          this.dashboard_list = resp.data.results
          this.dashboard_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
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
