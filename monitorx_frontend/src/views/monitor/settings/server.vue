采集点页面

<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-button
        icon="el-icon-back"
        size="small"
        @click="go_back"
      >返回</el-button>
      <el-button
        type="primary"
        icon="el-icon-circle-plus-outline"
        size="small"
        @click="create_server"
      >
        新增
      </el-button>
      <el-table
        :data="server_list"
        size="small"
        border
      >
        <el-table-column
          label="采集点名称"
          prop="name"
        > </el-table-column>
        <el-table-column
          label="标识"
          prop="code"
        ></el-table-column>
        <el-table-column
          label="地址"
          prop="ipaddr"
        ></el-table-column>
        <el-table-column
          label="唯一ID"
          prop="uuid"
        ></el-table-column>
        <el-table-column
          label="操作"
          probe="options"
        >
          <template slot-scope="scoped">
            <el-button
              type="primary"
              icon="el-icon-edit"
              size="mini"
              @click="update_server(scoped.row)"
            ></el-button>
            <el-popconfirm
              title="确定删除吗？"
              confirm-button-text="确定"
              cancel-button-text="不了"
              style="margin-left:10px"
              @confirm="delete_server(scoped.row)"
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
    </el-card>
    <!-- 采集节点的Dialog -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="server_dialog"
      width="50%"
    >
      <el-form
        ref="server_formRefs"
        :model="server_form"
        :rules="server_form_rules"
        label-width="100px"
      >
        <el-form-item
          label="名称"
          prop="name"
        >
          <el-input
            v-model="server_form.name"
            placeholder="请输入采集节点名称"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="标识"
          prop="code"
        >
          <el-input
            v-model="server_form.code"
            placeholder="请输入采集节点标识"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="唯一ID"
          prop="uuid"
        >
          <el-input
            v-model="server_form.uuid"
            placeholder="请输入采集节点唯一ID"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="地址"
          prop="ipaddr"
        >
          <el-input
            v-model="server_form.ipaddr"
            placeholder="请输入采集节点地址"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="采集组名称"
          prop="server_group__name"
        >
          <el-input
            v-model="server_form.server_group__name"
            disabled
            size="small"
          ></el-input>
        </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="server_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_server"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { getServerList, createServer, updateServerByID, deleteServerByID } from "@/views/monitor/api/server"

export default {
  name: "Server",
  data() {
    return {
      list_query: {
        page: 1,
        limit: 15,
        server_group__id: ''
      },
      // 采集组传过来的信息
      server_group_info: {
        id: null,
        name: null,
        server_group__id: null,
        server_group__name: null
      },
      dialog_map: {
        create_server: "新增采集点",
        update_server: "编辑采集点"
      },
      // 采集节点相关--------------------------------------------------
      server_list: [],
      server_list_total: 0,
      dialog_status: '',
      server_dialog: false,
      server_form: {
        name: "",
        code: "",
        uuid: "",
        ipaddr: "",
        server_group: null,
        server_group__name: null
      },
      server_form_rules: {
        code: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        ipaddr: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        name: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        uuid: [{ required: true, message: "该项不能为空", trigger: "blur" }]
      }
    }
  },
  created() {
    this.server_group_info = JSON.parse(this.$route.query.server_group_info)
    this.server_form.server_group__name = this.server_group_info.name
    this.list_query.server_group__id = this.server_group_info.id
    this.server_form.server_group = this.server_group_info.id
    this.get_server_list()
  },
  methods: {
    get_server_list() {
      getServerList(this.list_query)
        .then(resp => {
          this.server_list = resp.data.results
          this.server_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    create_server() {
      this.server_dialog = true
      this.dialog_status = "create_server"
      this.server_form.name = null
      this.server_form.code = null
      this.server_form.uuid = null
      this.server_form.ipaddr = null
    },
    update_server(row) {
      this.server_dialog = true
      this.dialog_status = "update_server"
      this.server_form = Object.assign({}, row)
    },
    submit_server() {
      if (this.dialog_status === "create_server") {
        // console.log(this.server_form, '===')
        createServer(this.server_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "新增采集点【" + this.server_form.name + "】成功"
            })
            this.server_dialog = false
            this.get_server_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.server_dialog = false
            this.get_server_list()
          })
      } else if (this.dialog_status === "update_server") {
        updateServerByID(this.server_form.id, this.server_form)
          .then(resp => {
            this.$message({
              type: "success",
              message: "更新采集点【" + this.server_form.name + "】成功"
            })
            this.server_dialog = false
            this.get_server_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.server_dialog = false
            this.get_server_list()
          })
      }
    },
    delete_server(row) {
      deleteServerByID(row.id)
        .then(() => {
          this.$message({
            type: "success",
            message: "删除采集点【" + row.name + "】成功"
          })
          this.get_server_list()
        })
        .catch(() => {
          this.$message({
            type: "error",
            message: "删除采集点【" + row.name + "】失败"
          })
          this.get_server_list()
        })
    },
    cancel_delete() {
      this.$message({
        type: "warning",
        message: "你考虑的很全面..."
      })
    },
    go_back() {
      this.$router.push({ name: "MonitorSettings" })
    }
  }
}
</script>

<style scoped>
.el-table {
  width: 100%;
  margin-top: 10px;
}
.el-input {
  width: 300px;
}
</style>
