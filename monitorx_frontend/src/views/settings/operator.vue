<template>
  <div class="app-container">
    <el-card class="box-card">
      <div>
        <el-button
          type="primary"
          size="small"
          icon="el-icon-circle-plus"
          @click="create_operator"
        >新增</el-button>
      </div>
      <el-table
        :data="operator_list"
        style="width: 100%"
        border
        size="small"
      >
        <el-table-column
          prop="name"
          label="运营商"
        >
        </el-table-column>
        <el-table-column
          prop="desc"
          label="描述"
        >
        </el-table-column>
        <el-table-column
          label="操作"
          width="120px;"
        >
          <template slot-scope="scoped">
            <el-button
              type="primary"
              icon="el-icon-edit"
              size="mini"
              @click="update_operator(scoped.row)"
            ></el-button>
            <el-popconfirm
              title="确定删除吗？"
              confirm-button-text="确定"
              cancel-button-text="不了"
              style="margin-left:10px"
              @confirm="delete_operator(scoped.row)"
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
        v-show="operator_list_total>0"
        :total="operator_list_total"
        :page.sync="list_query.page"
        :limit.sync="list_query.limit"
        @pagination="get_operator_list"
      ></pagination>
    </el-card>
    <el-dialog
      :title="textMap[dialogStatus]"
      :visible.sync="operator_dialog"
      width="50%"
    >
      <el-form
        ref="operator_formRefs"
        :model="operator_form"
        :rules="operator_form_rules"
        size="small"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="名称"
              prop="name"
            >
              <el-input v-model="operator_form.name"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="描述"
              prop="desc"
            >
              <el-input v-model="operator_form.desc"></el-input>
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
          @click="operator_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_operator"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"
import {
  getOperatorList,
  createOperator,
  updateOperatorID
} from "@/api/operator"

export default {
  name: "Operator",
  components: {
    Pagination
  },
  data() {
    return {
      list_query: {
        page: 1,
        limit: 15
      },
      operator_list: [],
      operator_list_total: 0,
      operator_dialog: false,
      textMap: {
        create_operator: "新增运营商",
        update_operator: "编辑运营商"
      },
      dialogStatus: "",
      operator_form: {
        id: null,
        name: null,
        desc: null
      },
      operator_form_rules: {
        name: [{ required: true, message: "不能为空", trigger: "blur" }],
        desc: [{ required: true, message: "不能为空", trigger: "blur" }]
      }
    }
  },
  created() {
    this.get_operator_list()
  },
  methods: {
    create_operator() {
      this.dialogStatus = "create_operator"
      this.operator_dialog = true
      this.operator_form.name = null
      this.operator_form.desc = null
    },
    update_operator(row) {
      this.dialogStatus = "update_operator"
      this.operator_dialog = true
      this.operator_form = Object.assign({}, row)
    },
    submit_operator() {
      if (this.dialogStatus === "create_operator") {
        createOperator(this.operator_form)
          .then(resp => {
            this.$message({
              type: "success",
              message: "新增成功"
            })
            this.operator_dialog = false
            this.get_operator_list()
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            })
            this.operator_dialog = false
            this.get_operator_list()
          })
      } else if (this.dialogStatus === "update_operator") {
        updateOperatorID(this.operator_form.id, this.operator_form)
          .then(resp => {
            this.$message({
              type: "success",
              message: "更新成功"
            })
            this.operator_dialog = false
            this.get_operator_list()
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            })
            this.operator_dialog = false
            this.get_operator_list()
          })
      }
    },
    get_operator_list() {
      getOperatorList(this.list_query).then(resp => {
        this.operator_list = resp.data.results
        this.operator_list_total = resp.data.count
      })
    },
    delete_operator(row) {},
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
.el-table {
  margin-top: 10px;
}
.el-input {
  width: 300px;
}
</style>
