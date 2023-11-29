<template>
  <div class="app-container">
    <el-card class="box-card">
      <div style="margin-top: 10px">
        <template>
          <el-tabs
            v-model="active_tab_name"
            @tab-click="tab_click"
          >
            <el-tab-pane
              label="虚拟机"
              name="instance"
            >
              <div>
                <el-input
                  v-model="instance_input_content"
                  placeholder="可以模糊搜索"
                  class="filter-item"
                  clearable
                  size="small"
                  @keyup.enter.native="search_instance"
                >
                  <el-select
                    slot="prepend"
                    v-model="type_input_content"
                    size="small"
                    placeholder="请选择"
                  >
                    <el-option
                      label="执行人"
                      value="user__username"
                    ></el-option>
                    <el-option
                      label="地域"
                      value="template__region"
                    ></el-option>
                    <el-option
                      label="主机名"
                      value="host_name"
                    ></el-option>
                    <el-option
                      label="购买数量"
                      value="amount"
                    ></el-option>
                  </el-select>
                  <el-button
                    slot="append"
                    icon="el-icon-search"
                    @click="search_instance"
                  ></el-button>
                </el-input>
                <el-button
                    type="primary"
                    icon="el-icon-circle-plus-outline"
                    size="small"
                    style="margin-left: 10px;"
                    @click="instance_dialog=true"
                >购买</el-button>
              </div>
              <el-table
                :data="instance_list"
                style="width: 100%; margin-top: 10px;"
                border
                size="small"
              >
                <el-table-column
                  prop="template__region"
                  label="地域名称"
                >
                </el-table-column>
                <el-table-column label="云厂商" align="center">
                    <template slot-scope="scope">
                      <span>{{ get_factory_map(scope.row.template__factory) }}</span>
                    </template>
                </el-table-column>
                <el-table-column
                  prop="host_name"
                  label="主机名"
                >
                </el-table-column>
                <el-table-column
                  prop="amount"
                  label="数量"
                >
                </el-table-column>
                <el-table-column
                  prop="update_time"
                  label="更新时间"
                >
                </el-table-column>
                <el-table-column
                  prop="username"
                  label="执行人"
                >
                </el-table-column>
                <el-table-column
                  label="操作"
                >
                <template slot-scope="scope">
                  <el-button
                    size="mini"
                    type="success"
                    @click="get_instance_detail(scope.row.id)" >详情
                  </el-button>
                  <el-button
                    size="mini"
                    type="primary"
                    @click="get_instance_log(scope.row.id)" >资源日志
                  </el-button>
                </template>
                
                </el-table-column>
              </el-table>
              <pagination
                v-show="instance_total>0"
                :total="instance_total"
                :page.sync="listQuery.page"
                :limit.sync="listQuery.limit"
                @pagination="get_instance_list"
              ></pagination>
            </el-tab-pane>
          </el-tabs>
        </template>
      </div>
    </el-card>
    <!-- 新增机型的Dialog -->
    <el-dialog
      title="购买实例"
      :visible.sync="instance_dialog"
      width="50%"
    >
      <el-form
        ref="create_instance_form"
        :model="create_instance_form"
        :rules="create_instance_form_rules"
        label-width="100px"
        size="small"
      >
      <el-form-item label="主机名" prop="host_name">
          <el-input
            v-model="create_instance_form.host_name"
            size="small"
            placeholder="tsh-plat2public-qa-kma"
            style="width: 300px;"
          ></el-input><el-tag size="small" type="danger" v-show="current_api_prefix === 'ali' && create_instance_form.amount == 1">阿里云提醒: 如果只购买一台，请确保主机名不以中划线”-“结尾</el-tag>
      </el-form-item>
      <el-form-item label="购买数量">
          <el-input
            v-model="create_instance_form.amount"
            size="small"
            style="width: 300px;"
          ></el-input>
      </el-form-item>
      <el-form-item label="描述" prop="desc">
          <el-input type="textarea" v-model="create_instance_form.desc" style="width: 300px;"></el-input>
      </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="instance_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          v-loading.fullscreen.lock="listLoading"
          @click="create_instance()"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 资产记录的Dialog -->
    <el-dialog
      title="资源记录"
      :visible.sync="instance_detail_dialog"
      width="90%"
    >
      <template>
        <el-descriptions title="">
            <el-descriptions-item label="云厂商">{{get_factory_map(instance.template__factory)}}</el-descriptions-item>
            <el-descriptions-item label="产品">{{global_product_map[instance.template__product]}}</el-descriptions-item>
            <el-descriptions-item label="项目">{{get_project_map(instance.template__project)}}</el-descriptions-item>
            <el-descriptions-item label="地域">{{instance.template__region}}</el-descriptions-item>
            <el-descriptions-item label="资产ID">{{instance.instance_ids}}</el-descriptions-item>
            <el-descriptions-item label="主机名">{{instance.template__host_name}}</el-descriptions-item>
            <el-descriptions-item label="可用区">{{instance.template__zone_id}}</el-descriptions-item>
            <el-descriptions-item label="子网">{{instance.template__subnet_id}}</el-descriptions-item>
            <el-descriptions-item label="磁盘尺寸">{{instance.template__system_disk_size}}</el-descriptions-item>
            <el-descriptions-item label="磁盘类型">{{instance.template__system_disk_category}}</el-descriptions-item>
            <!-- <el-descriptions-item label="入带宽">{{instance.internet_max_bandwidth_in}}</el-descriptions-item>
            <el-descriptions-item label="出带宽">{{instance.internet_max_bandwidth_out}}</el-descriptions-item> -->
            <el-descriptions-item label="付款类型">
              <el-tag size="small">{{instance.template__instance_charge_type}}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="购买数量">
              <el-tag size="small">{{instance.amount}}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="Celery任务ID">{{instance.celery_task_id}}</el-descriptions-item>
            <el-descriptions-item label="描述">{{instance.desc}}</el-descriptions-item>


        </el-descriptions>
        <el-table
              :data="record_list"
              style="width: 100%; margin-top: 10px;"
              border
              size="small"
            >
              <el-table-column
                prop="region"
                label="地域"
              >
              </el-table-column>
              <el-table-column label="云厂商" align="center">
                  <template slot-scope="scope">
                    <span>{{ get_factory_map(scope.row.factory) }}</span>
                  </template>
              </el-table-column>
              <el-table-column
                prop="resource_id"
                label="资产ID"
              >
              </el-table-column>
              <el-table-column
                prop="resource_name"
                label="资产名称"
              >
              </el-table-column>
              <el-table-column
                prop="resource_type"
                label="资产类型"
              >
              </el-table-column>
              <el-table-column label="资产状态">
              <template slot-scope="scope">
                    <el-tag v-if="scope.row.status == 0" type="primary">待开始</el-tag>
                    <el-tag v-else-if="scope.row.status == 1" type="primary">正在购买</el-tag>
                    <el-tag v-else-if="scope.row.status == 2" type="success">购买成功</el-tag>
                    <el-tag v-else-if="scope.row.status == 4" type="warning">资产启动</el-tag>
                    <el-tag v-else-if="scope.row.status == 5" type="warning">资产升降配</el-tag>
                    <el-tag v-else-if="scope.row.status == 6" type="warning">重启</el-tag>
                    <el-tag v-else-if="scope.row.status == 7" type="danger">已退还</el-tag>
                    <el-tag v-else-if="scope.row.status == 8" type="danger">已停止</el-tag>
                    <el-tag v-else type="danger">操作失败</el-tag >
              </template>
              </el-table-column>
              <el-table-column
                prop="update_time"
                label="更新时间"
              >
              </el-table-column>
              <el-table-column
                prop="username"
                label="执行人"
              >
              </el-table-column>
              <el-table-column
                label="操作"
              >
              <template slot-scope="scope">
                <el-button
                  size="mini"
                  type="success"
                  @click="get_record_log(scope.row.id)" >任务日志
                </el-button>
              </template>
              </el-table-column>
            </el-table>
            <pagination
              v-show="record_total>0"
              :total="record_total"
              :page.sync="listQuery.page"
              :limit.sync="listQuery.limit"
              @pagination="get_record_list"
            ></pagination>
      </template>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="instance_detail_dialog = false"
        >取 消</el-button>
      </span>
    </el-dialog>
    <el-dialog
      title="任务日志"
      :visible.sync="record_log_dialog"
      width="800px"
      :before-close="handleClose">
      <el-form ref="form" label-width="200px">
        <div>
           <!-- <textarea style="height: 500px;width: 100%;background-color: black;color: white"  v-model="record_log"></textarea> -->
           <json-viewer :value="record_log" copyable></json-viewer>

        </div>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="record_log_dialog= false">取消</el-button>
      </span>
    </el-dialog>
    <el-dialog
      title="资源日志"
      :visible.sync="instance_log_dialog"
      width="800px"
      :before-close="handleClose">
      <el-form ref="form" label-width="200px">
        <div>
           <json-viewer :value="instance_log" copyable></json-viewer>

        </div>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="instance_log_dialog= false">取消</el-button>
      </span>
    </el-dialog> 
  </div>
