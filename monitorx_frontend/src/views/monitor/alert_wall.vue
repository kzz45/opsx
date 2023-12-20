告警墙页面 当前正在告警的条目

<template>
  <div class="app-container">
    <el-card class="box-card">
      <!-- 有告警就播放音乐 -->
      <audio
        ref="audio"
        controls="controls"
        src="../../assets/baby.mp3"
        preload
        hidden
        loop
      ></audio>
      <!-- 当前告警列表 -->
      <el-row :gutter="10" style="margin-bottom: 20px">
        <el-col
          v-for="(item, index) in current_alert_list"
          :key="index"
          :span="6"
          style="padding-top: 20px;"
        >
          <div class="menuItem">
            <div
              :class="
                item.status === 'silence'
                  ? 'menuNum info'
                  : item.statistics[0].count[0].count > 0
                  ? 'menuNum danger'
                  : item.statistics[0].count[1].count > 0
                  ? 'menuNum warning'
                  : 'menuNum info'
              "
              @click="show_alert_detail(item)"
            >
              {{
                item.statistics[0].count[0].count +
                  item.statistics[0].count[1].count +
                  item.statistics[0].count[2].count +
                  item.statistics[0].count[3].count
              }}
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
        <span>当前没有任何告警，让我们一起来歌唱一下祖国吧</span>
        <br />
        <audio
          ref="nothing"
          controls="controls"
          src="../../assets/motherland.mp3"
          preload
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
        border
        size="small"
        style="margin-left: 10px"
      >
        <el-table-column label="告警时间" prop="start">
          <template slot-scope="scoped">{{
            scoped.row.start | parseTime("{y}-{m}-{d} {h}:{i}:{s}")
          }}</template>
        </el-table-column>
        <el-table-column label="告警项" prop="name"></el-table-column>
        <el-table-column label="实例" prop="instance_name"></el-table-column>
        <el-table-column label="告警消息" prop="summary"></el-table-column>
        <el-table-column label="级别" prop="level">
          <template slot-scope="scoped">
            <el-tag v-if="scoped.row.level === 'crit'" type="danger"
              >严重</el-tag
            >
            <el-tag v-if="scoped.row.level === 'warn'" type="warning"
              >警告</el-tag
            >
            <el-tag v-if="scoped.row.level === 'info'" type="warning"
              >普通</el-tag
            >
          </template>
        </el-table-column>
        <el-table-column label="操作" prop="options">
          <template slot-scope="scope">
            <el-button
              v-if="scope.row.silence === null"
              type="text"
              @click="silence_quick(scope.row)"
              >快速维护</el-button
            >
            <el-button v-else type="text">维护中</el-button>
          </template>
        </el-table-column>
      </el-table>
      <pagination
        v-show="alert_list_total > 0"
        :total="alert_list_total"
        :page.sync="list_query.page"
        :limit.sync="list_query.limit"
        @pagination="show_alert_detail_page"
      >
      </pagination>
    </el-drawer>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import { parseTime } from "@/utils";
import Pagination from "@/components/Pagination";
import { getAlertWallList } from "@/views/monitor/api/alert_wall";
import { getCurrentAlertList } from "@/views/monitor/api/current_alert";
import { createSilence } from "@/views/monitor/api/silence";
import { getAlertFocus } from "@/views/cmdb/api/domain_record";
import checkPermission from "@/utils/permission";

