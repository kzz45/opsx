<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-tabs
        v-model="active_tab_name"
        @tab-click="active_tab_click"
      >
        <!-- 采集组管理--------------------------------------------------  -->
        <el-tab-pane
          label="采集分组"
          name="server_group"
        >
          <div>
            <el-button
              type="primary"
              icon="el-icon-circle-plus-outline"
              size="small"
              @click="create_server_group"
            >
              新增
            </el-button>
          </div>
          <el-table
            :data="server_group_list"
            size="small"
            border
          >
            <el-table-column
              label="采集组名称"
              prop="name"
            > </el-table-column>
            <el-table-column
              label="采集组类型"
              prop="mode"
            >
              <template slot-scope="scoped">
                <el-tag
                  v-if="scoped.row.mode =='0'"
                  type="success"
                >自定义</el-tag>
                <el-tag
                  v-else
                  type="success"
                >API同步</el-tag>
              </template>
            </el-table-column>
            <!-- <el-table-column
              label="同步API"
              prop="policy"
            >
              <template slot-scope="scoped">
                <span
                  v-if="scoped.row.mode =='0'"
                  style="font-size: 10px;"
                >自定义分组没有API地址</span>
                <span v-else>{{ scoped.row.policy }}</span>
              </template>
            </el-table-column> -->
            <el-table-column
              label="操作"
              width="180px;"
            >
              <template slot-scope="scoped">
                <!-- 查看采集点 -->
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="查看采集节点"
                  placement="top"
                >
                  <el-button
                    type="success"
                    icon="el-icon-info"
                    size="mini"
                    @click="view_server_group(scoped.row)"
                  ></el-button>
                </el-tooltip>
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  size="mini"
                  @click="update_server_group(scoped.row)"
                ></el-button>
                <el-popconfirm
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left:10px"
                  @confirm="delete_server_group(scoped.row)"
                  @cancel="cancel_delete"
                >
                  <el-button
                    slot="reference"
                    type="danger"
                    icon="el-icon-delete"
                    size="mini"
                  ></el-button>
                </el-popconfirm>
              </template>
            </el-table-column>
          </el-table>
          <pagination
            v-show="server_group_list_total>0"
            :total="server_group_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_server_group_list"
          ></pagination>
        </el-tab-pane>
        <!-- 探测节点管理--------------------------------------------------  -->
        <!-- <el-tab-pane
          label="探测节点"
          name="probe"
        >
          <div>
            <el-button
              type="primary"
              icon="el-icon-circle-plus-outline"
              size="small"
              @click="create_probe"
            >
              新增
            </el-button>
          </div>
          <el-table
            :data="probe_list"
            size="small"
            border
          >
            <el-table-column
              label="名称"
              prop="name"
            ></el-table-column>
            <el-table-column
              label="标识"
              prop="uuid"
            ></el-table-column>
            <el-table-column
              label="API地址"
              prop="api"
            > </el-table-column>
            <el-table-column
              label="模式"
              prop="mode"
            ></el-table-column>
            <el-table-column
              label="操作"
              width="120px;"
            >
              <template slot-scope="scoped">
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  size="mini"
                  @click="update_probe(scoped.row)"
                ></el-button>
                <el-popconfirm
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left:10px"
                  @confirm="delete_probe(scoped.row)"
                  @cancel="cancel_delete"
                >
                  <el-button
                    slot="reference"
                    type="danger"
                    icon="el-icon-delete"
                    size="mini"
                  ></el-button>
                </el-popconfirm>
              </template>
            </el-table-column>
          </el-table>
          <pagination
            v-show="probe_list_total>0"
            :total="probe_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_probe_list"
          ></pagination>
        </el-tab-pane> -->
        <!-- 实例类型管理-------------------------------------------------- -->
        <el-tab-pane
          label="实例类型"
          name="instance_type"
        >
          <div>
            <el-button
              type="primary"
              icon="el-icon-circle-plus-outline"
              size="small"
              @click="create_instance_type"
            >
              新增
            </el-button>
          </div>
          <el-table
            :data="instance_type_list"
            size="small"
            border
          >
            <el-table-column
              label="类型名称"
              prop="name"
            ></el-table-column>
            <el-table-column
              label="类型别名"
              prop="value"
            > </el-table-column>
            <el-table-column
              label="操作"
              width="120px;"
            >
              <template slot-scope="scoped">
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  size="mini"
                  @click="update_instance_type(scoped.row)"
                ></el-button>
                <el-popconfirm
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left:10px"
                  @confirm="delete_instance_type(scoped.row)"
                  @cancel="cancel_delete"
                >
                  <el-button
                    slot="reference"
                    type="danger"
                    icon="el-icon-delete"
                    size="mini"
                  ></el-button>
                </el-popconfirm>
              </template>
            </el-table-column>
          </el-table>
          <pagination
            v-show="instance_type_list_total>0"
            :total="instance_type_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_instance_type_list"
          >
          </pagination>
        </el-tab-pane>
        <!-- 标签管理--------------------------------------------------  -->
        <el-tab-pane
          label="标签管理"
          name="label_manage"
        >
          <div>
            <el-button
              type="primary"
              icon="el-icon-circle-plus-outline"
              size="small"
              @click="create_label"
            >
              新增
            </el-button>
          </div>
          <el-table
            :data="label_list"
            size="small"
            border
          >
            <el-table-column
              label="标签名"
              prop="name"
            ></el-table-column>
            <el-table-column
              label="标签值"
              prop="value"
            ></el-table-column>
            <el-table-column
              label="标签类型"
              width="120px;"
            >
              <template slot-scope="scoped">
                <el-tag
                  v-if="scoped.row.mode == 0"
                  type="success"
                >内部标签</el-tag>
                <el-tag
                  v-else
                  type="success"
                >上报标签</el-tag>
              </template>
            </el-table-column>
            <el-table-column
              label="所属产品"
              prop="product__name"
            ></el-table-column>
            <el-table-column
              label="操作"
              width="120px;"
            >
              <template slot-scope="scoped">
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  size="mini"
                  @click="update_label(scoped.row)"
                ></el-button>
                <el-popconfirm
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left:10px"
                  @confirm="delete_label(scoped.row)"
                  @cancel="cancel_delete"
                >
                  <el-button
                    slot="reference"
                    type="danger"
                    icon="el-icon-delete"
                    size="mini"
                  ></el-button>
                </el-popconfirm>
              </template>
            </el-table-column>
          </el-table>
          <pagination
            v-show="label_list_total>0"
            :total="label_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_label_list"
          ></pagination>
        </el-tab-pane>
        <!-- 告警规则类型-------------------------------------------------- -->
        <el-tab-pane
          label="规则类型"
          name="alert_rule_type"
        >
          <div>
            <el-button
              type="primary"
              icon="el-icon-circle-plus-outline"
              size="small"
              @click="create_alert_rule_type"
            >
              新增
            </el-button>
          </div>
          <el-table
            :data="alert_rule_type_list"
            size="small"
            border
          >
            <el-table-column
              label="名称"
              prop="name"
            ></el-table-column>
            <el-table-column
              label="描述"
              prop="desc"
            ></el-table-column>
            <el-table-column
              label="操作"
              width="120px;"
            >
              <template slot-scope="scoped">
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  size="mini"
                  @click="update_alert_rule_type(scoped.row)"
                ></el-button>
                <el-popconfirm
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left:10px"
                  @confirm="delete_alert_rule_type(scoped.row)"
                  @cancel="cancel_delete"
                >
                  <el-button
                    slot="reference"
                    type="danger"
                    icon="el-icon-delete"
                    size="mini"
                  ></el-button>
                </el-popconfirm>
              </template>
            </el-table-column>
          </el-table>
          <pagination
            v-show="alert_rule_type_list_total>0"
            :total="alert_rule_type_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_alert_rule_type_list"
          ></pagination>
        </el-tab-pane>
        <!-- 告警等级-------------------------------------------------- -->
        <el-tab-pane
          label="告警等级"
          name="alert_level"
        >
          <div>
            <el-button
              type="primary"
              icon="el-icon-circle-plus-outline"
              size="small"
              @click="create_alert_level"
            >
              新增
            </el-button>
          </div>
          <el-table
            :data="alert_level_list"
            size="small"
            border
          >
            <el-table-column
              label="名称"
              prop="name"
            ></el-table-column>
            <el-table-column
              label="描述"
              prop="desc"
            ></el-table-column>
            <el-table-column
              label="操作"
              width="120px;"
            >
              <template slot-scope="scoped">
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  size="mini"
                  @click="update_alert_level(scoped.row)"
                ></el-button>
                <el-popconfirm
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left:10px"
                  @confirm="delete_alert_level(scoped.row)"
                  @cancel="cancel_delete"
                >
                  <el-button
                    slot="reference"
                    type="danger"
                    icon="el-icon-delete"
                    size="mini"
                  ></el-button>
                </el-popconfirm>
              </template>
            </el-table-column>
          </el-table>
          <pagination
            v-show="alert_level_list_total>0"
            :total="alert_level_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_alert_level"
          ></pagination>
        </el-tab-pane>
        <!-- dashboard管理-------------------------------------------------- -->
        <el-tab-pane
          label="大盘管理"
          name="dashboard_manage"
        >
          <div>
            <el-button
              type="primary"
              icon="el-icon-circle-plus-outline"
              size="small"
              @click="create_dashboard"
            >
              新增
            </el-button>
          </div>
          <el-table
            :data="dashboard_list"
            size="small"
            border
          >
            <el-table-column
              label="名称"
              prop="name"
            ></el-table-column>
            <el-table-column
              label="产品"
              prop="product__name"
            ></el-table-column>
            <el-table-column
              label="地址"
              prop="url"
              show-overflow-tooltip
            ></el-table-column>
            <el-table-column
              label="操作"
              width="120px;"
            >
              <template slot-scope="scoped">
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  size="mini"
                  @click="update_dashboard(scoped.row)"
                ></el-button>
                <el-popconfirm
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left:10px"
                  @confirm="delete_dashboard(scoped.row)"
                  @cancel="cancel_delete"
                >
                  <el-button
                    slot="reference"
                    type="danger"
                    icon="el-icon-delete"
                    size="mini"
                  ></el-button>
                </el-popconfirm>
              </template>
            </el-table-column>
          </el-table>
          <pagination
            v-show="dashboard_list_total>0"
            :total="dashboard_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_dashboard_list"
          ></pagination>
        </el-tab-pane>
      </el-tabs>
    </el-card>
    <!-- 采集组管理Dialog-------------------------------------------------- -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="server_group_dialog"
      width="50%"
    >
      <el-form
        ref="server_group_formRefs"
        :model="server_group_form"
        :rules="server_group_form_rules"
        label-width="100px"
        size="small"
      >
        <el-form-item
          label="采集组名称"
          prop="name"
        >
          <el-input
            v-model="server_group_form.name"
            placeholder="请输入采集组名称"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="采集组类型"
          prop="mode"
        >
          <el-radio-group v-model="server_group_form.mode">
            <el-radio :label="0">自定义分组</el-radio>
            <el-radio
              :label="1"
              disabled
            >同步分组</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item
          v-if="server_group_form.mode == 1"
          label="同步API"
          prop="policy"
        >
          <el-input
            v-model="server_group_form.policy"
            placeholder="请输入同步的API地址"
          ></el-input>
        </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="server_group_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_server_group"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 实例类型的Dialog-------------------------------------------------- -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="instance_type_dialog"
      width="50%"
    >
      <el-form
        ref="instance_type_formRefs"
        :model="instance_type_form"
        :rules="instance_type_form_rules"
        label-width="100px"
        size="small"
      >
        <el-form-item
          label="类型名称"
          prop="name"
        >
          <el-input
            v-model="instance_type_form.name"
            placeholder="请输入类型名称"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="类型代号"
          prop="value"
        >
          <el-input
            v-model="instance_type_form.value"
            placeholder="请输入类型代号"
          ></el-input>
        </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="instance_type_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_instance_type"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 探测节点管理Dialog--------------------------------------------------  -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="probe_dialog"
      width="50%"
    >
      <el-form
        ref="probe_formRefs"
        :model="probe_form"
        :rules="probe_form_rules"
        label-width="100px"
      >
        <el-form-item
          label="名称"
          prop="name"
        >
          <el-input
            v-model="probe_form.name"
            placeholder="请输入探测名称"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="标识"
          prop="uuid"
        >
          <el-input
            v-model="probe_form.uuid"
            placeholder="请输入探测唯一标识"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="API地址"
          prop="api"
        >
          <el-input
            v-model="probe_form.api"
            placeholder="请输入探测API地址"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="IP地址"
          prop="ipaddr"
        >
          <el-input
            v-model="probe_form.ipaddr"
            placeholder="请输入IP地址"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="服务器组"
          prop="server_group"
        >
          <el-select
            v-model="probe_form.server_group"
            placeholder="请选择服务器组"
            size="small"
            style="width: 300px;"
          >
            <el-option
              v-for="(item) in server_group_list"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          label="模式"
          prop="mode"
        >
          <el-select
            v-model="probe_form.mode"
            placeholder="请选择探测类型"
            size="small"
            clearable
            style="width: 300px"
          >
            <el-option
              label="http/tcp"
              value="http/tcp"
            ></el-option>
            <el-option
              label="ping"
              value="ping"
            ></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="probe_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_probe"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 标签管理Dialog-------------------------------------------------- -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="label_dialog"
      width="50%"
    >
      <el-form
        ref="label_formRefs"
        :model="label_form"
        :rules="label_form_rules"
        label-width="100px"
        size="small"
      >
        <el-form-item
          label="标签名"
          prop="name"
        >
          <el-input
            v-model="label_form.name"
            placeholder="请输入标签名称"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="标签值"
          prop="value"
        >
          <el-input
            v-model="label_form.value"
            placeholder="请输入标签名称"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="关联产品"
          prop="product"
        >
          <el-select
            v-model="label_form.product"
            placeholder="请选择产品"
            style="width: 300px;"
          >
            <el-option
              v-for="(item) in product_list"
              :key="item.id"
              :value="item.id"
              :label="item.name"
            ></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="label_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_label"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 告警规则类型Dialog-------------------------------------------------- -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="alert_rule_type_dialog"
      width="50%"
    >
      <el-form
        ref="alert_rule_type_formRefs"
        :model="alert_rule_type_form"
        :rules="alert_rule_type_form_rules"
        label-width="100px"
        size="small"
      >
        <el-form-item
          label="名称"
          prop="name"
        >
          <el-input
            v-model="alert_rule_type_form.name"
            placeholder="请输入告警规则类型名称"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="描述"
          prop="desc"
        >
          <el-input
            v-model="alert_rule_type_form.desc"
            placeholder="请输入告警规则类型描述"
          ></el-input>
        </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="alert_rule_type_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_alert_rule_type"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 告警等级Dialog-------------------------------------------------- -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="alert_level_dialog"
      width="50%"
    >
      <el-form
        ref="alert_level_formRefs"
        :model="alert_level_form"
        :rules="alert_level_form_rules"
        label-width="100px"
        size="small"
      >
        <el-form-item
          label="名称"
          prop="name"
        >
          <el-input
            v-model="alert_level_form.name"
            placeholder="请输入告警等级名称"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="描述"
          prop="desc"
        >
          <el-input
            v-model="alert_level_form.desc"
            placeholder="请输入告警等级描述"
          ></el-input>
        </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="alert_level_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_alert_level"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- dashboard的Dialog-------------------------------------------------- -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="dashboard_dialog"
      width="50%"
    >
      <el-form
        ref="dashboard_formRefs"
        :model="dashboard_form"
        :rules="dashboard_form_rules"
        label-width="100px"
        size="small"
      >
        <el-form-item
          label="名称"
          prop="name"
        >
          <el-input
            v-model="dashboard_form.name"
            placeholder="请输入大盘名称"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="描述"
          prop="describe"
        >
          <el-input
            v-model="dashboard_form.describe"
            placeholder="请输入大盘描述"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="产品"
          prop="product"
        >
          <el-select
            v-model="dashboard_form.product"
            placeholder="请选择产品"
            clearable
            filterable
            style="width: 300px;"
          >
            <el-option
              v-for="(item) in product_list"
              :key="item.id"
              :value="item.id"
              :label="item.name"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          label="URL"
          prop="url"
        >
          <el-input
            v-model="dashboard_form.url"
            placeholder="请输入大盘地址"
          ></el-input>
        </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="dashboard_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_dashboard"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { mapGetters } from "vuex"
