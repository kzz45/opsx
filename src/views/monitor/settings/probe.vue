<template>
  <div>
    <el-button
      type="primary"
      size="small"
      icon="el-icon-circle-plus"
      @click="create_probe"
    >新增</el-button>
    <el-table
      ref="probe_list_table_refs"
      :data="probe_list"
      empty-text="啥也没有"
      size="small"
      border
    >
      <el-table-column
        label="名称"
        prop="name"
      ></el-table-column>
      <el-table-column
        label="标识"
        prop="uuid"
      ></el-table-column>
      <el-table-column
        label="API地址"
        prop="api"
      ></el-table-column>
      <el-table-column
        label="模式"
        prop="mode"
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
            @click="update_probe(scoped.row)"
          ></el-button>
          <el-popconfirm
            title="确定删除吗？"
            confirm-button-text="确定"
            cancel-button-text="不了"
            style="margin-left: 10px"
            @confirm="delete_probe(scoped.row)"
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
      v-show="probe_list_total>0"
      :total="probe_list_total"
      :page.sync="list_query.page"
      :limit.sync="list_query.limit"
      @pagination="get_probe_list"
    ></pagination>
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="probe_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="50%"
    >
      <el-form
        ref="probe_formRefs"
        :model="probe_form"
        :rules="probe_form_rules"
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
                v-model="probe_form.name"
                size="small"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="标识"
              prop="uuid"
            >
              <el-input
                v-model="probe_form.uuid"
                size="small"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="API地址"
              prop="api"
            >
              <el-input
                v-model="probe_form.api"
                size="small"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="IP地址"
              prop="ipaddr"
            >
              <el-input
                v-model="probe_form.ipaddr"
                size="small"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="模式"
              prop="mode"
            >
              <el-select
                v-model="probe_form.mode"
                placeholder="请选择模式"
              >
                <el-option
                  label="http/tcp"
                  value="http/tcp"
                ></el-option>
                <el-option
                  label="ping"
                  value="ping"
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
          @click="probe_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_probe"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"
import { createProbe, updateProbe, getProbeList, deleteProbe } from '@/views/monitor/apis/probe'

export default {
  name: "ProbeSetting",
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
        create_probe: "新增探测点",
        update_probe: "编辑探测点"
      },
      dialog_status: "",
      // 探测节点管理--------------------------------------------------
      probe_list: [],
      probe_list_total: 0,
      probe_dialog: false,
      probe_mode_list: [],
      probe_form: {
        id: null,
        name: null,
        api: null,
        ipaddr: null,
        uuid: null,
        mode: 'http/tcp'
      },
      probe_form_rules: {
        name: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        api: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        ipaddr: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        uuid: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        mode: [{ required: true, message: "该项不能为空", trigger: "blur" }]
      }
    }
  },
  methods: {
    create_probe() {
      this.dialog_status = "create_probe"
      this.probe_dialog = true
    },
    update_probe(row) {
      this.dialog_status = "update_probe"
      this.probe_dialog = true
      this.probe_form = Object.assign({}, row)
    },
    delete_probe(row) {
      deleteProbe(row.id)
        .then(() => {
          this.$message({
            type: "success",
            message: "删除成功"
          })
          this.get_probe_list()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
          this.get_probe_list()
        })
    },
    submit_probe() {
      if (this.dialog_status === "create_probe") {
        this.$refs.probe_formRefs.validate((valid) => {
          if (valid) {
            createProbe(this.probe_form)
              .then(() => {
                this.$message({
                  type: "success",
                  message: "新增成功"
                })
                this.probe_dialog = false
                this.get_probe_list()
              })
              .catch((err) => {
                this.$message({
                  type: "error",
                  message: err
                })
                this.probe_dialog = false
                this.get_probe_list()
              })
          }
        })
      } else if (this.dialog_status === "update_probe") {
        updateProbe(this.probe_form.id, this.probe_form)
          .then(resp => {
            this.$message({
              type: "success",
              message: "更新成功"
            })
            this.probe_dialog = false
            this.get_probe_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.probe_dialog = false
            this.get_probe_list()
          })
      }
    },
    get_probe_list() {
      getProbeList(this.list_query)
        .then(resp => {
          this.probe_list = resp.data.results
          this.probe_list_total = resp.data.count
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
