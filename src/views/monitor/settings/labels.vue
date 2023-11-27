<template>
  <div>
    <el-button
      type="primary"
      size="small"
      icon="el-icon-circle-plus"
      @click="create_labels"
    >新增</el-button>
    <el-table
      ref="labels_list_table_refs"
      :data="labels_list"
      empty-text="啥也没有"
      size="small"
      border
    >
      <el-table-column
        label="名称"
        prop="name"
      ></el-table-column>
      <el-table-column
        label="值"
        prop="value"
      ></el-table-column>
      <el-table-column
        label="产品"
        prop="product__name"
      ></el-table-column>
      <el-table-column
        label="操作"
        width="120px"
      >
        <template slot-scope="scoped">
          <el-button
            type="primary"
            icon="el-icon-edit"
            size="mini"
            @click="update_labels(scoped.row)"
          ></el-button>
          <el-popconfirm
            title="确定删除吗？"
            confirm-button-text="确定"
            cancel-button-text="不了"
            style="margin-left: 10px"
            @confirm="delete_labels(scoped.row)"
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
      v-show="labels_list_total>0"
      :total="labels_list_total"
      :page.sync="list_query.page"
      :limit.sync="list_query.limit"
      @pagination="get_labels_list"
    ></pagination>
    <!-- 标签管理--------------------------------------------------  -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="labels_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="50%"
    >
      <el-form
        ref="labels_formRefs"
        :model="labels_form"
        :rules="labels_form_rules"
        label-width="100px"
        size="small"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="标签名"
              prop="name"
            >
              <el-select
                v-model="labels_form.name"
                clearable
                filterable
                allow-create
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
              prop="value"
            >
              <el-input
                v-model="labels_form.value"
                placeholder="请输入标签名称"
              ></el-input>
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
                v-model="labels_form.product"
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
          <el-col :span="12"></el-col>
        </el-row>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="labels_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_labels"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"
import { getProductList } from '@/views/monitor/apis/product'
import { createLabels, updateLabels, getLabelsList } from '@/views/monitor/apis/labels'

export default {
  name: "LabelsSetting",
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
        create_labels: "新增标签",
        update_labels: "编辑标签"
      },
      dialog_status: "",
      // 标签管理--------------------------------------------------
      labels_list: [],
      labels_list_total: 0,
      labels_dialog: false,
      labels_form: {
        id: null,
        name: null,
        value: null,
        product: null
      },
      labels_form_rules: {
        name: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        value: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        product: [{ required: true, message: "该项不能为空", trigger: "blur" }]
      },
      product_list: [],
      labels_name_list: []
    }
  },
  methods: {
    create_labels() {
      this.dialog_status = "create_labels"
      this.labels_dialog = true
      this.labels_form.name = null
      this.labels_form.value = null
      this.labels_form.product = null
      this.get_product_list()
      this.get_label_name_list()
    },
    update_labels(row) {
      this.dialog_status = "update_labels"
      this.labels_dialog = true
      this.labels_form = Object.assign({}, row)
      this.get_product_list()
    },
    delete_labels() { },
    submit_labels() {
      if (this.dialog_status === "create_labels") {
        this.$refs.labels_formRefs.validate((valid) => {
          if (valid) {
            createLabels(this.labels_form)
              .then((resp) => {
                this.$message({
                  type: "success",
                  message: "新增成功"
                })
                this.labels_dialog = false
                this.get_labels_list()
              })
              .catch((err) => {
                this.$message({
                  type: "error",
                  message: err
                })
                this.labels_dialog = false
                this.get_labels_list()
              })
          }
        })
      } else if (this.dialog_status === "update_labels") {
        updateLabels(this.labels_form.id, this.labels_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新成功"
            })
            this.labels_dialog = false
            this.get_labels_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.labels_dialog = false
            this.get_labels_list()
          })
      }
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
    get_labels_list() {
      getLabelsList(this.list_query)
        .then(resp => {
          this.labels_list = resp.data.results
          this.labels_list_total = resp.data.count
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
.el-button {
  vertical-align: top;
}
.el-table {
  width: 100%;
  margin-top: 10px;
}
</style>
