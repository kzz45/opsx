监控配置页面

<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-tabs
        v-model="active_tab_name"
        @tab-click="active_tab_click"
      >
        <!-- 任务管理-------------------------------------------------- -->
        <el-tab-pane
          label="任务管理"
          name="task_manage"
        >
          <div>
            <el-button
              type="primary"
              icon="el-icon-circle-plus-outline"
              size="small"
              @click="create_task"
            >新增任务
            </el-button>
            <el-radio-group
              v-model="task_mode"
              size="small"
              style="margin-left: 20px;"
              @change="change_task_mode"
            >
              <el-radio-button :label="0">基础任务</el-radio-button>
              <el-radio-button :label="1">业务任务</el-radio-button>
              <!-- <el-radio-button :label="2">探测任务</el-radio-button> -->
            </el-radio-group>
          </div>
          <el-table
            :data="task_list"
            size="small"
            border
          >
            <el-table-column
              label="任务名"
              prop="name"
            ></el-table-column>
            <el-table-column
              v-if="task_mode === 2"
              label="探测对象"
              prop="target"
            >
              <template slot-scope="scoped">
                <span>{{ scoped.row.target }}</span>
              </template>
            </el-table-column>
            <el-table-column
              v-if="task_mode === 2"
              label="探测类型"
              prop="mode"
            ></el-table-column>
            <el-table-column
              v-if="task_mode != 2"
              label="实例类型"
              prop="instance_type__name"
            >
              <template slot-scope="scoped">
                <svg-icon
                  v-if="scoped.row.instance_type__name=='machine'"
                  class="el-icon"
                  icon-class="ecs"
                  style="font-size: 20px;"
                ></svg-icon>
                <svg-icon
                  v-if="scoped.row.instance_type__name=='kubernetes'"
                  class="el-icon"
                  icon-class="kubernetes"
                  style="font-size: 20px;"
                ></svg-icon>
                <svg-icon
                  v-if="scoped.row.instance_type__name=='domain'"
                  class="el-icon"
                  icon-class="domain_type"
                  style="font-size: 20px;"
                ></svg-icon>
                <svg-icon
                  v-if="scoped.row.instance_type__name=='redis_cluster'"
                  class="el-icon"
                  icon-class="redis"
                  style="font-size: 20px;"
                ></svg-icon>
                <svg-icon
                  v-if="scoped.row.instance_type__name=='redis_standard'"
                  class="el-icon"
                  icon-class="redis"
                  style="font-size: 20px;"
                ></svg-icon>
                <svg-icon
                  v-if="scoped.row.instance_type__name=='mysql'"
                  class="el-icon"
                  icon-class="mysql"
                  style="font-size: 20px;"
                ></svg-icon>
                <svg-icon
                  v-if="scoped.row.instance_type__name=='mongodb'"
                  class="el-icon"
                  icon-class="mongodb"
                  style="font-size: 20px;"
                ></svg-icon>
                <svg-icon
                  v-if="scoped.row.instance_type__name=='slb'"
                  class="el-icon"
                  icon-class="slb"
                  style="font-size: 20px;"
                ></svg-icon>
              </template>
            </el-table-column>
            <el-table-column
              v-if="task_mode == 0"
              label="实例数量"
              prop="instances"
            >
              <template slot-scope="scoped">
                <el-tag type="success">{{ scoped.row.instances }}</el-tag>
                <!-- <el-tag
                  type="danger"
                  style="margin-left: 10px;"
                >{{ scoped.row.online_instances }}</el-tag> -->
              </template>
            </el-table-column>
            <el-table-column
              v-if="task_mode == 0"
              label="任务数量"
              prop="add_ons"
            >
              <template slot-scope="scoped">
                <span>{{ scoped.row.add_ons }}</span>
              </template>
            </el-table-column>
            <el-table-column
              v-if="task_mode == 0"
              label="已监控"
              prop="add_ons"
            >
              <template slot-scope="scoped">
                <!-- <el-tag type="success">{{ scoped.row.instances }}</el-tag> -->
                <el-tag
                  type="danger"
                  style="margin-left: 10px;"
                >{{ scoped.row.online_instances }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column
              v-if="task_mode == 1"
              label="挂载节点"
              prop="server_group"
            >
              <template slot-scope="scoped">
                <el-tag>{{ scoped.row.server_group__name }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column
              label="产品"
              prop="product__name"
            >
              <template slot-scope="scoped">
                <span>{{ scoped.row.product__name }}</span>
              </template>
            </el-table-column>
            <el-table-column
              v-if="task_mode == 1"
              label="URL"
              prop="url"
            >
              <template slot-scope="scoped">
                <span>{{ scoped.row.url }}</span>
              </template>
            </el-table-column>
            <el-table-column
              label="操作"
              prop="options"
              width="180px;"
            >
              <template slot-scope="scoped">
                <el-tooltip
                  v-if="task_mode === 0"
                  class="item"
                  effect="dark"
                  content="查看任务详情"
                  placement="top"
                >
                  <el-button
                    type="success"
                    icon="el-icon-info"
                    size="mini"
                    @click="view_prometheus_task(scoped.row)"
                  ></el-button>
                </el-tooltip>
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  size="mini"
                  @click="update_prometheus_task(scoped.row)"
                ></el-button>
                <el-popconfirm
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left: 10px"
                  @confirm="delete_task(scoped.row)"
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
            v-show="task_list_total>0"
            :total="task_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_task_list"
          >
          </pagination>
        </el-tab-pane>
        <!-- 告警规则管理-------------------------------------------------- -->
        <el-tab-pane
          label="告警规则"
          name="alert_rule_manage"
        >
          <div>
            <el-button
              type="primary"
              icon="el-icon-circle-plus-outline"
              size="small"
              @click="add_alert_rule"
            >新增规则
            </el-button>
            <el-radio-group
              v-model="alert_rule_type"
              size="small"
              style="margin-left: 20px;"
              @change="change_alert_rule_type"
            >
              <el-radio-button
                v-for="item in alert_rule_type_list"
                :key="item.id"
                :label="item.id"
              >{{ item.desc }}</el-radio-button>
            </el-radio-group>
          </div>
          <el-table
            ref="alert_rule_listRefs"
            :data="alert_rule_list"
            size="small"
            border
            @expand-change="get_children_rules"
          >
            <el-table-column
              label="名称"
              prop="name"
            ></el-table-column>
            <el-table-column
              label="规则(PromQL)"
              prop="expression"
            >
              <template slot-scope="scoped">
                {{ scoped.row.expression }} {{ scoped.row.op }} {{ scoped.row.value }}
              </template>
            </el-table-column>
            <!-- <el-table-column
              label="表达式"
              prop="op"
            ></el-table-column>
            <el-table-column
              label="阈值"
              prop="value"
            ></el-table-column> -->
            <el-table-column
              label="等级"
              prop="level"
            >
              <template slot-scope="scoped">
                <el-tag
                  v-if="scoped.row.level=='info'"
                  type="info"
                >普通</el-tag>
                <el-tag
                  v-else-if="scoped.row.level =='crit'"
                  type="danger"
                >严重</el-tag>
                <el-tag
                  v-else
                  type="warning"
                >警告</el-tag>
              </template>
            </el-table-column>
            <el-table-column
              label="告警消息"
              prop="summary"
            ></el-table-column>
            <el-table-column
              label="产品"
              prop="product__name"
            >
            </el-table-column>
            <!-- <el-table-column
              label="是否启用"
              prop="enable"
            >
              <template slot-scope="scoped">
                <el-tag
                  v-if="scoped.row.enable === true"
                  type="success"
                  size="small"
                >启用</el-tag>
                <el-tag
                  v-else
                  type="danger"
                  size="small"
                >禁用</el-tag>
              </template>
            </el-table-column> -->
            <el-table-column
              label="操作"
              probe="options"
              width="240px"
            >
              <template slot-scope="scoped">
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  size="mini"
                  @click="edit_alert_rule(scoped.row)"
                ></el-button>
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="查看子规则"
                  placement="top"
                >
                  <el-button
                    type="info"
                    icon="el-icon-arrow-down"
                    size="mini"
                    @click="view_alert_rule_children(scoped.row)"
                  ></el-button>
                </el-tooltip>
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="添加子规则"
                  placement="top"
                >
                  <el-button
                    type="success"
                    icon="el-icon-plus"
                    size="mini"
                    @click="add_alert_rule_children(scoped.row)"
                  ></el-button>
                </el-tooltip>
                <el-popconfirm
                  title="确定删除这条规则吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left: 10px"
                  @confirm="delete_alert_rule(scoped.row)"
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
            <el-table-column
              type="expand"
              width="1"
            >
              <template slot-scope="scoped">
                <el-table
                  :data="scoped.row.children_rules"
                  empty-text="这里没有子规则"
                  border
                  size="small"
                  style="margin-left: 20px;"
                >
                  <el-table-column
                    label="产品"
                    prop="product__name"
                  ></el-table-column>
                  <el-table-column
                    label="标签"
                    prop="match"
                  >
                    <template slot-scope="scope">
                      <el-tag
                        v-for="(item, index) in (JSON.parse(scope.row.match))"
                        :key="index"
                      >{{ item.name +'=' + item.value }}</el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column
                    label="表达式"
                    prop="op"
                  ></el-table-column>
                  <el-table-column
                    label="阈值"
                    prop="value"
                  ></el-table-column>
                  <el-table-column
                    label="等级"
                    prop="level"
                  >
                    <template slot-scope="scope">
                      <el-tag
                        v-if="scope.row.level=='info'"
                        type="info"
                      >普通</el-tag>
                      <el-tag
                        v-else-if="scope.row.level =='crit'"
                        type="danger"
                      >严重</el-tag>
                      <el-tag
                        v-else
                        type="warning"
                      >警告</el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column
                    label="是否覆盖"
                    prop="is_cover"
                  >
                    <template slot-scope="scope">
                      {{ scope.row.is_cover == 1?'是':'否' }}
                    </template>
                  </el-table-column>
                  <el-table-column
                    label="操作"
                    prop="options"
                  >
                    <template slot-scope="scope">
                      <el-button
                        type="primary"
                        icon="el-icon-edit"
                        size="mini"
                        @click="edit_alert_rule_children(scope.row)"
                      ></el-button>
                      <el-popconfirm
                        title="确定删除这条子规则吗？"
                        confirm-button-text="确定"
                        cancel-button-text="不了"
                        style="margin-left: 10px"
                        @confirm="delete_alert_rule_children(scope.row)"
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
              </template>
            </el-table-column>
          </el-table>
          <pagination
            v-show="alert_rule_list_total>0"
            :total="alert_rule_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_alert_rule_list"
          >
          </pagination>
        </el-tab-pane>
        <!-- 告警路由管理-------------------------------------------------- -->
        <el-tab-pane
          label="告警路由"
          name="alert_route_manage"
        >
          <div>
            <el-button
              type="primary"
              icon="el-icon-circle-plus-outline"
              size="small"
              @click="add_alert_route('parent')"
            >新增
            </el-button>
          </div>
          <el-table
            ref="alert_route_listRefs"
            :data="alert_route_list"
            size="small"
            border
            @expand-change="get_children_route"
          >
            <el-table-column
              label="名称"
              prop="name"
            ></el-table-column>
            <el-table-column
              label="通知组"
              prop="receiver__list"
            >
              <template slot-scope="scoped">
                <el-tag
                  v-for="(item, index) in scoped.row.receiver__list"
                  :key="index"
                >{{ item }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column
              label="重复告警"
              prop="repeat_interval"
            >
              <template slot-scope="scoped">
                <el-tag>{{ scoped.row.repeat_interval / 60 }}分钟</el-tag>
              </template>
            </el-table-column>
            <el-table-column
              label="匹配标签"
              prop="match"
            >
              <template slot-scope="scoped">
                <el-tag
                  v-for="(item, index) in (JSON.parse(scoped.row.match)).label"
                  :key="index"
                >{{ item.name + '=' + item.value }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column
              label="产品"
              prop="product__name"
            ></el-table-column>
            <el-table-column
              label="操作"
              probe="options"
              width="240px;"
            >
              <template slot-scope="scoped">
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  size="mini"
                  @click="edit_alert_route(scoped.row)"
                ></el-button>
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="查看子路由"
                  placement="top"
                >
                  <el-button
                    type="info"
                    icon="el-icon-arrow-down"
                    size="mini"
                    @click="view_alert_route_children(scoped.row)"
                  ></el-button>
                </el-tooltip>
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="添加子路由"
                  placement="top"
                >
                  <el-button
                    type="success"
                    icon="el-icon-plus"
                    size="mini"
                    @click="add_alert_route('children',scoped.row)"
                  ></el-button>
                </el-tooltip>
                <el-popconfirm
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left: 10px"
                  @confirm="delete_alert_route(scoped.row)"
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
            <el-table-column
              type="expand"
              width="1"
            >
              <template slot-scope="scoped">
                <el-table
                  :data="scoped.row.children_route"
                  empty-text="这里没有子路由"
                  border
                  size="small"
                  style="margin-left: 20px;"
                >
                  <el-table-column
                    label="名称"
                    prop="name"
                  ></el-table-column>
                  <el-table-column
                    label="通知组"
                    prop="receiver__list"
                  >
                    <template slot-scope="scope">
                      <el-tag
                        v-for="(item, index) in scope.row.receiver__list"
                        :key="index"
                      >{{ item }}</el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column
                    label="通知上层"
                    prop="is_raise"
                  >
                    <template slot-scope="scope">
                      {{ scope.row.is_raise == 0 ? '否':'是' }}
                    </template>
                  </el-table-column>
                  <el-table-column
                    label="重复告警"
                    prop="repeat_interval"
                  >
                    <template slot-scope="scope">
                      <el-tag>{{ scope.row.repeat_interval / 60 }}分钟</el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column
                    label="标签"
                    prop="match"
                  >
                    <template slot-scope="scope">
                      <el-tag
                        v-for="(item, index) in (JSON.parse(scope.row.match)).label"
                        :key="index"
                      >{{ item.name + '=' + item.value }}</el-tag>
                    </template>
                  </el-table-column>

                  <el-table-column
                    label="产品"
                    prop="product__name"
                  ></el-table-column>
                  <el-table-column
                    label="操作"
                    prop="options"
                  >
                    <template slot-scope="scope">
                      <el-button
                        type="primary"
                        icon="el-icon-edit"
                        size="mini"
                        @click="edit_alert_route_children(scope.row)"
                      ></el-button>
                      <el-popconfirm
                        title="确定删除吗？"
                        confirm-button-text="确定"
                        cancel-button-text="不了"
                        style="margin-left: 10px"
                        @confirm="delete_alert_route_children(scope.row)"
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
              </template>
            </el-table-column>
          </el-table>
          <pagination
            v-show="alert_route_list_total>0"
            :total="alert_route_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_alert_route_list"
          >
          </pagination>
        </el-tab-pane>
        <!-- 告警通知组管理-------------------------------------------------- -->
        <el-tab-pane
          label="告警通知"
          name="alert_group_manage"
        >
          <div>
            <el-button
              type="primary"
              icon="el-icon-circle-plus-outline"
              size="small"
              @click="add_alert_group"
            >新增通知组
            </el-button>
          </div>
          <el-table
            :data="alert_group_list"
            size="small"
            border
          >
            <el-table-column
              label="名称"
              prop="name"
            ></el-table-column>
            <!-- <el-table-column
              label="接收人"
              prop="user_list"
            >
              <template slot-scope="scoped">
                <el-tag
                  v-for="(item, index) in scoped.row.user_list"
                  :key="index"
                  style="margin-left: 2px;"
                  size="small"
                >{{ item.first_name }}</el-tag>
              </template>
            </el-table-column> -->
            <el-table-column
              label="通知渠道"
              prop="channel"
            >
              <template slot-scope="scoped">
                <svg-icon
                  v-if="scoped.row.channel=='wechat'"
                  class="el-icon"
                  icon-class="wechat-icon"
                  style="font-size: 20px;"
                ></svg-icon>
                <svg-icon
                  v-if="scoped.row.channel=='dingtalk'"
                  class="el-icon"
                  icon-class="dingtalk"
                  style="font-size: 20px;"
                ></svg-icon>
                <svg-icon
                  v-if="scoped.row.channel=='feishu'"
                  class="el-icon"
                  icon-class="feishu"
                  style="font-size: 20px;"
                ></svg-icon>
              </template>
            </el-table-column>
            <el-table-column
              label="WebHook"
              prop="webhook"
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
                  @click="edit_alert_group(scoped.row)"
                ></el-button>
                <el-popconfirm
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left: 10px"
                  @confirm="delete_alert_group(scoped.row)"
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
            v-show="alert_group_list_total>0"
            :total="alert_group_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_alert_group_list"
          >
          </pagination>
        </el-tab-pane>
        <!-- 告警回调管理 -->
        <!-- <el-tab-pane
          label="告警回调"
          name="alert_callback"
        >
          <div>
            <el-button
              type="primary"
              icon="el-icon-circle-plus-outline"
              size="small"
              @click="create_callback"
            >新增回调
            </el-button>
          </div>
          <el-table
            :data="callback_list"
            size="small"
            border
          >
            <el-table-column
              label="产品别名"
              prop="name"
            ></el-table-column>
            <el-table-column
              label="产品名称"
              prop="product__name"
            ></el-table-column>
            <el-table-column
              label="Robot"
              prop="robot"
            ></el-table-column>
            <el-table-column
              label="云厂商"
              prop="factory__name"
            ></el-table-column>
            <el-table-column
              label="操作"
              width="240px;"
            >
              <template slot-scope="scoped">
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  size="mini"
                  @click="update_callback(scoped.row)"
                ></el-button>
                <el-popconfirm
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left: 10px"
                  @confirm="delete_callback(scoped.row)"
                  @cancel="cancel_delete"
                >
                  <el-button
                    slot="reference"
                    type="danger"
                    icon="el-icon-delete"
                    size="mini"
                  ></el-button>
                </el-popconfirm>
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="事件回调地址"
                  placement="top"
                >
                  <el-button
                    type="info"
                    icon="el-icon-copy-document"
                    size="mini"
                    style="margin-left: 10px;"
                    @click="copy_event_callback_info(scoped.row)"
                  ></el-button>
                </el-tooltip>
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="告警回调地址"
                  placement="top"
                >
                  <el-button
                    type="warning"
                    icon="el-icon-copy-document"
                    size="mini"
                    style="margin-left: 10px;"
                    @click="copy_cms_callback_info(scoped.row)"
                  ></el-button>
                </el-tooltip>
              </template>
            </el-table-column>
          </el-table>
          <pagination
            v-show="callback_list_total>0"
            :total="callback_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_callback_list"
          >
          </pagination>
        </el-tab-pane> -->
        <!-- 任务分组管理-------------------------------------------------- -->
        <!-- <el-tab-pane
          label="分组任务"
          name="group_manage"
          disabled
        >
          <div>
            <el-button
              type="primary"
              icon="el-icon-circle-plus-outline"
              size="small"
              @click="add_group"
            >新增分组
            </el-button>
          </div>
          <el-table
            :data="group_list"
            size="small"
            border
          >
            <el-table-column
              label="实例类型"
              prop="instance_type__name"
            ></el-table-column>
            <el-table-column
              label="名称"
              prop="name"
            ></el-table-column>
            <el-table-column
              label="产品"
              prop="product"
            ></el-table-column>
            <el-table-column
              label="实体数量"
              prop="instance_num"
            ></el-table-column>
            <el-table-column
              label="分组标签"
              prop="group_tag"
            ></el-table-column>
            <el-table-column
              label="操作"
              prop="options"
            >
              <template slot-scope="scoped">
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  size="mini"
                  @click="edit_group(scoped.row)"
                ></el-button>
                <el-popconfirm
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left:10px"
                  @confirm="delete_group(scoped.row)"
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
            v-show="group_list_total>0"
            :total="group_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_group_list"
          >
          </pagination>
        </el-tab-pane> -->
      </el-tabs>
    </el-card>
    <!-- 告警规则Dialog-------------------------------------------------- -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="alert_rule_dialog"
      width="50%"
    >
      <el-form
        ref="alert_rule_formRefs"
        :model="alert_rule_form"
        :rules="alert_rule_form_rules"
        label-width="100px"
        size="small"
      >
        <el-form-item
          label="名称"
          prop="name"
        >
          <el-input
            v-model="alert_rule_form.name"
            clearable
            placeholder="告警规则名称"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="等级"
          prop="level"
        >
          <el-radio-group v-model="alert_rule_form.level">
            <el-radio label="crit">严重</el-radio>
            <el-radio label="warn">警告</el-radio>
            <el-radio label="info">普通</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item
          label="类型"
          prop="alert_rule_type"
        >
          <el-select
            v-model="alert_rule_form.alert_rule_type"
            placeholder="请选择告警规则类型"
            style="width: 300px"
          >
            <el-option
              v-for="item in alert_rule_type_list"
              :key="item.id"
              :value="item.id"
              :label="item.desc"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          label="持续时间(s)"
          prop="interval"
        >
          <el-input-number
            v-model="alert_rule_form.interval"
            placeholder="告警持续时间"
            style="width: 300px"
          ></el-input-number>
        </el-form-item>
        <el-form-item
          label="表达式"
          prop="expression"
        >
          <el-input
            v-model="alert_rule_form.expression"
            :autosize="{ minRows:2 }"
            type="textarea"
            placeholder="告警规则内容"
            style="width: 300px"
          ></el-input>
          <br>
          <el-select
            v-model="alert_rule_form.op"
            filterable
            clearable
            placeholder="操作符"
            style="width: 140px; margin-top: 10px"
          >
            <el-option
              v-for="item in operatorItems"
              :key="item.id"
              :value="item.id"
              :label="item.name"
            ></el-option>
          </el-select>
          <el-input-number
            v-model="alert_rule_form.value"
            placeholder="阈值"
            style="margin-left: 20px; margin-top: 10px; width: 140px"
          ></el-input-number>
        </el-form-item>
        <el-form-item
          label="信息"
          prop="summary"
        >
          <el-input
            v-model="alert_rule_form.summary"
            :autosize="{ minRows:2 }"
            type="textarea"
            placeholder="请输入告警信息"
            style="width: 300px"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="关联产品"
          prop="product"
        >
          <el-select
            v-model="alert_rule_form.product"
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
        <el-form-item
          label="状态"
          prop="enable"
        >
          <el-switch
            v-model="alert_rule_form.enable"
            active-color="#13ce66"
            inactive-color="#ff4949"
            active-text="启用"
            inactive-text="禁用"
          >
          </el-switch>
        </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="alert_rule_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_alert_rule"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 告警子规则Dialog-------------------------------------------------- -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="alert_rule_children_dialog"
      width="50%"
    >
      <el-form
        ref="alert_rule_children_formRefs"
        :model="alert_rule_children_form"
        :rules="alert_rule_children_form_rules"
        label-width="100px"
        size="small"
      >

        <el-form-item
          label="产品"
          prop="product"
        >
          <el-select
            v-model="alert_rule_children_form.product"
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
        <el-form-item label="标签选择">
          <labelHandler ref="label_handler"></labelHandler>
        </el-form-item>
        <el-form-item
          label="操作符"
          prop="op"
        >
          <el-select
            v-model="alert_rule_children_form.op"
            filterable
            clearable
            placeholder="操作符"
            style="width: 140px;"
          >
            <el-option
              v-for="item in operatorItems"
              :key="item.id"
              :value="item.id"
              :label="item.name"
            ></el-option>
          </el-select>
          <el-input-number
            v-model="alert_rule_children_form.value"
            placeholder="阈值"
            style="margin-left: 20px; width: 140px"
          ></el-input-number>
        </el-form-item>
        <el-form-item
          label="等级"
          prop="level"
        >
          <el-radio-group v-model="alert_rule_children_form.level">
            <el-radio label="crit">严重</el-radio>
            <el-radio label="warn">警告</el-radio>
            <el-radio label="info">普通</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item
          label="覆盖父规则"
          prop="is_cover"
        >
          <el-radio-group v-model="alert_rule_children_form.is_cover">
            <el-radio :label="1">是</el-radio>
            <el-radio :label="0">否</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button
          size="small"
          @click="alert_rule_children_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_alert_rule_children"
        >确 定</el-button>
      </div>
    </el-dialog>
    <!-- 告警路由Dialog-------------------------------------------------- -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="alert_route_dialog"
      width="50%"
    >
      <el-form
        ref="alert_route_formRefs"
        :model="alert_route_form"
        :rules="alert_route_form_rules"
        label-width="100px"
        size="small"
      >
        <el-form-item
          label="名称"
          prop="name"
        >
          <el-input
            v-model="alert_route_form.name"
            clearable
            placeholder="告警路由名称"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="通知组"
          prop="receiver"
        >
          <el-select
            v-model="alert_route_form.receiver"
            clearable
            filterable
            multiple
            autocomplete="on"
            placeholder="请选择通知组"
            style="width: 300px;"
          >
            <el-option
              v-for="(item) in alert_group_list"
              :key="item.id"
              :value="item.id"
              :label="item.name"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          label="是否正则"
          prop="match_re"
        >
          <el-radio-group v-model="alert_route_form.match_re">
            <el-radio :label="1">是</el-radio>
            <el-radio :label="0">否</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item
          label="选择标签"
          prop="match"
        >
          <labelHandler ref="label_handler"></labelHandler>
        </el-form-item>
        <el-form-item
          label="通知父规则"
          prop="is_raise"
        >
          <el-radio-group v-model="alert_route_form.is_raise">
            <el-radio :label="1">是</el-radio>
            <el-radio :label="0">否</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item
          label="聚合条件"
          prop="group_by"
        >
          <el-select
            v-model="alert_route_form.group_by"
            placeholder="请选择聚合条件"
            multiple
            filterable
            style="width: 300px"
          >
            <el-option
              v-for="item in conditionData"
              :key="item.value"
              :label="item.name"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          label="聚合时间(秒)"
          prop="group_wait"
        >
          <el-input-number
            v-model="alert_route_form.group_wait"
            :step="60"
            clearable
            placeholder="请输入归并时间"
            style="width: 300px"
          ></el-input-number>
        </el-form-item>
        <el-form-item
          label="重复聚合(秒)"
          prop="group_interval"
        >
          <el-input-number
            v-model="alert_route_form.group_interval"
            :step="60"
            clearable
            placeholder="请输入重复聚合时间"
            style="width: 300px"
          ></el-input-number>
        </el-form-item>
        <el-form-item
          label="重复发送(秒)"
          prop="repeat_interval"
        >
          <el-input-number
            v-model="alert_route_form.repeat_interval"
            :step="60"
            clearable
            placeholder="请输入重复发送时间"
            style="width: 300px"
          ></el-input-number>
        </el-form-item>
        <el-form-item
          label="关联产品"
          prop="product"
        >
          <el-select
            v-model="alert_route_form.product"
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
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="alert_route_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_alert_route"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 告警通知组Dialog-------------------------------------------------- -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="alert_group_dialog"
      width="50%"
    >
      <el-form
        ref="alert_group_formRefs"
        :model="alert_group_form"
        :rules="alert_group_form_rules"
        label-width="100px"
        size="small"
      >
        <el-form-item label="说明">
          <el-tag
            type="info"
            style="width: 300px;"
          >告警信息通知给谁(我们定义了一个通知用户组)</el-tag>
        </el-form-item>
        <el-form-item
          label="名称"
          prop="name"
        >
          <el-input
            v-model="alert_group_form.name"
            clearable
            placeholder="通知组名称"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="接收人"
          prop="users"
        >
          <el-select
            v-model="alert_group_form.users"
            clearable
            filterable
            :multiple="true"
            autocomplete="on"
            placeholder="请选择通知用户"
            style="width: 300px;"
          >
            <el-option
              v-for="item in user_list"
              :key="item.id"
              :value="item.id"
              :label="item.first_name"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="通知渠道">
          <el-input
            v-model="alert_group_form.webhook"
            placeholder="请输入robot"
          >
            <el-select
              slot="prepend"
              v-model="alert_group_form.channel"
              placeholder="选择渠道"
              style="width: 90px;"
            >
              <el-option
                label="微信"
                value="wechat"
              ></el-option>
              <el-option
                label="钉钉"
                value="dingtalk"
              ></el-option>
              <el-option
                label="飞书"
                value="feishu"
              ></el-option>
            </el-select>
          </el-input>
        </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="alert_group_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_alert_group"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 任务抓取管理Dialog-------------------------------------------------- -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="prometheus_task_dialog"
      width="50%"
    >
      <el-form
        ref="prometheus_task_formRefs"
        :model="prometheus_task_form"
        :rules="prometheus_task_form_rules"
        label-width="100px"
        size="small"
      >
        <el-form-item label="任务类型">
          <el-radio-group
            v-model="prometheus_task_form.mode"
            @change="change_task_mode"
          >
            <el-tooltip
              class="item"
              effect="dark"
              content="Prometheus任务"
              placement="top"
            >
              <el-radio
                :label="0"
                :disabled="prom_basic"
              >基础任务</el-radio>
            </el-tooltip>
            <el-tooltip
              class="item"
              effect="dark"
              content="具体的产品业务"
              placement="top"
            >
              <el-radio
                :label="1"
                :disabled="prom_business"
              >业务任务</el-radio>
            </el-tooltip>
            <el-tooltip
              class="item"
              effect="dark"
              content="探测任务"
              placement="top"
            >
              <el-radio
                :label="2"
                :disabled="prom_probe"
              >探测任务</el-radio>
            </el-tooltip>
          </el-radio-group>
        </el-form-item>
        <el-form-item
          label="任务名称"
          prop="name"
        >
          <el-input
            v-model="prometheus_task_form.name"
            placeholder="请输入Prometheus抓取任务名称"
            clearable
          ></el-input>
        </el-form-item>
        <el-form-item
          label="间隔时间(s)"
          prop="interval"
        >
          <el-input-number
            v-model="prometheus_task_form.interval"
            placeholder="请输入采集的间隔时间"
            style="width: 300px"
          >
          </el-input-number>
        </el-form-item>
        <el-form-item
          label="超时时间(s)"
          prop="timeout"
        >
          <el-input-number
            v-model="prometheus_task_form.timeout"
            placeholder="请输入采集的超时时间"
            style="width: 300px"
          ></el-input-number>
        </el-form-item>
        <el-form-item
          v-if="task_mode === 2"
          label="探测类型"
          prop="probe_mode"
        >
          <el-radio-group v-model="prometheus_task_form.probe_mode">
            <el-radio
              v-for="item in task_mode_list"
              :key="item.value"
              :label="item.value"
              :value="item.value"
            >{{ item.name }}</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item
          v-if="task_mode === 2"
          label="探测节点"
          prop="probe"
        >
          <el-select
            v-model="prometheus_task_form.probe"
            placeholder="请选择探测节点"
            size="small"
            clearable
            multiple
            style="width: 300px;"
          >
            <el-option
              v-for="item in task_probe_list"
              :key="item.id"
              :value="item.id"
              :label="item.name"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          v-if="task_mode === 2"
          label="探测对象"
          prop="target"
        >
          <el-input
            v-model="prometheus_task_form.target"
            clearable
            placeholder="请输入探测地址"
          ></el-input>
        </el-form-item>
        <el-form-item
          v-if="task_mode !== 2"
          label="实例类型"
          prop="instance_type"
        >
          <el-select
            v-model="prometheus_task_form.instance_type"
            size="small"
            clearable
            style="width: 300px;"
          >
            <el-option
              v-for="(item) in instance_type_list"
              :key="item.id"
              :value="item.id"
              :label="item.name"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          v-if="task_mode === 0"
          label="包含标签"
          prop="include_label"
        >
          <labelHandler ref="include_label_handler"></labelHandler>
        </el-form-item>
        <el-form-item
          v-if="task_mode === 0"
          label="不包含标签"
          prop="exclude_label"
        >
          <labelHandler ref="exclude_label_handler"></labelHandler>
        </el-form-item>
        <el-form-item
          v-if="task_mode === 1"
          label="URL地址"
          prop="url"
        >
          <el-input
            v-model="prometheus_task_form.url"
            placeholder="请输入URL(API)地址"
            clearable
          ></el-input>
        </el-form-item>
        <el-form-item
          v-if="task_mode === 1"
          label="挂载节点"
          prop="server_group"
        >
          <el-select
            v-model="prometheus_task_form.server_group"
            placeholder="请选择挂载节点"
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
          label="关联产品"
          prop="product"
        >
          <el-select
            v-model="prometheus_task_form.product"
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
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="prometheus_task_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_prometheus_task"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 任务分组管理Dialog-------------------------------------------------- -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="group_dialog"
    >
      <el-form
        ref="group_formRefs"
        :model="group_form"
        :rules="group_form_rules"
        label-width="100px"
        size="small"
      >
        <el-form-item
          label="分组名称"
          prop="name"
        >
          <el-input
            v-model="group_form.name"
            clearable
            placeholder="分组名称"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="分组类型"
          prop="mode"
        >
          <el-radio-group v-model="group_form.mode">
            <el-radio label="0">自定义</el-radio>
            <el-radio label="1">API同步</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item
          v-if="group_form.mode=='1'"
          label="API地址"
          prop="policy"
        >
          <el-input
            v-model="group_form.policy"
            placeholder="http开头"
          ></el-input>
        </el-form-item>
        <el-form-item label="标签选择"></el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="group_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_group"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 监控回调dialog-------------------------------------------------- -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="callback_dialog"
    >
      <el-form
        ref="callback_formRefs"
        :model="callback_form"
        :rules="callback_form_rules"
        label-width="100px"
        size="small"
      >
        <!-- <el-form-item
          label="类型"
          prop="types"
        >
          <el-radio-group v-model="callback_form.types">
            <el-radio :label="1">云监控</el-radio>
            <el-radio :label="2">云事件</el-radio>
          </el-radio-group>
        </el-form-item> -->
        <el-form-item
          label="产品别名"
          prop="name"
        >
          <el-input
            v-model="callback_form.name"
            clearable
            placeholder="产品别名"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="飞书Robot"
          prop="robot"
        >
          <el-input
            v-model="callback_form.robot"
            clearable
            placeholder="机器人地址"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="关联产品"
          prop="product"
        >
          <el-select
            v-model="callback_form.product"
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
        <el-form-item
          label="关联云厂"
          prop="factory"
        >
          <el-select
            v-model="callback_form.factory"
            placeholder="请选择云厂商"
            style="width: 300px;"
          >
            <el-option
              v-for="(item) in factory_list"
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
          @click="callback_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_callback"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { mapGetters } from "vuex"
import Pagination from "@/components/Pagination"
import labelHandler from "@/views/monitor/components/label_handler.vue"
import { getUserList } from "@/api/user"
import { getProductList } from "@/api/product"
import { getProbeList } from "@/views/monitor/api/probe"
import { getServerGroupList } from "@/views/monitor/api/server_group"
import {
  getProbeTaskList,
  createProbeTask,
  updateProbeTaskByID,
  deleteProbeTaskByID
} from "@/views/monitor/api/probe"
import { getLabelList } from "@/views/monitor/api/label"
import { getInstanceTypeList } from "@/views/monitor/api/instance_type"
import { getAlertRuleTypeList } from "@/views/monitor/api/alert_rule_type"
import {
  getAdJustList,
  createAdJust,
  updateAdJustByID,
  deleteAdJustByID
} from "@/views/monitor/api/adjust"
import {
  getTaskList,
  createTask,
  updateTaskByID,
  deleteTaskByID
} from "@/views/monitor/api/task"
import {
  getAlertRuleList,
  createAlertRule,
  updateAlertRuleByID,
  deleteAlertRuleByID
} from "@/views/monitor/api/alert_rule"
import {
  getAlertRouteList,
  createAlertRoute,
  updateAlertRouteByID,
  deleteAlertRouteByID
} from "@/views/monitor/api/alert_route"
import {
  getAlertUserGroupList,
  createAlertUserGroup,
  updateAlertUserGroupByID,
  deleteAlertUserGroupByID
} from "@/views/monitor/api/alert_user_group"
import { getFactoryList } from "@/api/factory"
import {
  getCallbackList,
  createCallback,
  updateCallbackByID,
  deleteCallbackByID
} from "@/views/monitor/api/callback"

export default {
  name: "AlertConfig",
  components: {
    Pagination,
    labelHandler
  },
  data() {
    return {
      list_query: {
        page: 1,
        limit: 15,
        mode: 0,
        alert_rule_type: null
      },
      active_tab_name: "task_manage",
      dialog_map: {
        create_alert_rule: "新增告警规则",
        update_alert_rule: "编辑告警规则",
        create_alert_rule_children: "添加告警子规则",
        update_alert_rule_children: "编辑告警子规则",
        create_alert_route: "新增告警路由",
        update_alert_route: "编辑告警路由",
        create_alert_route_children: "新增告警子路由",
        update_alert_route_children: "编辑告警子路由",
        create_alert_group: "新增告警通知组",
        update_alert_group: "编辑告警通知组",
        create_task: "新增告警任务(Prometheus Jobs)",
        update_task: "编辑告警任务(Prometheus Jobs)",
        create_group: "新增告警分组",
        update_group: "编辑告警分组",
        create_callback: "新增告警回调",
        update_callback: "编辑告警回调"
      },
      dialog_status: "",
      // 告警任务相关--------------------------------------------------
      task_mode: 0, // 默认的任务类型(基础任务)
      prom_basic: false,
      prom_business: false,
      prom_probe: true,
      prometheus_task_form: {
        id: "",
        mode: 0,
        name: "",
        interval: 60,
        timeout: 50,
        instance_type: null,
        product: null
      },
      prometheus_task_form_rules: {
        name: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        interval: [
          { required: true, message: "该项不能为空", trigger: "blur" }
        ],
        timeout: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        instance_type: [
          { required: true, message: "该项不能为空", trigger: "blur" }
        ],
        product: [{ required: true, message: "该项不能为空", trigger: "blur" }]
      },
      // 任务类型默认列表
      task_mode_list: [
        { name: "http", value: "http" },
        { name: "tcp", value: "tcp" },
        { name: "ping", value: "ping" }
      ],
      task_probe_list: [],
      server_group_list: [],
      alert_group_list: [],
      alert_group_list_total: 0,
      prometheus_task_dialog: false,
      task_list: [],
      task_list_total: 0,
      // 告警规则相关--------------------------------------------------
      alert_rule_type: 1,
      alert_rule_dialog: false,
      alert_rule_children_dialog: false,
      alert_rule_list: [],
      alert_rule_type_list: [],
      alert_rule_list_total: 0,
      alert_rule_form: {
        id: "",
        name: "",
        level: "crit",
        alert_rule_type: "",
        interval: 180,
        expression: "",
        op: "==",
        value: "",
        summary: "",
        enable: true,
        product: this.$store.getters.current_select_product_id
      },
      alert_rule_children_form: {
        id: null,
        product: null,
        op: "==",
        level: "crit",
        is_cover: 1
      },
      alert_rule_children_form_rules: {
        op: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        value: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        level: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        is_cover: [
          { required: true, message: "该项不能为空", trigger: "blur" }
        ],
        product: [{ required: true, message: "该项不能为空", trigger: "blur" }]
      },
      // 告警规则表达式操作符
      operatorItems: [
        { id: "==", name: "==" },
        { id: "!=", name: "!=" },
        { id: ">", name: ">" },
        { id: ">=", name: ">=" },
        { id: "<", name: "<" },
        { id: "<=", name: "<=" }
      ],
      alert_rule_form_rules: {
        name: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        level: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        interval: [
          { required: true, message: "该项不能为空", trigger: "blur" }
        ],
        expression: [
          { required: true, message: "该项不能为空", trigger: "blur" }
        ],
        summary: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        alert_rule_type: [
          { required: true, message: "该项不能为空", trigger: "blur" }
        ],
        product: [{ required: true, message: "该项不能为空", trigger: "blur" }]
      },
      // 告警路由相关--------------------------------------------------
      alert_route_dialog: false,
      alert_route_form: {
        id: "",
        name: "",
        match: "",
        match_re: 0,
        receiver: [],
        is_raise: 1,
        group_wait: 60,
        group_interval: 60,
        repeat_interval: 600,
        group_by: ["alertname", "level", "_product_id"],
        parent: 0, // 默认是父路由
        product: this.$store.getters.current_select_product_id
      },
      // 告警路由聚合条件
      conditionData: [
        { name: "alertname", value: "alertname" },
        { name: "level", value: "level" },
        { name: " _product_id", value: "_product_id" }
      ],
      alert_route_form_rules: {
        name: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        lables: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        receiver: [
          { required: true, message: "该项不能为空", trigger: "blur" }
        ],
        is_raise: [
          { required: true, message: "该项不能为空", trigger: "blur" }
        ],
        group_wait: [
          { required: true, message: "该项不能为空", trigger: "blur" }
        ],
        group_interval: [
          { required: true, message: "该项不能为空", trigger: "blur" }
        ],
        repeat_interval: [
          { required: true, message: "该项不能为空", trigger: "blur" }
        ],
        group_by: [
          { required: true, message: "该项不能为空", trigger: "blur" }
        ],
        product: [{ required: true, message: "该项不能为空", trigger: "blur" }]
      },
      alert_route_list: [],
      alert_route_list_temp: [],
      alert_route_list_total: 0,
      children_route: [],
      // 告警通知组相关--------------------------------------------------
      alert_group_dialog: false,
      alert_group_form: {
        id: "",
        name: "",
        users: [],
        webhook: "",
        channel: "feishu" // 告警通知组渠道
      },
      alert_group_form_rules: {
        name: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        users: [{ required: true, message: "该项不能为空", trigger: "blur" }]
      },
      wechat_channel: "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=",
      feishu_channel: "https://open.feishu.cn/open-apis/bot/v2/hook/",
      // 分组任务相关--------------------------------------------------
      group_form: {
        id: "",
        name: "",
        mode: "0"
      },
      group_form_rules: {
        name: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        mode: [{ required: true, message: "该项不能为空", trigger: "blur" }]
      },
      group_dialog: false,
      group_list: [],
      group_list_total: 0,
      user_list: [],
      product_list: [],
      label_list: [],
      instance_type_list: [],
      // 告警回调相关--------------------------------------------------
      callback_dialog: false,
      callback_form: {
        id: null,
        types: 1,
        name: "",
        robot: "",
        product: null,
        factory: null
      },
      callback_form_rules: {
        name: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        robot: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        product: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        factory: [{ required: true, message: "该项不能为空", trigger: "blur" }]
      },
      callback_list: [],
      callback_list_total: 0,
      factory_list: []
    }
  },
  computed: {
    ...mapGetters(["current_select_product_id", "current_select_product_name"])
  },
  watch: {
    current_select_product_id: function() {
      this.get_alert_route_list()
    }
  },
  created() {
    if (this.$route.params.active_tab_name === undefined) {
      this.active_tab_name = "task_manage"
    } else {
      this.active_tab_name = this.$route.params.active_tab_name
    }
    this.get_task_list()
    this.get_user_list()
    this.get_probe_list()
    this.get_label_list()
    this.get_product_list()
    this.get_alert_rule_list()
    this.get_instance_type_list()
    this.get_alert_rule_type_list()
    this.get_server_group_list()
  },
  methods: {
    // tab选择
    active_tab_click(tab) {
      if (tab.name === "alert_rule_manage") {
        this.get_alert_rule_list()
      } else if (tab.name === "alert_route_manage") {
        this.list_query.limit = 100
        this.get_alert_group_list()
        this.get_alert_route_list()
      } else if (tab.name === "alert_group_manage") {
        this.get_alert_group_list()
      } else if (tab.name === "task_manage") {
        this.get_task_list()
        this.get_probe_list()
        this.get_instance_type_list()
        this.get_server_group_list()
      } else if (tab.name === "group_manage") {
        //
      } else if (tab.name === "alert_callback") {
        this.get_product_list()
        this.get_factory_list()
        this.get_callback_list()
      }
    },
    // 告警规则类型列表
    get_alert_rule_type_list() {
      getAlertRuleTypeList(this.list_query)
        .then(resp => {
          this.alert_rule_type_list = resp.data.results
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 获取用户列表
    get_user_list() {
      getUserList(this.list_query)
        .then(resp => {
          this.user_list = resp.data.results
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 获取标签列表
    get_label_list() {
      getLabelList(this.list_query)
        .then(resp => {
          this.label_list = resp.data.results
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
      getProductList({ limit: 999 })
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
    // 获取实例类型列表
    get_instance_type_list() {
      getInstanceTypeList({ limit: 999 })
        .then(resp => {
          this.instance_type_list = resp.data.results
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 获取探测节点列表
    get_probe_list() {
      getProbeList({ limit: 999 })
        .then(resp => {
          this.task_probe_list = resp.data.results
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 获取采集组列表
    get_server_group_list() {
      getServerGroupList(this.list_query)
        .then(resp => {
          this.server_group_list = resp.data.results
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 任务管理相关--------------------------------------------------
    // 新增告警抓取任务
    create_task() {
      // console.log(this.task_mode, '===')
      this.prometheus_task_dialog = true
      this.dialog_status = "create_task"
      if (this.$refs.prometheus_task_formRefs) {
        this.$refs.prometheus_task_formRefs.resetFields()
      }
      this.prom_basic = false
      this.prom_business = false
      this.prom_probe = true
      if (this.task_mode === 0) {
        this.$nextTick(() => {
          this.$refs.exclude_label_handler.label_value_list = []
          this.$refs.include_label_handler.label_value_list = []
        })
        this.prometheus_task_form.name = null
        this.prometheus_task_form.product = null
        this.prometheus_task_form.instance_type = null
      } else if (this.task_mode === 1) {
        this.prometheus_task_form.name = null
        this.prometheus_task_form.url = null
        this.prometheus_task_form.product = null
        this.prometheus_task_form.instance_type = null
      } else if (this.task_mode === 2) {
        this.prometheus_task_form.name = null
        this.prometheus_task_form.product = null
        this.prometheus_task_form.probe = null
        this.prometheus_task_form.probe_mode = null
        this.prometheus_task_form.target = null
      }
    },
    // 编辑告警抓取任务
    update_prometheus_task(row) {
      // console.log(row, '====')
      this.prometheus_task_dialog = true
      this.dialog_status = "update_task"
      this.prometheus_task_form = Object.assign({}, row)
      if (this.task_mode === 0) {
        this.$nextTick(() => {
          this.$refs.exclude_label_handler.label_value_list = JSON.parse(
            row.match
          ).exclude
          this.$refs.include_label_handler.label_value_list = JSON.parse(
            row.match
          ).include
        })
        this.prom_basic = false
        this.prom_business = true
        this.prom_probe = true
      } else if (this.task_mode === 2) {
        this.prometheus_task_form.mode = 2
        this.prometheus_task_form.probe_mode = row.mode
        this.prom_basic = true
        this.prom_business = true
        this.prom_probe = false
      } else if (this.task_mode === 1) {
        this.prom_basic = true
        this.prom_business = false
        this.prom_probe = true
      }
    },
    // 新增或者编辑告警抓取任务
    submit_prometheus_task() {
      if (this.dialog_status === "create_task") {
        var post_data = Object.assign({}, this.prometheus_task_form)
        post_data.mode = this.task_mode
        var include = []
        var exclude = []
        if (this.task_mode === 0) {
          // 创建普通任务
          include = this.$refs.include_label_handler.label_value_list
          exclude = this.$refs.exclude_label_handler.label_value_list
          post_data.match = JSON.stringify({ exclude, include })
          createTask(post_data)
            .then(resp => {
              this.$message({
                type: "success",
                message: "新增任务成功"
              })
              this.prometheus_task_dialog = false
              this.get_task_list()
            })
            .catch(err => {
              this.$message({
                type: "error",
                message: err
              })
              this.prometheus_task_dialog = false
              this.get_task_list()
            })
        } else if (this.task_mode === 1) {
          // 创建业务任务
          createTask(post_data)
            .then(resp => {
              this.$message({
                type: "success",
                message: "新增任务成功"
              })
              this.prometheus_task_dialog = false
              this.get_task_list()
            })
            .catch(err => {
              this.$message({
                type: "error",
                message: err
              })
              this.prometheus_task_dialog = false
              this.get_task_list()
            })
        } else if (this.task_mode === 2) {
          // 创建探测任务
          // console.log(post_data, '====')
          post_data.mode = post_data.probe_mode
          createProbeTask(post_data)
            .then(resp => {
              this.$message({
                type: "success",
                message: "新增探测任务成功"
              })
              this.prometheus_task_dialog = false
              this.get_task_list()
            })
            .catch(err => {
              this.$message({
                type: "error",
                message: err
              })
              this.prometheus_task_dialog = false
              this.get_task_list()
            })
        }
      } else if (this.dialog_status === "update_task") {
        var update_data = Object.assign({}, this.prometheus_task_form)
        if (this.task_mode === 2) {
          // console.log(update_data, '====')
          update_data.mode = update_data.probe_mode
          updateProbeTaskByID(update_data.id, update_data)
            .then(resp => {
              this.$message({
                type: "success",
                message: "更新任务成功"
              })
              this.prometheus_task_dialog = false
              this.get_task_list()
            })
            .catch(err => {
              this.$message({
                type: "error",
                message: err
              })
              this.prometheus_task_dialog = false
              this.get_task_list()
            })
        } else if (this.task_mode === 0) {
          include = this.$refs.include_label_handler.label_value_list
          exclude = this.$refs.exclude_label_handler.label_value_list
          update_data.match = JSON.stringify({ exclude, include })
          updateTaskByID(update_data.id, update_data)
            .then(resp => {
              this.$message({
                type: "success",
                message: "更新任务成功"
              })
              this.prometheus_task_dialog = false
              this.get_task_list()
            })
            .catch(err => {
              this.$message({
                type: "error",
                message: err
              })
              this.prometheus_task_dialog = false
              this.get_task_list()
            })
        }
        if (this.task_mode === 1) {
          updateTaskByID(update_data.id, update_data)
            .then(resp => {
              this.$message({
                type: "success",
                message: "更新任务成功"
              })
              this.prometheus_task_dialog = false
              this.get_task_list()
            })
            .catch(err => {
              this.$message({
                type: "error",
                message: err
              })
              this.prometheus_task_dialog = false
              this.get_task_list()
            })
        }
      }
    },
    // 查看任务详情
    view_prometheus_task(row) {
      this.$router.push({
        path: "/monitor/task_detail/",
        query: { id: row.id, instance_type__name: row.instance_type__name }
      })
    },
    // 删除告警抓取任务
    delete_task(row) {
      if (this.task_mode === 2) {
        deleteProbeTaskByID(row.id)
          .then(resp => {
            this.$message({
              type: "success",
              message: "删除任务成功"
            })
            this.get_task_list()
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            })
            this.get_task_list()
          })
      } else {
        deleteTaskByID(row.id)
          .then(resp => {
            this.$message({
              type: "success",
              message: "删除任务成功"
            })
            this.get_task_list()
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            })
            this.get_task_list()
          })
      }
    },
    // 获取告警抓取任务列表
    get_task_list() {
      if (this.task_mode === 2) {
        this.task_list = []
        // this.list_query.mode = this.task_mode
        getProbeTaskList(this.list_query)
          .then(resp => {
            this.task_list = resp.data.results
            this.task_list_total = resp.data.count
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            })
          })
      } else {
        this.task_list = []
        this.list_query.mode = this.task_mode
        getTaskList(this.list_query)
          .then(resp => {
            this.task_list = resp.data.results
            this.task_list_total = resp.data.count
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            })
          })
      }
    },
    change_task_mode(label) {
      // console.log(this.task_mode, '======')
      // console.log(label, '====')
      this.task_mode = label
      if (this.task_mode === 0) {
        this.prometheus_task_form.mode = 0
      } else if (this.task_mode === 1) {
        this.prometheus_task_form.mode = 1
      } else if (this.task_mode === 2) {
        this.prometheus_task_form.mode = 2
      }
      this.get_task_list()
    },
    // 告警规则相关--------------------------------------------------
    change_alert_rule_type(label) {
      this.alert_rule_type = label
      this.get_alert_rule_list()
    },
    // 新增告警规则
    add_alert_rule() {
      this.alert_rule_dialog = true
      this.dialog_status = "create_alert_rule"
      this.alert_rule_form.name = null
      this.alert_rule_form.alert_rule_type = null
      this.alert_rule_form.expression = null
      this.alert_rule_form.op = null
      this.alert_rule_form.value = null
      this.alert_rule_form.summary = null
      this.alert_rule_form.product = null
      this.alert_rule_form.enable = true
    },
    // 编辑告警规则
    edit_alert_rule(row) {
      this.alert_rule_dialog = true
      this.dialog_status = "update_alert_rule"
      this.alert_rule_form = Object.assign({}, row)
    },
    // 查看告警子规则
    view_alert_rule_children(row) {
      const $table = this.$refs.alert_rule_listRefs
      this.alert_rule_list.map(item => {
        if (row.id !== item.id) {
          $table.toggleRowExpansion(item, false)
        }
      })
      $table.toggleRowExpansion(row)
    },
    // 添加告警规则子规则
    add_alert_rule_children(row) {
      this.alert_rule_children_dialog = true
      this.dialog_status = "create_alert_rule_children"
      // if (this.$refs.alert_rule_children_formRefs) {
      //   this.$refs.alert_rule_children_formRefs.resetFields()
      // }
      this.alert_rule_children_form.alert_rule = row.id
      this.alert_rule_children_form.product = null
      this.alert_rule_children_form.op = "=="
      this.alert_rule_children_form.value = null
      this.alert_rule_children_form.is_cover = 1
      this.$refs.label_handler.label_value_list = []
    },
    // 编辑告警子规则
    edit_alert_rule_children(row) {
      this.alert_rule_children_dialog = true
      this.dialog_status = "update_alert_rule_children"
      this.alert_rule_children_form = Object.assign({}, row)
      this.$nextTick(() => {
        this.$refs.label_handler.label_value_list = JSON.parse(row.match)
      })
      // console.log(this.alert_rule_children_form, '========')
    },
    // 新增或者编辑告警规则
    submit_alert_rule() {
      if (this.dialog_status === "create_alert_rule") {
        createAlertRule(this.alert_rule_form)
          .then(resp => {
            this.$message({
              type: "success",
              message: "新增告警规则成功"
            })
            this.alert_rule_dialog = false
            this.get_alert_rule_list()
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            })
            this.alert_rule_dialog = false
            this.get_alert_rule_list()
          })
      } else if (this.dialog_status === "update_alert_rule") {
        updateAlertRuleByID(this.alert_rule_form.id, this.alert_rule_form)
          .then(resp => {
            this.$message({
              type: "success",
              message: "更新告警规则成功"
            })
            this.alert_rule_dialog = false
            this.get_alert_rule_list()
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            })
            this.alert_rule_dialog = false
            this.get_alert_rule_list()
          })
      }
    },
    // 新增或者编辑告警子规则
    submit_alert_rule_children() {
      if (this.dialog_status === "create_alert_rule_children") {
        var post_data = Object.assign({}, this.alert_rule_children_form)
        post_data.match = JSON.stringify(
          this.$refs.label_handler.label_value_list
        )
        // console.log(post_data, '======')
        createAdJust(post_data)
          .then(resp => {
            this.$message({
              type: "success",
              message: "新增子规则成功"
            })
            this.alert_rule_children_dialog = false
          })
          .catch(err => {
            this.$message({
              type: "success",
              message: err
            })
            this.alert_rule_children_dialog = false
          })
      } else if (this.dialog_status === "update_alert_rule_children") {
        var update_data = Object.assign({}, this.alert_rule_children_form)
        update_data.match = JSON.stringify(
          this.$refs.label_handler.label_value_list
        )
        updateAdJustByID(update_data.id, update_data)
          .then(resp => {
            this.$message({
              type: "success",
              message: "更新子规则成功"
            })
            this.alert_rule_children_dialog = false
          })
          .catch(err => {
            this.$message({
              type: "success",
              message: err
            })
            this.alert_rule_children_dialog = false
          })
      }
    },
    // 删除告警规则
    delete_alert_rule(row) {
      deleteAlertRuleByID(row.id)
        .then(resp => {
          this.$message({
            type: "success",
            message: "删除规则成功"
          })
          this.get_alert_rule_list()
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
          this.get_alert_rule_list()
        })
    },
    // 删除告警子规则
    delete_alert_rule_children(row) {
      deleteAdJustByID(row.id)
        .then(resp => {
          this.$message({
            type: "success",
            message: "删除子规则成功"
          })
          this.get_alert_rule_list()
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
          this.get_alert_rule_list()
        })
    },
    // 获取告警规则列表
    get_alert_rule_list() {
      this.list_query.alert_rule_type = this.alert_rule_type
      getAlertRuleList(this.list_query)
        .then(resp => {
          this.alert_rule_list = resp.data.results.map(item => {
            item.children_rules = []
            return item
          })
          this.alert_rule_list_total = resp.data.count
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 获取告警子规则
    get_children_rules(row) {
      getAdJustList({ alert_rule__id: row.id })
        .then(resp => {
          row.children_rules = resp.data.results
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 告警路由相关--------------------------------------------------
    // 添加告警路由或者子路由
    add_alert_route(params, data) {
      this.alert_route_dialog = true
      if (params === "parent") {
        // 父路由
        this.dialog_status = "create_alert_route"
        this.alert_route_form.name = null
        this.alert_route_form.receiver = null
        this.alert_route_form.parent = 0
        this.$refs.label_handler.label_value_list = []
      } else {
        // 子路由
        this.dialog_status = "create_alert_route_children"
        this.alert_route_form.parent = params !== "parent" ? data.id : 0
        this.alert_route_form.name = null
        this.alert_route_form.receiver = null
        this.$refs.label_handler.label_value_list = []
      }
    },
    // 编辑告警路由
    edit_alert_route(row) {
      this.alert_route_dialog = true
      this.dialog_status = "update_alert_route"
      this.alert_route_form = Object.assign({}, row)
      this.alert_route_form.receiver = row.receiver
      this.alert_route_form.group_by = JSON.parse(row.group_by)
      this.$nextTick(() => {
        this.$refs.label_handler.label_value_list = JSON.parse(row.match).label
        this.alert_route_form.match_re = JSON.parse(row.match).match_re
      })
    },
    // 查看告警子路由
    view_alert_route_children(row) {
      const $table = this.$refs.alert_route_listRefs
      this.alert_route_list.map(item => {
        if (row.id !== item.id) {
          $table.toggleRowExpansion(item, false)
        }
      })
      $table.toggleRowExpansion(row)
    },
    // 编辑告警子路由
    edit_alert_route_children(row) {
      this.alert_route_dialog = true
      this.dialog_status = "update_alert_route_children"
      this.alert_route_form = Object.assign({}, row)
      this.alert_route_form.receiver = row.receiver
      this.alert_route_form.group_by = JSON.parse(row.group_by)
      // this.alert_route_form.group_wait = row.group_wait / 60
      this.$nextTick(() => {
        this.$refs.label_handler.label_value_list = JSON.parse(row.match).label
      })
    },
    // 删除告警子路由
    delete_alert_route_children(row) {
      deleteAlertRouteByID(row.id)
        .then(resp => {
          this.$message({
            type: "success",
            message: "删除子路由成功"
          })
          this.get_alert_route_list()
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
          this.get_alert_route_list()
        })
    },
    // 新增或者编辑告警路由或者子路由
    submit_alert_route() {
      if (
        this.dialog_status === "create_alert_route" ||
        this.dialog_status === "create_alert_route_children"
      ) {
        var create_data = Object.assign({}, this.alert_route_form)
        // create_data.receiver = Array.from(String(this.alert_route_form.receiver), Number)
        create_data.group_by = JSON.stringify(this.alert_route_form.group_by)
        // create_data.group_wait = create_data.group_wait * 60
        var param = {
          label: this.$refs.label_handler.label_value_list,
          match_re: this.alert_route_form.match_re
        }
        create_data.match = JSON.stringify(param)
        // console.log(create_data, '============')
        createAlertRoute(create_data)
          .then(resp => {
            this.$message({
              type: "success",
              message: "新增路由成功"
            })
            this.alert_route_dialog = false
            this.get_alert_route_list()
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            })
            this.alert_route_dialog = false
            this.get_alert_route_list()
          })
      } else if (
        this.dialog_status === "update_alert_route" ||
        this.dialog_status === "update_alert_route_children"
      ) {
        var update_data = Object.assign({}, this.alert_route_form)
        // update_data.receiver = Array.from(String(this.alert_route_form.receiver), Number)
        update_data.group_by = JSON.stringify(this.alert_route_form.group_by)
        // update_data.group_wait = update_data.group_wait * 60
        var update_param = {
          label: this.$refs.label_handler.label_value_list,
          match_re: this.alert_route_form.match_re
        }
        update_data.match = JSON.stringify(update_param)
        // console.log(update_data, '============')
        updateAlertRouteByID(update_data.id, update_data)
          .then(resp => {
            this.$message({
              type: "success",
              message: "更新路由成功"
            })
            this.alert_route_dialog = false
            this.get_alert_route_list()
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            })
            this.alert_route_dialog = false
            this.get_alert_route_list()
          })
      }
    },
    // 解析告警通知组
    parse_alert_group(reciver) {
      var data = []
      if (reciver) {
        data = this.alert_group_list
          .filter(item => {
            return reciver.indexOf(item.id)
          })
          .map(item => item.name)
          .join(",")
        return data
      }
      // console.log(data, '====')
    },
    // 删除告警路由
    delete_alert_route() {},
    // 获取告警路由列表
    get_alert_route_list() {
      this.list_query = {
        page: 1,
        limit: 15,
        product__id: this.$store.getters.current_select_product_id,
        parent: 0
      }
      getAlertRouteList(this.list_query)
        .then(resp => {
          this.alert_route_list = resp.data.results.map(item => {
            item.children_route = []
            return item
          })
          this.alert_route_list_total = resp.data.count
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 获取告警子路由
    get_children_route(row) {
      this.list_query = {
        page: 1,
        limit: 15,
        product__id: this.$store.getters.current_select_product_id,
        parent: row.id
      }
      getAlertRouteList(this.list_query)
        .then(resp => {
          row.children_route = resp.data.results
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 告警通知组相关--------------------------------------------------
    // 添加告警通知组
    add_alert_group() {
      this.alert_group_dialog = true
      this.dialog_status = "create_alert_group"
      if (this.$refs.alert_group_formRefs) {
        this.$refs.alert_group_formRefs.resetFields()
      }
      this.alert_group_form.name = null
      this.alert_group_form.users = null
      this.alert_group_form.webhook = null
    },
    // 编辑告警通知组
    edit_alert_group(row) {
      this.alert_group_dialog = true
      this.dialog_status = "update_alert_group"
      this.alert_group_form = Object.assign({}, row)
    },
    // 新增或者编辑告警通知组
    submit_alert_group() {
      if (this.dialog_status === "create_alert_group") {
        createAlertUserGroup(this.alert_group_form)
          .then(resp => {
            this.$message({
              type: "success",
              message: "新增通知组成功"
            })
            this.alert_group_dialog = false
            this.get_alert_group_list()
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            })
            this.alert_group_dialog = false
            this.get_alert_group_list()
          })
      } else if (this.dialog_status === "update_alert_group") {
        updateAlertUserGroupByID(
          this.alert_group_form.id,
          this.alert_group_form
        )
          .then(resp => {
            this.$message({
              type: "success",
              message: "更新通知组成功"
            })
            this.alert_group_dialog = false
            this.get_alert_group_list()
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            })
            this.alert_group_dialog = false
            this.get_alert_group_list()
          })
      }
    },
    // 删除告警通知组
    delete_alert_group(row) {
      deleteAlertUserGroupByID(row.id)
        .then(resp => {
          this.$message({
            type: "success",
            message: "删除用户组成功"
          })
          this.get_alert_group_list()
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
          this.get_alert_group_list()
        })
    },
    // 获取告警通知组列表
    get_alert_group_list() {
      getAlertUserGroupList(this.list_query)
        .then(resp => {
          this.alert_group_list = resp.data.results
          this.alert_group_list_total = resp.data.count
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 告警分组相关--------------------------------------------------
    add_group() {
      this.group_dialog = true
      this.dialog_status = "create_group"
      if (this.$refs.group_formRefs) {
        this.$refs.group_formRefs.resetFields()
      }
    },
    edit_group() {},
    submit_group() {},
    delete_group() {},
    get_group_list() {},
    // 告警回调--------------------------------------------------
    create_callback() {
      this.callback_dialog = true
      this.dialog_status = "create_callback"
      this.callback_form.name = null
      this.callback_form.robot = null
      this.callback_form.product = null
      this.callback_form.factory = null
    },
    update_callback(row) {
      this.callback_dialog = true
      this.dialog_status = "update_callback"
      this.callback_form = Object.assign({}, row)
    },
    submit_callback() {
      if (this.dialog_status === "create_callback") {
        createCallback(this.callback_form)
          .then(resp => {
            this.$message({
              type: "success",
              message: "新增成功"
            })
            this.callback_dialog = false
            this.get_callback_list()
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            })
            this.callback_dialog = false
            this.get_callback_list()
          })
      } else if (this.dialog_status === "update_callback") {
        updateCallbackByID(this.callback_form.id, this.callback_form)
          .then(resp => {
            this.$message({
              type: "success",
              message: "更新成功"
            })
            this.callback_dialog = false
            this.get_callback_list()
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            })
            this.callback_dialog = false
            this.get_callback_list()
          })
      }
    },
    delete_callback(row) {
      deleteCallbackByID(row.id)
        .then(resp => {
          this.$message({
            type: "success",
            message: "删除成功"
          })
          this.get_callback_list()
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
          this.get_callback_list()
        })
    },
    copy_cms_callback_info(row) {
      const callback_url =
        process.env.VUE_APP_CMS_CALLBACK + "?project=" + row.name
      this.$copyText(callback_url)
        .then(resp => {
          this.$message({
            type: "success",
            message: "复制成功"
          })
        })
        .catch(err => {
          this.$message({
            type: "danger",
            message: err
          })
        })
    },
    copy_event_callback_info(row) {
      const callback_url =
        process.env.VUE_APP_EVENT_CALLBACK + "?project=" + row.name
      this.$copyText(callback_url)
        .then(resp => {
          this.$message({
            type: "success",
            message: "复制成功"
          })
        })
        .catch(err => {
          this.$message({
            type: "danger",
            message: err
          })
        })
    },
    get_callback_list() {
      getCallbackList(this.list_query)
        .then(resp => {
          this.callback_list = resp.data.results
          this.callback_list_total = resp.data.count
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
          this.factory_list = resp.data.results
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
.el-button {
  vertical-align: top;
}
</style>
