<template>
  <div>
    <el-card class="box-card">
      <el-row>
        <el-col :span="12">
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
        </el-col>
        <el-col :span="12">
          <el-date-picker
            v-model="year_month"
            type="month"
            placeholder="按月份搜索"
            value-format="yyyy-MM"
            size="small"
          >
          </el-date-picker>
          <el-button
            icon="el-icon-search"
            size="small"
            type="primary"
            style="margin-left: 10px;"
            @click="search_month"
          ></el-button>
        </el-col>
      </el-row>

      <el-table
        :data="project_detail_list"
        empty-text="啥也没有"
        size="small"
        show-summary
        border
      >
        <el-table-column
          label="账期"
          prop="ymd"
        ></el-table-column>
        <el-table-column
          label="产品名称"
          prop="product__name"
        ></el-table-column>
        <el-table-column
          label="金额"
          prop="money"
        ></el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { getProjectList, getDetailList } from '@/views/bills/apis/detail'

export default {
  name: "ProjectTable",
  data() {
    return {
      list_query: {
        page: 1,
        limit: 100
      },
      year_month: "",
      project_select_input: "",
      project_list: [],
      project_detail_list: []
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
    },
    search_month() {
      const params = "ymd"
      this.list_query[params] = this.year_month
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
