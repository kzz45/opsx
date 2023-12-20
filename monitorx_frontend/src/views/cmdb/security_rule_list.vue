<template>
  <div class="app-container">
    <el-card class="box-card">
      <!-- 搜索相关 -->
      <div>
        <el-button
          size="small"
          icon="el-icon-back"
          @click="go_back"
        >返回</el-button>
        <!-- <el-input
          v-model="listQuery.name__contains"
          placeholder="名称"
          class="filter-item"
          size="small"
          clearable
          @change="clear_refresh"
          @keyup.enter.native="search_filter"
        >
          <el-button
            slot="append"
            icon="el-icon-search"
            @click="search_filter"
          ></el-button>
        </el-input> -->
      </div>
      <!-- 安全组列表表格 -->
      <el-table
        :data="security_rule_list"
        style="width: 100%"
        border
        size="small"
      >
        <!-- <el-table-column
          prop="name"
          label="规则名称"
        >
        </el-table-column> -->
        <el-table-column
          v-if="supplier===3"
          prop="rule_id"
          label="规则 ID"
        >
        </el-table-column>
        <el-table-column
          prop="policy"
          label="策略"
        >
        </el-table-column>
        <el-table-column
          prop="direction"
          label="方向"
        >
        </el-table-column>
        <el-table-column
          prop="protocol"
          label="协议"
        >
        </el-table-column>
        <el-table-column
          prop="priority"
          label="优先级"
        >
        </el-table-column>
        <el-table-column
          prop="ip"
          label="对象"
        >
        </el-table-column>
        <el-table-column
          prop="port"
          label="端口"
        >
        </el-table-column>
        <el-table-column
          label="操作"
          width="120px;"
        >
          <el-button
            type="info"
            icon="el-icon-edit"
            size="mini"
            disabled
          ></el-button>
          <!-- <template slot-scope="{ row }">
            <el-tooltip
              class="item"
              effect="dark"
              content="没想好"
              placement="top"
            >
              <el-button
                type="warning"
                icon="el-icon-edit"
                size="mini"
              ></el-button>
            </el-tooltip>
            <el-tooltip
              class="item"
              effect="dark"
              content="没想好"
              placement="top"
            >
              <el-button
                type="danger"
                icon="el-icon-share"
                size="mini"
              ></el-button>
            </el-tooltip> -->
          <!-- </template> -->
        </el-table-column>
      </el-table>
      <!-- 分页组件 -->
      <pagination
        v-show="total>0"
        :total="total"
        :page.sync="listQuery.page"
        :limit.sync="listQuery.limit"
        @pagination="get_security_rule_list"
      ></pagination>
    </el-card>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import { getSecurityRuleList } from '@/views/cmdb/api/security'

export default {
  name: 'SecurityRuleList',
  components: { Pagination },
  data() {
    return {
      listQuery: {
        page: 1,
        limit: 15,
        security__security_id: this.$route.query.security_id
      },
      supplier: this.$route.query.supplier,
      vpc: this.$route.query.vpc,
      total: 0,
      security_rule_list: [],
      sync_loading: false
    }
  },
  computed: {
  },
  created() {
    this.get_security_rule_list()
  },
  methods: {
    get_security_rule_list() {
      getSecurityRuleList(this.listQuery)
        .then(response => {
          this.security_rule_list = response.data.results
          this.total = response.data.count
          setTimeout(() => {
            this.listLoading = false
          }, 1.5 * 1000)
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    view_security_rules(row) {
      // console.log("view_securityRules", row)
      this.$router.push({
        path: "/cmdb/security_rule_list/",
        query: { security__security_id: row.security_id }
      })
    },
    search_filter() {
      this.get_security_rule_list()
    },
    clear_refresh() {
      this.get_security_rule_list()
    },
    inter_subnet_detail(row) {
      this.$router.push('/settings/subnet_list')
    },
    go_back() {
      this.$router.push({
        path: "/cmdb/security_list/",
        query: { vpc: this.vpc, supplier: this.supplier }
      })
    }
  }
}
</script>

<style scoped>
.el-table {
  margin-top: 15px;
}
.el-input {
  width: 250px;
  margin-left: 10px;
}
.el-button {
  vertical-align: top;
}
</style>
