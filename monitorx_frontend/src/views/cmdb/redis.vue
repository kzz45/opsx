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
            <el-option
              label="连接串"
              value="conn"
            ></el-option>
            <el-option
              label="内网IP"
              value="private_ip"
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
            @click="associate_redis_to_product"
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
      <!-- 表格列表 -->
      <el-table
        ref="redis_table_refs"
        :data="redis_list"
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
          label="连接串"
          prop="conn"
        ></el-table-column>
        <el-table-column
          label="实例类型"
          prop="types"
        >
          <template slot-scope="scoped">
            <el-tag
              v-if="scoped.row.types == 0"
              type="primary"
              size="small"
            >集群版</el-tag>
            <el-tag
              v-else
              type="primary"
              size="small"
            >标准版</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          label="使用状态"
          prop="status"
        >
          <template slot-scope="scoped">
            <el-tag
              v-if="scoped.row.status == 1"
              type="success"
            >使用中</el-tag>
            <el-tag
              v-else
              type="warning"
            >已退还</el-tag>
          </template>
        </el-table-column>
        <!-- <el-table-column
          label="地区"
          prop="region__name"
        ></el-table-column> -->
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
              <el-form-item label="连接串:">
                <span>{{ props.row.conn }}</span>
              </el-form-item>
              <el-form-item label="端口:">
                <span>{{ props.row.port }}</span>
              </el-form-item>
              <el-form-item label="内网地址:">
                <span>{{ props.row.private_ip }}</span>
              </el-form-item>
              <el-form-item label="外网地址:">
                <span>{{ props.row.public_ip }}</span>
              </el-form-item>
              <el-form-item label="厂商:">
                <span>{{ props.row.factory__name }}</span>
              </el-form-item>
              <el-form-item label="付费方式:">
                <span>{{ props.row.pay_type }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
      </el-table>
      <pagination
        v-show="redis_total>0"
        :total="redis_total"
        :page.sync="listQuery.page"
        :limit.sync="listQuery.limit"
        @pagination="get_redis_list"
      ></pagination>
    </el-card>
    <!-- 分配Redis到分组或者产品的Dialog -->
    <el-dialog
      :title="dialogTextMap[dialogStatus]"
      :visible.sync="group_product_dialog"
      width="50%"
    >
      <el-form
        ref="associate_machineRefs"
        :model="associate_redis"
        label-width="100px"
      >
        <el-form-item
          label="产品名称"
          prop="product_id"
        >
          <el-select
            v-model="product_id"
            placeholder="请选择产品"
            style="width: 300px;"
            size="small"
          >
            <el-option
              v-for="item in product_list"
              :key="item.id"
              :label="'【' + item.id + '】' + item.name"
              :value="item.id"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          label="分组名称"
          prop="group_id"
        >
          <el-select
            v-model="group_id"
            placeholder="请选择分组"
            style="width: 300px;"
            size="small"
          >
            <el-option
              v-for="item in group_list"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            >
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="group_product_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_associate"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { mapGetters } from "vuex"
import { getFactoryList } from "@/api/factory"
import Pagination from "@/components/Pagination"
import { getProductList } from "@/api/product"
import { getHostGroupList } from "@/api/host_group"
import { getRedisList, updateRedisByID } from "@/views/cmdb/api/redis"
import { getRegionList } from "@/views/cmdb/api/region"

export default {
  components: {
    Pagination
  },
  data() {
    return {
      listQuery: {
        page: 1,
        limit: 15,
        external_uuid__contains: ""
      },
      redis_total: 0,
      redis_list: [],
      dialogVisible: false,
      associate_loading: false,
      input_content: "",
      select_input: "external_name",
      show_more_search: false,
      more_search_form: {
        status: null,
        region__name: null,
        factory__name: null
      },
      region_filter_list: [],
      factory_name_list: [],
      status_filter_list: [
        { text: "使用中", value: 0 },
        { text: "已退还", value: 2 }
      ],
      multipleSelection: [],
      group_product_dialog: false,
      dialogTextMap: {
        group: "关联分组",
        product: "关联产品和分组"
      },
      dialogStatus: "",
      product_list: [],
      group_list: [],
      product_id: "",
      group_id: "",
      associate_redis: {}
    }
  },
  computed: {
    ...mapGetters(["current_select_product_id", "current_select_product_name"])
  },
  watch: {
    // 全局组件global-product选择变化时 自动刷新列表
    current_select_product_id: function() {
      this.get_redis_list()
    }
  },
  created() {
    this.get_redis_list()
    this.get_region_list()
    this.get_factory_list()
    this.get_product_list()
    this.get_machine_group_list()
  },
  methods: {
    // 获取地区列表
    get_region_list() {
      getRegionList({ limit: 999 })
        .then(resp => {
          this.region_filter_list = resp.data.results
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 获取厂商列表
    get_factory_list() {
      getFactoryList({ limit: 999 })
        .then(resp => {
          this.factory_name_list = resp.data.results
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 获取产品列表
    get_product_list() {
      getProductList(this.listQuery)
        .then(response => {
          this.product_list = response.data.results
          this.product_total = response.data.count
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 获取分组列表
    get_machine_group_list() {
      this.listQuery["product__id"] = this.product_id
      getHostGroupList(this.listQuery)
        .then(resp => {
          this.group_list = resp.data.results
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 搜索
    search_handler() {
      var params = this.select_input + "__contains"
      this.listQuery[params] = this.input_content
      this.get_redis_list()
    },
    // 获取redis列表
    get_redis_list() {
      const params = "project__product__id"
      this.listQuery[params] = this.current_select_product_id
      if (this.current_select_product_id === 0) {
        this.listQuery[params] = ""
      } else {
        this.listQuery[params] = this.current_select_product_id
      }
      getRedisList(this.listQuery)
        .then(response => {
          this.redis_list = response.data.results
          this.redis_total = response.data.count
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    clear_refresh() {
      this.get_redis_list()
    },
    get_row_key(row) {
      return row.id
    },
    // 展开表格行内容
    toggleExpand(row) {
      const $table = this.$refs.redis_table_refs
      this.redis_list.map(item => {
        if (row.id !== item.id) {
          $table.toggleRowExpansion(item, false)
        }
      })
      $table.toggleRowExpansion(row)
    },
    handle_associate_command(command) {},
    // 更多搜索
    more_search() {
      this.show_more_search = !this.show_more_search
      this.more_search_form.status = null
      this.more_search_form.factory__name = null
      this.more_search_form.region__name = null
    },
    // 更多搜索
    more_search_submit() {
      this.listQuery["status"] = this.more_search_form.status
      this.listQuery["factory__name"] = this.more_search_form.factory__name
      this.listQuery["region__name"] = this.more_search_form.region__name
      this.get_redis_list()
    },
    handleSelectionChange(val) {
      this.multipleSelection = val
    },
    // 分配redis到产品和分组
    associate_redis_to_product() {
      if (this.multipleSelection.length <= 0) {
        this.$message({
          type: "warning",
          message: "没有选择的人生是徒劳的"
        })
        return
      }
      this.group_product_dialog = true
      this.dialogStatus = "product"
    },
    // 分配redis到产品和分组
    submit_associate() {
      this.associate_loading = true
      for (let index = 0; index < this.multipleSelection.length; index++) {
        updateRedisByID(this.multipleSelection[index].id, {
          product: this.product_id,
          group: this.group_id
        })
          .then(_ => {
            this.$message({
              type: "success",
              message: "分配Redis至产品成功"
            })
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: "分配Redis至产品失败" + err
            })
          })
        this.associate_loading = false
      }
      this.group_product_dialog = false
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
