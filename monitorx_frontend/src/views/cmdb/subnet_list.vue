<template>
  <div class="app-container">
    <el-card class="box-card">
      <!-- 搜索相关 -->
      <div>
        <el-button
          size="small"
          icon="el-icon-back"
          @click="go_back"
        >返回</el-button>
        <el-input
          v-model="listQuery.name__contains"
          placeholder="子网名称"
          class="filter-item"
          style="width:300px;margin-left:10px"
          size="small"
          clearable
          @change="clear_refresh"
          @keyup.enter.native="search_filter"
        >
          <el-button
            slot="append"
            icon="el-icon-search"
            @click="search_filter"
          ></el-button>
        </el-input>
        <el-button
          v-if="checkPermission(['admin','ops'])"
          type="primary"
          size="small"
          icon="el-icon-circle-plus"
          style="margin-left: 10px"
          @click="create_subnet"
        >新增</el-button>
      </div>
      <!-- 子网列表表格 -->
      <el-table
        :data="subnet_id_list"
        style="width: 100%"
        border
        size="small"
      >
        <el-table-column
          prop="name"
          label="子网名称"
        >
        </el-table-column>
        <el-table-column
          prop="subnet_id"
          label="子网 ID"
        >
        </el-table-column>
        <el-table-column
          prop="cidr_block"
          label="CIDR"
        >
        </el-table-column>
        <el-table-column
          prop="zone__name"
          label="可用区"
        >
        </el-table-column>
        <el-table-column
          prop="factory__name"
          label="厂商"
        >
        </el-table-column>
        <el-table-column
          label="操作"
          width="80px;"
        >
          <template slot-scope="scoped">
            <el-button
              v-if="checkPermission(['admin','ops'])"
              type="warning"
              icon="el-icon-edit"
              size="mini"
              @click="edit_subnet_info(scoped.row)"
            ></el-button>
          </template>
        </el-table-column>
      </el-table>
      <!-- 分页组件 -->
      <pagination
        v-show="total>0"
        :total="total"
        :page.sync="listQuery.page"
        :limit.sync="listQuery.limit"
        @pagination="get_subnet_list"
      ></pagination>
      <!-- 创建subnet的Dialog -->
      <el-dialog
        title="创建子网"
        :visible.sync="createSubnetDialogFormVisible"
        width="50%"
      >
        <el-form
          :model="subnet_create_form"
          label-width="100px"
        >
          <el-form-item
            label="子网名称"
            style="width:300px"
            prop="name"
          >
            <el-input
              v-model="subnet_create_form.subnetName"
              style="width:300px"
              size="small"
            ></el-input>
          </el-form-item>
          <el-form-item
            label="区域"
            style="width:300px"
            prop="region"
          >
            <el-input
              v-model="subnet_create_form.region"
              style="width:300px"
              size="small"
              disabled
            ></el-input>
          </el-form-item>
          <el-form-item
            label="可用区"
            style="width:300px"
            prop="zoneId"
          >
            <el-select
              v-model="subnet_create_form.zoneId"
              style="width:300px"
              size="small"
            >
              <el-option
                v-for="item in zone_List"
                :key="item.id"
                :label="item.name"
                :value="`${item.name},${item.zone_id}`"
              >
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item
            label="CIDR"
            style="width:300px"
            prop="cidr_block"
          >
            <el-input
              v-model="subnet_create_form.cidr"
              style="width:300px"
              size="small"
            >
              <el-button
                v-if="cidrCheckResult==1"
                slot="append"
                style="color:green"
                icon="el-icon-success"
                @click="cidr_check"
              >
              </el-button>
              <el-button
                v-if="cidrCheckResult==2"
                slot="append"
                style="color:red"
                icon="el-icon-warning"
                @click="cidr_check"
              >
              </el-button>
              <el-button
                v-if="cidrCheckResult==0"
                slot="append"
                style="color:orange"
                icon="el-icon-question"
                @click="cidr_check"
              >
              </el-button>
            </el-input>
          </el-form-item>
        </el-form>
        <span
          slot="footer"
          class="dialog-footer"
        >
          <el-button
            size="small"
            @click="createSubnetDialogFormVisible = false"
          >取 消</el-button>
          <el-button
            type="primary"
            size="small"
            @click="submit_subnet_create"
          >确 定</el-button>
        </span>
      </el-dialog>
      <!-- 编辑或者更新子网信息Dialog -->
      <el-dialog
        title="编辑子网---真的在做了"
        :visible.sync="dialogFormVisible"
        width="50%"
      >
        <el-form
          :model="subnet_info_form"
          label-width="100px"
        >
          <el-form-item
            label="子网 ID"
            prop="subnet_id"
          >
            <el-input
              v-model="subnet_info_form.subnet_id"
              size="medium"
              disabled
            ></el-input>
          </el-form-item>
          <el-form-item
            label="子网名称"
            prop="name"
          >
            <el-input
              v-model="subnet_info_form.name"
              size="medium"
            ></el-input>
          </el-form-item>
          <el-form-item
            label="描述"
            prop="desc"
          >
            <el-input
              v-model="subnet_info_form.desc"
              size="medium"
            ></el-input>
          </el-form-item>
          <el-form-item
            label="CIDR"
            prop="cidr_block"
          >
            <el-input
              v-model="subnet_info_form.cidr_block"
              size="medium"
              disabled
            ></el-input>
          </el-form-item>
        </el-form>
        <span
          slot="footer"
          class="dialog-footer"
        >
          <el-button @click="dialogFormVisible = false">取 消</el-button>
          <el-button
            type="primary"
            @click="dialogFormVisible = false"
          >确 定</el-button>
        </span>
      </el-dialog>
    </el-card>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import { getSubnetList, updateSubnetByID, addSubnet } from '@/views/cmdb/api/subnet'
