<template>
  <div class="app-container">
    <el-card class="box-card">
      <div>
        <el-button
          v-if="checkPermission(['admin'])"
          type="primary"
          size="small"
          icon="el-icon-circle-plus"
          @click="create_factory"
        >新增</el-button>
      </div>
      <el-table
        :data="factory_list"
        style="width: 100%"
        border
        size="small"
      >
        <el-table-column
          prop="name"
          label="厂商"
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
              v-if="checkPermission(['admin'])"
              type="primary"
              icon="el-icon-edit"
              size="mini"
              @click="update_factory(scoped.row)"
            ></el-button>
            <el-popconfirm
              v-if="checkPermission(['admin'])"
              title="确定删除吗？"
              confirm-button-text="确定"
              cancel-button-text="不了"
              style="margin-left:10px"
              @confirm="delete_factory(scoped.row)"
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
        v-show="factory_list_total>0"
        :total="factory_list_total"
        :page.sync="list_query.page"
        :limit.sync="list_query.limit"
        @pagination="get_factory_list"
      ></pagination>
    </el-card>

    <el-dialog
      :title="textMap[dialogStatus]"
      :visible.sync="factory_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="50%"
    >
      <el-form
        ref="factory_form_refs"
        :model="factory_form"
        :rules="factory_form_rules"
        size="small"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="云厂商名称"
              prop="name"
            >
              <el-input
                v-model="factory_form.name"
                size="small"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="云厂商描述"
              prop="desc"
            >
              <el-input
                v-model="factory_form.desc"
                size="small"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="kms账号"
              prop="kms_account"
            >
              <el-input
                v-model="factory_form.kms_account"
                size="small"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="rolearn"
              prop="rolearn"
            >
              <el-input
                v-model="factory_form.rolearn"
                size="small"
              ></el-input>
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
          @click="factory_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_factory"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"
import {
  getFactoryList,
  createFactory,
  updateFactoryID,
  deleteFactoryByID
} from "@/api/factory"
import checkPermission from "@/utils/permission"
export default {
  name: "FactoryList",
  components: {
    Pagination
  },
  data() {
    return {
      list_query: {
        page: 1,
        limit: 15
      },
      factory_list: [],
      factory_list_total: 0,
      textMap: {
        create_factory: "新增云厂",
        update_factory: "编辑云厂"
      },
      dialogStatus: "",
      factory_dialog: false,
      factory_form: {
        id: null,
        name: null,
        kms_account: "",
        desc: null,
        rolearn: null
      },
      factory_form_rules: {
        name: [{ required: true, message: "不能为空", trigger: "blur" }],
        desc: [{ required: true, message: "不能为空", trigger: "blur" }]
      }
    }
  },
  created() {
    this.get_factory_list()
  },
  methods: {
    checkPermission,
    get_factory_list() {
      getFactoryList(this.list_query).then(response => {
        this.factory_list = response.data.results
        this.factory_list_total = response.data.count
      })
    },
    create_factory() {
      this.dialogStatus = "create_factory"
      this.factory_dialog = true
      this.factory_form.name = null
      this.factory_form.desc = null
      this.factory_form.kms_account = ""
      this.factory_form.rolearn = null
    },
    update_factory(row) {
      this.dialogStatus = "update_factory"
      this.factory_dialog = true
      this.factory_form = Object.assign({}, row)
    },
    delete_factory(row) {
      deleteFactoryByID(row.id)
        .then(() => {
          this.$message({
            type: "success",
            message: "删除成功"
          })
          this.get_factory_list()
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err.message
          })
          this.get_factory_list()
        })
    },
    submit_factory() {
      if (this.dialogStatus === "create_factory") {
        createFactory(this.factory_form)
          .then(resp => {
            this.$message({
              type: "success",
              message: "新增成功"
            })
            this.factory_dialog = false
            this.get_factory_list()
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            })
            this.factory_dialog = false
            this.get_factory_list()
          })
      } else if (this.dialogStatus === "update_factory") {
        updateFactoryID(this.factory_form.id, this.factory_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新成功"
            })
            this.factory_dialog = false
            this.get_factory_list()
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err.message
            })
            this.factory_dialog = false
            this.get_factory_list()
          })
      }
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
.el-table {
  margin-top: 10px;
}
.el-input {
  width: 200px;
}
</style>
