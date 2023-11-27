<template>
  <div>
    <el-row style="margin-bottom: 10px;">
      <el-col :span="6">
        <el-select
          v-model="product_select_input"
          size="small"
          placeholder="按产品搜索"
          style="width: 200px;"
          clearable
          filterable
        >
          <el-option
            v-for="(item, index) in product_list"
            :key="index"
            :label="item.name+':'+item.code"
            :value="item.code"
          ></el-option>
        </el-select>
        <el-button
          type="primary"
          size="small"
          icon="el-icon-search"
          style="margin-left: 10px;"
          @click="search_product"
        ></el-button>
      </el-col>
      <el-col :span="6">
        <el-select
          v-model="project_select_input"
          placeholder="按项目搜索"
          size="small"
          style="width: 200px;"
          clearable
          filterable
        >
          <el-option
            v-for="(item, index) in project_list"
            :key="index"
            :label="item.desc"
            :value="item.name"
          ></el-option>
        </el-select>
        <el-button
          type="primary"
          size="small"
          style="margin-left: 10px;"
          icon="el-icon-search"
          @click="search_project"
        ></el-button>
      </el-col>
      <el-col :span="6">
        <el-date-picker
          v-model="year_month"
          type="month"
          placeholder="按月份搜索"
          size="small"
          value-format="yyyy-MM"
        >
        </el-date-picker>
        <el-button
          icon="el-icon-search"
          size="small"
          type="primary"
          style="margin-left: 10px;"
          @click="search_month"
        ></el-button>
      </el-col>
      <el-col :span="6">
        <el-tooltip
          class="item"
          effect="dark"
          content="批量分配项目"
          placement="top"
        >
          <el-button
            icon="el-icon-check"
            type="primary"
            size="small"
            @click="batch_project"
          >
          </el-button>
        </el-tooltip>
        <el-tooltip
          class="item"
          effect="dark"
          content="导出Excel"
          placement="top"
        >
          <el-button
            :loading="downloadLoading"
            icon="el-icon-document"
            type="danger"
            size="small"
            style="margin-left: 10px;"
            @click="download_all"
          ></el-button>
        </el-tooltip>
      </el-col>
    </el-row>

    <el-table
      ref="bill_list_table_refs"
      :data="bill_list"
      empty-text="啥也没有"
      size="small"
      border
      @selection-change="handleSelectionChange"
    >
      <el-table-column
        type="selection"
        width="55"
      ></el-table-column>
      <el-table-column
        label="实例名称"
        prop="instance_name"
      ></el-table-column>
      <el-table-column
        label="实例ID"
        prop="instance_id"
      ></el-table-column>
      <el-table-column
        label="产品(外部)"
        prop="product__name"
      ></el-table-column>
      <el-table-column
        label="账户"
        prop="account__owner_name"
      ></el-table-column>
      <el-table-column
        label="项目"
        prop="project__desc"
      ></el-table-column>
      <el-table-column
        label="账期"
        prop="ymd"
      ></el-table-column>
      <el-table-column
        label="金额"
        prop="money"
      ></el-table-column>
      <el-table-column
        label="操作"
        width="80px;"
      >
        <template slot-scope="scoped">
          <el-button
            type="primary"
            icon="el-icon-edit"
            size="mini"
            @click="update_bill(scoped.row)"
          ></el-button>
        </template>
      </el-table-column>
    </el-table>
    <pagination
      v-show="bill_list_total>0"
      :total="bill_list_total"
      :page.sync="list_query.page"
      :limit.sync="list_query.limit"
      @pagination="get_bill_list"
    ></pagination>

    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="bill_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="60%"
    >
      <el-form
        ref="bill_formRef"
        :model="bill_form"
        :rules="bill_form_rules"
        size="small"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="实例名称"
              prop="name"
            >
              <el-input v-model="bill_form.instance_name"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="所属产品"
              prop="desc"
            >
              <el-select
                v-model="bill_form.project"
                placeholder="归属产品"
                filterable
              >
                <el-option
                  v-for="(item, index) in project_list"
                  :key="index"
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
          @click="bill_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_bill"
        >确 定</el-button>
      </span>
    </el-dialog>

    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="batch_dialog"
      width="50%"
    >
      <el-form
        ref="batch_formRefs"
        :model="batch_form"
        label-width="100px"
      >
        <el-form-item
          label="分配项目"
          prop="project"
        >
          <el-select
            v-model="batch_form.project"
            placeholder="按项目搜索"
            size="small"
            clearable
            filterable
          >
            <el-option
              v-for="(item, index) in project_list"
              :key="index"
              :label="item.name"
              :value="item.id"
            ></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="batch_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_batch"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"
import { getBillList, updateBill } from '@/views/bills/apis/bill'
import { getProjectList } from '@/views/bills/apis/project'
import { getProductList } from '@/views/bills/apis/product'
import { getAccountList } from '@/views/bills/apis/account'

