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
          @clear="clear_refresh"
          @change="search_handler"
        >
          <el-select
            slot="prepend"
            v-model="select_input"
            size="small"
            placeholder="请选择"
          >
            <el-option
              label="实例名称"
              value="name"
            ></el-option>
            <el-option
              label="实例ID"
              value="slb_id"
            ></el-option>
            <el-option
              label="地址"
              value="address"
            ></el-option>
          </el-select>
          <el-button
            slot="append"
            icon="el-icon-search"
            @click="search_handler"
          ></el-button>
        </el-input>
        <el-button
          style="margin-left: 10px;"
          v-if="current_group_role==='运维'"
          v-show="multipleSelection.length > 0"
          type="danger"
          size="small"
          @click="label_dialog=true"
        >
          打标签
        </el-button>
        <el-button
          v-if="current_group_role==='运维'"
          v-show="multipleSelection.length > 0"
          type="warning"
          size="small"
          @click="operate_lbs('stop')"
        >
          停止实例
      </el-button>
      <el-button
          v-if="current_group_role==='运维'"
          v-show="multipleSelection.length > 0"
          type="success"
          size="small"
          @click="operate_lbs('start')"
        >
          开启实例
      </el-button>
      </div>
      <el-table
        ref="slb_table_refs"
        :data="slb_list"
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
          prop="name"
        ></el-table-column>
        <el-table-column
          label="实例ID"
          prop="slb_id"
        ></el-table-column>
        <el-table-column
          label="实例类型"
          prop="network_type"
        ></el-table-column>
        <el-table-column
          label="地址"
          prop="address"
        ></el-table-column>
        <el-table-column
          prop="status"
          label="状态"
        >
        <template slot-scope="scoped">
            <el-tag :type="get_lb_status_tag(scoped.row.status)">{{ scoped.row.status }}</el-tag>
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
          width="120px;"
        >
          <template slot-scope="scope">
            <el-tooltip
              v-if="checkPermission(['admin','ops'])"
              class="item"
              effect="dark"
              content="编辑"
              placement="top-start"
            >
              <el-button
                type="primary"
                icon="el-icon-edit"
                size="mini"
                @click="edit_slb_info(scope)"
              ></el-button>
            </el-tooltip>
            <el-tooltip
              class="item"
              effect="dark"
              content="详情"
              placement="top-start"
            >
              <el-button
                type="info"
                icon="el-icon-info"
                size="mini"
                @click="toggleExpand(scope.row)"
              ></el-button>
            </el-tooltip>
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
                <span>{{ props.row.name }}</span>
              </el-form-item>
              <el-form-item label="实例ID:">
                <span>{{ props.row.slb_id }}</span>
              </el-form-item>
              <el-form-item label="地址:">
                <span>{{ props.row.address }}</span>
              </el-form-item>
              <el-form-item label="状态:">
                <span>{{ props.row.status }}</span>
              </el-form-item>
              <el-form-item label="地区:">
                <span>{{ props.row.region__name }}</span>
              </el-form-item>
              <el-form-item label="厂商:">
                <span>{{ props.row.factory__name }}</span>
              </el-form-item>
              <el-form-item label="网络类型:">
                <span>{{ props.row.network_type }}</span>
              </el-form-item>
              <el-form-item label="VPC:">
                <span>{{ props.row.vpc__name }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
      </el-table>
      <!-- 分页组件 -->
      <pagination
        v-show="total>0"
        :total="total"
        :page.sync="listQuery.page"
        :limit.sync="listQuery.limit"
        @pagination="get_slb_list"
      ></pagination>
    </el-card>
    <!-- 编辑或者更新内容的Dialog -->
    <el-dialog
      title="编辑"
      :visible.sync="edit_slb_dialog"
      width="50%"
    >
      <el-form
        ref="edit_slb_form"
        :model="edit_slb_form"
        label-width="100px"
      >
        <el-form-item
          label="实例名称"
          prop="name"
        >
          <el-input
            v-model="edit_slb_form.name"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="实例ID"
          prop="slb_id"
        >
          <el-input
            v-model="edit_slb_form.slb_id"
            size="small"
            disabled
          ></el-input>
        </el-form-item>
        <el-form-item
          label="地址"
          prop="address"
        >
          <el-input
            v-model="edit_slb_form.address"
            size="small"
            disabled
          ></el-input>
        </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="edit_slb_dialog = false"
        >取 消</el-button>
        <el-button
          size="small"
          type="primary"
          @click="submit_slb('edit_slb_form')"
        >确 定</el-button>
      </span>
    </el-dialog>
    <el-dialog
      title="标签"
      :visible.sync="label_dialog"
      width="800px"
      :before-close="handle_close"
    >
      <el-form ref="form" label-width="200px">
        <div>
          <!-- <textarea style="height: 500px;width: 100%;background-color: black;color: white"  v-model="record_log"></textarea> -->
          <resource-label :labels="lb_labels" @change="getLoadBalancerLabel"></resource-label>
        </div>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="operate_lbs('label')">打标签</el-button>
        <el-button @click="label_dialog= false">取消</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Pagination from "@/components/Pagination"
import { getSLBList } from "@/views/cmdb/api/slb"
import checkPermission from "@/utils/permission"
import ResourceLabel from '@/components/ResourceLabel'
import { getCloudManageApiPrefix, startLoadBalancer, stopLoadBalancer, labelLoadBalancer } from '@/views/cmdb/api/cloud_manage'
export default {
  name: "SLBList",
  components: {
    Pagination,
    ResourceLabel
  },
  data() {
    return {
      listQuery: {
        page: 1,
        limit: 15
      },
      total: 0,
      lb_labels: [{ value: '' }],
      current_group_role: '',
      multipleSelection: [],
      select_input: "name",
      input_content: "",
      dialogVisible: false,
      refresh_loading: false,
      edit_slb_dialog: false,
      slb_list: [],
      current_api_prefix: '',
      region: '',
      factory: '',
      kms_account: '',
      edit_slb_form: {
        id: "",
        name: "",
        slb_id: "",
        address: ""
      },
      label_dialog: false,
    }
  },
  watch: {
    current_select_product_name: function() {
      this.get_current_group_role()
    },
    multipleSelection: function () {
      if (this.multipleSelection.length > 0) {
        // 选择第一个实例的factory_name作为云厂商
        this.current_api_prefix = getCloudManageApiPrefix(this.multipleSelection[0]["factory__name"])
        // 选择第一个实例的region_name作为地域
        this.region = this.multipleSelection[0]["region__region_id"]
        this.factory = this.multipleSelection[0]["factory"]
        this.kms_account = this.multipleSelection[0]["factory__kms_account"]
      }
    }
  },
  computed: {
    ...mapGetters(["current_select_product_id", "current_select_product_name", "group_roles"]),
  },

  created() {
    this.get_slb_list()
    this.get_current_group_role()

  },
  methods: {
    checkPermission,
    getLoadBalancerLabel(labels) {
      this.lb_labels = labels
    },
    get_lb_status_tag(status) {
        if (status && (status.toUpperCase().indexOf("ACTIVE") !== -1)) {
          return 'success'
        } else if (status && (status.toUpperCase().indexOf("STOP") !== -1)) {
          return 'warning'
        } else if (status && (status.toUpperCase().indexOf("DELET") !== -1 || status.toUpperCase().indexOf("TERMINAT") !== -1)) {
          return 'danger'
        } else {
          return 'primary'
        }
    },
    get_current_group_role() {
      this.current_group_role = this.group_roles['' + this.current_select_product_name + '']
      // console.log("current_group_role", this.current_group_role)
    },
    handleSelectionChange(val) {
      this.multipleSelection = val
    },
    operate_lbs(otype) {
        var lbs_id = []
        var lbs_name = []
        var msg = ''
        var operator_function = ''
        var provider_list = []
        var region_list = []
        var params = {}
        var gcp_project_ids = []
        var gcp_project_zones = []
        this.multipleSelection.forEach((obj, key) => {
          if (provider_list.indexOf(obj["factory__name"]) === -1) {
            provider_list.push(obj["factory__name"])
          }
          if (region_list.indexOf(obj["region__name"]) === -1) {
            region_list.push(obj["region__name"])
          }
          lbs_id.push(obj["slb_id"])
          lbs_name.push(obj["name"])
          gcp_project_ids.push(obj['project__project_id'] ? obj['project__project_id'] : obj["gcp_project_id"])
          gcp_project_zones.push(obj["zone__name"])
        })
        if (provider_list.length > 1) {
          this.$alert("您勾选的实例属于多个云供应商。目前不支持一次勾选多个云厂商实例。请重新勾选", '提示', {
                confirmButtonText: '确定'
          })
          return false
        }
        if (region_list.length > 1) {
          this.$alert("您勾选的实例属于多个地域。目前不支持一次勾选多个地域的实例。请重新勾选", '提示', {
                confirmButtonText: '确定'
          })
          return false
        }
        if (gcp_project_ids.length > 0) {
          var size = new Set(gcp_project_ids).size
          if (size !== 1) {
            this.$alert("您勾选的实例属于不同的gcp project。目前不支持一次勾选多个project的实例。请重新勾选", '提示', {
                confirmButtonText: '确定'
            })
            return false
          }
        }

        if (gcp_project_zones.length > 0) {
          var siz = new Set(gcp_project_zones).size
          if (siz !== 1) {
            this.$alert("您勾选的实例属于不同的gcp区域。目前不支持一次勾选多个区域的实例。请重新勾选", '提示', {
                confirmButtonText: '确定'
            })
            return false
          }
        }
        switch (otype) {
          case "start": {
            msg = '此操作将开启' + lbs_name.join(", ") + ', 是否继续?'
            params = { 'lb_ids': lbs_id, 'region': this.region, 'factory': this.factory, 'gcp_project_id': gcp_project_ids.length > 0 ? gcp_project_ids[0] : 0, 'gcp_project_zone': gcp_project_zones.length > 0 ? gcp_project_zones[0] : 0, 'kms_account': this.kms_account }
            operator_function = startLoadBalancer
            break
          }
          case "label": {
            msg = '此操作将实例' + lbs_name.join(", ") + '打上标签是否继续?'
            params = { 'lb_ids': lbs_id, 'region': this.region, 'factory': this.factory, 'labels': this.machine_labels, 'gcp_project_id': gcp_project_ids.length > 0 ? gcp_project_ids[0] : 0, 'gcp_project_zone': gcp_project_zones.length > 0 ? gcp_project_zones[0] : 0, 'kms_account': this.kms_account }
            operator_function = labelLoadBalancer
            break
          }
          case "stop": {
            msg = '此操作将停止' + lbs_name.join(", ") + ', 是否继续?'
            params = { 'lb_ids': lbs_id, 'region': this.region, 'factory': this.factory, 'gcp_project_id': gcp_project_ids.length > 0 ? gcp_project_ids[0] : 0, 'gcp_project_zone': gcp_project_zones.length > 0 ? gcp_project_zones[0] : 0, 'kms_account': this.kms_account }
            operator_function = stopLoadBalancer
            break
          }
        }
        this.$confirm(msg, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'error'
        }).then(() => {
          this.listLoading = true
          operator_function(this.current_api_prefix, params)
          .then(response => {
            this.$alert(response.data.msg, '提示', {
                confirmButtonText: '确定',
                callback: action => {
                    location.reload()
                }
                })
          }).catch((err) => {
            this.$message({
              type: 'warning',
              message: err
            })
          })
        }).catch((e) => {
          console.log(e)
          this.$message({
            type: 'warning',
            message: '取消成功'
          })
        })
    },
    get_slb_list() {
      getSLBList(this.listQuery)
        .then(response => {
          this.slb_list = response.data.results
          this.total = response.data.count
          this.refresh_loading = false
          setTimeout(() => {
            this.listLoading = false
          }, 1.5 * 1000)
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    refresh_from_remote() {},
    search_handler() {
      // console.log(this.select_input, this.input_content)
      var params = this.select_input + "__contains"
      this.listQuery[params] = this.input_content
      this.get_slb_list()
    },
    clear_refresh() {
      this.get_slb_list()
    },
    edit_slb_info(scope) {
      this.edit_slb_dialog = true
      this.edit_slb_form.id = scope.row.id
      this.edit_slb_form.name = scope.row.name
      this.edit_slb_form.slb_id = scope.row.slb_id
      this.edit_slb_form.address = scope.row.address
    },
    submit_slb() {
      this.edit_slb_dialog = false
      // console.log(this.edit_slb_form)
    },
    get_row_key(row) {
      return row.id
    },
    toggleExpand(row) {
      const $table = this.$refs.slb_table_refs
      this.slb_list.map(item => {
        if (row.id !== item.id) {
          $table.toggleRowExpansion(item, false)
        }
      })
      $table.toggleRowExpansion(row)
    },
    handle_sync_command(command) {
      // console.log(command)
      if (command === "sync_slb_from_aliyun") {
        // console.log('同步阿里云SLB业务逻辑')
      } else if (command === "sync_slb_from_qcloud") {
        // console.log('同步腾讯云SLB业务逻辑')
      }
    },
    handle_close() {
      this.label_dialog = false
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
.iconfont_green {
  font-family: "iconfont" !important;
  font-size: 20px;
  font-style: normal;
  color: #67c23a;
}
.iconfont_red {
  font-family: "iconfont" !important;
  font-size: 20px;
  font-style: normal;
  color: #f56c6c;
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
