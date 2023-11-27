<template>
  <div class="app-container">
    <el-card class="box-card">

      <el-button
        type="primary"
        size="small"
        icon="el-icon-circle-plus"
        @click="create_sls"
      >新增</el-button>
      <el-table
        ref="sls_list_table_refs"
        :data="sls_list"
        empty-text="啥也没有"
        size="small"
        border
      >
        <el-table-column
          label="Logstore"
          prop="log"
        >
        </el-table-column>
        <el-table-column
          label="Project"
          prop="project"
        >
        </el-table-column>
        <el-table-column
          label="描述"
          prop="desc"
        >
        </el-table-column>
        <el-table-column
          label="所属产品"
          prop="product__name"
        >
        </el-table-column>
        <el-table-column
          label="所属云厂"
          prop="factory__name"
        >
        </el-table-column>
        <el-table-column
          label="操作"
          width="180px"
        >
          <template slot-scope="scoped">
            <el-tooltip
              class="item"
              effect="dark"
              content="查询日志"
              placement="top"
            >
              <el-button
                type="success"
                icon="el-icon-data-analysis"
                size="mini"
                @click="view_sls(scoped.row)"
              ></el-button>
            </el-tooltip>
            <el-button
              type="primary"
              icon="el-icon-edit"
              size="mini"
              @click="update_sls(scoped.row)"
            ></el-button>
            <el-popconfirm
              title="确定删除吗？"
              confirm-button-text="确定"
              cancel-button-text="不了"
              style="margin-left: 10px"
              @confirm="delete_sls(scoped.row)"
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
        v-show="sls_list_total>0"
        :total="sls_list_total"
        :page.sync="list_query.page"
        :limit.sync="list_query.limit"
        @pagination="get_sls_list"
      ></pagination>

    </el-card>
    <!-- 日志服务管理dialog--------------------------------------------------  -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="sls_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="60%"
    >
      <el-form
        ref="sls_formRef"
        :model="sls_form"
        :rules="sls_form_rules"
        size="small"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="Project"
              prop="project"
            >
              <el-input v-model="sls_form.project"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="Logstore"
              prop="log"
            >
              <el-input v-model="sls_form.log"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="描述"
              prop="desc"
            >
              <el-input v-model="sls_form.desc"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="所属产品"
              prop="product"
            >
              <el-select
                v-model="sls_form.product"
                placeholder="请选择产品"
                clearable
                filterable
              >
                <el-option
                  v-for="(item, index) in product_list"
                  :key="index"
                  :label="item.name"
                  :value="item.id"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="Endpoint"
              prop="endpoint"
            >
              <el-input v-model="sls_form.endpoint"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="临时角色"
              prop="assumerole"
            >
              <el-select
                v-model="sls_form.assumerole"
                placeholder="请选择临时角色"
                clearable
                filterable
              >
                <el-option
                  v-for="(item, index) in assumerole_list"
                  :key="index"
                  :label="item.name"
                  :value="item.id"
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
          @click="sls_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_sls"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"
import permission from "@/directive/permission/index.js"
import { mapGetters } from "vuex"
import { getProductList } from '@/views/settings/apis/product'
import { getAssumeRoleList } from '@/views/settings/apis/rolearn'
import { createSls, getSlsList, updateSls, deleteSls } from "@/views/settings/apis/sls"

export default {
  name: "SettingsSls",
  components: {
    Pagination
  },
  directives: {
    permission
  },
  data() {
    return {
      list_query: {
        page: 1,
        limit: 15
      },
      dialog_map: {
        create_sls: "新增日志查询",
        update_sls: "编辑日志查询"
      },
      dialog_status: "",
      product_list: [],
      factory_list: [],
      assumerole_list: [],
      // 日志服务管理--------------------------------------------------
      sls_list: [],
      sls_list_total: 0,
      sls_dialog: false,
      sls_form: {
        id: null,
        log: null,
        desc: null,
        project: null,
        endpoint: null,
        product: null,
        assumerole: null
      },
      sls_form_rules: {
        log: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        desc: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        project: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        product: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        endpoint: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        assumerole: [{ required: true, message: '不能为空', trigger: ['blur'] }]
      }
    }
  },
  computed: {
    ...mapGetters(["user_id", "is_superuser"])
  },
  created() {
    this.get_sls_list()
  },
  methods: {
    // 云厂管理--------------------------------------------------
    create_sls() {
      this.dialog_status = "create_sls"
      this.sls_dialog = true
      this.sls_form.log = null
      this.sls_form.desc = null
      this.get_product_list()
      this.get_assumerole_list()
    },
    update_sls(row) {
      this.dialog_status = "update_sls"
      this.sls_dialog = true
      this.sls_form = Object.assign({}, row)
      this.get_product_list()
      this.get_assumerole_list()
    },
    delete_sls(row) {
      deleteSls(row.id)
        .then(() => {
          this.$message({
            type: "success",
            message: "删除成功"
          })
          this.get_sls_list()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
          this.get_sls_list()
        })
    },
    view_sls() { },
    submit_sls() {
      if (this.dialog_status === "create_sls") {
        createSls(this.sls_form)
          .then((resp) => {
            this.$message({
              type: "success",
              message: "新增成功"
            })
            this.sls_dialog = false
            this.get_sls_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.sls_dialog = false
            this.get_sls_list()
          })
      } else if (this.dialog_status === "update_sls") {
        updateSls(this.sls_form.id, this.sls_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新成功"
            })
            this.sls_dialog = false
            this.get_sls_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.sls_dialog = false
            this.get_sls_list()
          })
      }
    },
    get_sls_list() {
      getSlsList(this.list_query)
        .then((resp) => {
          this.sls_list = resp.data.results
          this.sls_list_total = resp.data.count
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
    get_assumerole_list() {
      getAssumeRoleList({ limit: 100 })
        .then(resp => {
          this.assumerole_list = resp.data.results
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
