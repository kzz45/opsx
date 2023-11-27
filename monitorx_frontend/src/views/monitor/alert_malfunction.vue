<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-tabs
        v-model="active_tab_name"
        @tab-click="active_tab_click"
      >
        <div>
          <el-input
            v-model="search_input_content"
            placeholder="搜点啥"
            size="small"
            clearable
            style="width: 300px;"
            @keyup.enter.native="search_alert"
          >
            <el-select
              slot="prepend"
              v-model="search_select_input"
              size="small"
              style="width: 80px;"
            >
              <el-option
                label="实例"
                value="endpoint"
              ></el-option>
            </el-select>
            <el-button
              slot="append"
              icon="el-icon-search"
              @click="search_alert"
            ></el-button>
          </el-input>
        </div>
        <!-- 告警列表-------------------------------------------------- -->
        <el-tab-pane
          label="告警列表"
          name="alert_list"
        >
          <el-table
            ref="alert_list_table_refs"
            :data="alert_list"
            empty-text="啥也没有"
            size="small"
            border
          >
            <el-table-column
              label="告警名称"
              prop="name"
            ></el-table-column>
            <el-table-column
              label="对象"
              prop="instance_name"
            ></el-table-column>
            <el-table-column
              label="消息"
              prop="summary"
            ></el-table-column>
            <el-table-column
              label="等级"
              prop="level"
            >
              <template slot-scope="scoped">
                <el-tag :type="scoped.row.level == 'crit'?'danger':(scoped.row.level == 'warn'?'warning':'success')">{{ scoped.row.level== 'crit'?'严重':(scoped.row.level == 'warn'?'警告':'普通') }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column
              label="开始时间"
              prop="start_at"
            >
              <template slot-scope="scoped">
                <span>{{ scoped.row.start_at | parseTime('{y}-{m}-{d} {h}:{i}:{s}') }}</span>
              </template>
            </el-table-column>
            <el-table-column
              label="结束时间"
              prop="end_at"
            >
              <template slot-scope="scoped">
                <span>{{ scoped.row.end_at | parseTime('{y}-{m}-{d} {h}:{i}:{s}') }}</span>
              </template>
            </el-table-column>
            <el-table-column
              label="状态"
              prop="state"
            >
              <template slot-scope="scoped">
                <el-tag
                  v-if="scoped.row.state == 'firing'"
                  type="danger"
                >崩盘</el-tag>
                <el-tag
                  v-else
                  type="success"
                >恢复</el-tag>
              </template>
            </el-table-column>
            <el-table-column
              label="产品"
              prop="product__name"
            ></el-table-column>
          </el-table>
          <pagination
            v-show="alert_list_total>0"
            :total="alert_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_alert_list"
          ></pagination>
        </el-tab-pane>
        <!-- 事故列表-------------------------------------------------- -->
        <el-tab-pane
          label="事故列表"
          name="adcident_list"
        >
          <el-table
            ref="adcident_list_table_refs"
            :data="adcident_list"
            empty-text="啥也没有"
            size="small"
            border
          ></el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script>
import { parseTime } from '@/utils'
import Pagination from "@/components/Pagination"
import { getAlertMsgList } from '@/views/monitor/apis/alertmsg'

export default {
  name: "AlertMalfunction",
  components: {
    Pagination
  },
  filters: {
    formatDuring(mss) {
      if (mss) {
        var days = parseInt(mss / (60 * 60 * 24))
        var hours = parseInt((mss % (60 * 60 * 24)) / (60 * 60))
        var minutes = parseInt((mss % (60 * 60)) / 60)
        return days + " 天 " + hours + " 小时 " + minutes + " 分钟 "
      }
    },
    parseTime(time, cFormat) {
      return parseTime(time, cFormat)
    }
  },
  data() {
    return {
      list_query: {
        page: 1,
        limit: 15
      },
      search_input_content: "",
      search_select_input: "endpoint",
      dialog_map: {
      },
      dialog_status: "",
      active_tab_name: "alert_list",
      alert_list: [],
      alert_list_total: 0,
      adcident_list: [],
      adcident_list_total: 0
    }
  },
  created() {
    this.get_alert_list()
  },
  methods: {
    active_tab_click() { },
    search_alert() {
      var params = this.search_select_input + "__contains"
      this.list_query[params] = this.search_input_content
      this.get_alert_list()
    },
    get_alert_list() {
      getAlertMsgList(this.list_query)
        .then(resp => {
          this.alert_list = resp.data.results
          this.alert_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
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
