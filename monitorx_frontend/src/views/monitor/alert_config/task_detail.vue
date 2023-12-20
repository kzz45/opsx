任务详情页面

<template>
  <div class="app-container">
    <el-card class="box-card">
      <div style="margin-top: 10px;">
        <el-button
          icon="el-icon-back"
          size="small"
          @click="go_back"
        >返回</el-button>
        <el-button
          type="primary"
          icon="el-icon-circle-plus-outline"
          size="small"
          @click="create_add_on"
        >新增子任务</el-button>
      </div>
      <div>
        <el-table
          :data="add_on_list"
          size="small"
          border
        >
          <el-table-column
            label="任务名称"
            prop="name"
          >
          </el-table-column>
          <el-table-column label="任务详情">
            <template slot-scope="scoped">
              {{ !scoped.row.probe? scoped.row.scheme +'://\{\{ instance \}\}:'+ scoped.row.port + scoped.row.args:scoped.row.scheme +'://'+ scoped.row.probe__api +scoped.row.probe_args }}
            </template>
          </el-table-column>
          <el-table-column
            label="间隔时间"
            prop="interval"
          >
          </el-table-column>
          <el-table-column
            label="超时时间"
            prop="timeout"
          >
          </el-table-column>
          <el-table-column
            label="操作"
            prop="options"
          >
            <template slot-scope="scoped">
              <el-button
                type="primary"
                icon="el-icon-edit"
                size="mini"
                @click="update_add_on(scoped.row)"
              ></el-button>
              <el-popconfirm
                title="确定删除吗？"
                confirm-button-text="确定"
                cancel-button-text="不了"
                style="margin-left: 10px"
                @confirm="delete_add_on(scoped.row)"
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
          v-show="add_on_list_total>0"
          :total="add_on_list_total"
          :page.sync="list_query.page"
          :limit.sync="list_query.limit"
          @pagination="get_add_on_list"
        >
        </pagination>
      </div>
    </el-card>
    <!-- 子任务的Dialog -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="add_on_dialog"
      width="50%"
    >
      <el-form
        ref="add_on_formRefs"
        :model="add_on_form"
        :rules="add_on_form_rules"
        label-width="100px"
        size="small"
      >
        <el-form-item
          label="任务名称"
          prop="name"
        >
          <el-input
            v-model="add_on_form.name"
            clearable
            placeholder="请输入任务抓取的名称"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="间隔时间"
          prop="interval"
        >
          <el-input-number
            v-model="add_on_form.interval"
            placeholder="请输入抓取的间隔时间"
            style="width: 300px"
          >
          </el-input-number>
        </el-form-item>
        <el-form-item
          label="超时时间"
          prop="timeout"
        >
          <el-input-number
            v-model="add_on_form.timeout"
            placeholder="请输入抓取的超时时间"
            style="width: 300px"
          ></el-input-number>
        </el-form-item>
        <el-form-item
          label="任务筛选"
          prop="style"
        >
          <el-select
            v-model="add_on_form.style"
            clearable
            placeholder="请选择类型"
            style="width: 140px;"
          >
            <el-option
              label="机器"
              value="machine"
            ></el-option>
            <el-option
              label="探测"
              value="probe"
            ></el-option>
            <el-option
              label="自定义"
              value="custom"
            ></el-option>
          </el-select>
          <el-select
            v-model="add_on_form.module"
            clearable
            style="width: 140px; margin-left: 20px;"
          >
            <el-option
              v-if="add_on_form.style === 'machine'"
              label="端口"
              value="port"
            ></el-option>
            <el-option
              v-if="add_on_form.style === 'machine'"
              label="进程"
              value="process"
            ></el-option>
            <el-option
              v-if="add_on_form.style === 'machine'"
              label="脚本"
              value="script"
            ></el-option>
            <el-option
              v-if="add_on_form.style === 'probe'"
              label="HTTP/HTTPS"
              value="http"
            ></el-option>
            <el-option
              v-if="add_on_form.style === 'probe'"
              label="TCP"
              value="tcp"
            ></el-option>
            <el-option
              v-if="add_on_form.style === 'probe'"
              label="PING"
              value="ping"
            ></el-option>
            <el-option
              v-if="add_on_form.style === 'custom'"
              label="proxy模式"
              value="proxy"
            ></el-option>
            <el-option
              v-if="add_on_form.style === 'custom'"
              label="direct模式"
              value="direct"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          v-if="add_on_form.module === 'port'||add_on_form.module === 'tcp'||add_on_form.module === 'direct'"
          label="端口号"
          prop="port"
        >
          <div
            v-for="(item, index) in port_list"
            :key="index"
          >
            <el-input-number
              v-model="item.port"
              placeholder="请输入端口号"
              style="width:300px; margin-top: 2px;"
            ></el-input-number>
            <el-button
              type="danger"
              size="small"
              :disabled="port_list.length === 1? true: false"
              style="margin-left: 10px; margin-top: 2px;"
              @click="del_port(item)"
            >-</el-button>
            <el-button
              type="primary"
              size="small"
              style="margin-left: 10px; margin-top: 2px;"
              @click="add_port"
            >+</el-button>
          </div>
        </el-form-item>
        <el-form-item
          v-if="add_on_form.module === 'process'"
          label="进程"
        >
          <div
            v-for="(item, index) in process_list"
            :key="index"
          >
            <el-input
              v-model="item.name"
              placeholder="请输入名称"
              clearable
              style="width: 140px"
            ></el-input>
            <el-input
              v-model="item.cmdline"
              placeholder="请输入cmline"
              clearable
              style="width: 140px; margin-left: 20px;"
            ></el-input>
            <el-button
              type="danger"
              size="small"
              :disabled="process_list.length === 1? true: false"
              style="margin-left: 10px; margin-top: 2px;"
              @click="del_process(item)"
            >-</el-button>
            <el-button
              type="primary"
              size="small"
              style="margin-left: 10px; margin-top: 2px;"
              @click="add_process"
            >+</el-button>
          </div>
        </el-form-item>
        <el-form-item
          v-if="add_on_form.module === 'script'"
          label="脚本名称"
        >
          <div
            v-for="(item, index) in script_list"
            :key="index"
          >
            <el-input
              v-model="item.script"
              placeholder="请输入脚本名称或者脚本目录"
              clearable
            ></el-input>
            <el-button
              type="primary"
              size="small"
              style="margin-left: 10px;"
            >+</el-button>
          </div>
        </el-form-item>
        <el-form-item
          v-if="add_on_form.module === 'http'"
          label="url"
          prop="taskUrl"
        >
          <el-input
            v-model="add_on_form.taskUrl"
            placeholder="请输入URL地址"
            clearable
          ></el-input>
        </el-form-item>
        <el-form-item
          v-if="add_on_form.style === 'probe' || add_on_form.module === 'proxy'"
          label="探测节点"
          prop="probe"
        >
          <el-select
            v-model="add_on_form.probe"
            clearable
            style="width: 300px"
          >
            <el-option
              v-for="(item, index) in probe_list"
              :key="index"
              :value="item.id"
              :label="item.name"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          v-if="add_on_form.module === 'direct'"
          label="请求方式"
          prop="scheme"
        >
          <el-radio-group v-model="add_on_form.scheme">
            <el-radio label="http">http</el-radio>
            <el-radio label="https">https</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item
          v-if="add_on_form.module === 'proxy'"
          label="代理参数"
          prop="paramlist"
        >
          <el-input
            v-model="add_on_form.paramlist"
            :autosize="{ minRows:2}"
            clearable
            :placeholder="'支持宏变量 可选{{ instance.endpoint }}, {{ instance.ip }}, {{ instance.name }}'"
            type="textarea"
            style="width: 300px;"
          ></el-input>
        </el-form-item>
        <el-form-item
          v-if="add_on_form.module === 'direct'"
          label="请求参数"
          prop="args"
        >
          <el-input
            v-model="add_on_form.args"
            clearable
            placeholder="请输入参数名称"
          ></el-input>
        </el-form-item>
        <el-form-item
          v-if="params_data.instance_type__name !== 'machine'"
          label="采集服务器"
          prop="server_group"
        >
          <el-select
            v-model="add_on_form.server_group"
            size="small"
            style="width: 300px"
          >
            <el-option
              v-for="(item, index) in server_group_list"
              :key="index"
              :value="item.id"
              :label="item.name"
            ></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button
          size="small"
          @click="add_on_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_add_on"
        >确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"
