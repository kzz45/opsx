<template>
  <div class="app-container">
    <el-card class="box-card">
      <!-- 搜索相关 -->
      <div>
        <el-input
          v-model="input_content"
          placeholder="准备找啥(支持模糊搜索)"
          class="input-with-select"
          clearable
          size="small"
        >
          <el-select
            slot="prepend"
            v-model="select_input"
            size="small"
            placeholder="请选择"
          >
            <el-option
              label="实例ID"
              value="external_uuid"
            ></el-option>
            <el-option
              label="实例名称"
              value="external_name"
            ></el-option>
            <el-option
              label="连接串"
              value="conn"
            ></el-option>
          </el-select>
          <el-button
            slot="append"
            icon="el-icon-search"
            @click="search_handler"
          ></el-button>
        </el-input>
        <el-tooltip
          effect="dark"
          content="分配资源"
          placement="top-start"
        >
          <el-button
            size="small"
            icon="el-icon-position"
            style="margin-left: 10px"
            :loading="associate_loading"
            @click="associate_mysql_to_product"
          >
          </el-button>
        </el-tooltip>
      </div>
      <!-- 表格列表内容 -->
      <el-table
        ref="mysql_table_refs"
        :data="mysql_list"
        :row-key="get_row_key"
        border
        size="small"
        @selection-change="handleSelectionChange"
      >
        <el-table-column
          type="selection"
          width="55"
        >
        </el-table-column>
        <el-table-column
          label="实例名称"
          prop="external_name"
        ></el-table-column>
        <el-table-column
          label="连接串"
          prop="conn"
        ></el-table-column>
        <!-- <el-table-column
          label="实例ID"
          prop="external_uuid"
        ></el-table-column> -->
        <el-table-column
          label="使用状态"
          prop="local_status"
        >
          <template slot-scope="scoped">
            <el-tag
              v-if="scoped.row.local_status == 0"
              type="success"
            >使用中</el-tag>
            <el-tag
              v-else
              type="warning"
            >已退还</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          label="地区"
          prop="region__name"
        ></el-table-column>
        <el-table-column
          label="厂商"
          prop="factory__name"
        ></el-table-column>
        <el-table-column
          label="操作"
          width="80px"
        >
          <template slot-scope="scope">
            <el-button
              type="info"
              icon="el-icon-info"
              size="mini"
              @click="toggleExpand(scope.row)"
            ></el-button>
          </template>
        </el-table-column>
        <el-table-column
          type="expand"
          width="1"
        >
          <template slot-scope="props">
            <el-form
              label-position="left"
              inline
              class="table-expand"
            >
              <el-form-item label="实例名称:">
                <span>{{ props.row.external_name }}</span>
              </el-form-item>
              <el-form-item label="实例ID:">
                <span>{{ props.row.external_uuid }}</span>
              </el-form-item>
              <el-form-item label="实例状态:">
                <span>{{ props.row.external_status }}</span>
              </el-form-item>
              <el-form-item label="连接串:">
                <span>{{ props.row.conn }}</span>
              </el-form-item>
              <el-form-item label="端口:">
                <span>{{ props.row.port }}</span>
              </el-form-item>
              <el-form-item label="版本:">
                <span>{{ props.row.version }}</span>
              </el-form-item>
              <el-form-item label="机型:">
                <span>{{ props.row.flavor_name }}</span>
              </el-form-item>
              <el-form-item label="CPU:">
                <span>{{ props.row.cpu }}</span>
              </el-form-item>
              <el-form-item label="内存:">
                <span>{{ props.row.mem }}</span>
              </el-form-item>
              <el-form-item label="磁盘:">
                <span>{{ props.row.disk }}</span>
              </el-form-item>
              <el-form-item label="厂商:">
                <span>{{ props.row.factory__name }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
      </el-table>
      <!-- 分页组件 -->
      <pagination
        v-show="mysql_total>0"
        :total="mysql_total"
        :page.sync="listQuery.page"
        :limit.sync="listQuery.limit"
        @pagination="get_mysql_list"
      ></pagination>
    </el-card>
    <!-- 分配分组或者产品的Dialog -->
    <el-dialog
      :title="dialogTextMap[dialogStatus]"
      :visible.sync="group_product_dialog"
      width="50%"
    >
      <el-form
        ref="associate_mysqlRefs"
        :model="associate_mysql"
        label-width="100px"
      >
        <el-form-item
          label="产品名称"
          prop="product_id"
        >
          <el-select
            v-model="product_id"
            placeholder="请选择产品"
            style="width: 300px;"
            size="small"
          >
            <el-option
              v-for="item in product_list"
              :key="item.id"
              :label="'【' + item.id + '】' + item.name"
              :value="item.id"
            >
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="group_product_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_associate"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { mapGetters } from "vuex"
import Pagination from "@/components/Pagination"
import { getProductList } from "@/api/product"
import { getMySQLList, updateMySQLByID } from "@/views/cmdb/api/mysql"

export default {
  name: "MySQLList",
  components: {
    Pagination
  },
  data() {
    return {
      listQuery: {
        page: 1,
        limit: 15
      },
      dialogTextMap: {
        group: "关联分组",
        product: "关联产品"
      },
      dialogStatus: "",
      mysql_total: 0,
      mysql_list: [],
      dialogVisible: false,
      associate_loading: false,
      group_product_dialog: false,
      input_content: "",
      select_input: "external_name",
      multipleSelection: [],
      product_list: [],
      product_id: "",
      associate_mysql: {}
    }
  },
  computed: {
    ...mapGetters(["current_select_product_id", "current_select_product_name"])
  },
  watch: {
    // 全局组件global-product选择变化时 自动刷新机器列表
    current_select_product_id: function() {
      this.get_mysql_list()
    }
  },
  created() {
    this.get_product_list()
    this.get_mysql_list()
  },
  methods: {
    // 表格行的选择
    handleSelectionChange(val) {
      this.multipleSelection = val
    },
    // 搜索
    search_handler() {
      var params = this.select_input + "__contains"
      this.listQuery.page = 1
      this.listQuery[params] = this.input_content
      this.get_mysql_list()
    },
    // 获取MySQL列表
    get_mysql_list() {
      const params = "project__product__id"
      this.listQuery[params] = this.current_select_product_id
      // 如果是选择的产品是全部【0】就展示全部
      if (this.current_select_product_id === 0) {
        this.listQuery[params] = ""
      } else {
        this.listQuery[params] = this.current_select_product_id
      }
      getMySQLList(this.listQuery)
        .then(resp => {
          this.mysql_list = resp.data.results
          this.mysql_total = resp.data.count
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    get_row_key(row) {
      return row.id
    },
    // 展开表格行内容
    toggleExpand(row) {
      const $table = this.$refs.mysql_table_refs
      this.mysql_list.map(item => {
        if (row.id !== item.id) {
          $table.toggleRowExpansion(item, false)
        }
      })
      $table.toggleRowExpansion(row)
    },
    // 获取产品列表
    get_product_list() {
      getProductList({ limit: 999 })
        .then(response => {
          this.product_list = response.data.results
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 分配mysql到产品
    associate_mysql_to_product() {
      if (this.multipleSelection.length <= 0) {
        this.$message({
          type: "warning",
          message: "没有选择的人生是徒劳的"
        })
        return
      }
      this.group_product_dialog = true
      this.dialogStatus = "product"
    },
    submit_associate() {
      for (let index = 0; index < this.multipleSelection.length; index++) {
        updateMySQLByID(this.multipleSelection[index].id, {
          product: this.product_id
        })
          .then(_ => {
            this.$message({
              type: "success",
              message: "分配MySQL至产品成功"
            })
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: "分配MySQL至产品失败" + err
            })
          })
        this.associate_loading = false
      }
      this.group_product_dialog = false
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
  width: 400px;
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
