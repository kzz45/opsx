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
      <el-table
        ref="registry_ns_list_table_refs"
        :data="registry_ns_list"
        empty-text="啥也没有"
        size="small"
        border
      >
        <el-table-column
          label="名称"
          prop="name"
        ></el-table-column>
        <el-table-column
          label="描述"
          prop="desc"
        ></el-table-column>
        <el-table-column label="操作"></el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { getRegistryNsList } from "@/views/container/apis/registry"

export default {
  data() {
    return {
      list_query: {
        page: 1,
        limit: 15
      },
      registry_ns_list: [],
      registry_ns_list_total: 0
    }
  },
  created() {
    this.registry_info = JSON.parse(this.$route.query.registry_info)
    this.registry_id = this.registry_info.id
    this.get_registry_ns_list()
  },
  methods: {
    go_back() {
      this.$router.push({ name: "ClusterSettings" })
    },
    get_registry_ns_list() {
      getRegistryNsList({ registry: this.registry_id }).then((resp) => {
        this.registry_ns_list = resp.data.results
        this.registry_ns_list_total = resp.data.counts
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