</template>

<script>
import Vue from 'vue'
import Pagination from '@/components/Pagination'
import {getResourceList, createInstance, getResource, getTemplate, getInstanceLog,getRecordList,getRecordCeleryLog,setCurrentApiPrefixFromLocalStorage,getCurrentApiPrefixFromLocalStorage} from '@/views/cmdb/api/cloud_manage'
import { getFactoryMap, getProjectMap } from '@/utils/auth'
import { mapGetters } from 'vuex'


export default {
  name: "Instance",
  components: { Pagination },
  data() {
    return {
      current_api_prefix: getCurrentApiPrefixFromLocalStorage() ? getCurrentApiPrefixFromLocalStorage() : 'ali',
      template_id: this.$route.params.template_id,
      instance_detail_dialog: false,
      active_tab_name: 'instance',
      listQuery: {
        page: 1,
        limit: 15
      },
      record_list: [],
      record_total: 0,
      // 资源操作日志相关--------------------------------------------------
      instance_list: [],
      instance_total: 0,
      type_input_content: '',
      instance_input_content: '',
      record_log_dialog: false,
      sync_loading: false,
      instance_dialog: false,
      instance_log_dialog: false,
      instance_log: '',
      listLoading: false,
      record_log: '',
      instance: {},
      template: {},
      create_instance_form_rules: {
          amount: [{ required: true, message: '不能为空', trigger: 'blur' }],
      },
      create_instance_form: {
          host_name: "",
          template: this.$route.params.template_id,
          amount: 1,
          desc: ''
      },
    }
  },
  watch: {
  },
  computed: {
    ...mapGetters([
      'global_product_list',
      'global_product_map',
      'current_select_product_id'
    ])
  },
  created() {
    this.get_instance_list()
    this.get_template()
  },
  methods: {
    get_factory_map(factory_id) {
      var factory_name = getFactoryMap(factory_id)
      return factory_name
    },
    get_project_map(project_id) {
      var project_name = getProjectMap(project_id)
      console.log("project_id",project_id)
      console.log("project_name",project_name)
      return project_name
    },
    get_record_log(id) {
      getRecordCeleryLog({'id': id})
      .then((resp) => {
          this.record_log = resp.data
          this.record_log_dialog= true

        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    get_template() {
      getTemplate(this.current_api_prefix, this.active_tab_name, this.template_id)
      .then((resp) => {
          this.template = resp.data
          this.create_instance_form.host_name = this.template.host_name
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    get_instance_detail(id) {
      getResource(this.current_api_prefix,this.active_tab_name, {'id': id})
      .then((resp) => {
          this.instance = resp.data
          this.get_record_list()
          this.instance_detail_dialog = true
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    get_record_list() {
      // this.listQuery['factory'] = this.instance.template__factory
      // this.listQuery['region'] = this.instance.template__region
      // this.listQuery['resource_type'] = this.active_tab_name
      this.listQuery['celery_task_id'] = this.instance.celery_task_id
      getRecordList(this.listQuery)
        .then(response => {
          this.record_list = response.data.results
          this.record_total = response.data.count
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
    get_instance_log(id) {
      getInstanceLog(this.current_api_prefix, this.active_tab_name, id)
      .then((resp) => {
          this.instance_log = resp.data
          this.instance_log_dialog= true
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    tab_click(tab) {
      this.active_tab_name = tab.name
      this.get_instance_list()
    },
    create_instance() {
      this.$refs.create_instance_form.validate((valid) => {
          if (valid) {
            this.listLoading = true
            createInstance(this.current_api_prefix, this.create_instance_form)
            .then(response => {
                  this.$alert(response.data.msg, '提示', {
                  confirmButtonText: '确定',
                  callback: action => {
                     location.reload()
                  }
                  })
              // alert(response.data.msg)
            }).catch(err => {
              console.log("create_instance err",err)
              this.listLoading = false
              this.$alert(err, '提示', {
                confirmButtonText: '确定',
                // callback: action => {
                //    location.reload()
                // }
                })
            })
          } else {
            this.$message({
              type: "warning",
              message: "配置有误，请检查"
            })
          }
        }
        )

    },
    // 搜索执行日志
    search_instance() {
      // this.reset_list_query()
      var params = this.type_input_content + "__contains"
      this.listQuery.page = 1
      this.listQuery[params] = this.instance_input_content
      this.get_instance_list()
    },
    // 获取资源执行日志列表
    get_instance_list() {
      this.listQuery['template'] = this.template_id
      getResourceList(this.current_api_prefix, this.active_tab_name, this.listQuery)
        .then(response => {
          this.instance_list = response.data.results
          this.instance_total = response.data.count
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
    handleClose(){
      this.instance_log_dialog= false
      this.record_log_dialog= false
      this.instance_dialog=false
    }
  }
}
</script>

<style scoped>
.el-select {
  width: 120px;
}
.el-input {
  width: 400px;
}
.dashboard-div {
  width: 20%;
  display: inline-block;
  margin-left: 0;
  margin-top: 10px;
}
.el-card__body {
  padding-bottom: 0;
}
.dashboard-button-div {
  width: 180px;
  height: 50px;
}
.dashboard-div-icon {
  float: left;
  width: 50px;
  height: 100%;
  margin-right: 10px;
}
.el-icon {
  font-size: 32px;
  line-height: 50px;
  color: #606266;
}
.dashboard-div-body {
  float: left;
  width: 120px;
  height: 100%;
  text-align: left;
}
.dashboard-title {
  font-size: 15px;
  margin-top: 6px;
  color: #606266;
  height: 18px;
  line-height: 18px;
}
.dashboard-desc {
  color: #999999;
  margin-top: 6px;
  font-size: 12px;
}
.ellipsis {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
