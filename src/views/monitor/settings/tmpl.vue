<template>
  <div>
    <el-button
      type="primary"
      size="small"
      icon="el-icon-circle-plus"
      @click="create_tmpl"
    >新增</el-button>
    <el-table
      ref="tmpl_list_table_refs"
      :data="tmpl_list"
      empty-text="啥也没有"
      size="small"
      border
    >
      <el-table-column
        label="名称"
        prop="name"
      ></el-table-column>
      <el-table-column
        label="类型"
        prop="mode"
      >
        <template slot-scope="scoped">
          <el-tag
            v-if="scoped.row.mode === 0"
            type="primary"
            size="small"
          >通知模版</el-tag>
          <el-tag
            v-if="scoped.row.mode === 1"
            type="primary"
            size="small"
          >Prom模版</el-tag>
          <el-tag
            v-if="scoped.row.mode === 2"
            type="primary"
            size="small"
          >Alert模版</el-tag>
          <el-tag
            v-if="scoped.row.mode === 3"
            type="primary"
            size="small"
          >实例模版</el-tag>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        width="120px"
      >
        <template slot-scope="scoped">
          <el-button
            type="primary"
            icon="el-icon-edit"
            size="mini"
            @click="update_tmpl(scoped.row)"
          ></el-button>
          <el-popconfirm
            title="确定删除吗？"
            confirm-button-text="确定"
            cancel-button-text="不了"
            style="margin-left: 10px"
            @confirm="delete_tmpl(scoped.row)"
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
      v-show="tmpl_list_total>0"
      :total="tmpl_list_total"
      :page.sync="list_query.page"
      :limit.sync="list_query.limit"
      @pagination="get_tmpl_list"
    ></pagination>
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="tmpl_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="50%"
    >
      <el-form
        ref="tmpl_formRefs"
        :model="tmpl_form"
        :rules="tmpl_form_rules"
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
                v-model="tmpl_form.name"
                size="small"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="类型"
              prop="mode"
            >
              <el-select
                v-model="tmpl_form.mode"
                placeholder=""
              >
                <el-option
                  v-for="(item, index) in tmpl_mode_list"
                  :key="index"
                  :value="item.id"
                  :label="item.name"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <el-form-item
              label="模板内容"
              prop="content"
            >
              <el-input
                v-model="tmpl_form.content"
                :autosize="{ minRows:10, maxRows: 20 }"
                type="textarea"
                placeholder="模板内容"
                style="width: 540px;"
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
          @click="tmpl_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_tmpl"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"
import { createTmpl, updateTmpl, deleteTmpl, getTmplList } from '@/views/monitor/apis/tmpl'

export default {
  name: "TmplConfig",
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
        create_tmpl: "新增模板",
        update_tmpl: "编辑模板"
      },
      dialog_status: "",
      tmpl_list: [],
      tmpl_list_total: 0,
      tmpl_dialog: false,
      tmpl_mode_list: [
        { id: 0, name: "通知模版" },
        { id: 1, name: "Prom模版" },
        { id: 2, name: "Alert模版" },
        { id: 3, name: "实例模版" }
      ],
      tmpl_form: {
        id: null,
        name: null,
        mode: null,
        content: null
      },
      tmpl_form_rules: {
        name: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        mode: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        content: [{ required: true, message: "该项不能为空", trigger: "blur" }]
      }
    }
  },
  methods: {
    create_tmpl() {
      this.dialog_status = "create_tmpl"
      this.tmpl_dialog = true
      this.tmpl_form.name = null
      this.tmpl_form.mode = null
      this.tmpl_form.content = null
    },
    update_tmpl(row) {
      this.dialog_status = "update_tmpl"
      this.tmpl_dialog = true
      this.tmpl_form = Object.assign({}, row)
    },
    delete_tmpl(row) {
      deleteTmpl(row.id)
        .then(resp => {
          this.$message({
            type: "success",
            message: "删除成功"
          })
          this.get_tmpl_list()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
          this.get_tmpl_list()
        })
    },
    submit_tmpl() {
      if (this.dialog_status === "create_tmpl") {
        this.$refs.tmpl_formRefs.validate((valid) => {
          if (valid) {
            createTmpl(this.tmpl_form)
              .then((resp) => {
                this.$message({
                  type: "success",
                  message: "新增成功"
                })
                this.tmpl_dialog = false
                this.get_tmpl_list()
              })
              .catch((err) => {
                this.$message({
                  type: "error",
                  message: err
                })
                this.tmpl_dialog = false
                this.get_tmpl_list()
              })
          }
        })
      } else if (this.dialog_status === "update_tmpl") {
        updateTmpl(this.tmpl_form.id, this.tmpl_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新成功"
            })
            this.tmpl_dialog = false
            this.get_tmpl_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.tmpl_dialog = false
            this.get_tmpl_list()
          })
      }
    },
    get_tmpl_list() {
      getTmplList(this.list_query)
        .then(resp => {
          this.tmpl_list = resp.data.results
          this.tmpl_list_total = resp.data.count
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
.el-button {
  vertical-align: top;
}
.el-table {
  width: 100%;
  margin-top: 10px;
}
</style>
