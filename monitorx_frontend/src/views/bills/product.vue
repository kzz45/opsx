<template>
  <div>
    <el-input
      v-model="input_content"
      placeholder="搜点啥"
      clearable
      size="small"
      style="width: 300px;"
      @keyup.enter.native="search_product"
    >
      <el-select
        slot="prepend"
        v-model="select_input"
        size="small"
        style="width: 100px;"
      >
        <el-option
          label="产品名称"
          value="name"
        ></el-option>
        <el-option
          label="产品Code"
          value="code"
        ></el-option>
      </el-select>
      <el-button
        slot="append"
        icon="el-icon-search"
        @click="search_product"
      ></el-button>
    </el-input>
    <el-table
      ref="product_list_table_refs"
      :data="product_list"
      empty-text="啥也没有"
      size="small"
      border
    >
      <el-table-column
        label="产品名称"
        prop="name"
      ></el-table-column>
      <el-table-column
        label="产品Code"
        prop="code"
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
            @click="update_product(scoped.row)"
          ></el-button>
          <el-popconfirm
            title="确定删除吗？"
            confirm-button-text="确定"
            cancel-button-text="不了"
            style="margin-left: 10px"
            @confirm="delete_product(scoped.row)"
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
      v-show="product_list_total>0"
      :total="product_list_total"
      :page.sync="list_query.page"
      :limit.sync="list_query.limit"
      @pagination="get_product_list"
    ></pagination>
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="product_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="60%"
    >
      <el-form
        ref="product_formRef"
        :model="product_form"
        :rules="product_form_rules"
        size="small"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="产品名称"
              prop="name"
            >
              <el-input v-model="product_form.name"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="产品Code"
              prop="code"
            >
              <el-input v-model="product_form.code"></el-input>
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
          @click="product_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_product"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"
import { getProductList, updateProduct } from '@/views/bills/apis/product'

export default {
  name: "BillProduct",
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
        create_product: "新增产品",
        update_product: "编辑产品"
      },
      dialog_status: "",
      input_content: "",
      select_input: "name",
      product_list: [],
      product_list_total: 0,
      product_dialog: false,
      product_form: {
        id: null,
        name: null,
        code: null
      },
      product_form_rules: {}
    }
  },
  created() {
    // this.get_product_list()
  },
  methods: {
    get_product_list() {
      getProductList(this.list_query)
        .then(resp => {
          this.product_list = resp.data.results
          this.product_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    update_product(row) {
      this.dialog_status = "update_product"
      this.product_dialog = true
      this.product_form = Object.assign({}, row)
    },
    delete_product() { },
    submit_product() {
      if (this.dialog_status === "update_product") {
        updateProduct(this.product_form.id, this.product_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新成功"
            })
            this.product_dialog = false
            this.get_product_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.product_dialog = false
            this.get_product_list()
          })
      }
    },
    search_product() {
      var params = ""
      params = this.select_input + "__contains"
      this.list_query[params] = this.input_content
      getProductList(this.list_query)
        .then(resp => {
          this.product_list = resp.data.results
          this.product_list_total = resp.data.count
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
