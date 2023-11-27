<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-tabs
        v-model="active_tab_name"
        @tab-click="active_tab_click"
      >
        <!-- configmap管理--------------------------------------------------  -->
        <el-tab-pane
          label="Istio"
          name="istio_settings"
        >
          <el-table
            ref="configmap_list_table_refs"
            :data="configmap_list"
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
      active_tab_name: "istio_settings"
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
