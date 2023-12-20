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
        <el-input
          v-model="listQuery.name__contains"
          placeholder="安全组名称"
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
        </el-input>
      </div>
      <!-- 安全组列表表格 -->
      <el-table
        :data="security_list"
        style="width: 100%"
        border
        size="small"
      >
        <el-table-column
          prop="name"
          label="安全组名称"
        >
        </el-table-column>
        <!-- <el-table-column
          prop="alias_name"
          label="安全组别名"
        >
        </el-table-column> -->
        <el-table-column
          prop="security_id"
          label="安全组 ID"
        >
        </el-table-column>

        <el-table-column
          prop="desc"
          label="描述"
        >
        </el-table-column>
        <!-- <el-table-column
          prop="vpc__name"
          label="VPC"
        >
        </el-table-column> -->

        <el-table-column
          label="操作"
          width="120px;"
        >
          <template slot-scope="{ row }">
            <el-button
              v-if="checkPermission(['admin','ops'])"
              type="warning"
              icon="el-icon-edit"
              size="mini"
              @click="edit_security_info(row)"
            ></el-button>
            <el-tooltip
              class="item"
              effect="dark"
              content="规则详情"
              placement="top"
            >
              <el-button
                type="success"
                icon="el-icon-share"
                size="mini"
                @click="view_security_rules(row)"
              ></el-button>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>
      <!-- 分页组件 -->
      <pagination
        v-show="total>0"
        :total="total"
        :page.sync="listQuery.page"
        :limit.sync="listQuery.limit"
        @pagination="get_security_list"
      ></pagination>
      <!-- 编辑Dialog -->
      <el-dialog
        title="编辑安全组"
        :visible.sync="dialogFormVisible"
        width="50%"
      >
        <el-form
          :model="security_info_form"
          label-width="100px"
        >
          <el-form-item
            label="安全组 ID"
            style="width:300px"
            prop="security_id"
          >
            <el-input
              v-model="security_info_form.security_id"
              size="small"
              disabled
            ></el-input>
          </el-form-item>
          <el-form-item
            label="安全组名称"
            style="width:300px"
            prop="name"
          >
            <el-input
              v-model="security_info_form.name"
              size="small"
              disabled
            ></el-input>
          </el-form-item>
          <el-form-item
            label="描述"
            style="width:300px"
            prop="desc"
          >
            <el-input
              v-model="security_info_form.desc"
              size="small"
            ></el-input>
          </el-form-item>
        </el-form>
        <span
          slot="footer"
          class="dialog-footer"
        >
          <el-button @click="dialogFormVisible = false">取 消</el-button>
          <el-button
            type="primary"
            @click="submit_security_info"
          >确 定</el-button>
        </span>
      </el-dialog>
    </el-card>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import { getSecurityList, updateSecurityByID } from '@/views/cmdb/api/security'
import checkPermission from "@/utils/permission"
export default {
  name: 'SecurityList',
  components: { Pagination },
  data() {
    return {
      listQuery: {
        page: 1,
        limit: 15,
        name__contains: '',
        vpc: this.$route.query.vpc
      },
      supplier: this.$route.query.supplier,
      total: 0,
      security_list: [],
      security_info_form: {
        id: null,
        region: '',
        name: '',
        desc: '',
        security_id: '',
        vpc__name: ''
      },
      image_dialog: false,
      dialogFormVisible: false,
      sync_loading: false
    }
  },
  computed: {
  },
  created() {
    this.get_security_list()
  },
  methods: {
    checkPermission,
    get_security_list() {
      getSecurityList(this.listQuery)
        .then(response => {
          // console.log("getSecurityList-response", response.data.results)
          this.security_list = response.data.results
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
    edit_security_info(param) {
      this.dialogFormVisible = true
      this.security_info_form.id = param.id
      this.security_info_form.security_id = param.security_id
      this.security_info_form.name = param.name
      this.security_info_form.desc = param.desc
      this.security_info_form.vpc__name = param.vpc__name
    },
    view_security_rules(row) {
      // console.log("view_securityRules", this.vpcId)
      this.$router.push({
        path: "/cmdb/security_rule_list/",
        query: { security_id: row.security_id, vpc: this.listQuery.vpc, supplier: this.supplier }
      })
    },
    submit_security_info() {
      updateSecurityByID(this.security_info_form.id, this.security_info_form)
        .then(() => {
          this.$message({
            type: "success",
            message: "编辑成功"
          })
          this.dialogFormVisible = false
          this.get_security_list()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err.message
          })
        })
      this.get_security_list()
      this.dialogFormVisible = false
    },
    search_filter() {
      this.get_security_list()
    },
    clear_refresh() {
      this.get_security_list()
    },
    inter_subnet_detail(row) {
      this.$router.push('/settings/subnet_list')
    },
    go_back() {
      this.$router.push({ name: "Other", params: { active_tab_name: 'network_resouce' } })
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
