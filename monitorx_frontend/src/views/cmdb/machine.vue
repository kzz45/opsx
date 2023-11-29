<template>
  <div class="app-container">
    <el-card class="box-card">
      <!-- 搜索相关 -->
      <div>
        <el-input
          v-model="input_content"
          placeholder="找点啥(多个搜索用逗号分隔)"
          class="input-with-select"
          clearable
          size="small"
          @keyup.enter.native="search_handler"
          @clear="reset_search"
        >
          <el-select
            slot="prepend"
            v-model="select_input"
            size="small"
            placeholder="请选择"
            @change="reset_search"
          >
            <el-option
              label="实例ID"
              value="external_uuid"
            ></el-option>
            <el-option
              label="实例名称"
              value="external_name"
            ></el-option>
            <el-option
              label="外网IP"
              value="public_ip"
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
          v-if="current_group_role==='运维'"
          effect="dark"
          content="分配资源"
          placement="top-start"
        >
          <el-button
            size="small"
            icon="el-icon-position"
            style="margin-left: 10px"
            :loading="associate_loading"
            @click="associate_machine_to_product"
          >
          </el-button>
        </el-tooltip>
        <el-button
          type="info"
          size="small"
          style="margin-left: 10px"
          :icon="show_more_search?'el-icon-arrow-up':'el-icon-arrow-down'"
          @click="more_search"
        >
          {{ show_more_search ? "收起搜索": "更多搜索" }}
        </el-button>
        <el-tooltip
          v-if="current_group_role==='运维'"
          effect="dark"
          content="导入资源"
          placement="top-start"
        >
          <el-button
            size="small"
            type="primary"
            icon="el-icon-upload"
            style="margin-left: 10px"
            @click="open_upload"
          >
          </el-button>
        </el-tooltip>
        <el-button
          v-if="current_group_role==='运维'"
          v-show="multipleSelection.length > 0"
          type="danger"
          size="small"
          style="margin-left: 10px"
          @click="label_dialog=true"
        >
          打标签
        </el-button>
        <el-button
          v-if="current_group_role==='运维'"
          v-show="multipleSelection.length > 0"
          type="warning"
          size="small"
          @click="operate_instances('stop')"
        >
          停止实例
        </el-button>
        <el-button
          v-if="current_group_role==='运维'"
          v-show="multipleSelection.length > 0"
          type="info"
          size="small"
          @click="operate_instances('reboot')"
        >
          重启实例
        </el-button>
        <el-button
          v-if="current_group_role==='运维'"
          v-show="multipleSelection.length > 0"
          type="success"
          size="small"
          @click="operate_instances('start')"
        >
          开启实例
        </el-button>
        <el-button
          v-if="current_group_role==='运维'"
          v-show="multipleSelection.length > 0"
          type="primary"
          size="small"
          @click="modify_instance_dialog=true"
        >
          升/降配实例
        </el-button>
        <el-button
          v-if="current_group_role==='运维'"
          v-show="multipleSelection.length > 0"
          type="danger"
          size="small"
          @click="operate_instances('delete')"
        >
          删除实例
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
                    prop="zone__region__name"
                  >
                    <el-select
                      v-model="more_search_form.zone__region__name"
                      placeholder="请选择地区"
                      size="small"
                      filterable
                      @change="more_search_submit"
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
                      filterable
                      size="small"
                      @change="more_search_submit"
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
                    prop="external_status"
                  >
                    <el-select
                      v-model="more_search_form.external_status"
                      placeholder="请选择状态"
                      size="small"
                      @change="more_search_submit"
                    >
                      <el-option
                        v-for="item in status_filter_list"
                        :key="item"
                        :label="item"
                        :value="item"
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
      <!-- 机器列表表格 -->
      <el-table
        ref="machine_table_refs"
        v-loading="listLoading"
        :data="ecs_list"
        :row-key="get_row_key"
        tooltip-effect="dark"
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
          label="内网IP"
          prop="private_ip"
        ></el-table-column>
        <el-table-column
          label="机型"
          prop="cpu"
        >
          <template slot-scope="scoped">
            {{ scoped.row.cpu }}核 / {{ scoped.row.mem }}G
          </template>
        </el-table-column>
        <el-table-column
          label="地区"
          prop="region__name"
        ></el-table-column>
        <el-table-column
          label="使用状态"
          prop="external_status"
        >
          <template slot-scope="scoped">
            <el-tag :type="get_instance_status_tag(scoped.row.external_status)">{{ get_instance_status(scoped.row.external_status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          label="厂商"
          prop="factory__name"
        ></el-table-column>
        <el-table-column
          v-for="column in bindTableColumns"
          :key="column.prop"
          :prop="column.prop"
          :label="column.label"
        >
        </el-table-column>
        <el-table-column
          label="操作"
          width="200px"
        >
          <template slot-scope="scope">
            <el-button
              type="info"
              icon="el-icon-info"
              size="mini"
              @click="get_real_instance(scope.row)"
            ></el-button>
            <el-tooltip
              class="item"
              effect="dark"
              content="查看归属项目"
              placement="top"
            >
              <el-button
                type="success"
                size="mini"
                icon="el-icon-s-promotion"
                style="margin-left: 5px;"
                @click="view_under_project(scope.row)"
              ></el-button>
            </el-tooltip>
            <el-tooltip
              class="item"
              effect="dark"
              content="实例操作日志"
              placement="top"
            >
              <el-button
                type="warning"
                size="mini"
                icon="el-icon-chat-dot-square"
                style="margin-left: 5px;"
                @click="view_operate_log(scope.row)"
              ></el-button>
            </el-tooltip>
            <!-- <el-dropdown style="margin-left: 10px">
              <el-button
                type="danger"
                size="mini"
                icon="el-icon-question"
              >
              </el-button>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item>开机</el-dropdown-item>
                <el-dropdown-item>关机</el-dropdown-item>
                <el-dropdown-item>重启</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown> -->

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
              <el-form-item label="主机名称:">
                <span>{{ props.row.external_hostname }}</span>
              </el-form-item>
              <el-form-item label="实例状态:">
                <el-tag :type="get_instance_status_tag(scoped.row.external_status)">{{ get_instance_status(scoped.row.external_status) }}</el-tag>
              </el-form-item>
              <el-form-item label="内网地址:">
                <span>{{ props.row.private_ip }}</span>
              </el-form-item>
              <el-form-item label="外网地址:">
                <span>{{ props.row.public_ip }}</span>
              </el-form-item>
              <el-form-item label="机型:">
                <span>{{ props.row.external_flavor }}</span>
              </el-form-item>
              <el-form-item label="CPU:">
                <span>{{ props.row.cpu }}</span>
              </el-form-item>
              <el-form-item label="内存:">
                <span>{{ props.row.mem }}</span>
              </el-form-item>
              <el-form-item label="磁盘:">
                <span>{{ props.row.disk }}</span>
              </el-form-item>
              <el-form-item label="地区:">
                <span>{{ props.row.region__name }}</span>
              </el-form-item>
              <el-form-item label="可用区:">
                <span>{{ props.row.zone__name }}</span>
              </el-form-item>
              <el-form-item label="厂商:">
                <span>{{ props.row.factory__name }}</span>
              </el-form-item>
              <el-form-item label="所属产品:">
                <span>{{ props.row.product__name }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
      </el-table>
      <pagination
        v-show="total>0"
        :total="total"
        :page.sync="listQuery.page"
        :limit.sync="listQuery.limit"
        @pagination="get_ecs_list"
      ></pagination>
    </el-card>
    <!-- 资产记录的Dialog -->
    <el-dialog
      title="资源记录"
      :visible.sync="instance_detail_dialog"
      width="80%"
    >
      <template>
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
            <span>{{ instance.factory__name }}</span>
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
              >任务日志
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
    <!-- 查看更新信息的Dialog -->
    <el-dialog
      title="你想看啥"
      :visible.sync="dialogVisible"
      width="50%"
    >
      <el-checkbox-group v-model="checkedTableColumns">
        <el-checkbox
          v-for="column in machineTableColumns"
          :key="column.prop"
          :label="column.prop"
          :disabled="column.disabled"
          class="el-checkbox-width"
          border
        >{{ column.label }}</el-checkbox>
      </el-checkbox-group>
    </el-dialog>
    <!-- 分配分组或者产品的Dialog -->
    <el-dialog
      :title="dialogTextMap[dialogStatus]"
      :visible.sync="group_product_dialog"
      width="50%"
    >
      <el-form
        ref="associate_machineRefs"
        :model="associate_machine"
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
    <el-dialog
      title="任务日志"
      :visible.sync="record_log_dialog"
      width="800px"
      :before-close="handle_close"
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
      title="标签"
      :visible.sync="label_dialog"
      width="800px"
      :before-close="handle_close"
    >
      <el-form ref="form" label-width="200px">
        <div>
          <!-- <textarea style="height: 500px;width: 100%;background-color: black;color: white"  v-model="record_log"></textarea> -->
          <resource-label :labels="machine_labels" @change="getMachineLabel"></resource-label>

        </div>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="operate_instances('label')">打标签</el-button>
        <el-button @click="label_dialog= false">取消</el-button>
      </span>
    </el-dialog>
    <el-dialog
      v-loading="listLoading"
      :visible.sync="real_instance_dialog"
      width="800px"
      :before-close="handle_close"
    >
      <el-descriptions title="实例详情">
        <el-descriptions-item label="实例名称">{{ real_instance.external_name }}</el-descriptions-item>
        <el-descriptions-item label="实例ID">{{ real_instance.external_uuid }}</el-descriptions-item>
        <el-descriptions-item label="主机名称">{{ real_instance.external_hostname }}</el-descriptions-item>
        <el-descriptions-item label="实例状态">
          <el-tag :type="get_instance_status_tag(real_instance.external_status)">{{ get_instance_status(real_instance.external_status) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="内网地址">{{ real_instance.private_ip }}</el-descriptions-item>
        <el-descriptions-item label="外网地址">{{ real_instance.public_ip }}</el-descriptions-item>
        <el-descriptions-item label="机型">{{ real_instance.external_flavor }}</el-descriptions-item>
        <!-- <el-descriptions-item label="CPU">{{real_instance.cpu}}</el-descriptions-item>
        <el-descriptions-item label="内存">{{real_instance.mem}}</el-descriptions-item> -->
        <el-descriptions-item label="磁盘">{{ real_instance.disk }}</el-descriptions-item>
        <el-descriptions-item label="地区">{{ real_instance.region__name }}</el-descriptions-item>
        <el-descriptions-item label="可用区">{{ real_instance.zone__name }}</el-descriptions-item>
        <el-descriptions-item label="厂商">{{ real_instance.factory__name }}</el-descriptions-item>
        <el-descriptions-item label="所属产品">{{ real_instance.product__name }}</el-descriptions-item>
        <el-descriptions-item label="所属项目">{{ real_instance.project__name }}</el-descriptions-item>
        <el-descriptions-item label="标签">{{ real_instance.tags }}</el-descriptions-item>
      </el-descriptions>
      <span slot="footer" class="dialog-footer">
        <el-button @click="real_instance_dialog= false">取消</el-button>
      </span>
    </el-dialog>
    <!-- 升降配机器 -->
    <el-dialog
      title="升/降配机器"
      :visible.sync="modify_instance_dialog"
      width="50%"
    >
      <el-form
        ref="flavor"
        :model="modify_instance_form"
        label-width="100px"
      >
        <el-form-item
          label="机器规格"
        >
          <el-select
            v-model="modify_instance_form.instance_type"
            placeholder="请选择规格"
            filterable
            style="width: 300px;"
            size="small"
          >
            <el-option
              v-for="item in flavor_list"
              :key="item.name"
              :label="item.name"
              :value="item.name"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="modify_instance_form.desc" type="textarea" style="width: 300px;"></el-input>
        </el-form-item>
        <!-- <el-form-item
          label="磁盘规格"
        >
          <el-select
            v-model="modify_instance_form.system_disk_category"
            placeholder="请选择磁盘规格"
            style="width: 300px;"
            size="small"
          >
            <el-option
              v-for="item in get_system_disk_category_list()"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            >
            </el-option>
          </el-select>
        </el-form-item> -->
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="modify_instance_dialog=false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="operate_instances('modify')"
        >确 定</el-button>
      </span>
    </el-dialog>
    <el-dialog
      title="导入资源"
      :visible.sync="uploadVisible"
      width="50%"
    >
      <el-form
        ref="upload_formRefs"
        :model="uploadData"
        label-width="100px"
      >
        <el-form-item
          label="字段示例"
          style="width:600px"
        >
          <el-col :span="24">
            点击按钮复制表头字段
            <el-button
              type="plain"
              size="mini"
              icon="el-icon-copy-document"
              @click="copyText"
            >
            </el-button>
          </el-col>
        </el-form-item>
        <el-form-item
          label="选择云厂"
          style="width:600px"
          prop="factory"
        >
          <el-select
            v-model="uploadData.factory"
            size="small"
            clearable
            filterable
            style="width: 300px"
          >
            <el-option
              v-for="item in factory_name_list"
              :key="item.name"
              :label="item.name"
              :value="item.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          label="选择产品"
          style="width:600px"
          prop="product"
        >
          <el-select
            v-model="uploadData.product"
            size="small"
            clearable
            filterable
            style="width: 300px"
          >
            <el-option
              v-for="item in product_list"
              :key="item.name"
              :label="item.name"
              :value="item.id"
            ></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <el-upload
        class="inline-block"
        :action="'#'"
        :on-change="onBeforeUpload"
        :on-exceed="onExceed"
        :auto-upload="false"
        :file-list="uploadFileList"
        accept=".csv"
        :limit="1"
      >
        <el-button size="small" type="primary" style="margin-left: 20px">
          上传csv
        </el-button>
      </el-upload>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="reset_uploadData"
        >关 闭</el-button>
        <el-button
          type="primary"
          size="small"
          @click="onUpload"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Pagination from '@/components/Pagination'
import ResourceLabel from '@/components/ResourceLabel'

import { getMachineList, updateMachineByID, postUpload } from '@/views/cmdb/api/machine'
import { getCloudManageApiPrefix, startInstance, stopInstance, rebootInstance, modifyInstance, deleteInstance,
getRecordList, getRecordCeleryLog, labelInstance, getRealInstance } from '@/views/cmdb/api/cloud_manage'

import { getProductList } from '@/api/product'
import { getProjectList } from '@/api/project'

import { getFactoryList } from '@/api/factory'
import { getHostGroupList } from '@/api/host_group'
import { getRegionList } from '@/views/cmdb/api/region'
import { getFlavorList } from '@/views/cmdb/api/flavor'

export default {
  name: "MachineList",
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
      real_instance: {
        external_status: ''
      },
      machine_labels: [{ value: '' }],
      total: 0,
      label_dialog: false,
      record_log_dialog: false,
      record_log: '',
      record_total: 0,
      record_list: [],
      instance_detail_dialog: false,
      group_product_dialog: false,
      dialogTextMap: {
        group: "关联分组",
        product: "关联产品和分组"
      },
      flavor_list: [],
      flavor_total: 0,
      modify_instance_form: {
        instance_type: "",
        system_disk_category: "",
        desc: ""
      },
      current_api_prefix: '',
      current_group_role: '',
      real_instance_dialog: false,
      modify_instance_dialog: false,

      dialogStatus: '',
      associate_machine: {},
      product_id: "",
      group_id: "",
      group_list: [],
      product_list: [],
      listLoading: false,
      real_instance_Loading: false,
      dialogVisible: false,
      associate_loading: false,
      refresh_loading: false,
      input_content: '',
      select_input: 'external_uuid',
      public_ip: '',
      private_ip: '',
      instance: {},
      region: '',
      factory: '',
      kms_account: '',
      ecs_list: [],
      multipleSelection: [],
      machineTableColumns: [
        {
          prop: "external_hostname",
          label: "主机名称",
          show: false,
          disabled: false
        },
        { prop: "public_ip", label: "外网IP", show: false, disabled: false },
        { prop: "external_flavor", label: "机型", show: false, disabled: false }
      ],
      region_filter_list: [],
      factory_name_list: [],
      status_filter_list: ["RUNNING", "STOPPED", "DELETED,TERMINATED,DELETING", "STARTING"],
      show_more_search: false,
      more_search_form: {
        external_status: null,
        factory__name: null,
        zone__region__name: null
      },
      uploadData: {
        resourceType: "machine",
        factory: "",
        product: ""
      },
      uploadFileList: [],
      uploadVisible: false
    }
  },
  computed: {
    ...mapGetters(["current_select_product_id", "current_select_product_name", "group_roles"]),
    bindTableColumns() {
      return this.machineTableColumns.filter(column => column.show)
    },
    // 查看更多信息
    checkedTableColumns: {
      get() {
        return this.bindTableColumns.map(column => column.prop)
      },
      set(checked) {
        this.machineTableColumns.forEach((column, index) => {
          if (checked.includes(column.prop)) {
            column.show = true
          } else {
            column.show = false
          }
        })
      }
    }
  },
  watch: {
    // 全局组件global-product选择变化时 自动刷新机器列表
    current_select_product_id: function() {
      this.get_ecs_list()
      this.get_machine_group_list()
    },
    current_select_product_name: function() {
      this.get_current_group_role()
    },
    product_id: function() {
      this.get_machine_group_list()
    },
    modify_instance_dialog: function (new_val, old_val) {
      if (new_val) {
        this.get_flavor_list()
      }
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
  created() {
    const params = "product__id"
    this.listQuery[params] = this.current_select_product_id
    if (this.current_select_product_id === 0) {
      this.listQuery[params] = ""
    } else {
      this.listQuery[params] = this.current_select_product_id
    }
    console.log(this.listQuery, "-----")
    this.get_ecs_list()
    this.get_region_list()
    this.get_factory_list()
    this.get_product_list()
    this.get_machine_group_list()
    this.get_current_group_role()
  },
  methods: {
    reset_search() {
      this.listQuery = {
        page: 1,
        limit: 15
      }
    },
    copyText() {
      var copyTextArea = document.createElement("textarea")
      copyTextArea.value = "instanceId,instanceName,hostname,instanceStatus,instanceType,cpu,memory,osName,description,ipAddress,innerIpAddress"
      document.body.appendChild(copyTextArea)
      copyTextArea.select()
      var copyed = document.execCommand("copy")
      if (copyed) {
        document.body.removeChild(copyTextArea)
        this.$message({
            message: "复制成功!",
            type: 'success'
          })
      }
    },
    reset_uploadData() {
      this.uploadVisible = false
      this.uploadFileList = []
      this.uploadData = {
        resourceType: "machine",
        factory: "",
        product: ""
      }
    },
    open_upload() {
      this.uploadVisible = true
    },
    onUpload() {
      // console.log("onUpload", this.uploadFileList)
      const formData = new FormData()
      formData.append('file', this.uploadFileList[0].raw)
      formData.append('resourceType', 'machine')
      formData.append('factory', this.uploadData.factory)
      formData.append('product', this.uploadData.product)
      postUpload(formData).then((res) => {
        if (res.data.code === '0') {
          this.reset_uploadData()
          this.$message({
            message: "上传成功! 请稍等数据解析后查看!",
            type: 'success'
          })
        } else {
          this.reset_uploadData()
          this.$message({
            message: res.data.message,
            type: 'error'
          })
        }
      }).catch((e) => {
        this.reset_uploadData()
        this.$message({
            message: e,
            type: 'error'
        })
      })
    },
    onExceed() {
      this.$message({
        message: "只允许上传一个文件!",
        type: 'error'
      })
    },
    onBeforeUpload(file) {
      const filetype = file.name.replace(/.+\./, '')
      if (filetype !== "csv") {
        this.$message.error('只允许上传CSV!')
        return false
      }
      this.uploadFileList.push(file)
      return true
    },
    get_current_group_role() {
      this.current_group_role = this.group_roles['' + this.current_select_product_name + '']
      // console.log("current_group_role", this.current_group_role)
    },
    get_instance_status(status) {
      if (status) {
        return status.toUpperCase()
      } else {
        return "UNKWOWN"
      }
    },
    get_instance_status_tag(status) {
        if (status && (status.toUpperCase().indexOf("RUNNING") !== -1)) {
          return 'success'
        } else if (status && (status.toUpperCase().indexOf("STOP") !== -1)) {
          return 'warning'
        } else if (status && (status.toUpperCase().indexOf("DELET") !== -1 || status.toUpperCase().indexOf("TERMINAT") !== -1)) {
          return 'danger'
        } else {
          return 'primary'
        }
    },
    get_real_instance(row) {
      var prefix = getCloudManageApiPrefix(row["factory__name"])
      if (prefix === '') {
        this.$alert(row["factory__name"] + "暂时没有ap调用。无法获取到实时的状态。", '提示', {
                confirmButtonText: '确定'
          })
          return false
      }
      this.real_instance_dialog = true
      this.listLoading = true
      getRealInstance(prefix, row)
        .then((resp) => {
            this.real_instance = resp.data
            this.listLoading = false
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
          })
    },
    getMachineLabel(labels) {
      this.machine_labels = labels
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
    get_record_list() {
      this.listQuery['resource_id'] = this.instance.external_uuid
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
    view_operate_log(instance) {
      console.log("instance", instance)
      this.instance_detail_dialog = true
      this.instance = instance
      this.get_record_list()
    },
    get_system_disk_category_list() {
        switch (true) {
        case /ali|阿里云|alibaba/iug.test(this.current_api_prefix): {
          return [
              { 'id': 'cloud_efficiency', 'name': 'cloud_efficiency' },
              { 'id': 'cloud_ssd', 'name': 'cloud_ssd' },
              { 'id': 'cloud_essd', 'name': 'cloud_essd' }
          ]
        }
        case /aws|亚马逊/iug.test(this.current_api_prefix): {
          return [
              { 'id': 'gp2', 'name': 'gp2' },
              { 'id': 'gp3', 'name': 'gp3' }
          ]
        }
        case /gcp|谷歌云|google/iug.test(this.current_api_prefix): {
          return []
        }
      }
    },
    get_flavor_list() {
      this.listQuery["factory"] = this.multipleSelection[0]["factory"]
      getFlavorList(this.listQuery).then(response => {
          this.flavor_list = response.data.results
          this.flavor_total = response.data.count
          setTimeout(() => {
            this.listLoading = false
          }, 1.5 * 1000)
        }).catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    operate_instances(otype) {
        var instances_id = []
        var instances_name = []
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
          instances_id.push(obj["external_uuid"])
          instances_name.push(obj["external_name"])
          gcp_project_ids.push(obj['project__project_id'] ? obj['project__project_id'] : obj["gcp_project_id"])
          gcp_project_zones.push(obj["zone__name"])
        })
        if (provider_list.length > 1) {
          this.$alert("您勾选的机器实例属于多个云供应商。目前不支持一次勾选多个云厂商实例。请重新勾选", '提示', {
                confirmButtonText: '确定'
          })
          return false
        }
        if (region_list.length > 1) {
          this.$alert("您勾选的机器实例属于多个地域。目前不支持一次勾选多个地域的实例。请重新勾选", '提示', {
                confirmButtonText: '确定'
          })
          return false
        }
        if (gcp_project_ids.length > 0) {
          var size = new Set(gcp_project_ids).size
          if (size !== 1) {
            this.$alert("您勾选的机器实例属于不同的gcp project。目前不支持一次勾选多个project的实例。请重新勾选", '提示', {
                confirmButtonText: '确定'
            })
            return false
          }
        }

        if (gcp_project_zones.length > 0) {
          var siz = new Set(gcp_project_zones).size
          if (siz !== 1) {
            this.$alert("您勾选的机器实例属于不同的gcp区域。目前不支持一次勾选多个区域的实例。请重新勾选", '提示', {
                confirmButtonText: '确定'
            })
            return false
          }
        }

        switch (otype) {
          case "label": {
            msg = '此操作将实例' + instances_name.join(", ") + '打上标签是否继续?'
            params = { 'instance_ids': instances_id, 'region': this.region, 'factory': this.factory, 'labels': this.machine_labels, 'gcp_project_id': gcp_project_ids.length > 0 ? gcp_project_ids[0] : 0, 'gcp_project_zone': gcp_project_zones.length > 0 ? gcp_project_zones[0] : 0, 'kms_account': this.kms_account }
            operator_function = labelInstance
            break
          }
          case "start": {
            msg = '此操作将开启' + instances_name.join(", ") + ', 是否继续?'
            params = { 'instance_ids': instances_id, 'region': this.region, 'factory': this.factory, 'gcp_project_id': gcp_project_ids.length > 0 ? gcp_project_ids[0] : 0, 'gcp_project_zone': gcp_project_zones.length > 0 ? gcp_project_zones[0] : 0, 'kms_account': this.kms_account }
            operator_function = startInstance
            break
          }
          case "stop": {
            msg = '此操作将停止' + instances_name.join(", ") + ', 是否继续?'
            params = { 'instance_ids': instances_id, 'region': this.region, 'factory': this.factory, 'gcp_project_id': gcp_project_ids.length > 0 ? gcp_project_ids[0] : 0, 'gcp_project_zone': gcp_project_zones.length > 0 ? gcp_project_zones[0] : 0, 'kms_account': this.kms_account }
            operator_function = stopInstance
            break
          }
          case "reboot": {
            if (this.current_api_prefix === 'gcp') {
              this.$alert("gcp不支持重启操作。请分两步走，先停止实例，然后再开启实例。", '提示', {
                confirmButtonText: '确定'
              })
              return false
            }
            msg = '此操作将重启' + instances_name.join(", ") + ', 是否继续?'
            params = { 'instance_ids': instances_id, 'region': this.region, 'factory': this.factory, 'gcp_project_id': gcp_project_ids.length > 0 ? gcp_project_ids[0] : 0, 'gcp_project_zone': gcp_project_zones.length > 0 ? gcp_project_zones[0] : 0, 'kms_account': this.kms_account }
            operator_function = rebootInstance
            break
          }
          case "modify": {
            msg = '此操作将升/降配' + instances_name.join(", ") + ', 是否继续?'
            params = Object.assign({ 'instance_ids': instances_id, 'region': this.region, 'factory': this.factory, 'gcp_project_id': gcp_project_ids.length > 0 ? gcp_project_ids[0] : 0, 'gcp_project_zone': gcp_project_zones.length > 0 ? gcp_project_zones[0] : 0, 'kms_account': this.kms_account }, this.modify_instance_form)
            operator_function = modifyInstance
            break
          }
          case "delete": {
            msg = '此操作删除' + instances_name.join(", ") + ', 是否继续?'
            params = { 'instance_ids': instances_id, 'region': this.region, 'factory': this.factory, 'gcp_project_id': gcp_project_ids.length > 0 ? gcp_project_ids[0] : 0, 'gcp_project_zone': gcp_project_zones.length > 0 ? gcp_project_zones[0] : 0, 'kms_account': this.kms_account }
            operator_function = deleteInstance
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
    // 搜索
    search_handler() {
      var params = this.select_input + "__contains"
      this.listQuery.page = 1
      this.listQuery[params] = this.input_content
      // console.log("search_handler", this.listQuery)
      this.get_ecs_list()
    },
    more_search() {
      this.show_more_search = !this.show_more_search
      this.more_search_form.external_status = null
      this.more_search_form.factory__name = null
      this.more_search_form.zone__region__name = null
    },
    more_search_submit() {
      console.log(this.more_search_form, '====')

      this.listQuery["external_status__in"] = this.more_search_form.external_status
      this.listQuery["factory__name"] = this.more_search_form.factory__name
      this.listQuery["zone__region__name"] = this.more_search_form.zone__region__name
      this.get_ecs_list()
    },
    // 获取机器列表
    get_ecs_list() {
      const params = "product__id"
      this.listQuery[params] = this.current_select_product_id

      if (this.current_select_product_id === 0) {
        this.listQuery[params] = ""
      } else {
        this.listQuery[params] = this.current_select_product_id
      }
      // 只选择在使用中的
      // this.listQuery["status"] = 0
      // console.log(this.listQuery)
      getMachineList(this.listQuery)
        .then(response => {
          this.ecs_list = response.data.results
          this.total = response.data.count
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    get_row_key(row) {
      return row.id
    },
    // 展开表格行
    toggleExpand(row) {
      const $table = this.$refs.machine_table_refs
      this.ecs_list.map(item => {
        if (row.id !== item.id) {
          $table.toggleRowExpansion(item, false)
        }
      })
      $table.toggleRowExpansion(row)
    },
    // 表格行的选择
    handleSelectionChange(val) {
      this.multipleSelection = val
    },
    // 处理同步机器的逻辑
    handle_sync_command(command) {
      // console.log(command)
      if (command === "sync_machine_from_aliyun") {
        // console.log('同步阿里云机器业务逻辑')
      } else if (command === "sync_machine_from_qcloud") {
        // console.log('同步腾讯云机器业务逻辑')
      }
    },
    // 分配机器到产品和分组
    associate_machine_to_product() {
      if (this.multipleSelection.length <= 0) {
        this.$message({
          type: "warning",
          message: "请勾选实例"
        })
        return
      }
      this.group_product_dialog = true
      this.dialogStatus = "product"
    },
    submit_associate() {
      this.associate_loading = true
      // console.log(this.product_id, this.group_id, '====')
      for (let index = 0; index < this.multipleSelection.length; index++) {
        // console.log(this.multipleSelection[index], '????')
        updateMachineByID(this.multipleSelection[index].id, {
          product: this.product_id,
          group: this.group_id
        })
          .then(_ => {
            this.$message({
              type: "success",
              message: "分配机器至产品成功"
            })
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: "分配机器至产品失败" + err
            })
          })
        this.associate_loading = false
      }
      this.group_product_dialog = false
    },
    // 获取产品列表
    get_product_list() {
      getProductList({ limit: 999 })
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
      // this.listQuery.page = 1
      // this.listQuery.limit = 999
      // this.listQuery["product__id"] = this.product_id
      getHostGroupList({ product__id: this.product_id, limit: 999 })
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
    view_under_project(row) {
      // console.log(row.project, '======')
      if (row.project === null) {
        this.$message({
          type: "info",
          message: "机器还没有关联到项目"
        })
      } else {
        getProjectList({ id: row.project_id }).then(resp => {
          // console.log("getProjectList",resp.data.results)
           const parObj = JSON.stringify(resp.data.results[0])
           this.$router.push({ path: '/btree/btree_detail/', query: { project_info: parObj } })
        })
        // this.$router.push({
        //   path: "/btree/btree_detail/",
        //   query: { project_id: row.project, project_name: row.project__name }
        // })
        // const parObj = JSON.stringify(row)
        // this.$router.push({ path: '/btree/btree_detail/', query: { project_info: parObj } })
      }
    },
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
    handle_close() {
      this.real_instance_dialog = false
      this.record_log_dialog = false
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
.iconfont_lcoal {
  font-size: 10px;
  font-style: normal;
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
.inline-block {
  display: inline-block;
  margin-left:10px;
}
</style>