export default {
  name: "BillDetail",
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
        batch_project: "批量分配项目",
        update_bill: "编辑实例产品"
      },
      dialog_status: "",
      product_select_input: "",
      project_select_input: "",
      account_select_input: "",
      bill_dialog: false,
      bill_form: {
        id: null,
        instance_name: null,
        project: null
      },
      bill_form_rules: {},
      year_month: "",
      bill_list: [],
      all_data: [],
      bill_list_total: 0,
      project_list: [],
      product_list: [],
      account_list: [],
      batch_dialog: false,
      batch_form: {
        project: null
      },
      multi_selected_list: [],
      downloadLoading: false
    }
  },
  created() {
    this.get_product_list()
    this.get_project_list()
    this.get_account_list()
  },
  methods: {
    get_bill_list() {
      getBillList(this.list_query)
        .then(resp => {
          this.bill_list = resp.data.results
          this.bill_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    update_bill(row) {
      this.bill_dialog = true
      this.dialog_status = "update_bill"
      this.get_project_list()
      this.bill_form = Object.assign({}, row)
    },
    submit_bill() {
      if (this.dialog_status === "update_bill") {
        updateBill(this.bill_form.id, this.bill_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新成功"
            })
            this.bill_dialog = false
            this.get_bill_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.bill_dialog = false
            this.get_bill_list()
          })
      }
    },
    get_project_list() {
      getProjectList({ limit: 999 })
        .then((resp) => {
          this.project_list = resp.data.results
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    get_product_list() {
      getProductList({ limit: 999 })
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
    get_account_list() {
      getAccountList({ limit: 999 })
        .then(resp => {
          this.account_list = resp.data.results
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    search_product() {
      const params = "product__code"
      this.list_query[params] = this.product_select_input.toLowerCase()
      getBillList(this.list_query)
        .then(resp => {
          this.bill_list = resp.data.results
          this.bill_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    search_project() {
      if (this.project_select_input == null || this.project_select_input === "") {
        const params = "project__isnull"
        this.list_query[params] = true
        // console.log(this.list_query)
        getBillList(this.list_query)
          .then(resp => {
            this.bill_list = resp.data.results
            this.bill_list_total = resp.data.count
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
          })
      } else {
        const params = "project__name"
        this.list_query[params] = this.project_select_input.toLowerCase()
        getBillList(this.list_query)
          .then(resp => {
            this.bill_list = resp.data.results
            this.bill_list_total = resp.data.count
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
          })
      }
    },
    handleSelectionChange(val) {
      this.multi_selected_list = val
    },
    batch_project() {
      if (this.multi_selected_list.length <= 0) {
        this.$message({
          type: "warning",
          message: "没有选择的人生是徒劳的"
        })
        return
      }
      this.batch_dialog = true
      this.dialog_status = "batch_project"
    },
    submit_batch() {
      for (let index = 0; index < this.multi_selected_list.length; index++) {
        updateBill(this.multi_selected_list[index].id, {
          project: this.batch_form.project
        })
          .then(resp => {
            this.$message({
              type: "success",
              message: "修改成功"
            })
            this.batch_dialog = false
            this.get_bill_list()
          })
          .catch(err => {
            this.$message.error(err)
            this.batch_dialog = false
            this.get_bill_list()
          })
      }
    },
    search_account() {
      const params = "account__owner_id"
      this.list_query[params] = this.account_select_input
      getBillList(this.list_query)
        .then(resp => {
          this.bill_list = resp.data.results
          this.bill_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    search_month() {
      const params = "ymd"
      this.list_query[params] = this.year_month
      getBillList(this.list_query)
        .then(resp => {
          this.bill_list = resp.data.results
          this.bill_list_total = resp.data.count
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    download_all() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = ['实例名称', '实例ID', '产品(外部)', '账户', '产品(内部)', '账期', '金额']
        const filterVal = ['instance_name', 'instance_id', 'product__name', 'account__owner_name', 'project__desc', 'ymd', 'money']
        const list = this.bill_list
        const data = this.formatJson(filterVal, list)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: 'bill_detail',
          autoWidth: true,
          bookType: 'xlsx'
        })
        this.downloadLoading = false
      })
    },
    download() {
      if (this.multi_selected_list.length) {
        this.downloadLoading = true
        import('@/vendor/Export2Excel').then(excel => {
          const tHeader = ['实例名称', '实例ID', '产品(外部)', '账户', '产品(内部)', '账期', '金额']
          const filterVal = ['instance_name', 'instance_id', 'product__name', 'account__owner_name', 'project__desc', 'ymd', 'money']
          const list = this.multi_selected_list
          const data = this.formatJson(filterVal, list)
          excel.export_json_to_excel({
            header: tHeader,
            data,
            filename: 'bill_detail',
            autoWidth: true,
            bookType: 'xlsx'
          })
          this.$refs.bill_list_table_refs.clearSelection()
          this.downloadLoading = false
        })
      } else {
        this.$message({
          type: "warning",
          message: "没有选择的人生是徒劳的"
        })
      }
    },
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => v[j]))
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
