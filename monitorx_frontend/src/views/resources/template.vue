<template>
  <div class="app-container">
    <!-- <el-card class="box-card"> -->
    <div style="margin-top: 10px">
      <template>
        <el-tabs
          v-model="active_tab_name"
          @tab-click="tab_click"
        >
          <el-tab-pane
            label="虚拟机"
            name="instance"
          >
            <instance-template
              v-if="active_tab_name=='instance'"
              :provider_list="provider_list"
              :factory_list="factory_list"
              :factory_map="factory_map"
            > </instance-template>
          </el-tab-pane>
          <el-tab-pane
            label="负载均衡"
            name="loadbalancer"
          >
            <loadbalancer-template
              v-if="active_tab_name=='loadbalancer'"
              :provider_list="provider_list"
              :factory_list="factory_list"
              :factory_map="factory_map"
            > </loadbalancer-template>
          </el-tab-pane>
        </el-tabs>
      </template>
    </div>
    <!-- </el-card> -->

  </div>
</template>

<script>
import InstanceTemplate from '@/views/Template/instance'
import LoadbalancerTemplate from '@/views/Template/loadbalancer'

import { getFactoryList } from '@/api/factory'
import { setFactoryMap, setTemplateActiveTab, getTemplateActiveTab } from '@/utils/auth'

export default {
  name: "Resource",
  components: {
    InstanceTemplate,
    LoadbalancerTemplate
  },
  data() {
    return {
      provider_list: [
        { "name": "阿里云", "value": "ali" },
        { "name": "亚马逊", "value": "aws" },
        { "name": "谷歌云", "value": "gcp" }
      ],
      active_tab_name: getTemplateActiveTab() ? getTemplateActiveTab() : 'instance',
      listQuery: {
        page: 1,
        limit: 15
      },
      factory_list: [],
      factory_map: {}
    }
  },
  created() {
    this.get_factory_list()
  },
  methods: {
    tab_click(tab) {
      this.active_tab_name = tab.name
      setTemplateActiveTab(tab.name)
    },
    get_factory_list() {
      this.factory_list = []
      getFactoryList({ limit: 999 })
        .then(resp => {
          this.factory_list = resp.data.results
          for (const index in this.factory_list) {
            this.factory_map[this.factory_list[index]['id']] = this.factory_list[index]['name']
          }
          setFactoryMap(JSON.stringify(this.factory_map))
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
.el-select {
  width: 120px;
}
.el-input {
  width: 400px;
}
.el-button--mini {
  padding: 7px 10px;
}
.dashboard-div {
  width: 25%;
  display: inline-block;
  margin-left: 0;
  margin-top: 10px;
}
.el-card__body {
  padding-bottom: 0;
}
.dashboard-button-div {
  width: 180px;
  height: 160px;
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
  margin-bottom: 10px;
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
  /* overflow: hidden; */
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
