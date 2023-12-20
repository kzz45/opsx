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

        <el-select
          slot="prepend"
          v-model="action_type"
          size="small"
          placeholder="操作类别"
          style="width: 100px; margin-left: 10px"
        >
          <el-option
            label="全部操作"
            value=""
          ></el-option>
          <el-option
            label="添加记录"
            value="createRecord"
          ></el-option>
          <el-option
            label="修改记录"
            value="updateRecord"
          ></el-option>
          <el-option
            label="修改状态"
            value="updateRecordStatus"
          ></el-option>
        </el-select>
        <el-input
          v-model="input_content"
          placeholder="关键字"
          class="search-input-style"
          size="small"
          clearable
          style="width: 300px; margin-left: 10px"
          @input="set_keyword($event)"
        >
          <i
            slot="suffix"
            class="el-input__icon el-icon-search"
          ></i>
        </el-input>
        <el-button
          type="primary"
          size="small"
          style="margin-left: 10px"
          @click="search_record"
        >查询</el-button>
      </div>
      <el-table
        :data="operation_record_list"
        size="small"
        style="width: 100%; margin-top: 10px"
        border
      >
        <el-table-column
          prop="operator"
          label="操作人"
        >
        </el-table-column>
        <el-table-column
          prop="action"
          label="操作类别"
        >
        </el-table-column>
        <el-table-column
          prop="timeString"
          label="操作时间"
        >
        </el-table-column>
        <el-table-column
          prop="detail"
          label="详情"
        >
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <pagination
        v-show="operation_record_total>0"
        :total="operation_record_total"
        :page.sync="listQuery.page"
        :limit.sync="listQuery.limit"
        @pagination="get_audit"
      ></pagination>
    </el-card>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import { getRecordAudit } from '@/views/cmdb/api/domain_record'

export default {
  name: "DomainOperationRecord",
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
      operation_record_list: [],
      operation_record_list_all: [],
      operation_record_total: 0
    }
  },
  created() {
    this.get_audit()
  },
  methods: {
    set_keyword(param) {
      var searchVal = param.toLowerCase()
      this.searchParam.keyword = searchVal
    },
    search_record() {
      this.searchParam.action = this.action_type
      getRecordAudit(this.searchParam).then(res => {
        if (res.data.data == null) {
          this.operation_record_list = []
          this.operation_record_total = 0
        } else {
          this.operation_record_list_all = res.data.data
          this.operation_record_list = res.data.data.slice((this.listQuery.page - 1) * this.listQuery.limit, (this.listQuery.page) * this.listQuery.limit)
          this.operation_record_total = res.data.totalNumber
        }
      })
    },
    get_audit() {
      getRecordAudit(this.searchParam).then(response => {
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
