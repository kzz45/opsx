仪表盘页面

<template>
  <div class="app-container">
    <el-card class="box-card">
      <div style="margin-bottom: 20px;">
        <div>
          <div style="margin-bottom: 20px;">
            <template v-for="(item, index) in dashboard_list">
              <el-tooltip
                :key="item.id"
                effect="dark"
                placement="top"
              >
                <div slot="content">
                  {{ item.describe }}
                </div>
                <div
                  class="dashboard-div"
                  :style="(index + 1) % 5 === 0 ? {'padding-right': 0} : {'padding-right': '12px'}"
                >
                  <el-button
                    style="width: 100%"
                    plain
                    @click="view_dashboard(item.url)"
                  >
                    <div class="dashboard-button-div">
                      <div class="dashboard-div-icon">
                        <svg-icon
                          class="el-icon"
                          icon-class="grafana"
                        ></svg-icon>
                      </div>
                      <div class="dashboard-div-body">
                        <div class="dashboard-title ellipsis">
                          {{ item.name }}
                        </div>
                        <div class="dashboard-desc ellipsis">
                          产品: {{ item.product__name }}
                        </div>
                      </div>
                    </div>
                  </el-button>
                </div>
              </el-tooltip>
            </template>
          </div>
        </div>
      </div>
      <div
        v-if="dashboard_list.length === 0"
        style="text-align: center; height: 500px; line-height: 200px"
      >
        <span>当前还未添加仪表盘视图，请去【监控管理】-【仪表盘管理】添加</span>
      </div>
    </el-card>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { getDashboardList } from '@/views/monitor/api/dashboard'

export default {
  name: "DashboardList",
  data() {
    return {
      list_query: {
        page: 1,
        limit: 999
      },
      dashboard_list: []
    }
  },
  computed: {
    ...mapGetters(['current_select_product_id', 'current_select_product_name'])
  },
  watch: {
    current_select_product_id: function () {
      this.get_dashboard_list()
    }
  },
  created() {
    this.get_dashboard_list()
  },
  methods: {
    view_dashboard(url) {
      window.open(url, "_blank")
    },
    get_dashboard_list() {
      const params = "product__id__in"
      this.list_query[params] = this.current_select_product_id
      // 如果是选择的产品是全部【0】就展示全部
      if (this.current_select_product_id === 0) {
        this.list_query[params] = ""
      } else {
        this.list_query[params] = this.current_select_product_id
      }
      getDashboardList(this.list_query)
        .then(resp => {
          this.dashboard_list = resp.data.results
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
.dashboard-div {
  width: 20%;
  display: inline-block;
  margin-left: 0;
  margin-top: 10px;
}
.el-card__body {
  padding-bottom: 0;
}
.dashboard-button-div {
  width: 180px;
  height: 50px;
}
.dashboard-div-icon {
  float: left;
  width: 50px;
  height: 100%;
  margin-right: 10px;
}
.el-icon {
  font-size: 32px;
  line-height: 50px;
  color: #606266;
}
.dashboard-div-body {
  float: left;
  width: 120px;
  height: 100%;
  text-align: left;
}
.dashboard-title {
  font-size: 15px;
  margin-top: 6px;
  color: #606266;
  height: 18px;
  line-height: 18px;
}
.dashboard-desc {
  color: #999999;
  margin-top: 6px;
  font-size: 12px;
}
.ellipsis {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>

