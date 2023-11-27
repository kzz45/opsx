<template>
  <div class="app-container">
    <el-card class="box-card">
      <div>
        <el-button
          type="info"
          icon="el-icon-back"
          size="small"
          @click="go_back"
        >返回</el-button>
      </div>
      <el-tabs
        v-model="active_tab_name"
        @tab-click="active_tab_click"
      >
        <el-tab-pane
          label="容器"
          name="pod_settings"
        >
          <el-table
            ref="pod_list_table_refs"
            :data="pod_list"
            empty-text="啥也没有"
            size="small"
            border
          >
            <el-table-column
              label="名称"
              prop="pod_name"
            ></el-table-column>
            <el-table-column label="镜像">{{ image_version }}</el-table-column>
            <el-table-column
              label="状态"
              prop="phase"
            ></el-table-column>
            <el-table-column
              label="PodIP"
              prop="pod_ip"
            ></el-table-column>
            <el-table-column
              label="HostIP"
              prop="host_ip"
            ></el-table-column>
            <el-table-column
              label="操作"
              width="180px;"
            >
              <template slot-scope="scoped">
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="终端"
                  placement="top"
                >
                  <el-button
                    type="primary"
                    icon="el-icon-s-platform"
                    size="mini"
                    @click="pod_terminal(scoped.row)"
                  ></el-button>
                </el-tooltip>
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="日志"
                  placement="top"
                >
                  <el-button
                    type="info"
                    icon="el-icon-chat-line-round"
                    size="mini"
                    @click="view_pod_logs(scoped.row)"
                  ></el-button>
                </el-tooltip>
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="监控"
                  placement="top"
                >
                  <el-button
                    type="success"
                    icon="el-icon-data-line"
                    size="mini"
                    @click="view_pod_monitor(scoped.row)"
                  ></el-button>
                </el-tooltip>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane
          label="服务"
          name="service_settings"
        >
          <el-table
            ref="service_list_table_refs"
            :data="service_list"
            empty-text="啥也没有"
            size="small"
            border
          ></el-table>
        </el-tab-pane>
        <el-tab-pane
          label="路由"
          name="ingress_settings"
        >
          <el-table
            ref="ingress_list_table_refs"
            :data="ingress_list"
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
import { getReleaseInfo } from '@/views/container/apis/release'

export default {
  data() {
    return {
      active_tab_name: "pod_settings",
      pod_list: [],
      service_list: [],
      ingress_list: []
    }
  },
  created() {
    this.app_info = JSON.parse(this.$route.query.app_info)
    console.log(this.app_info)
    this.image_version = this.app_info.image__name + ":" + this.app_info.image__version
    this.release_name = this.app_info.name
    this.cluster_name = this.app_info.cluster__name
    this.get_release_info()
  },
  methods: {
    go_back() {
      this.$router.push({ name: "ContainerOverview" })
    },
    active_tab_click() { },
    get_release_info() {
      getReleaseInfo({ "release_name": this.release_name, "cluster_name": this.cluster_name })
        .then(resp => {
          this.pod_list = resp.data.msg
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    pod_terminal() { },
    view_pod_logs() { },
    view_pod_monitor() { }
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
.el-form {
  margin-top: 10px;
}
.el-tabs {
  width: 100%;
  margin-top: 10px;
}
.el-table {
  width: 100%;
  margin-top: 10px;
}
</style>
