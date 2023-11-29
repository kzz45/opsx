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
              label="负载均衡"
              name="loadbalancer"
            >
              <div>
                <el-input
                  v-model="loadbalancer_input_content"
                  placeholder="可以模糊搜索"
                  class="filter-item"
                  clearable
                  size="small"
                  @keyup.enter.native="search_loadbalancer"
                >
                  <el-select
                    slot="prepend"
                    v-model="type_input_content"
                    size="small"
                    placeholder="请选择"
                  >
                    <el-option
                      label="负载均衡名"
                      value="name"
                    ></el-option>
                    <el-option
                      label="执行人"
                      value="user__username"
                    ></el-option>
                    <el-option
                      label="地域"
                      value="template__region"
                    ></el-option>
                  </el-select>
                  <el-button
                    slot="append"
                    icon="el-icon-search"
                    @click="search_loadbalancer"
                  ></el-button>
                </el-input>
                <el-button
                  type="primary"
                  icon="el-icon-circle-plus-outline"
                  size="small"
                  style="margin-left: 10px;"
                  @click="loadbalancer_dialog=true"
                >购买</el-button>
              </div>
              <el-table
                :data="loadbalancer_list"
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
                  prop="name"
                  label="负载均衡名"
                >
                </el-table-column>
                <el-table-column
                  prop="data"
                  label="数据"
                >
                  <template slot-scope="scope">
                    <json-viewer
                      :value="scope.row.data"
                      copyable
                    ></json-viewer>
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
                      @click="get_loadbalancer_detail(scope.row.id)"
                    >详情
                    </el-button>
                    <el-button
                      size="mini"
                      type="primary"
                      @click="get_loadbalancer_log(scope.row.id)"
                    >资源日志
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
              <pagination
                v-show="loadbalancer_total>0"
                :total="loadbalancer_total"
                :page.sync="listQuery.page"
                :limit.sync="listQuery.limit"
                @pagination="get_loadbalancer_list"
              ></pagination>
            </el-tab-pane>
          </el-tabs>
        </template>
      </div>
    </el-card>
    <!-- 新增机型的Dialog -->
    <el-dialog
      title="购买实例"
      :visible.sync="loadbalancer_dialog"
      width="50%"
    >
      <el-form
        ref="create_loadbalancer_form"
        :model="create_loadbalancer_form"
        :rules="create_loadbalancer_form_rules"
        label-width="100px"
        size="small"
      >
      <el-form-item label="负载均衡名" prop="name">
          <el-input
            v-model="create_loadbalancer_form.name"
            size="small"
            placeholder="load_balancer_name"
            style="width: 300px;"
          ></el-input>
      </el-form-item>
      <el-form-item label="后端信息" prop="data">
         <div v-for="(item, index) in create_loadbalancer_form.data" v-bind:key="index">
          <el-form label-width="100px">
           <el-form-item label="监听端口">
              <el-input
                v-model="item.listener.listener_port"
                size="small"
                placeholder="监听端口"
                style="width: 120px;"
              ></el-input>
           </el-form-item>
           <!-- <el-form-item label="服务器组名">
              <el-input
                v-model="item.listener.server_group"
                size="small"
                placeholder="服务器组名"
                style="width: 200px;"
              ></el-input>
           </el-form-item> -->
           <el-form-item label="前端协议" v-show="current_api_prefix == 'ali'">
             <el-select
              v-model="item.listener.protocol"
              placeholder="协议"
              size="small"
              filterable
             >
                <el-option
                  v-for="(i) in ['HTTP','HTTPS','TCP']"
                  :key="i"
                  :value="i"
                ></el-option>
            </el-select>
           </el-form-item>
           <el-form-item label="转发类型" v-show="current_api_prefix == 'aws'">
            <el-select
              v-model="item.listener.type"
              placeholder="forward"
              size="small"
              filterable
            >
              <el-option
                v-for="(i) in ['forward','authenticate-oidc', 'authenticate-cognito', 'fixed-response', 'redirect']"
                :key="i"
                :value="i"
              ></el-option>
            </el-select>
           </el-form-item>
           <el-form-item label="后端端口">
             <el-input
                v-model="item.target_group.target_port"
                size="small"
                placeholder="后端端口"
                style="width: 120px;"
              ></el-input>
           </el-form-item>
           <el-form-item label="后端协议">
            <el-select
              v-model="item.target_group.protocol"
              placeholder="后端协议"
              size="small"
              filterable
            >
              <el-option
                v-for="(i) in ['HTTP','HTTPS','TCP']"
                :key="i"
                :value="i"
              ></el-option>
            </el-select>
           </el-form-item>
           <el-form-item label="后端组">
            <project-machine :factory=template.factory :project_id=template.project :selected_data=item.target_group.instance_ids> </project-machine>
           </el-form-item>
           </el-form>
         </div>
        <el-button  style="margin-left:5px" @click.prevent="add_data()" type="primary"><i class="el-icon-plus"></i></el-button>
        <el-button  @click.prevent="remove_data(index)" type="danger"><i class="el-icon-minus"></i></el-button>

      </el-form-item>
      <el-form-item label="描述" prop="desc">
        <el-input v-model="create_loadbalancer_form.desc" type="textarea" style="width: 300px;"></el-input>
      </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="loadbalancer_dialog = false"
        >取 消</el-button>
        <el-button
          v-loading.fullscreen.lock="listLoading"
          type="primary"
          size="small"
          @click="create_loadbalancer()"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 资产记录的Dialog -->
    <el-dialog
      title="资源记录"
      :visible.sync="loadbalancer_detail_dialog"
      width="90%"
    >
      <template>
        <el-descriptions title="">
          <el-descriptions-item label="云厂商">{{ get_factory_map(loadbalancer.template__factory) }}</el-descriptions-item>
          <el-descriptions-item label="产品">{{ global_product_map[loadbalancer.template__product] }}</el-descriptions-item>
          <el-descriptions-item label="项目">{{ get_project_map(loadbalancer.template__project) }}</el-descriptions-item>
          <el-descriptions-item label="地域">{{ loadbalancer.template__region }}</el-descriptions-item>
          <el-descriptions-item label="资产ID">{{ loadbalancer.lb_arn }}</el-descriptions-item>
          <el-descriptions-item label="负载均衡名">{{ loadbalancer.template__name }}</el-descriptions-item>
          <el-descriptions-item label="可用区">{{ loadbalancer.template__zone_id }}</el-descriptions-item>
          <el-descriptions-item label="子网">{{ loadbalancer.template__subnet_id }}</el-descriptions-item>
          <el-descriptions-item label="Celery任务ID">{{ loadbalancer.celery_task_id }}</el-descriptions-item>
          <el-descriptions-item label="描述">{{ loadbalancer.desc }}</el-descriptions-item>
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
              <el-tag v-else type="danger">操作失败</el-tag>
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
                @click="get_record_log(scope.row.id)"
              >
                任务日志
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
          @click="loadbalancer_detail_dialog = false"
        >取 消</el-button>
      </span>
    </el-dialog>
    <el-dialog
      title="任务日志"
      :visible.sync="record_log_dialog"
      width="800px"
      :before-close="handleClose"
    >
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
      :visible.sync="loadbalancer_log_dialog"
      width="800px"
      :before-close="handleClose"
    >
      <el-form ref="form" label-width="200px">
        <div>
          <json-viewer :value="loadbalancer_log" copyable></json-viewer>
        </div>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="loadbalancer_log_dialog= false">取消</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import ProjectMachine from '@/components/project_machine'