import Pagination from "@/components/Pagination"
import { getProductList } from "@/api/product"
import {
  getServerGroupList,
  createServerGroup,
  updateServerGroupByID,
  deleteServerGroupByID
} from "@/views/monitor/api/server_group"
import {
  getProbeList,
  createProbe,
  updateProbeByID,
  deleteProbeByID
} from "@/views/monitor/api/probe"
import {
  getLabelList,
  createLabel,
  updateLabelByID,
  deleteLabelByID
} from "@/views/monitor/api/label"
import {
  getInstanceTypeList,
  createInstanceType,
  updateInstanceTypeByID,
  deleteInstanceTypeByID
} from "@/views/monitor/api/instance_type"
import {
  getAlertRuleTypeList,
  createAlertRuleType,
  updateAlertRuleTypeByID
} from "@/views/monitor/api/alert_rule_type"
import {
  getAlertLevelList,
  createAlertLevel,
  updateAlertLevelByID
} from "@/views/monitor/api/alert_level"
import {
  getDashboardList,
  createDashboard,
  updateDashboardByID,
  deleteDashboardByID
} from "@/views/monitor/api/dashboard"

export default {
  name: "MonitorSettings",
  components: {
    Pagination
  },
  data() {
    return {
      list_query: {
        page: 1,
        limit: 15
      },
      active_tab_name: "server_group",
      dialog_map: {
        create_server_group: "新增采集组",
        update_server_group: "编辑采集组",
        create_probe: "新增探测节点",
        update_probe: "编辑探测节点",
        create_instance_type: "新增实体类型",
        update_instance_type: "编辑实体类型",
        create_label: "新增标签",
        update_label: "编辑标签",
        create_alert_rule_type: "新增告警规则类型",
        update_alert_rule_type: "编辑告警规则类型",
        create_alert_level: "新增告警等级",
        update_alert_level: "编辑告警等级",
        create_dashboard: "新增大盘",
        update_dashboard: "编辑大盘"
      },
      dialog_status: "",
      // 采集组相关--------------------------------------------------
      server_group_list: [],
      server_group_list_total: 0,
      server_group_dialog: false,
      server_group_form: {
        id: "",
        name: "",
        mode: 0
      },
      server_group_form_rules: {
        name: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        mode: [{ required: true, message: "该项不能为空", trigger: "blur" }]
      },
      // 探测节点相关--------------------------------------------------
      probe_list: [],
      probe_list_total: 0,
      probe_dialog: false,
      probe_form: {
        id: "",
        name: "",
        api: "",
        ipaddr: "",
        uuid: "",
        mode: "http/tcp"
      },
      probe_form_rules: {
        name: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        uuid: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        api: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        ipaddr: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        server_group: [
          { required: true, message: "该项不能为空", trigger: "blur" }
        ],
        mode: [
          {
            required: true,
            message: "该项不能为空",
            trigger: ["blur", "change"]
          }
        ]
      },
      // 实体类型相关--------------------------------------------------
      instance_type_list: [],
      instance_type_list_total: 0,
      instance_type_dialog: false,
      instance_type_form: {
        id: "",
        name: null,
        value: null
      },
      instance_type_form_rules: {
        name: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        value: [{ required: true, message: "该项不能为空", trigger: "blur" }]
      },
      // 标签相关--------------------------------------------------
      label_dialog: false,
      label_form: {
        id: "",
        name: "",
        value: null,
        product: null
      },
      label_form_rules: {
        name: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        product: [{ required: true, message: "该项不能为空", trigger: "blur" }]
      },
      label_list: [],
      label_list_total: 0,
      // 告警规则类型相关--------------------------------------------------
      alert_rule_type_list: [],
      alert_rule_type_list_total: 0,
      alert_rule_type_dialog: false,
      alert_rule_type_form: {
        id: null,
        name: null,
        desc: null
      },
      alert_rule_type_form_rules: {
        name: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        desc: [{ required: true, message: "该项不能为空", trigger: "blur" }]
      },
      // 告警等级相关--------------------------------------------------
      alert_level_list: [],
      alert_level_list_total: 0,
      alert_level_dialog: false,
      alert_level_form: {
        id: null,
        name: null,
        desc: null
      },
      alert_level_form_rules: {
        name: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        desc: [{ required: true, message: "该项不能为空", trigger: "blur" }]
      },
      // dashboard相关--------------------------------------------------
      dashboard_list: [],
      dashboard_list_total: 0,
      dashboard_dialog: false,
      dashboard_form: {
        id: null,
        name: null,
        describe: null,
        product: null,
        url: null
      },
      dashboard_form_rules: {
        name: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        describe: [
          { required: true, message: "该项不能为空", trigger: "blur" }
        ],
        product: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        url: [{ required: true, message: "该项不能为空", trigger: "blur" }]
      },
      product_list: []
    }
  },
  computed: {
    ...mapGetters(["current_select_product_id", "current_select_product_name"])
  },
  watch: {
    current_select_product_id: function() {
      this.get_dashboard_list()
    }
  },
  created() {
    this.get_product_list()
    this.get_server_group_list()
  },
  methods: {
    active_tab_click(tab) {
      if (tab.name === "server_group") {
        this.list_query.page = 1
        this.get_server_group_list()
      } else if (tab.name === "probe") {
        this.list_query.page = 1
        this.get_probe_list()
      } else if (tab.name === "instance_type") {
        this.list_query.page = 1
        this.get_instance_type_list()
      } else if (tab.name === "label_manage") {
        this.list_query.page = 1
        this.get_label_list()
      } else if (tab.name === "alert_rule_type") {
        this.list_query.page = 1
        this.get_alert_rule_type_list()
      } else if (tab.name === "alert_level") {
        this.list_query.page = 1
        this.get_alert_level()
      } else if (tab.name === "dashboard_manage") {
        this.list_query.page = 1
        this.get_dashboard_list()
      }
    },
    // 获取产品列表
    get_product_list() {
      // getProductList(this.list_query)
      getProductList({ limit: 100 })
        .then(resp => {
          this.product_list = resp.data.results
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 探测相关--------------------------------------------------
    get_probe_list() {
      getProbeList(this.list_query)
        .then(resp => {
          this.probe_list = resp.data.results
          this.probe_list_total = resp.data.count
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    create_probe() {
      this.probe_dialog = true
      this.dialog_status = "create_probe"
      // if (this.$refs.probe_formRefs) {
      //   this.$refs.probe_formRefs.resetFields()
      // }
      this.probe_form.name = null
      this.probe_form.uuid = null
      this.probe_form.api = null
      this.probe_form.ipaddr = null
      this.probe_form.server_group = null
    },
    update_probe(row) {
      this.probe_dialog = true
      this.dialog_status = "update_probe"
      this.probe_form = Object.assign({}, row)
    },
    submit_probe() {
      if (this.dialog_status === "create_probe") {
        createProbe(this.probe_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "新增探测节点【" + this.probe_form.name + "】成功"
            })
            this.probe_dialog = false
            this.get_probe_list()
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            })
            this.probe_dialog = false
            this.get_probe_list()
          })
      } else if (this.dialog_status === "update_probe") {
        updateProbeByID(this.probe_form.id, this.probe_form)
          .then(resp => {
            this.$message({
              type: "success",
              message: "更新探测节点【" + this.probe_form.name + "】成功"
            })
            this.probe_dialog = false
            this.get_probe_list()
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            })
            this.probe_dialog = false
            this.get_probe_list()
          })
      }
    },
    delete_probe(row) {
      deleteProbeByID(row.id)
        .then(() => {
          this.$message({
            type: "success",
            message: "删除探测节点【" + row.name + "】成功"
          })
          this.get_probe_list()
        })
        .catch(() => {
          this.$message({
            type: "error",
            message: "删除探测节点【" + row.name + "】失败"
          })
          this.get_probe_list()
        })
    },
    // 实体类型相关--------------------------------------------------
    get_instance_type_list() {
      getInstanceTypeList(this.list_query)
        .then(resp => {
          this.instance_type_list = resp.data.results
          this.instance_type_list_total = resp.data.count
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    create_instance_type() {
      this.instance_type_dialog = true
      this.dialog_status = "create_instance_type"
      // if (this.$refs.instance_type_formRefs) {
      //   this.$refs.instance_type_formRefs.resetFields()
      // }
      this.instance_type_form.name = null
      this.instance_type_form.value = null
    },
    update_instance_type(row) {
      this.instance_type_dialog = true
      this.dialog_status = "update_instance_type"
      this.instance_type_form = Object.assign({}, row)
    },
    submit_instance_type() {
      if (this.dialog_status === "create_instance_type") {
        createInstanceType(this.instance_type_form)
          .then(() => {
            this.$message({
              type: "success",
              message:
                "新增实体类型【" + this.instance_type_form.name + "】成功"
            })
            this.instance_type_dialog = false
            this.get_instance_type_list()
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            })
            this.instance_type_dialog = false
            this.get_instance_type_list()
          })
      } else if (this.dialog_status === "update_instance_type") {
        updateInstanceTypeByID(
          this.instance_type_form.id,
          this.instance_type_form
        )
          .then(resp => {
            this.$message({
              type: "success",
              message:
                "更新实体类型【" + this.instance_type_form.name + "】成功"
            })
            this.instance_type_dialog = false
            this.get_instance_type_list()
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            })
            this.instance_type_dialog = false
            this.get_instance_type_list()
          })
      }
    },
    delete_instance_type(row) {
      deleteInstanceTypeByID(row.id)
        .then(() => {
          this.$message({
            type: "success",
            message: "删除实体类型【" + row.name + "】成功"
          })
          this.get_instance_type_list()
        })
        .catch(() => {
          this.$message({
            type: "error",
            message: "删除实体类型【" + row.name + "】失败"
          })
          this.get_instance_type_list()
        })
    },
    // 采集组相关--------------------------------------------------
    get_server_group_list() {
      getServerGroupList(this.list_query)
        .then(resp => {
          this.server_group_list = resp.data.results
          this.server_group_list_total = resp.data.count
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    view_server_group(row) {
      const parObj = JSON.stringify(row)
      this.$router.push({
        path: "/monitor/server/",
        query: { server_group_info: parObj }
      })
    },
    view_server_group_machine(row) {
      this.$router.push({
        name: "InstanceObject",
        params: { server_group__id: row.id, server_group__name: row.name }
      })
    },
    create_server_group() {
      this.server_group_dialog = true
      this.dialog_status = "create_server_group"
      // if (this.$refs.server_group_formRefs) {
      //   this.$refs.server_group_formRefs.resetFields()
      // }
      this.server_group_form.name = null
    },
    update_server_group(row) {
      this.server_group_dialog = true
      this.dialog_status = "update_server_group"
      this.server_group_form = Object.assign({}, row)
    },
    submit_server_group() {
      if (this.dialog_status === "create_server_group") {
        createServerGroup(this.server_group_form)
          .then(resp => {
            this.$message({
              type: "success",
              message: "新增采集组【" + this.server_group_form.name + "】成功"
            })
            this.server_group_dialog = false
            this.get_server_group_list()
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            })
            this.server_group_dialog = false
            this.get_server_group_list()
          })
      } else if (this.dialog_status === "update_server_group") {
        updateServerGroupByID(this.server_group_form.id, this.server_group_form)
          .then(resp => {
            this.$message({
              type: "success",
              message: "更新采集组【" + this.server_group_form.name + "】成功"
            })
            this.server_group_dialog = false
            this.get_server_group_list()
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            })
            this.server_group_dialog = false
            this.get_server_group_list()
          })
      }
    },
    delete_server_group(row) {
      deleteServerGroupByID(row.id)
        .then(resp => {
          this.$message({
            type: "success",
            message: "删除采集组【" + row.name + "】成功"
          })
          this.server_group_dialog = false
          this.get_server_group_list()
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
          this.server_group_dialog = false
          this.get_server_group_list()
        })
    },
    // 标签相关--------------------------------------------------
    create_label() {
      this.label_dialog = true
      this.dialog_status = "create_label"
      // if (this.$refs.label_formRefs) {
      //   this.$refs.label_formRefs.resetFields()
      // }
      this.label_form.name = null
      this.label_form.value = null
      this.label_form.product = null
    },
    update_label(row) {
      this.label_dialog = true
      this.dialog_status = "update_label"
      this.label_form = Object.assign({}, row)
    },
    submit_label() {
      if (this.dialog_status === "create_label") {
        createLabel(this.label_form)
          .then(resp => {
            this.$message({
              type: "success",
              message: "新增标签成功"
            })
            this.label_dialog = false
            this.get_label_list()
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            })
            this.label_dialog = false
            this.get_label_list()
          })
      } else if (this.dialog_status === "update_label") {
        updateLabelByID(this.label_form.id, this.label_form)
          .then(resp => {
            this.$message({
              type: "success",
              message: "更新标签成功"
            })
            this.label_dialog = false
            this.get_label_list()
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            })
            this.label_dialog = false
            this.get_label_list()
          })
      }
    },
    delete_label(row) {
      deleteLabelByID(row.id)
        .then(resp => {
          this.$message({
            type: "success",
            message: "删除标签成功"
          })
          this.get_label_list()
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
          this.get_label_list()
        })
    },
    get_label_list() {
      getLabelList(this.list_query).then(resp => {
        this.label_list = resp.data.results
        this.label_list_total = resp.data.count
      })
    },
    // 告警规则类型相关--------------------------------------------------
    create_alert_rule_type() {
      this.alert_rule_type_dialog = true
      this.dialog_status = "create_alert_rule_type"
      // if (this.$refs.alert_rule_type_formRefs) {
      //   this.$refs.alert_rule_type_formRefs.resetFields()
      // }
      this.alert_rule_type_form.name = null
      this.alert_rule_type_form.desc = null
    },
    update_alert_rule_type(row) {
      this.alert_rule_type_dialog = true
      this.dialog_status = "update_alert_rule_type"
      this.alert_rule_type_form = Object.assign({}, row)
    },
    delete_alert_rule_type() {},
    submit_alert_rule_type() {
      if (this.dialog_status === "create_alert_rule_type") {
        createAlertRuleType(this.alert_rule_type_form)
          .then(resp => {
            this.$message({
              type: "success",
              message: "新增告警规则类型成功"
            })
            this.alert_rule_type_dialog = false
            this.get_alert_rule_type_list()
          })
          .catch(err => {
            this.$message({
              type: "success",
              message: err
            })
            this.alert_rule_type_dialog = false
            this.get_alert_rule_type_list()
          })
      } else if (this.dialog_status === "update_alert_rule_type") {
        updateAlertRuleTypeByID(
          this.alert_rule_type_form.id,
          this.alert_rule_type_form
        )
          .then(resp => {
            this.$message({
              type: "success",
              message: "更新告警规则类型成功"
            })
            this.alert_rule_type_dialog = false
            this.get_alert_rule_type_list()
          })
          .catch(err => {
            this.$message({
              type: "success",
              message: err
            })
            this.alert_rule_type_dialog = false
            this.get_alert_rule_type_list()
          })
      }
    },
    get_alert_rule_type_list() {
      getAlertRuleTypeList(this.list_query)
        .then(resp => {
          this.alert_rule_type_list = resp.data.results
          this.alert_rule_type_list_total = resp.data.count
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 告警等级相关--------------------------------------------------
    create_alert_level() {
      this.alert_level_dialog = true
      this.dialog_status = "create_alert_level"
      // if (this.$refs.alert_level_formRefs) {
      //   this.$refs.alert_level_formRefs.resetFields()
      // }
      this.alert_level_form.name = null
      this.alert_level_form.desc = null
    },
    update_alert_level(row) {
      this.alert_level_dialog = true
      this.dialog_status = "update_alert_level"
      this.alert_level_form = Object.assign({}, row)
    },
    submit_alert_level() {
      if (this.dialog_status === "create_alert_level") {
        createAlertLevel(this.alert_level_form)
          .then(resp => {
            this.$message({
              type: "success",
              message: "新增告警等级成功"
            })
            this.alert_level_dialog = false
            this.get_alert_level()
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            })
            this.alert_level_dialog = false
            this.get_alert_level()
          })
      } else if (this.dialog_status === "update_alert_level") {
        updateAlertLevelByID(this.alert_level_form.id, this.alert_level_form)
          .then(resp => {
            this.$message({
              type: "success",
              message: "更新告警等级成功"
            })
            this.alert_level_dialog = false
            this.get_alert_level()
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            })
            this.alert_level_dialog = false
            this.get_alert_level()
          })
      }
    },
    delete_alert_level(row) {},
    get_alert_level() {
      getAlertLevelList(this.list_query)
        .then(resp => {
          this.alert_level_list = resp.data.results
          this.alert_level_list_total = resp.data.count
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // dashboard管理相关--------------------------------------------------
    create_dashboard() {
      this.dashboard_dialog = true
      this.dialog_status = "create_dashboard"
      this.dashboard_form.name = null
      this.dashboard_form.describe = null
      this.dashboard_form.product = null
      this.dashboard_form.url = null
    },
    update_dashboard(row) {
      this.dashboard_dialog = true
      this.dialog_status = "update_dashboard"
      this.dashboard_form = Object.assign({}, row)
    },
    submit_dashboard() {
      if (this.dialog_status === "create_dashboard") {
        createDashboard(this.dashboard_form)
          .then(resp => {
            this.$message({
              type: "success",
              message: "新增大盘成功"
            })
            this.dashboard_dialog = false
            this.get_dashboard_list()
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            })
            this.dashboard_dialog = false
            this.get_dashboard_list()
          })
      } else if (this.dialog_status === "update_dashboard") {
        updateDashboardByID(this.dashboard_form.id, this.dashboard_form)
          .then(resp => {
            this.$message({
              type: "success",
              message: "更新大盘成功"
            })
            this.dashboard_dialog = false
            this.get_dashboard_list()
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            })
            this.dashboard_dialog = false
            this.get_dashboard_list()
          })
      }
    },
    delete_dashboard(row) {
      deleteDashboardByID(row.id)
        .then(resp => {
          this.$message({
            type: "success",
            message: "删除大盘成功"
          })
          this.get_dashboard_list()
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
          this.get_dashboard_list()
        })
    },
    get_dashboard_list() {
      const params = "product__id__in"
      this.list_query[params] = this.current_select_product_id
      // 如果是选择的产品是全部【0】就展示全部
      if (this.current_select_product_id === 0) {
        this.list_query[params] = ""
      } else {
        this.list_query[params] = this.current_select_product_id
      }
      getDashboardList(this.list_query)
        .then(resp => {
          this.dashboard_list = resp.data.results
          this.dashboard_list_total = resp.data.count
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    cancel_delete() {
      this.$message({
        type: "warning",
        message: "你考虑的很全面..."
      })
    }
  }
}
</script>

<style scoped>
.el-table {
  width: 100%;
  margin-top: 10px;
}
.el-input {
  width: 300px;
}
</style>
