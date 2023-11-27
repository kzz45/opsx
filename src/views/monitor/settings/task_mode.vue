<template>
  <div>
    <el-button
      type="primary"
      size="small"
      icon="el-icon-circle-plus"
      @click="create_task_mode"
    >新增</el-button>
    <el-table
      ref="task_mode_list_table_refs"
      :data="task_mode_list"
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
        label="默认参数"
        prop="args"
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
            @click="update_task_mode(scoped.row)"
          ></el-button>
          <el-popconfirm
            title="确定删除吗？"
            confirm-button-text="确定"
            cancel-button-text="不了"
            style="margin-left: 10px"
            @confirm="delete_task_mode(scoped.row)"
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
      v-show="task_mode_list_total>0"
      :total="task_mode_list_total"
      :page.sync="list_query.page"
      :limit.sync="list_query.limit"
      @pagination="get_task_mode_list"
    ></pagination>
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="task_mode_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="50%"
    >
      <el-form
        ref="task_mode_formRefs"
        :model="task_mode_form"
        :rules="task_mode_form_rules"
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
                v-model="task_mode_form.name"
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
                v-model="task_mode_form.desc"
                size="small"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="参数"
              prop="args"
            >
              <el-input
                v-model="task_mode_form.args"
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
          @click="task_mode_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_task_mode"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"
import { createTaskMode, updateTaskMode, getTaskModeList, deleteTaskMode } from '@/views/monitor/apis/task_mode'

export default {
  name: "TaskModeSetting",
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
        create_task_mode: "新增任务模式",
        update_task_mode: "编辑任务模式"
      },
      dialog_status: "",
      task_mode_list: [],
      task_mode_list_total: 0,
      task_mode_dialog: false,
      task_mode_mode_list: [],
      task_mode_form: {
        id: null,
        name: null,
        desc: null,
        args: null
      },
      task_mode_form_rules: {
        name: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        desc: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        args: [{ required: true, message: "该项不能为空", trigger: "blur" }]
      }
    }
  },
  methods: {
    create_task_mode() {
      this.dialog_status = "create_task_mode"
      this.task_mode_dialog = true
      this.task_mode_form.name = null
      this.task_mode_form.desc = null
    },
    update_task_mode(row) {
      this.dialog_status = "update_task_mode"
      this.task_mode_dialog = true
      this.task_mode_form = Object.assign({}, row)
    },
    delete_task_mode(row) {
      deleteTaskMode(row.id)
        .then(resp => {
          this.$message({
            type: "success",
            message: "删除成功"
          })
          this.get_task_mode_list()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
          this.get_task_mode_list()
        })
    },
    submit_task_mode() {
      if (this.dialog_status === "create_task_mode") {
        this.$refs.task_mode_formRefs.validate((valid) => {
          if (valid) {
            createTaskMode(this.task_mode_form)
              .then((resp) => {
                this.$message({
                  type: "success",
                  message: "新增成功"
                })
                this.task_mode_dialog = false
                this.get_task_mode_list()
              })
              .catch((err) => {
                this.$message({
                  type: "error",
                  message: err
                })
                this.task_mode_dialog = false
                this.get_task_mode_list()
              })
          }
        })
      } else if (this.dialog_status === "update_task_mode") {
        updateTaskMode(this.task_mode_form.id, this.task_mode_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新成功"
            })
            this.task_mode_dialog = false
            this.get_task_mode_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.task_mode_dialog = false
            this.get_task_mode_list()
          })
      }
    },
    get_task_mode_list() {
      getTaskModeList(this.list_query)
        .then(resp => {
          this.task_mode_list = resp.data.results
          this.task_mode_list_total = resp.data.count
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