import {
getResourceList, createLoadBalancer,
getResource, getTemplate,
getLoadBalancerLog, getRecordList,
getRecordCeleryLog, getCurrentApiPrefixFromLocalStorage } from '@/views/cmdb/api/cloud_manage'
import { getFactoryMap, getProjectMap } from '@/utils/auth'
import { mapGetters } from 'vuex'

export default {
  name: "Loadbalancer",
  components: { Pagination, ProjectMachine },
  data() {
    return {
      current_api_prefix: getCurrentApiPrefixFromLocalStorage() ? getCurrentApiPrefixFromLocalStorage() : 'ali',
      template_id: this.$route.params.template_id,
      loadbalancer_detail_dialog: false,
      active_tab_name: 'loadbalancer',
      listQuery: {
        page: 1,
        limit: 15
      },
      record_list: [],
      record_total: 0,
      // 资源操作日志相关--------------------------------------------------
      loadbalancer_list: [],
      loadbalancer_total: 0,
      type_input_content: 'name',
      loadbalancer_input_content: '',
      record_log_dialog: false,
      sync_loading: false,
      loadbalancer_dialog: false,
      loadbalancer_log_dialog: false,
      loadbalancer_log: '',
      listLoading: false,
      record_log: '',
      loadbalancer: {},
      template: {},
      create_loadbalancer_form_rules: {
          name: [{ required: true, message: '不能为空', trigger: 'blur' }]
      },
      create_loadbalancer_form: {
          name: "",
          template: this.$route.params.template_id,
          data: [{ "listener": { "protocol": "HTTP","listener_port": "", "type": "forward" }, "target_group": { "protocol": "HTTP", "target_port": "", "instance_ids": [] } }],
          desc: ""
      }
    }
  },
  // watch: {

  // },
  computed: {
    ...mapGetters([
      'global_product_list',
      'global_product_map',
      'current_select_product_id'
    ])
  },
  created() {
    this.get_template()
    this.get_loadbalancer_list()
  },
  methods: {
    get_factory_map(factory_id) {
      var factory_name = getFactoryMap(factory_id)
      return factory_name
    },
    get_project_map(project_id) {
      var project_name = getProjectMap(project_id)
      return project_name
    },
    get_record_log(id) {
      getRecordCeleryLog({ 'id': id })
      .then((resp) => {
          this.record_log = resp.data
          this.record_log_dialog = true
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
          console.log('template', this.template)
          this.create_loadbalancer_form.name = this.template.name
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    get_loadbalancer_detail(id) {
      getResource(this.current_api_prefix, this.active_tab_name, { 'id': id })
      .then((resp) => {
          this.loadbalancer = resp.data
          this.get_record_list()
          this.loadbalancer_detail_dialog = true
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    get_record_list() {
      // this.listQuery['factory'] = this.loadbalancer.template__factory
      // this.listQuery['region'] = this.loadbalancer.template__region
      // this.listQuery['resource_type'] = this.active_tab_name
      this.listQuery['celery_task_id'] = this.loadbalancer.celery_task_id
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
    get_loadbalancer_log(id) {
      getLoadBalancerLog(this.current_api_prefix, this.active_tab_name, id)
      .then((resp) => {
          this.loadbalancer_log = resp.data
          this.loadbalancer_log_dialog = true
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
      this.get_loadbalancer_list()
    },
    create_loadbalancer() {
      this.$refs.create_loadbalancer_form.validate((valid) => {
          if (valid) {
            this.listLoading = true
            var lb_name = this.create_loadbalancer_form.name
            this.create_loadbalancer_form.data.forEach(function(item){
                item['listener']['group_name'] =  lb_name + '-' + item['listener']['listener_port']
            })
            createLoadBalancer(this.current_api_prefix, this.create_loadbalancer_form)
            .then(response => {
                  this.$alert(response.data.msg, '提示', {
                  confirmButtonText: '确定',
                  callback: action => {
                     location.reload()
                  }
                  })
              // alert(response.data.msg)
            }).catch(err => {
              this.listLoading = false
              this.$alert(err, '提示', {
                confirmButtonText: '确定'
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
    search_loadbalancer() {
      // this.reset_list_query()
      var params = this.type_input_content + "__contains"
      this.listQuery.page = 1
      this.listQuery[params] = this.loadbalancer_input_content
      this.get_loadbalancer_list()
    },
    // 获取资源执行日志列表
    get_loadbalancer_list() {
      this.listQuery['template'] = this.template_id
      getResourceList(this.current_api_prefix, this.active_tab_name, this.listQuery)
        .then(response => {
          this.loadbalancer_list = response.data.results
          console.log("loadbalancer_list", this.loadbalancer_list)
          this.loadbalancer_total = response.data.count
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
    handleClose() {
      this.loadbalancer_log_dialog = false
      this.record_log_dialog = false
      this.loadbalancer_dialog = false
    },
    add_data() {
      this.create_loadbalancer_form.data.push({ "listener": { "protocol": "HTTP", "listener_port": "", "type": "forward" }, "target_group": { "protocol": "HTTP", "target_port": "", "instance_ids": [] } })
    },
    remove_data(index) {
      if (this.create_loadbalancer_form.data.length === 1) {
        return false
      }

      this.create_loadbalancer_form.data.splice(index, 1)
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
