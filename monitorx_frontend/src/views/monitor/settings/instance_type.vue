<template>
  <div>
    <el-button
      type="primary"
      size="small"
      icon="el-icon-circle-plus"
      @click="create_instance_type"
    >新增</el-button>
    <el-table
      ref="instance_type_list_table_refs"
      :data="instance_type_list"
      empty-text="啥也没有"
      size="small"
      border
    >
      <el-table-column
        label="名称"
        prop="name"
      ></el-table-column>
      <el-table-column
        label="别名"
        prop="desc"
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
            @click="update_instance_type(scoped.row)"
          ></el-button>
          <el-popconfirm
            title="确定删除吗？"
            confirm-button-text="确定"
            cancel-button-text="不了"
            style="margin-left: 10px"
            @confirm="delete_instance_type(scoped.row)"
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
      v-show="instance_type_list_total>0"
      :total="instance_type_list_total"
      :page.sync="list_query.page"
      :limit.sync="list_query.limit"
      @pagination="get_instance_type_list"
    ></pagination>
    <!-- 实例类型--------------------------------------------------  -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="instance_type_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="50%"
    >
      <el-form
        ref="instance_type_formRefs"
        :model="instance_type_form"
        :rules="instance_type_form_rules"
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
                v-model="instance_type_form.name"
                size="small"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="别名"
              prop="desc"
            >
              <el-input
                v-model="instance_type_form.desc"
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
          @click="instance_type_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_instance_type"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"
import { createInstanceType, updateInstanceType, deleteInstanceType, getInstanceTypeList } from '@/views/monitor/apis/instance_type'

export default {
  name: "InstanceTypeSetting",
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
        create_instance_type: "新增实例类型",
        update_instance_type: "编辑实例类型"
      },
      dialog_status: "",
      // 实例类型--------------------------------------------------
      instance_type_list: [],
      instance_type_list_total: 0,
      instance_type_dialog: false,
      instance_type_form: {
        id: null,
        name: null,
        desc: null
      },
      instance_type_form_rules: {
        name: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        desc: [{ required: true, message: "该项不能为空", trigger: "blur" }]
      }
    }
  },
  methods: {
    // 实例类型--------------------------------------------------
    create_instance_type() {
      this.dialog_status = "create_instance_type"
      this.instance_type_dialog = true
    },
    update_instance_type(row) {
      this.dialog_status = "update_instance_type"
      this.instance_type_dialog = true
      this.instance_type_form = Object.assign({}, row)
    },
    delete_instance_type(row) {
      deleteInstanceType(row.id)
        .then(resp => {
          this.$message({
            type: "success",
            message: "删除成功"
          })
          this.get_instance_type_list()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
          this.get_instance_type_list()
        })
    },
    submit_instance_type() {
      if (this.dialog_status === "create_instance_type") {
        this.$refs.instance_type_formRefs.validate((valid) => {
          if (valid) {
            createInstanceType(this.instance_type_form)
              .then((resp) => {
                this.$message({
                  type: "success",
                  message: "新增成功"
                })
                this.instance_type_dialog = false
                this.get_instance_type_list()
              })
              .catch((err) => {
                this.$message({
                  type: "error",
                  message: err
                })
                this.instance_type_dialog = false
                this.get_instance_type_list()
              })
          }
        })
      } else if (this.dialog_status === "update_instance_type") {
        updateInstanceType(this.instance_type_form.id, this.instance_type_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新成功"
            })
            this.instance_type_dialog = false
            this.get_instance_type_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.instance_type_dialog = false
            this.get_instance_type_list()
          })
      }
    },
    get_instance_type_list() {
      getInstanceTypeList(this.list_query)
        .then(resp => {
          this.instance_type_list = resp.data.results
          this.instance_type_list_total = resp.data.count
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
