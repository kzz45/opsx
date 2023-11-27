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
        ref="cluster_ns_list_table_refs"
        :data="cluster_ns_list"
        empty-text="啥也没有"
        size="small"
        border
      >
        <el-table-column
          label="名称"
          prop="name"
        ></el-table-column>
        <el-table-column
          label="所属集群"
          prop="cluster__name"
        ></el-table-column>
        <el-table-column label="操作"></el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { getClusterNsList } from '@/views/container/apis/cluster'

export default {
  data() {
    return {
      cluster_ns_list: [],
      cluster_ns_list_total: 0
    }
  },
  created() {
    this.cluster_info = JSON.parse(this.$route.query.cluster_info)
    this.cluster_id = this.cluster_info.id
    this.get_cluster_ns_list()
  },
  methods: {
    go_back() {
      this.$router.push({ name: "ClusterSettings" })
    },
    creata_ns() { },
    update_ns() { },
    delete_ns() { },
    submit_ns() { },
    get_cluster_ns_list() {
      getClusterNsList({ cluster: this.cluster_id })
        .then(resp => {
          this.cluster_ns_list = resp.data.results
          this.cluster_ns_list_total = resp.data.counts
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
