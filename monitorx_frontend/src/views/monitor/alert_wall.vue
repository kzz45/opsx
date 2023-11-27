<template>
  <div class="app-container">
    <el-card class="box-card">
      <!-- 有告警就播放音乐 -->
      <audio
        ref="background"
        controls="controls"
        src="../../assets/baby.mp3"
        preload
        hidden
        loop
      >
      </audio>
      <!-- 当前告警列表 -->
      <el-row :gutter="10">
        <el-col
          v-for="(item, index) in current_alert_list"
          :key="index"
          :span="6"
          style="padding-top: 20px;"
        >
          <div class="menuItem">
            <div
              :class="item.status === 'silence'?'menuNum info':(item.statistics[0].count[0].count>0?'menuNum danger':(item.statistics[0].count[1].count>0?'menuNum warning':'menuNum info'))"
              @click="show_alert_detail(item)"
            >
              {{ item.statistics[0].count[0].count + item.statistics[0].count[1].count + item.statistics[0].count[2].count }}
            </div>
            <div class="menuContent">
              <div class="menuTitle">
                <span>{{ item.product__name }} </span>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
      <!-- 当前没有告警  -->
      <div
        v-if="current_alert_list.length === 0"
        style="text-align: center; height: 500px; line-height: 200px"
      >
        <span>当前没有任何告警, 让我们一起来歌唱一下祖国吧</span>
        <br>
        <audio
          ref="nothing"
          controls="controls"
          src="../../assets/motherland.mp3"
          preload
          autoplay
          loop
        ></audio>
      </div>
    </el-card>
    <!-- 查看当前告警的Dialog -->
    <el-drawer
      :title="dialog_map[dialog_status]"
      :visible.sync="current_alert_dialog"
      :destroy-on-close="true"
      :before-close="close_current_alert_dialog"
      direction="btt"
      size="50%"
    >
      <el-table
        :data="alert_list"
        size="small"
        border
      >
        <el-table-column
          label="告警时间"
          prop="start"
        >
          <template slot-scope="scoped">{{ scoped.row.start | parseTime('{y}-{m}-{d} {h}:{i}:{s}') }}</template>
        </el-table-column>
        <el-table-column
          label="告警项"
          prop="name"
        ></el-table-column>
        <el-table-column
          label="实例"
          prop="instance_name"
        ></el-table-column>
        <el-table-column
          label="告警消息"
          prop="summary"
        ></el-table-column>
        <el-table-column
          label="级别"
          prop="level"
        >
          <template slot-scope="scoped">
            <el-tag
              v-if="scoped.row.level === 'crit'"
              type="danger"
              size="small"
            >严重</el-tag>
            <el-tag
              v-if="scoped.row.level === 'warn'"
              type="warning"
              size="small"
            >警告</el-tag>
            <el-tag
              v-if="scoped.row.level === 'info'"
              type="warning"
              size="small"
            >普通</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          label="操作"
          width="120px;"
        >
          <template slot-scope="scope">
            <el-button
              v-if="scope.row.silence === null"
              type="text"
            >快速维护</el-button>
            <el-button
              v-else
              type="text"
            >维护中</el-button>
          </template>
        </el-table-column>
      </el-table>
      <pagination
        v-show="alert_list_total>0"
        :total="alert_list_total"
        :page.sync="list_query.page"
        :limit.sync="list_query.limit"
        @pagination="get_alert_list"
      >
      </pagination>
    </el-drawer>
  </div>
</template>

<script>
import { parseTime } from '@/utils'
import Pagination from "@/components/Pagination"
import { getCurrentAlertWallList, getCurrentAlertList } from '@/views/monitor/apis/current_alert'

export default {
  name: "AlertWall",
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
        limit: 15,
        product: null
      },
      dialog_map: {
        current_alert: this.temp_product_name + "当前告警"
      },
      dialog_status: "",
      current_alert_list: [],
      current_alert_dialog: false,
      temp_product_id: null,
      temp_product_name: null,
      alert_list: [],
      alert_list_total: 0
    }
  },
  watch: {
    current_alert_list: {
      handler() {
        if (this.current_alert_list.length > 0) {
          for (let index = 0; index < this.current_alert_list.length; index++) {
            const element = this.current_alert_list[index]
            // 严重+警告
            this.should_play = element.statistics[0].count[0].count + element.statistics[0].count[1].count
          }
          if (this.should_play > 0) {
            this.background_play()
          }
        }
      },
      deep: true
    }
  },
  created() {
    this.get_current_alert()
  },
  methods: {
    // 有告警的背景音乐播放
    background_play() {
      this.$nextTick(() => {
        this.$refs.background.play()
      })
    },
    get_current_alert() {
      getCurrentAlertWallList()
        .then(resp => {
          this.current_alert_list = resp.data.map(item => {
            item.statistics.map((ele, index) => {
              return ele
            })
            return item
          })
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    show_alert_detail(item) {
      this.current_alert_dialog = true
      this.dialog_status = "current_alert"
      this.temp_product_id = item.product_id
      this.temp_product_name = item.product__name
      this.dialog_map.current_alert = "【" + this.temp_product_name + "】" + "当前告警"
      this.list_query.product = this.temp_product_id
      getCurrentAlertList(this.list_query)
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
    },
    get_alert_list() {
      getCurrentAlertList(this.list_query)
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
    },
    close_current_alert_dialog(done) {
      this.list_query.page = 1
      this.list_query.limit = 15
      done()
    }
  }
}
</script>

<style lang="scss" scoped>
.menuItem {
  background: #f2f6fc;
  padding: 20px;
  display: flex;
  border-radius: 12px;
  margin-right: 10px;
  max-height: 120px;
  .menuNum {
    width: 100px;
    height: 80px;
    text-align: center;
    line-height: 80px;
    background-size: 100%;
    font-size: calc(1.1vw + 1.1vh + 1.1vmin);
    color: #fff;
    margin-right: 10px;
  }
  .warning {
    background: url("../../assets/warning.png") no-repeat center;
    background-size: 100%;
  }
  .info {
    background: url("../../assets/info.png") no-repeat center;
    background-size: 100%;
  }
  .danger {
    background: url("../../assets/danger.png") no-repeat center;
    background-size: 100%;
  }
  .menuContent {
    width: 100%;
    padding: 10px 10px;
    position: relative;
    .menuTitle {
      font-size: 18px;
    }
    .menuBody {
      font-size: 18px;
    }
  }
}
.el-button {
  vertical-align: top;
}
.el-dropdown-link {
  cursor: pointer;
  color: #409eff;
}
.el-icon-arrow-down {
  font-size: 12px;
}
</style>
