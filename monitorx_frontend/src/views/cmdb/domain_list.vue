<template>
  <div class="app-container">
    <el-card class="box-card">
      <!-- 搜索相关 -->
      <div>
        <el-input
          v-model="domain_input_content"
          placeholder="域名名称"
          size="small"
          class="filter-item"
          clearable
          @input="search_domain($event)"
        >
          <i
            slot="suffix"
            class="el-input__icon el-icon-search"
          ></i>
        </el-input>
        <el-tooltip
          effect="dark"
          content="SSL端口设置"
          placement="top-start"
        >
          <el-button
            v-if="checkPermission(['admin','ops'])"
            size="small"
            type="primary"
            icon="el-icon-edit-outline"
            style="margin-left: 10px"
            @click="view_ssl_check_port_list()"
          >
          </el-button>
        </el-tooltip>
        <el-tooltip
          effect="dark"
          content="SSL报警关注"
          placement="top-start"
        >
          <el-button
            v-if="checkPermission(['admin','ops'])"
            size="small"
            type="success"
            icon="el-icon-view"
            style="margin-left: 10px"
            @click="view_ssl_alert_focus()"
          >
          </el-button>
        </el-tooltip>
      </div>
      <el-table
        :data="domain_list"
        style="width: 100%; margin-top: 10px"
        border
        size="small"
      >
        <el-table-column
          prop="domain"
          label="主域名"
        >
        </el-table-column>
        <el-table-column
          prop="supplier"
          label="厂商"
        >
        </el-table-column>
        <el-table-column
          label="操作"
          width="120px;"
        >
          <template slot-scope="scoped">
            <el-tooltip
              class="item"
              effect="dark"
              content="记录值"
              placement="top"
            >
              <el-button
                type="primary"
                icon="el-icon-aim"
                size="mini"
                @click="view_record_detail(scoped.row)"
              ></el-button>
            </el-tooltip>
            <el-tooltip
              v-if="checkPermission(['admin','ops'])"
              class="item"
              effect="dark"
              content="操作记录"
              placement="top"
            >
              <el-button
                type="primary"
                icon="el-icon-tickets"
                size="mini"
                @click="view_operation_record(scoped.row)"
              ></el-button>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>
      <pagination
        v-show="domain_total>0"
        :total="domain_total"
        :page.sync="listQuery.page"
        :limit.sync="listQuery.limit"
        @pagination="get_domain_list"
      ></pagination>
    </el-card>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"
import { getDomainList } from "@/views/cmdb/api/domain_record"
import checkPermission from "@/utils/permission"

export default {
  name: "DomainList",
  components: {
    Pagination
  },
  data() {
    return {
      listQuery: {
        page: 1,
        limit: 15
      },
      domain_input_content: "",
      domain_list: [],
      domain_list_for_search: [],
      domain_total: 0
    }
  },
  computed: {},
  created() {
    this.get_domain_list()
  },
  methods: {
    checkPermission,
    // 获取域名列表
    get_domain_list() {
      getDomainList(this.listQuery)
        .then(response => {
          this.domain_list_for_search = response.data.resultList
          this.domain_list = response.data.resultList.slice(
            (this.listQuery.page - 1) * this.listQuery.limit,
            this.listQuery.page * this.listQuery.limit
          )
          this.domain_total = response.data.totalNumber
          setTimeout(() => {
            this.listLoading = false
          }, 1.5 * 1000)
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 搜索域名
    search_domain(param) {
      var searchVal = param.toLowerCase()
      var newListData = []
      if (searchVal !== "") {
        this.domain_list_for_search.filter(item => {
          if (item.domain.toLowerCase().indexOf(searchVal) !== -1) {
            newListData.push(item)
          }
        })
        this.domain_list = newListData
      } else {
        this.get_domain_list()
      }
    },
    // 查看记录详情
    view_record_detail(row) {
      const parObj = JSON.stringify(row)
      this.$router.push({
        path: "/cmdb/domain_record_list/",
        query: { domain_info: parObj }
      })
    },
    // 查看操作记录
    view_operation_record(row) {
      this.$router.push({
        path: "/cmdb/domain_operation_record/",
        query: { domain: row.domain }
      })
    },
    view_ssl_check_port_list() {
      this.$router.push({
        path: "/cmdb/domain_ssl_check_port/"
      })
    },
    view_ssl_alert_focus() {
      this.$router.push({
        path: "/cmdb/domain_ssl_alert_focus/"
      })
    }
  }
}
</script>

<style scoped>
.el-table {
  margin-top: 15px;
}
.el-select {
  width: 120px;
}
.el-input {
  width: 300px;
}
.iconfont_green {
  font-family: "iconfont" !important;
  font-size: 20px;
  font-style: normal;
  color: #67c23a;
}
.iconfont_red {
  font-family: "iconfont" !important;
  font-size: 20px;
  font-style: normal;
  color: #f56c6c;
}
.table-expand {
  font-size: 0;
}
.table-expand label {
  width: 90px;
  color: #99a9bf;
}
.table-expand .el-form-item {
  margin-right: 0;
  margin-bottom: 0;
  width: 50%;
}
</style>
