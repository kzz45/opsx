<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-tabs
        v-model="active_tab_name"
        @tab-click="active_tab_click"
      >
        <!-- configmap管理--------------------------------------------------  -->
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
        <!-- 保密字典管理--------------------------------------------------  -->
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
export default {
  data() {
    return {
      active_tab_name: "service_settings",
      service_list: [],
      service_list_total: 0,
      ingress_list: [],
      ingress_list_total: 0
    }
  },
  methods: {
    active_tab_click() { }
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
