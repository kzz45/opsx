<template>
 <div>
<el-input
    v-model="instance_input_content"
    placeholder="多个搜索用逗号分隔"
    class="filter-item"
    clearable
    size="small"
    @keyup.enter.native="search_machine"
>
    <el-select
    slot="prepend"
    style="width:120px"
    v-model="type_input_content"
    size="small"
    placeholder="请选择"
    >
    <el-option
        label="实例ID"
        value="external_uuid"
    ></el-option>
    <el-option
        label="实例名"
        value="external_name"
    ></el-option>
    <el-option
        label="内网ip"
        value="private_ip"
    ></el-option>
    </el-select>
    <el-button
    slot="append"
    icon="el-icon-search"
    @click="search_machine"
    ></el-button>
</el-input>
<el-table
    :data="machine_list"
    v-loading='listLoading'
    border
    size="small"
    @selection-change="handleSelectionChange"
    >
    <el-table-column
        type="selection"
        width="55"
    >
    </el-table-column>
    <el-table-column
        prop="external_name"
        label="实例名称"
    >
    </el-table-column>
    <el-table-column
        prop="external_uuid"
        label="实例ID"
    >
    </el-table-column>
    <el-table-column
        prop="private_ip"
        label="内网IP"
    >
    </el-table-column>
    <el-table-column
        prop="factory__name"
        label="厂商"
    >
    </el-table-column>
    <el-table-column
        prop="region__name"
        label="地区"
    >
    </el-table-column>
    <el-table-column
        label="使用状态"
        prop="external_status"
    >
    <template slot-scope="scoped">
        <el-tag :type="get_instance_status_tag(scoped.row.external_status)">{{ get_instance_status(scoped.row.external_status) }}</el-tag>
    </template>
    </el-table-column>
    </el-table>
    <pagination
        v-show="machine_list_total>0"
        :total="machine_list_total"
        :page.sync="list_query.page"
        :limit.sync="list_query.limit"
        @pagination="get_machine_list"
    ></pagination>
    </div>
</template>

<script>
import Vue from 'vue'
import Pagination from '@/components/Pagination'
import { getMachineList } from '@/views/cmdb/api/machine'
import { mapGetters } from 'vuex'

export default {
  name: "ProjectMachine",
  components: {
    Pagination,
  },
  watch: {
    multipleSelection: function () {
      //先清空数组
      this.selected_data.splice(0,this.selected_data.length)

      if (this.multipleSelection.length > 0) {
          this.multipleSelection.forEach(element => {
              this.selected_data.push(element["external_uuid"])
          })
      }
    }
  },
  props: [
      "project_id",
      "selected_data",
      "factory"
  ],
  created() {
      this.get_machine_list()
  },
  computed: {
    ...mapGetters([
      'global_product_list',
      'global_product_map',
      'current_select_product_id'
    ])
  },
  data() {
    return {
      list_query: {
        page: 1,
        limit: 15
      },
      instance_input_content: "",
      type_input_content: "external_uuid",
      listLoading: false,
      multipleSelection: [],
      current_api_prefix: '',
      machine_search_input: '',
      machine_search_select: 'external_name',
      machine_list: [],
      machine_list_total: 0,
      machine_labels: [{value: ''}],
    }
  },
  methods: {
    search_machine() {
    var params = this.type_input_content + "__contains"
      this.list_query.page = 1
      this.list_query[params] = this.instance_input_content
      this.get_machine_list()

    },
    handleSelectionChange(val) {
      this.multipleSelection = val
    },
    get_instance_status_tag(status) {
        if (status && (status.toUpperCase().indexOf("RUNNING") != -1)) {
          return 'success'
        } else if (status && (status.toUpperCase().indexOf("STOP") != -1)) {
          return 'warning'

        } else if (status && (status.toUpperCase().indexOf("DELET") != -1 || status.toUpperCase().indexOf("TERMINAT") != -1)) {
          return 'danger'
        } else {
          return 'primary'
        }
    },
    get_instance_status(status) {
      if (status) {
        return status.toUpperCase()
      } else {
        return "UNKWOWN"
      }
    },
    get_machine_list() {
      this.list_query["project__id"] = this.project_id
      this.list_query["factory"] = this.factory
      getMachineList(this.list_query)
        .then(resp => {
          this.machine_list = resp.data.results
          this.machine_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
  }
}
</script>