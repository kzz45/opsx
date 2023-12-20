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
              label="端口"
              value="port"
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
        <el-link disabled>此页面新增域名端口仅用于日常检查, 如需告警请出门</el-link>
        <el-link href="/cmdb/domain_ssl_alert_focus">右转</el-link>
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
          label="操作"
          width="120px"
        >
          <template slot-scope="{ row }">
            <el-tooltip
              v-if="checkPermission(['admin','ops'])"
              class="item"
              effect="dark"
              content="修改记录"
              placement="top"
            >
              <el-button
                type="primary"
                icon="el-icon-edit"
                size="mini"
                @click="edit_record(row)"
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
        @pagination="get_checkPort"
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
            placeholder="请填写端口号"
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
          @click="reset_record_create_form"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_create_record"
        >确 定</el-button>
      </span>
    </el-dialog>
    <el-dialog
      title="修改条目"
      :visible.sync="editRecordDialogFormVisible"
      width="50%"
    >
      <el-form
        :model="record_edit_form"
        label-width="100px"
      >
        <el-form-item
          label="域名"
          style="width:600px"
          prop="domain"
        >
          <el-input
            v-model="record_edit_form.domain"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="端口"
          style="width:600px"
          prop="port"
        >
          <el-input
            v-model="record_edit_form.port"
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
          @click="editRecordDialogFormVisible = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_edit_record"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import { getCheckPort, addCheckPort, updateCheckPort } from '@/views/cmdb/api/domain_record'
import checkPermission from "@/utils/permission"
export default {
  name: "DomainCheckPortList",
  components: { Pagination },
  data() {
    return {
      listQuery: {
        page: 1,
        limit: 15
      },
      action_type: '',
      input_content: '',
      searchParam: {
        domain: this.$route.query.domain,
        action: '',
        keyword: ''
      },
      record_create_form: {
        domain: '',
        port: ''
      },
      record_edit_form: {
        id: '',
        domain: '',
        port: ''
      },
      select_input: 'domain',
      createRecordDialogFormVisible: false,
      editRecordDialogFormVisible: false,
      operation_record_list: [],
      operation_record_list_all: [],
      operation_record_total: 0
    }
  },
  watch: {
    // 换了搜索对象就初始化记录
    select_input() {
      this.input_content = ''
      this.listQuery = new Map()
      this.listQuery["page"] = 1
      this.listQuery["limit"] = 15
      this.listQuery["domain"] = JSON.parse(this.$route.query.domain_info).domain
      this.get_checkPort()
    }
  },
  created() {
    this.get_checkPort()
  },
  methods: {
    checkPermission,
    // set_keyword(param) {
    //   var searchVal = param.toLowerCase()
    //   this.searchParam.keyword = searchVal
    // },
    search_handler() {
      const params = this.select_input
      this.listQuery.page = 1
      if (this.input_content !== '') {
        this.listQuery[params] = this.input_content
      } else {
        delete this.listQuery[params]
      }
      this.get_checkPort()
    },
    get_checkPort() {
      getCheckPort(this.listQuery).then(response => {
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
      // console.log("record_create_form", this.record_create_form)
      addCheckPort(this.record_create_form)
        .then((res) => {
          if (res.data.code !== "0") {
            this.$message({
            type: "error",
            message: res.data.message
          })
          this.$refs.record_create_formRefs.resetFields()
          } else {
          this.$message({
            type: "success",
            message: "创建成功"
          })
          this.$refs.record_create_formRefs.resetFields()
          }
          this.createRecordDialogFormVisible = false
          this.get_checkPort()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
          this.$refs.record_create_formRefs.resetFields()
        })
      this.get_checkPort()
      this.createRecordDialogFormVisible = false
    },
    // 修改记录
    edit_record(param) {
      this.editRecordDialogFormVisible = true
      this.record_edit_form.id = param.id
      this.record_edit_form.domain = param.domain
      this.record_edit_form.port = param.port
    },
    // 提交修改的解析
    submit_edit_record() {
      updateCheckPort(this.record_edit_form)
        .then((res) => {
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
          this.editRecordDialogFormVisible = false
          this.get_checkPort()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
      this.get_checkPort()
      this.editRecordDialogFormVisible = false
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