import { cidrCheck } from "@/views/cmdb/api/vpc"
import { getZoneList } from './api/zone'
import checkPermission from "@/utils/permission"
export default {
  name: 'SubnetList',
  components: { Pagination },
  data() {
    return {
      listQuery: {
        page: 1,
        limit: 15,
        name__contains: '',
        vpc__vpc_id: this.$route.query.vpcId
      },
      total: 0,
      subnet_list: [],
      zone_List: [],
      subnet_list_show: [],
      subnet_id_list: [],
      subnet_info_form: {
        id: null,
        region: '',
        name: '',
        desc: '',
        subnet_id: '',
        cidr_block: '',
        factory__name: '',
        region__name: ''
      },
      createSubnetDialogFormVisible: false,
      subnet_create_form: {
        project: this.$route.query.project,
        region: this.$route.query.region,
        subnetName: '',
        vpcId: this.$route.query.vpcId,
        cidr: '',
        supplier: this.$route.query.supplier,
        zoneId: ''
      },
      image_dialog: false,
      dialogFormVisible: false,
      sync_loading: false,
      cidrCheckResult: 0
    }
  },
  computed: {
  },
  created() {
    this.get_subnet_list()
    this.get_zone_list()
  },
  methods: {
    checkPermission,
    cidr_check() {
      var param = {
        vpc: this.$route.query.vpcCidr,
        cidr: this.subnet_create_form.cidr
      }
      cidrCheck(param).then(response => {
        if (response.data.status) {
          this.cidrCheckResult = 1
          this.$message({
            type: "success",
            message: response.data.msg
          })
        } else {
          this.cidrCheckResult = 2
          this.$message({
            type: "error",
            message: response.data.msg
          })
        }
      })
    },
    get_zone_list() {
      var param = {
        region__region_id: this.$route.query.region,
        factory__id: this.$route.query.supplier
      }
      getZoneList(param).then(response => {
        // console.log("getZoneList", response.data.results)
        this.zone_List = response.data.results
      })
    },
    get_subnet_list() {
      getSubnetList(this.listQuery)
        .then(response => {
          // console.log("getSubnetList", response)
          this.subnet_id_list = response.data.results
          this.total = response.data.count
          setTimeout(() => {
            this.listLoading = false
          }, 1.5 * 1000)
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 创建subnet
    create_subnet() {
      this.createSubnetDialogFormVisible = true
      this.subnet_create_form.subnetName = ''
      this.subnet_create_form.cidr = ''
      this.subnet_create_form.zoneId = ''
      this.cidrCheckResult = 0
    },
    // 提交创建的subnet
    submit_subnet_create() {
      // console.log("submit_subnet_create", this.subnet_create_form)
      addSubnet(this.subnet_create_form)
        .then(() => {
          this.$message({
            type: "success",
            message: "创建成功"
          })
          this.createSubnetDialogFormVisible = false
          this.get_subnet_list()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
      this.get_subnet_list()
      this.createSubnetDialogFormVisible = false
    },
    edit_subnet_info(param) {
      this.dialogFormVisible = true
      this.subnet_info_form.id = param.id
      this.subnet_info_form.subnet_id = param.subnet_id
      this.subnet_info_form.name = param.name
      this.subnet_info_form.factory__name = param.factory__name
      this.subnet_info_form.cidr_block = param.cidr_block
      this.subnet_info_form.desc = param.desc
      this.subnet_info_form.region = param.region
    },
    submit_vpc_info() {
      updateSubnetByID(this.subnet_info_form.id, this.subnet_info_form)
        .then(() => {
          this.$message({
            type: "success",
            message: "编辑成功"
          })
          this.dialogFormVisible = false
          this.get_subnet_list()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
      this.get_subnet_list()
      this.dialogFormVisible = false
    },
    search_filter() {
      this.get_subnet_list()
    },
    clear_refresh() {
      this.get_subnet_list()
    },
    go_back() {
      this.$router.push({ name: "Other", params: { active_tab_name: 'network_resouce' } })
    }
  }
}
</script>

<style scoped>
.el-table {
  margin-top: 15px;
}
/* .el-input {
  width: 200px;
  margin-left: 10px;
} */
</style>
