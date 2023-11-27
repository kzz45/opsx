<template>
  <div>
    <el-card class="box-card">
      <el-select
        v-model="project_select_input"
        placeholder="按项目查询"
        size="small"
        style="width: 200px;"
        clearable
        filterable
      >
        <el-option
          v-for="(item, index) in project_list"
          :key="index"
          :value="item.id"
          :label="item.name"
        ></el-option>
      </el-select>
      <el-button
        type="primary"
        size="small"
        style="margin-left: 10px;"
        icon="el-icon-search"
        @click="search_project"
      ></el-button>

      <div id="project_echart"></div>
    </el-card>
  </div>
</template>

<script>
import { getProjectList, getDetailList } from '@/views/bills/apis/detail'

export default {
  name: "ProjectBar",
  data() {
    return {
      list_query: {
        page: 1,
        limit: 100
      },
      project_select_input: "",
      project_list: []
    }
  },
  created() {
    this.get_project_list()
  },
  methods: {
    get_project_list() {
      getProjectList().then(resp => {
        this.project_list = resp.data
      })
    },
    search_project() {
      const params = "project"
      this.list_query[params] = this.project_select_input
      getDetailList(this.list_query)
        .then(resp => {
          this.project_detail_list = resp.data.results
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
.el-input {
  width: 200px;
}
.el-select {
  width: 200px;
}
.el-input-number {
  width: 200px;
}
.el-tag {
  vertical-align: middle;
}
.el-button {
  vertical-align: top;
}
.el-table {
  width: 100%;
  margin-top: 10px;
}
</style>
