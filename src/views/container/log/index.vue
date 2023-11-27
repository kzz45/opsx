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
          ></el-table>
        </el-tab-pane>
        <!-- 构建记录--------------------------------------------------  -->
        <el-tab-pane
          label="构建记录"
          name="build_log"
        >
          <el-table
            ref="build_log_list_table_refs"
            :data="build_log_list"
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
      active_tab_name: "action_log",
      action_log_list: [],
      action_log_list_total: 0,
      build_log_list: [],
      build_log_list_total: 0
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
