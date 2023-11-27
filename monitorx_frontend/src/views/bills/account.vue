<template>
  <div>
    <el-table
      ref="account_list_table_refs"
      :data="account_list"
      empty-text="啥也没有"
      size="small"
      border
    >
      <el-table-column
        label="账户"
        prop="owner_name"
      ></el-table-column>
      <el-table-column
        label="OwnerID"
        prop="owner_id"
      ></el-table-column>
      <el-table-column
        label="操作"
        width="120px;"
      >
        <template slot-scope="scoped">
          <el-button
            type="primary"
            icon="el-icon-edit"
            size="mini"
            @click="update_account(scoped.row)"
          ></el-button>
          <el-popconfirm
            title="确定删除吗？"
            confirm-button-text="确定"
            cancel-button-text="不了"
            style="margin-left: 10px"
            @confirm="delete_account(scoped.row)"
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
      v-show="account_list_total>0"
      :total="account_list_total"
      :page.sync="list_query.page"
      :limit.sync="list_query.limit"
      @pagination="get_account_list"
    ></pagination>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"
import { getAccountList } from '@/views/bills/apis/account'

export default {
  name: "BillAccount",
  components: {
    Pagination
  },
  data() {
    return {
      list_query: {
        page: 1,
        limit: 15
      },
      account_list: [],
      account_list_total: 0
    }
  },
  created() {
    // this.get_account_list()
  },
  methods: {
    get_account_list() {
      getAccountList(this.list_query)
        .then(resp => {
          this.account_list = resp.data.results
          this.account_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    update_account() { },
    delete_account() { },
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
.el-input-number {
  width: 200px;
}
.el-tag {
  vertical-align: middle;
}
.el-button {
  vertical-align: top;
}
.el-table {
  width: 100%;
  margin-top: 10px;
}
</style>