export default {
  name: "AlertWall",
  components: {
    Pagination
  },
  filters: {
    formatDuring(mss) {
      if (mss) {
        var days = parseInt(mss / (60 * 60 * 24));
        var hours = parseInt((mss % (60 * 60 * 24)) / (60 * 60));
        var minutes = parseInt((mss % (60 * 60)) / 60);
        return days + " 天 " + hours + " 小时 " + minutes + " 分钟 ";
      }
    },
    parseTime(time, cFormat) {
      return parseTime(time, cFormat);
    }
  },
  data() {
    return {
      interval_time: null,
      list_query: {
        page: 1,
        limit: 15,
        product__id: this.temp_product_id
      },
      dialog_map: {
        current_alert: this.temp_product_name + "当前告警"
      },
      dialog_status: "",
      current_alert_list: [],
      current_alert_dialog: false,
      should_play: 0,
      temp_product_id: null,
      temp_product_name: null,
      alert_list: [],
      alert_list_total: 0,
      issueLists: [],
      sslAlert: false,
      sslAlertNum: 0
    };
  },
  computed: {
    ...mapGetters(["user_id"])
  },
  watch: {
    current_alert_list: {
      handler() {
        if (this.current_alert_list.length > 0) {
          for (let index = 0; index < this.current_alert_list.length; index++) {
            const element = this.current_alert_list[index];
            // 严重+警告
            this.should_play =
              element.statistics[0].count[0].count +
              element.statistics[0].count[1].count;
          }
          if (this.should_play > 0) {
            // this.mp3_play()
          }
        }
      },
      deep: true
    }
  },
  beforeDestroy() {
    clearInterval(this.interval_time);
  },
  created() {
    // this.get_issue_list();
    // this.get_ssl_alert();
    this.get_current_alert();
    this.refresh();
  },
  methods: {
    checkPermission,
    get_ssl_alert() {
      var param = {};
      param["user"] = this.$store.getters.name;
      getAlertFocus(param).then(response => {
        // console.log("getAlertFocus", response.data)
        if (response.data.code === "0") {
          for (const index in response.data.data) {
            if (response.data.data[index]["certStatus"] !== "Safe") {
              this.sslAlert = true;
              this.sslAlertNum += 1;
            }
          }
        }
      });
    },
    show_ssl_alert_detail() {
      this.$router.push({ path: "/cmdb/domain_ssl_alert_focus" });
    },
    handelClick(name) {
      // console.log(name)
      if (name === "Gitlab问题用户") {
        this.$router.push({ path: "/notice/git_issue_user" });
      } else if (
        name.startsWith("无归属的机器") ||
        name.startsWith("无归属的MySQL") ||
        name.startsWith("无归属的MongoDB") ||
        name.startsWith("无归属的Redis")
      ) {
        this.$router.push({ path: "/btree/btree" });
      } else if (name.startsWith("闲置EIP")) {
        this.$router.push({ path: "/notice/idle_eip" });
      }
    },
    get_issue_list() {
      for (const item of JSON.parse(localStorage.getItem("noticeList"))) {
        this.issueLists.push(item);
      }
      // console.log("issueLists", this.issueLists)
    },
    // 音乐播放
    mp3_play() {
      this.$nextTick(() => {
        this.$refs.audio.play();
      });
    },
    // 自动刷新页面(一分钟)
    refresh() {
      this.interval_time = setInterval(() => {
        setTimeout(this.get_current_alert(), 0);
      }, 60000);
    },
    // 查看告警详情
    show_alert_detail(item) {
      this.current_alert_dialog = true;
      this.dialog_status = "current_alert";
      this.temp_product_id = item.product_id;
      this.temp_product_name = item.product__name;
      this.dialog_map.current_alert =
        "【" + this.temp_product_name + "】" + "当前告警";
      this.list_query.product__id = this.temp_product_id;
      // const params = "silence__isnull"
      // this.list_query[params] = true
      getCurrentAlertList(this.list_query)
        .then(resp => {
          this.alert_list = resp.data.results;
          this.alert_list_total = resp.data.count;
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          });
        });
    },
    // 查看告警详情
    show_alert_detail_page() {
      // const params = "silence__isnull"
      // this.list_query[params] = true
      getCurrentAlertList(this.list_query)
        .then(resp => {
          this.alert_list = resp.data.results;
          this.alert_list_total = resp.data.count;
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          });
        });
    },
    close_current_alert_dialog(done) {
      this.list_query.page = 1;
      this.list_query.limit = 15;
      done();
    },
    // 获取当前的告警
    get_current_alert() {
      getAlertWallList({ by_product: 1 })
        .then(resp => {
          this.current_alert_list = resp.data.map(item => {
            item.statistics.map((ele, index) => {
              return ele;
            });
            return item;
          });
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          });
        });
    },
    // 快速维护(默认快速维护一个小时)
    silence_quick(row) {
      console.log(row, "====");
      var match_label = Object.assign([]);
      match_label.push({ name: "_endpoint", value: row.endpoint });
      match_label.push({ name: "alertname", value: row.name });
      var silence_data = Object.assign({});
      silence_data.start = Math.round(new Date().getTime() / 1000);
      silence_data.unit = "h";
      silence_data.duration = 3600;
      silence_data.end =
        Number(silence_data.start) + Number(silence_data.duration);
      silence_data.product = row.product;
      silence_data.source = 1; // 代表维护策略来源是通过告警大屏配置的
      silence_data.user = this.$store.getters.user_id;
      silence_data.describe = "快速维护_" + row.instance_name;
      silence_data.match = JSON.stringify(match_label);
      // console.log(silence_data, '----')
      createSilence(silence_data)
        .then(resp => {
          this.$message({
            type: "success",
            message: "快速维护成功"
          });
          this.current_alert_dialog = false;
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          });
          this.current_alert_dialog = false;
        });
    }
  }
};
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
    background: url("./assets/warning.png") no-repeat center;
    background-size: 100%;
  }
  .info {
    background: url("./assets/info.png") no-repeat center;
    background-size: 100%;
  }
  .danger {
    background: url("./assets/danger.png") no-repeat center;
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
.el-divider {
  background-color: #e6e6fa;
  height: 2px;
  margin: 30px 0;
}
</style>
