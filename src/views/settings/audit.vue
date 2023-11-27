<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-tabs
        v-model="active_tab_name"
        @tab-click="active_tab_click"
      >
        <!-- 操作记录--------------------------------------------------  -->
        <el-tab-pane
          label="操作记录"
          name="action_log"
        >
          <el-table
            ref="action_log_list_table_refs"
            :data="action_log_list"
            empty-text="啥也没有"
            size="small"
            border
          >
            <el-table-column
              label="用户"
              prop="user__first_name"
            ></el-table-column>
            <el-table-column
              label="动作"
              prop="action"
            ></el-table-column>
            <el-table-column
              label="模块"
              prop="model"
            ></el-table-column>
            <el-table-column
              label="主体"
              prop="body"
            ></el-table-column>
            <el-table-column
              label="时间"
              prop="update_at"
            ></el-table-column>
          </el-table>
          <pagination
            v-show="action_log_list_total>0"
            :total="action_log_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_action_log_list"
          ></pagination>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"
import permission from "@/directive/permission/index.js"
import checkPermission from '@/utils/permission'
import { mapGetters } from "vuex"
import { getHistoryList } from '@/views/settings/apis/history'

export default {
  name: "SettingsAudit",
  components: {
    Pagination
  },
  directives: {
    permission
  },
  data() {
    return {
      list_query: {
        page: 1,
        limit: 15
      },
      active_tab_name: "action_log",
      dialog_map: {
      },
      dialog_status: "",
      // 操作记录--------------------------------------------------
      action_log_list: [],
      action_log_list_total: 0
    }
  },
  computed: {
    ...mapGetters(["user_id", "is_superuser"])
  },
  created() {
    this.get_action_log_list()
  },
  methods: {
    checkPermission,
    active_tab_click(tab) {
      if (tab.name === "action_log") {
        this.get_action_log_list()
      }
    },
    get_action_log_list() {
      getHistoryList(this.list_query)
        .then(resp => {
          this.action_log_list = resp.data.results
          this.action_log_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
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
.el-button {
  vertical-align: top;
}
.el-table {
  width: 100%;
  margin-top: 10px;
}
</style>
