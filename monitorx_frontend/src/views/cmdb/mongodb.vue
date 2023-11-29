<template>
  <div class="app-container">
    <el-card class="box-card">
      <!-- 搜索相关 -->
      <div>
        <el-input
          v-model="input_content"
          placeholder="准备找啥(支持模糊搜索)"
          class="input-with-select"
          size="small"
          clearable
          @change="clear_refresh"
          @keyup.enter.native="search_handler"
        >
          <el-select
            slot="prepend"
            v-model="select_input"
            size="small"
            placeholder="请选择"
          >
            <el-option
              label="实例名称"
              value="external_name"
            ></el-option>
            <el-option
              label="实例ID"
              value="external_uuid"
            ></el-option>
          </el-select>
          <el-button
            slot="append"
            icon="el-icon-search"
            @click="search_handler"
          ></el-button>
        </el-input>
        <el-tooltip
          effect="dark"
          content="分配资源"
          placement="top-start"
        >
          <el-button
            size="small"
            icon="el-icon-position"
            style="margin-left: 10px"
            :loading="associate_loading"
            @click="associate_mongodb_to_product"
          >
          </el-button>
        </el-tooltip>
        <el-button
          type="info"
          size="small"
          style="margin-left: 10px;"
          :icon="show_more_search?'el-icon-arrow-up':'el-icon-arrow-down'"
          @click="more_search"
        >
          {{ show_more_search ? "收起搜索": "更多搜索" }}
        </el-button>
        <el-form
          :model="more_search_form"
          label-width="100px;"
          style="margin-top: 10px;"
        >
          <el-collapse-transition>
            <div v-show="show_more_search">
              <el-row>
                <el-col :span="6">
                  <el-form-item
                    label="地区: "
                    prop="region__name"
                  >
                    <el-select
                      v-model="more_search_form.region__name"
                      placeholder="请选择地区"
                      size="small"
                      clearable
                    >
                      <el-option
                        v-for="(item) in region_filter_list"
                        :key="item.id"
                        :value="item.name"
                      ></el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="6">
                  <el-form-item
                    label="厂商: "
                    prop="factory__name"
                  >
                    <el-select
                      v-model="more_search_form.factory__name"
                      placeholder="请选择厂商"
                      size="small"
                      clearable
                    >
                      <el-option
                        v-for="(item) in factory_name_list"
                        :key="item.id"
                        :value="item.name"
                      ></el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="6">
                  <el-form-item
                    label="使用状态: "
                    prop="status"
                  >
                    <el-select
                      v-model="more_search_form.status"
                      placeholder="请选择状态"
                      size="small"
                      clearable
                    >
                      <el-option
                        v-for="(item) in status_filter_list"
                        :key="item.value"
                        :label="item.text"
                        :value="item.value"
                      ></el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="6">
                  <el-form-item label="操作: ">
                    <el-button
                      type="primary"
                      size="small"
                      icon="el-icon-search"
                      @click="more_search_submit"
                    ></el-button>
                  </el-form-item>
                </el-col>
              </el-row>
            </div>
          </el-collapse-transition>
        </el-form>
      </div>
      <!-- mongodb列表 -->
      <el-table
        ref="mongodb_list_refs"
        :data="mongodb_list"
        :row-key="get_row_key"
        style="width: 100%"
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
          label="实例名称"
          prop="external_name"
        ></el-table-column>
        <el-table-column
          label="实例ID"
          prop="external_uuid"
        ></el-table-column>
        <el-table-column
          label="连接串"
          prop="primary_conn"
        ></el-table-column>
        <el-table-column label="实例类型">
          <template slot-scope="scoped">
            <el-tag
              v-if="scoped.row.db_type === 'replicate'"
              type="primary"
              size="small"
            >副本集</el-tag>
            <el-tag
              v-else
              type="primary"
              size="small"
            >分片集</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          label="使用状态"
          prop="status"
        >
          <template slot-scope="scoped">
            <el-tag
              v-if="scoped.row.status == 0"
              type="success"
            >使用中</el-tag>
            <el-tag
              v-else
              type="warning"
            >已退还</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          label="地区"
          prop="region__name"
        ></el-table-column>
        <el-table-column
          label="厂商"
          prop="factory__name"
        ></el-table-column>
        <el-table-column
          label="操作"
          width="80px;"
        >
          <template slot-scope="scope">
            <el-button
              type="info"
              icon="el-icon-info"
              size="mini"
              @click="toggleExpand(scope.row)"
            ></el-button>
          </template>
        </el-table-column>
        <el-table-column
          type="expand"
          width="1"
        >
          <template slot-scope="props">
            <el-form
              label-position="left"
              inline
              class="table-expand"
            >
              <el-form-item label="实例名称:">
                <span>{{ props.row.external_name }}</span>
              </el-form-item>
              <el-form-item label="实例ID:">
                <span>{{ props.row.external_uuid }}</span>
              </el-form-item>
              <el-form-item label="类型:">
                <span>{{ props.row.db_type }}</span>
              </el-form-item>
              <el-form-item label="副本集名:">
                <span>{{ props.row.replica_set_name }}</span>
              </el-form-item>
              <el-form-item label="主连接串:">
                <span>{{ props.row.primary_conn }}</span>
              </el-form-item>
              <el-form-item label="主端口:">
                <span>{{ props.row.primary_port }}</span>
              </el-form-item>
              <el-form-item label="副连接串:">
                <span>{{ props.row.secondary_conn }}</span>
              </el-form-item>
              <el-form-item label="副端口:">
                <span>{{ props.row.secondary_port }}</span>
              </el-form-item>
              <el-form-item label="只读连接串:">
                <span>{{ props.row.readonly_conn }}</span>
              </el-form-item>
              <el-form-item label="只读端口:">
                <span>{{ props.row.readonly_port }}</span>
              </el-form-item>
              <el-form-item label="分片连接串:">
                <span>{{ props.row.shard_conn }}</span>
              </el-form-item>
              <el-form-item label="mongos连接串:">
                <span>{{ props.row.mongos_conn }}</span>
              </el-form-item>
              <el-form-item label="mongos端口:">
                <span>{{ props.row.mongos_port }}</span>
              </el-form-item>
              <el-form-item label="厂商:">
                <span>{{ props.row.factory__name }}</span>
              </el-form-item>
              <el-form-item label="规格:">
                <span>{{ props.row.flavor_name }}</span>
              </el-form-item>
              <el-form-item label="版本:">
                <span>{{ props.row.version }}</span>
              </el-form-item>
              <el-form-item label="最大连接数:">
                <span>{{ props.row.connections }}</span>
              </el-form-item>
              <el-form-item label="磁盘:">
                <span>{{ props.row.disk }}</span>
              </el-form-item>
              <el-form-item label="IOPS:">
                <span>{{ props.row.iops }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
      </el-table>
      <pagination
        v-show="mongodb_list_total>0"
        :total="mongodb_list_total"
        :page.sync="list_query.page"
        :limit.sync="list_query.limit"
        @pagination="get_mongodb_list"
      ></pagination>
    </el-card>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"
import { getMongodbList } from "@/views/cmdb/api/mongodb"

export default {
  components: {
    Pagination
  },
  data() {
    return {
      list_query: {
        page: 1,
        limit: 15
      },
      input_content: "",
      select_input: "external_name",
      associate_loading: false,
      show_more_search: false,
      region_filter_list: [],
      factory_name_list: [],
      more_search_form: {},
      status_filter_list: [
        { text: "使用中", value: 0 },
        { text: "已退还", value: 2 }
      ],
      mongodb_list: [],
      mongodb_list_total: 0
    }
  },
  created() {
    this.get_mongodb_list()
  },
  methods: {
    clear_refresh() {
      this.get_mongodb_list()
    },
    search_handler() {
      var params = this.select_input + "__contains"
      this.list_query[params] = this.input_content
      this.get_mongodb_list()
    },
    associate_mongodb_to_product() {},
    more_search() {},
    more_search_submit() {},
    get_row_key(row) {
      return row.id
    },
    handleSelectionChange() {},
    toggleExpand(row) {
      const $table = this.$refs.mongodb_list_refs
      this.mongodb_list.map(item => {
        if (row.id !== item.id) {
          $table.toggleRowExpansion(item, false)
        }
      })
      $table.toggleRowExpansion(row)
    },
    get_mongodb_list() {
      getMongodbList(this.list_query)
        .then(response => {
          this.mongodb_list = response.data.results
          this.mongodb_list_total = response.data.count
        })
        .catch(err => {
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
.el-table {
  margin-top: 15px;
}
.el-select {
  width: 120px;
}
.el-input {
  width: 400px;
}
.table-expand {
  font-size: 0;
}
.table-expand label {
  width: 90px;
  color: #99a9bf;
}
.table-expand .el-form-item {
  margin-right: 0;
  margin-bottom: 0;
  width: 50%;
}
</style>
