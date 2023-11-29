这里是产品管理的配置页面

<template>
  <div class="app-container">
    <el-card class="box-card">
      <!-- 新增或者搜索相关 -->
      <div>
        <el-input
          v-model="input_select"
          placeholder="搜索"
          class="filter-item"
          size="small"
          clearable
          style="width: 400px"
          @keyup.enter.native="search_product"
        >
          <el-select
            slot="prepend"
            v-model="select_input"
            size="small"
            style="width: 100px"
            placeholder="请选择"
          >
            <el-option
              label="产品名称"
              value="name"
            ></el-option>
            <el-option
              label="产品ID"
              value="id"
            ></el-option>
          </el-select>
          <el-button
            slot="append"
            icon="el-icon-search"
            :loading="button_loading"
            @click="search_product"
          ></el-button>
        </el-input>
        <el-button
          v-if="checkPermission(['admin'])"
          type="primary"
          size="small"
          icon="el-icon-circle-plus"
          style="margin-left: 10px"
          @click="create_product"
        >新增</el-button>
      </div>
      <!-- 产品列表表格 -->
      <el-table
        :data="product_list"
        style="width: 100%"
        border
        size="small"
      >
        >
        <el-table-column
          label="产品名称"
          prop="name"
        >
        </el-table-column>
        <el-table-column
          label="描述"
          prop="desc"
        >
        </el-table-column>
        <!-- <el-table-column
          label="用户组"
          prop="user_group__name"
        >
        </el-table-column> -->
        <el-table-column
          label="操作"
          width="180px;"
        >
          <template slot-scope="scoped">
            <el-button
              v-if="checkPermission(['admin'])"
              type="primary"
              icon="el-icon-edit"
              size="mini"
              @click="update_product(scoped.row)"
            ></el-button>
            <el-popconfirm
              v-if="checkPermission(['admin'])"
              title="确定删除吗？"
              confirm-button-text="确定"
              cancel-button-text="不了"
              style="margin-left:10px"
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
            <el-tooltip
              v-if="checkPermission(['admin', 'ops'])"
              class="item"
              effect="dark"
              content="产品分组"
              placement="top"
            >
              <el-button
                type="info"
                icon="el-icon-folder"
                size="mini"
                style="margin-left:10px"
                @click="goto_groups(scoped.row)"
              ></el-button>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>
      <pagination
        v-show="product_total>0"
        :total="product_total"
        :page.sync="list_query.page"
        :limit.sync="list_query.limit"
        @pagination="get_product_list"
      ></pagination>
    </el-card>
    <!-- 新增或者编辑产品的Dialog -->
    <el-dialog
      :title="textMap[dialogStatus]"
      :visible.sync="product_dialog"
      width="50%"
    >
      <el-form
        ref="product_form"
        :model="product_form"
        :rules="product_form_rules"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="产品名称"
              prop="name"
            >
              <el-input
                v-model="product_form.name"
                size="small"
                :disabled="product_name_disable"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="产品描述"
              prop="desc"
            >
              <el-input
                v-model="product_form.desc"
                size="small"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="用户组"
              prop="user_group"
            >
              <el-select
                v-model="product_form.user_group"
                placeholder="请选择用户组"
                clearable
                filterable
                size="small"
              >
                <el-option
                  v-for="(item, index) in user_group_list"
                  :key="index"
                  :label="item.name"
                  :value="item.id"
                  size="small"
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
import {
  getProductList,
  createProduct,
  updateProductID,
  deleteProductByID
} from "@/api/product"
import { getCmdbUserGroupList } from "@/views/settings/apis/user_group"
import checkPermission from "@/utils/permission"
export default {
  name: "Product",
  components: {
    Pagination
  },
  props: {
    clearable: { type: Boolean, default: false }
  },
  data() {
    return {
      input_select: "",
      select_input: "name",
      button_loading: false,
      list_query: {
        page: 1,
        limit: 15
      },
      textMap: {
        create: "新增产品",
        update: "更新产品"
      },
      dialogStatus: "",
      product_name_disable: false,
      product_list: [],
      product_total: 0,
      product_dialog: false,
      product_form: {
        id: null,
        name: null,
        desc: null,
        user_group: []
      },
      product_form_rules: {
        name: [{ required: true, message: "不能为空", trigger: "blur" }],
        desc: [{ required: true, message: "不能为空", trigger: "blur" }]
      },
      user_group_list: []
    }
  },
  created() {
    this.get_product_list()
  },
  methods: {
    checkPermission,
    get_product_list() {
      getProductList(this.list_query)
        .then(response => {
          this.product_list = response.data.results
          this.product_total = response.data.count
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    create_product() {
      this.product_dialog = true
      this.dialogStatus = "create_product"
      this.product_name_disable = false
      this.product_form.name = null
      this.product_form.desc = null
      this.product_form.user_group = null
      this.get_user_group_list()
    },
    update_product(row) {
      this.product_dialog = true
      this.dialogStatus = "update_product"
      this.product_form = Object.assign({}, row)
      this.get_user_group_list()
    },
    get_user_group_list() {
      getCmdbUserGroupList(this.list_query)
        .then(resp => {
          this.user_group_list = resp.data.results
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    submit_product() {
      if (this.dialogStatus === "create_product") {
        createProduct(this.product_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "新增成功"
            })
            this.product_dialog = false
            this.get_product_list()
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            })
            this.product_dialog = false
            this.get_product_list()
          })
      } else if (this.dialogStatus === "update_product") {
        updateProductID(this.product_form.id, this.product_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新成功"
            })
            this.product_dialog = false
            this.get_product_list()
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            })
            this.product_dialog = false
            this.get_product_list()
          })
      }
    },
    delete_product(row) {
      deleteProductByID(row.id)
        .then(() => {
          this.$message({
            type: "success",
            message: "删除成功"
          })
          this.get_product_list()
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
          this.get_product_list()
        })
    },
    search_product() {
      this.button_loading = true
      const params = this.select_input + "__contains"
      this.list_query.page = 1
      this.list_query[params] = this.input_select
      this.get_product_list()
      this.button_loading = false
    },
    goto_groups(row) {
      const parObj = JSON.stringify(row)
      this.$router.push({
        path: "/settings/host_group",
        query: { product_info: parObj }
      })
      // this.$router.push(
      //   {
      //     path: "/settings/host_group",
      //     name: 'HostGroup',
      //     query: { product_id: row.id, product_name: row.name }
      //   })
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
.el-table {
  width: 100%;
  margin-top: 10px;
}
.el-button {
  vertical-align: top;
}
</style>