import { getServerGroupList } from '@/views/monitor/api/server_group'
import { getAddOnList, createAddOn, updateAddOnByID, deleteAddOnByID } from '@/views/monitor/api/addon'

export default {
  name: "TaskDetail",
  components: {
    Pagination
  },
  data() {
    return {
      list_query: {
        page: 1,
        limit: 15,
        task__id: ''
      },
      // 上层任务传递过来的
      params_data: {
        id: null,
        instance_type__name: null
      },
      add_on_list: [], // 子任务列表
      add_on_list_total: 0,
      dialog_map: {
        create_pull: "新增抓取子任务",
        update_pull: "编辑抓取子任务"
      },
      dialog_status: "",
      add_on_dialog: false,
      add_on_form: {
        id: null,
        name: null,
        style: '',
        module: '',
        interval: 60, // 间隔时间
        timeout: 50, // 超时时间
        port: 2021, // 这个是客户端的端口
        taskUrl: '',
        taskPort: '',
        scheme: 'http',
        probe_args: '',
        paramlist: '',
        request: '',
        args: '',
        paramList: null
      },
      add_on_form_rules: {
        name: [{ required: true, message: '该项不能为空', trigger: 'blur' }],
        interval: [{ required: true, message: '该项不能为空', trigger: 'blur' }],
        timeout: [{ required: true, message: '该项不能为空', trigger: 'blur' }],
        module: [{ required: true, message: '该项不能为空', trigger: 'blur' }],
        probe: [{ required: true, message: '该项不能为空', trigger: 'blur' }],
        paramlist: [{ required: true, message: '该项不能为空', trigger: 'blur' }],
        args: [{ required: true, message: '该项不能为空', trigger: 'blur' }],
        taskPort: [{ required: true, message: '该项不能为空', trigger: 'blur' }],
        taskUrl: [{ required: true, message: '该项不能为空', trigger: 'blur' }],
        server_group: [{ required: true, message: '该项不能为空', trigger: 'blur' }]
      },
      port_list: [{ port: '2021' }],
      script_list: [{ script: '' }],
      process_list: [{ name: '', cmdline: '' }],
      probe_list: [],
      server_group_list: []
    }
  },
  created() {
    this.params_data.id = this.$route.query.id
    this.params_data.instance_type__name = this.$route.query.instance_type__name
    this.list_query.task__id = this.$route.query.id
    this.get_server_group_list()
    this.get_add_on_list()
  },
  methods: {
    go_back() {
      this.$router.push({ name: "AlertConfig", params: { active_tab_name: 'task_manage' } })
    },
    create_add_on() {
      this.add_on_dialog = true
      this.dialog_status = "create_pull"
      this.add_on_form.name = null
      this.add_on_form.style = null
      this.add_on_form.module = null
      // if (this.$refs.add_on_formRefs) {
      //   this.$refs.add_on_formRefs.resetFields()
      // }
    },
    update_add_on(row) {
      this.add_on_dialog = true
      this.dialog_status = "update_pull"
      this.add_on_form = Object.assign({}, this.add_on_form, row)
      // 端口监控
      if (row.module === 'port') {
        this.port_list = []
        row.args.split(/=(?=.)/)[1].split(',').map(item => {
          this.port_list.push({ port: item })
        })
      }
      // 进程监控
      if (row.module === "process") {
        this.process_list = []
        row.args.split(/=(?=.)/)[1].split('|').map(item => {
          // console.log(item.split(',')[0], item.split(',')[1])
          this.process_list.push({ name: item.split(',')[0], cmdline: item.split(',')[1] })
        })
      }
      // direct模式
      if (row.module === 'direct') {
        this.add_on_form.paramList = row.probe_args
        this.add_on_form.args = row.args
        this.port_list = [{ port: row.port }]
      }
    },
    submit_add_on() {
      if (this.dialog_status === "create_pull") {
        var post_data = Object.assign({}, this.add_on_form)
        post_data.task = this.params_data.id
        if (post_data.style === 'machine') {
          // 机器类型
          post_data.port = 2021
          var create_str = ''
          if (this.add_on_form.module === 'port') {
            // 端口监控
            this.port_list.forEach(item => {
              create_str += item.port + ',' // 多个端口逗号分隔
            })
            post_data.args = '/port/?port=' + create_str.slice(0, -1)
          } else if (this.add_on_form.module === "process") {
            // 进程监控
            this.process_list.forEach(item => {
              create_str += item.name + ',' + item.cmdline + '|' // 多个进程组竖线分隔
            })
            post_data.args = '/process/?list=' + create_str.slice(0, -1)
          } else if (this.add_on_form.module === "script") {
            // 脚本监控
            this.script_list.forEach(item => {
              create_str += item.script + ',' // 多个脚本逗号分隔
            })
            post_data.args = '/script/?name=' + create_str.slice(0, -1)
          }
        } else if (this.add_on_form.style === "probe") {
          // 探测类型
          if (this.add_on_form.module === 'http') {
            // http 探测(服务域名之类)
            post_data.probe_args = '/probe/?module=http_2xx&target={{ instance }}' + this.add_on_form.taskUrl
          } else if (this.add_on_form.module === 'tcp') {
            // tcp 探测(服务tcp类型)
            post_data.probe_args = '/probe/?module=tcp&target={{ instance }}:' + this.port_list[0].port
          } else {
            // ping 探测(服务网络健康状态之ping服务)
            post_data.probe_args = '/probe/?module=icmp&target={{ instance }}'
          }
        } else if (this.add_on_form.style === "custom") {
          // 自定义类型
          if (this.add_on_form.module === 'proxy') {
            // 代理模式
            this.add_on_form.probe_args = this.add_on_form.paramlist
          } else if (this.add_on_form.module === "direct") {
            // 直接模式
            post_data.port = this.port_list[0].port
            post_data.args = this.add_on_form.request
            post_data.server_group = this.add_on_form.server_group
          }
        }
        createAddOn(post_data)
          .then(resp => {
            this.$message({
              type: "success",
              message: "新增子任务成功"
            })
            this.add_on_dialog = false
            this.get_add_on_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.add_on_dialog = false
            this.get_add_on_list()
          })
      } else if (this.dialog_status === "update_pull") {
        var update_data = Object.assign({}, this.add_on_form)
        update_data.task = this.params_data.id
        if (update_data.style === 'machine') {
          // 机器类型
          update_data.port = 2021
          var update_str = ''
          if (this.add_on_form.module === 'port') {
            // 端口监控
            this.port_list.forEach(item => {
              update_str += item.port + ',' // 多个端口逗号分隔
            })
            update_data.args = '/port/?port=' + update_str.slice(0, -1)
          } else if (this.add_on_form.module === "process") {
            // 进程监控
            this.process_list.forEach(item => {
              update_str += item.name + ',' + item.cmdline + '|' // 多个进程组竖线分隔
            })
            update_data.args = '/process/?list=' + update_str.slice(0, -1)
          } else if (this.add_on_form.module === "script") {
            // 脚本监控
            this.script_list.forEach(item => {
              update_str += item.script + ',' // 多个脚本逗号分隔
            })
            update_data.args = '/script/?name=' + update_str.slice(0, -1)
          }
        }
        updateAddOnByID(update_data.id, update_data)
          .then(resp => {
            this.$message({
              type: "success",
              message: "更新任务成功"
            })
            this.add_on_dialog = false
            this.get_add_on_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.add_on_dialog = false
            this.get_add_on_list()
          })
      }
    },
    delete_add_on(row) {
      deleteAddOnByID(row.id)
        .then(resp => {
          this.$message({
            type: "success",
            message: "删除任务成功"
          })
          this.get_add_on_list()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
          this.get_add_on_list()
        })
    },
    cancel_delete() {
      this.$message({
        type: "warning",
        message: "你考虑的很全面..."
      })
    },
    get_add_on_list() {
      getAddOnList(this.list_query)
        .then(resp => {
          this.add_on_list = resp.data.results
          this.add_on_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    get_probe_list() { },
    get_server_group_list() {
      getServerGroupList(this.list_query)
        .then(resp => {
          this.server_group_list = resp.data.results
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    add_port() {
      var port_value = ''
      this.port_list.push({ port: port_value })
    },
    del_port(item) {
      var index = this.port_list.indexOf(item)
      if (index !== -1) {
        this.port_list.splice(index, 1)
      }
    },
    add_process() {
      var process_name = ''
      var process_cmline = ''
      this.process_list.push({
        name: process_name,
        cmdline: process_cmline
      })
    },
    del_process(item) {
      var index = this.process_list.indexOf(item)
      if (index !== -1) {
        this.process_list.splice(index, 1)
      }
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
.el-button {
  vertical-align: top;
}
.el-tag {
  vertical-align: top;
}
</style>
