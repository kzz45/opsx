<template>
  <div>
    <el-input
      v-model="input_content"
      placeholder="搜点啥"
      clearable
      size="small"
      style="width: 300px;"
      @keyup.enter.native="search_project"
    >
      <el-select
        slot="prepend"
        v-model="select_input"
        size="small"
        style="width: 100px;"
      >
        <el-option
          label="产品名称"
          value="desc"
        ></el-option>
        <el-option
          label="产品Code"
          value="code"
        ></el-option>
      </el-select>
      <el-button
        slot="append"
        icon="el-icon-search"
        @click="search_project"
      ></el-button>
    </el-input>
    <el-button
      type="primary"
      size="small"
      icon="el-icon-circle-plus"
      style="margin-left: 10px;"
      @click="create_project"
    >新增</el-button>
    <el-table
      ref="project_list_table_refs"
      :data="project_list"
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
        label="Code"
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
            @click="update_project(scoped.row)"
          ></el-button>
          <el-popconfirm
            title="确定删除吗？"
            confirm-button-text="确定"
            cancel-button-text="不了"
            style="margin-left: 10px"
            @confirm="delete_project(scoped.row)"
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
      v-show="project_list_total>0"
      :total="project_list_total"
      :page.sync="list_query.page"
      :limit.sync="list_query.limit"
      @pagination="get_project_list"
    ></pagination>
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="project_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="60%"
    >
      <el-form
        ref="project_formRef"
        :model="project_form"
        :rules="project_form_rules"
        size="small"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="项目名称"
              prop="name"
            >
              <el-input v-model="project_form.name"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="项目描述"
              prop="desc"
            >
              <el-input v-model="project_form.desc"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="项目Code"
              prop="code"
            >
              <el-input v-model="project_form.code"></el-input>
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
          @click="project_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_project"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"
import { getProjectList, createProject, updateProject, deleteProject } from '@/views/bills/apis/project'

export default {
  name: "BillProject",
  components: {
    Pagination
  },
  data() {
    return {
      list_query: {
        page: 1,
        limit: 15
      },
      input_content: "",
      select_input: "desc",
      dialog_map: {
        create_project: "新增项目",
        update_project: "编辑项目"
      },
      dialog_status: "",
      project_dialog: false,
      project_form: {
        id: null,
        name: null,
        desc: null,
        code: null
      },
      project_form_rules: {},
      project_list: [],
      project_list_total: 0
    }
  },
  methods: {
    create_project() {
      this.dialog_status = "create_project"
      this.project_dialog = true
      this.project_form.name = null
      this.project_form.desc = null
      this.project_form.code = null
    },
    update_project(row) {
      this.dialog_status = "update_project"
      this.project_dialog = true
      this.project_form = Object.assign({}, row)
    },
    delete_project(row) {
      deleteProject(row.id)
        .then(resp => {
          this.$message({
            type: "success",
            message: "删除成功"
          })
          this.get_project_list()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
          this.get_project_list()
        })
    },
    submit_project() {
      if (this.dialog_status === "create_project") {
        createProject(this.project_form)
          .then((resp) => {
            this.$message({
              type: "success",
              message: "新增成功"
            })
            this.project_dialog = false
            this.get_project_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.project_dialog = false
            this.get_project_list()
          })
      } else if (this.dialog_status === "update_project") {
        updateProject(this.project_form.id, this.project_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新成功"
            })
            this.project_dialog = false
            this.get_project_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.project_dialog = false
            this.get_project_list()
          })
      }
    },
    get_project_list() {
      getProjectList(this.list_query)
        .then((resp) => {
          this.project_list = resp.data.results
          this.project_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    search_project() {
      var params = ""
      params = this.select_input + "__contains"
      this.list_query[params] = this.input_content
      getProjectList(this.list_query)
        .then(resp => {
          this.project_list = resp.data.results
          this.project_list_total = resp.data.count
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
