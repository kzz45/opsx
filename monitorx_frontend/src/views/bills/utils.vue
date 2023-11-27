<template>
  <div>
    <el-row style="margin-bottom: 10px;">
      <el-col :span="6">
        <el-input
          v-model="instance_name_input"
          placeholder="按实例名称搜索"
          size="small"
          style="width: 300px;"
        >
          <template slot="prepend">实例名称</template>
          <el-button
            slot="append"
            size="small"
            icon="el-icon-search"
            @click="search_instance"
          ></el-button>
        </el-input>
      </el-col>
      <!-- <el-col :span="6">
        <el-select
          v-model="project_select_input"
          placeholder="按项目搜索"
          size="small"
          style="width: 200px;"
          clearable
          filterable
        >
          <el-option
            v-for="(item, index) in project_list"
            :key="index"
            :label="item.name"
            :value="item.id"
          ></el-option>
        </el-select>
        <el-button
          type="primary"
          size="small"
          style="margin-left: 10px;"
          icon="el-icon-search"
          @click="search_project"
        ></el-button>
      </el-col> -->
    </el-row>
    <el-table
      ref="utils_list_table_refs"
      :data="utils_list"
      empty-text="啥也没有"
      size="small"
      border
    >
      <el-table-column
        label="实例名称"
        prop="instance_name"
      ></el-table-column>
      <el-table-column
        label="实例ID"
        prop="instance_id"
      ></el-table-column>
      <el-table-column
        label="项目"
        prop="project__desc"
      ></el-table-column>
      <el-table-column
        label="月份"
        prop="month"
      ></el-table-column>
      <el-table-column
        label="CPU(Core)"
        prop="cpu"
      ></el-table-column>
      <el-table-column
        label="CPU利用率"
        prop="cpu_max"
      >
        <template slot-scope="scoped">
          <el-tag
            type="danger"
            size="small"
          >{{ scoped.row.cpu_max }}</el-tag>
          <el-tag
            size="small"
            style="margin-left:10px;"
          >{{ scoped.row.cpu_avg }}</el-tag>
          <el-tag
            type="success"
            size="small"
            style="margin-left:10px;"
          >{{ scoped.row.cpu_min }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column
        label="内存"
        prop="mem"
      ></el-table-column>
      <el-table-column
        label="内存利用率"
        prop="mem_max"
      >
        <template slot-scope="scoped">
          <el-tag
            type="danger"
            size="small"
          >{{ scoped.row.mem_max }}</el-tag>
          <el-tag
            size="small"
            style="margin-left:10px;"
          >{{ scoped.row.mem_avg }}</el-tag>
          <el-tag
            type="success"
            size="small"
            style="margin-left:10px;"
          >{{ scoped.row.mem_min }}</el-tag>
        </template>
      </el-table-column>
    </el-table>
    <pagination
      v-show="utils_list_total>0"
      :total="utils_list_total"
      :page.sync="list_query.page"
      :limit.sync="list_query.limit"
      @pagination="get_utils_list"
    ></pagination>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"
import { getUtilsList, getProjectList } from '@/views/bills/apis/utils'

export default {
  name: "EcsUtils",
  components: {
    Pagination
  },
  data() {
    return {
      list_query: {
        page: 1,
        limit: 15
      },
      instance_name_input: "",
      project_select_input: "",
      project_list: [],
      utils_list: [],
      utils_list_total: 0
    }
  },
  created() {

  },
  methods: {
    get_utils_list() {
      getUtilsList(this.list_query)
        .then(resp => {
          this.utils_list = resp.data.results
          this.utils_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    get_project_list() {
      getProjectList()
        .then((resp) => {
          this.project_list = resp.data
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    search_project() {
      const params = "project"
      this.list_query[params] = this.project_select_input
      getUtilsList(this.list_query)
        .then(resp => {
          this.utils_list = resp.data.results
          this.utils_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    search_instance() {
      const params = "instance_name__contains"
      this.list_query[params] = this.instance_name_input
      getUtilsList(this.list_query)
        .then(resp => {
          this.utils_list = resp.data.results
          this.utils_list_total = resp.data.count
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
