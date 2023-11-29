<template>
  <div class="app-container">
    <el-card class="box-card">
      <!--  搜索相关  -->
      <div>
        <el-button
          size="small"
          icon="el-icon-back"
          @click="go_back"
        >返回</el-button>
        <el-input
          v-model="input_content"
          placeholder="关键字"
          class="input-with-select"
          size="small"
          clearable
          style="width: 400px; margin-left: 10px"
        >
          <el-select
            slot="prepend"
            v-model="select_input"
            size="small"
            placeholder="请选择"
            style="width: 100px;"
          >
            <el-option
              label="域名"
              value="domain"
            ></el-option>
            <el-option
              label="证书状态"
              value="certStatus"
            ></el-option>
          </el-select>
          <el-button
            slot="append"
            icon="el-icon-search"
            @click="search_handler"
          ></el-button>
        </el-input>
        <el-button
          v-if="checkPermission(['admin','ops'])"
          type="primary"
          size="small"
          icon="el-icon-circle-plus"
          style="margin-left: 10px"
          @click="create_record"
        >新增</el-button>
      </div>
      <el-table
        :data="operation_record_list"
        size="small"
        style="width: 100%; margin-top: 10px"
        border
      >
        <el-table-column
          prop="id"
          label="ID"
        >
        </el-table-column>
        <el-table-column
          prop="domain"
          label="域名"
        >
        </el-table-column>
        <el-table-column
          prop="port"
          label="端口"
        >
        </el-table-column>
        <el-table-column
          prop="certStatus"
          label="证书状态"
          :filters="[
            { text: '正常', value: 'Safe' },
            { text: '即将到期', value: 'Expiring' },
            { text: '错误', value: 'Wrong' },
            { text: '过期', value: 'Expired' },
          ]"
          :filter-method="filterHandler"
        >
          <template slot-scope="scoped">
            <el-tag
              v-if="scoped.row.certStatus === 'Wrong'"
              type="danger"
            >错误</el-tag>
            <el-tag
              v-if="scoped.row.certStatus === 'Expired'"
              type="danger"
            >过期</el-tag>
            <el-tag
              v-if="scoped.row.certStatus === 'Safe'"
              type="success"
            >正常</el-tag>
            <el-tag
              v-if="scoped.row.certStatus === 'Expiring'"
              type="warning"
            >即将到期</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="noticeGroupName"
          label="通知组"
        >
        </el-table-column>
        <el-table-column
          label="操作"
          width="120px"
        >
          <template slot-scope="{ row }">
            <el-tooltip
              v-if="checkPermission(['admin','ops'])"
              class="item"
              effect="dark"
              content="检查证书"
              placement="top"
            >
              <el-button
                type="success"
                icon="el-icon-s-promotion"
                size="mini"
                @click="check_record(row)"
              ></el-button>
            </el-tooltip>
            <el-tooltip
              v-if="checkPermission(['admin','ops'])"
              class="item"
              effect="dark"
              content="删除条目"
              placement="top"
            >
              <el-button
                type="danger"
                icon="el-icon-delete"
                size="mini"
                @click="delete_record(row)"
              ></el-button>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <pagination
        v-show="operation_record_total>0"
        :total="operation_record_total"
        :page.sync="listQuery.page"
        :limit.sync="listQuery.limit"
        @pagination="get_alertFocus"
      ></pagination>
    </el-card>
    <el-dialog
      title="新增条目"
      :visible.sync="createRecordDialogFormVisible"
      width="50%"
    >
      <el-form
        ref="record_create_formRefs"
        :model="record_create_form"
        label-width="100px"
      >
        <el-form-item
          label="域名"
          style="width:300px"
          prop="domain"
        >
          <el-input
            v-model="record_create_form.domain"
            placeholder="请填写完整域名"
            oninput="value=value.replace(' ','')"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="端口"
          style="width:300px"
          prop="port"
        >
          <el-input
            v-model="record_create_form.port"
            placeholder="请填写端口, 默认为443"
            oninput="value=value.replace(/[^\d]/g,'')"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="通知组"
          style="width:300px"
          prop="noticeGroup"
        >
          <el-select
            v-model="record_create_form.noticeGroupName"
            size="small"
            clearable
            filterable
            style="width: 300px"
            @change="set_params($event)"
          >
            <el-option
              v-for="item in alert_group_list"
              :key="item.name"
              :label="item.name"
              :value="{NoticeGroupName: item.name, WebhookUrl: item.webhook}"
            ></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="reset_record_create_form"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_create_record"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import { getAlertFocus, addAlertFocust, delAlertFocust, checkSsl } from '@/views/cmdb/api/domain_record'
import { getAlertUserGroupList } from '@/views/monitor/api/alert_user_group'
import checkPermission from "@/utils/permission"
export default {
  name: "DomainAlertFocus",
  components: { Pagination },
  data() {
    return {
      listQuery: {
        page: 1,
        limit: 15,
        user: this.$store.getters.name
      },
      input_content: '',
      record_create_form: {
        domain: '',
        noticeGroupName: '',
        webhookUrl: '',
        port: '443',
        user: this.$store.getters.name
      },
      select_input: 'domain',
      createRecordDialogFormVisible: false,
      operation_record_list: [],
      operation_record_list_all: [],
      operation_record_total: 0,
      alert_group_list: []
    }
  },
  watch: {
    // 换了搜索对象就初始化记录
    select_input() {
      this.input_content = ''
      this.listQuery = new Map()
      this.listQuery["page"] = 1
      this.listQuery["limit"] = 15
    }
  },
  created() {
    this.get_alertFocus()
    this.get_notice_group_list()
  },
  methods: {
    checkPermission,
    check_record(param) {
      var requestBody = {}
      requestBody["domain"] = param.domain
      requestBody["port"] = param.port
      checkSsl(requestBody)
        .then(resp => {
          // console.log("checkSsl", resp)
          if (resp.data.code === "0") {
            this.$message({
              message: '正在检查证书, 请稍候刷新页面确认',
              type: 'success'
            })
            this.get_alertFocus()
          } else {
            this.$message({
              message: '检查出错, ' + resp.data.message,
              type: 'error'
            })
            this.get_alertFocus()
          }
        })
        .catch(error => {
          this.$message({
            message: '检查失败' + error,
            type: 'error'
          })
        })
    },
    set_params(param) {
      this.record_create_form.noticeGroupName = param.NoticeGroupName
      this.record_create_form.webhookUrl = param.WebhookUrl
    },
    get_notice_group_list() {
      this.listQuery["limit"] = 999
      getAlertUserGroupList(this.listQuery)
        .then(resp => {
          // console.log("get_notice_group_list", resp.data.results)
          this.alert_group_list = resp.data.results
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    filterHandler(value, row, column) {
      const property = column['property']
      return row[property] === value
    },
    search_handler() {
      const params = this.select_input
      this.listQuery.page = 1
      if (this.input_content !== '') {
        this.listQuery[params] = this.input_content
      } else {
        delete this.listQuery[params]
      }
      this.get_alertFocus()
    },
    get_alertFocus() {
      getAlertFocus(this.listQuery).then(response => {
        if (response.data.data == null) {
          this.operation_record_list = []
          this.operation_record_total = 0
        } else {
          this.operation_record_list_all = response.data.data
          this.operation_record_list = response.data.data.slice((this.listQuery.page - 1) * this.listQuery.limit, (this.listQuery.page) * this.listQuery.limit)
          this.operation_record_total = response.data.totalNumber
        }
      })
    },
    go_back() {
      this.$router.push({ name: "DomainList", params: { active_tab_name: "domain_resouce" } })
    },
    create_record() {
      this.createRecordDialogFormVisible = true
    },
    reset_record_create_form() {
      this.createRecordDialogFormVisible = false
      this.$refs.record_create_formRefs.resetFields()
    },
     // 提交创建的记录
     submit_create_record() {
      if (this.record_create_form.port.replaceAll('0', '') === '') {
        this.$message({
          type: "error",
          message: "端口都是0, 你认真的??"
        })
        return
      }
      addAlertFocust(this.record_create_form)
        .then((res) => {
          // console.log("addAlertFocust", this.record_create_form)
          if (res.data.code !== "0") {
            this.$message({
            type: "error",
            message: res.data.message
          })
          this.$refs.record_create_formRefs.resetFields()
          } else {
          this.$message({
            type: "success",
            message: "添加成功"
          })
          this.$refs.record_create_formRefs.resetFields()
          }
          this.createRecordDialogFormVisible = false
          this.get_alertFocus()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
          this.$refs.record_create_formRefs.resetFields()
        })
      this.get_alertFocus()
      this.createRecordDialogFormVisible = false
    },
    // 删除记录
    delete_record(param) {
      delAlertFocust(param.id)
      .then((res) => {
        // console.log("delAlertFocust", res)
          if (res.data.code !== "0") {
            this.$message({
            type: "error",
            message: res.data.message
          })
          } else {
          this.$message({
            type: "success",
            message: "修改成功"
          })
          }
          this.get_alertFocus()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
      this.get_alertFocus()
    }
  }
}
</script>

<style scoped>
.el-select {
  width: 300px;
}
.el-input {
  width: 300px;
}
</style>
