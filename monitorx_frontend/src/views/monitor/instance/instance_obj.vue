实例对象页面

<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-tabs
        v-model="active_tab_name"
        @tab-click="active_tab_click"
      >
        <!-- 机器对象相关-------------------------------------------------- -->
        <el-tab-pane
          label="机器"
          name="machine_obj"
        >
          <div>
            <el-input
              v-model="input_content"
              placeholder="搜点啥"
              size="small"
              clearable
              @keyup.enter.native="search_machine"
            >
              <el-select
                slot="prepend"
                v-model="select_input"
                size="small"
              >
                <el-option
                  label="实例名称"
                  value="name"
                ></el-option>
                <el-option
                  label="实例ID"
                  value="endpoint"
                ></el-option>
                <el-option
                  label="内网IP"
                  value="private_ip"
                ></el-option>
                <el-option
                  label="外网IP"
                  value="public_ip"
                ></el-option>
              </el-select>
              <el-button
                slot="append"
                icon="el-icon-search"
                @click="search_machine"
              ></el-button>
            </el-input>
            <el-dropdown
              v-if="checkPermission(['admin','ops'])"
              style="margin-left: 10px;"
              @command="handle_batch_command"
            >
              <el-button
                type="primary"
                size="small"
              >
                更多菜单<i class="el-icon-arrow-down el-icon--right"></i>
              </el-button>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item
                  icon="el-icon-close-notification"
                  command="batch_disable_monitor"
                  style="color: #F56C6C;"
                >批量不监控</el-dropdown-item>
                <el-dropdown-item
                  icon="el-icon-guide"
                  command="batch_use_public"
                  style="color: #17A589"
                >批量用外网</el-dropdown-item>
                <el-dropdown-item
                  icon="el-icon-attract"
                  command="batch_mount_server"
                  style="color: #409EFF;"
                >挂载采集点</el-dropdown-item>
                <el-dropdown-item
                  icon="el-icon-upload"
                  command="create_instances"
                  style="color: #67C23A;"
                >批量录实例</el-dropdown-item>
                <el-dropdown-item
                  icon="el-icon-check"
                  command="batch_allocate_product"
                  style="color: #E6A23C;"
                >批量分产品</el-dropdown-item>
                <el-dropdown-item
                  icon="el-icon-download"
                  command="download_machine_list_table"
                  style="color: #909399;"
                >导出表数据</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
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
                        label="所属产品: "
                        prop="product__name"
                      >
                        <el-select
                          v-model="more_search_form.product__name"
                          placeholder="请选择产品"
                          size="small"
                          clearable
                        >
                          <el-option
                            v-for="(item) in product_list"
                            :key="item.id"
                            :label="item.name"
                            :value="item.name"
                          ></el-option>
                        </el-select>
                      </el-form-item>
                    </el-col>
                    <el-col :span="6">
                      <el-form-item
                        label="监控节点: "
                        prop="server_group__name"
                      >
                        <el-select
                          v-model="more_search_form.server_group__name"
                          placeholder="请选择监控节点"
                          size="small"
                          clearable
                        >
                          <el-option
                            v-for="(item) in server_group_list"
                            :key="item.id"
                            :label="item.name"
                            :value="item.name"
                          ></el-option>
                        </el-select>
                      </el-form-item>
                    </el-col>
                    <el-col :span="6">
                      <el-form-item
                        label="是否监控: "
                        prop="enable"
                      >
                        <el-select
                          v-model="more_search_form.enable"
                          placeholder="请选择状态"
                          size="small"
                          clearable
                        >
                          <el-option
                            label="是"
                            :value="1"
                          ></el-option>
                          <el-option
                            label="否"
                            :value="0"
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
                          style="vertical-align: middle;"
                          @click="more_search_submit"
                        ></el-button>
                      </el-form-item>
                    </el-col>
                  </el-row>
                </div>
              </el-collapse-transition>
            </el-form>
          </div>
          <el-table
            id="machine_list_table"
            ref="machine_list_table_refs"
            :data="machine_list"
            :row-key="get_row_key"
            size="small"
            border
            @selection-change="handleSelectionChange"
          >
            <el-table-column
              type="selection"
              width="55"
            ></el-table-column>
            <el-table-column
              label="实例名称"
              prop="name"
            ></el-table-column>
            <el-table-column
              label="Endpoint"
              prop="endpoint"
            ></el-table-column>
            <el-table-column
              label="内网IP"
              prop="private_ip"
            >
              <template slot-scope="scoped">
                <el-tag
                  v-if="scoped.row.use_public_ip == 0"
                  type="success"
                >{{ scoped.row.private_ip }}</el-tag>
                <span v-else> {{ scoped.row.private_ip }}</span>
              </template>
            </el-table-column>
            <el-table-column
              label="外网IP"
              prop="public_ip"
            >
              <template slot-scope="scoped">
                <el-tag
                  v-if="scoped.row.use_public_ip == 1"
                  type="success"
                >{{ scoped.row.public_ip }}</el-tag>
                <span v-else> {{ scoped.row.public_ip }}</span>
              </template>
            </el-table-column>
            <el-table-column
              label="所属产品"
              prop="product__name"
            ></el-table-column>
            <el-table-column
              label="监控节点"
              prop="server_group__name"
            >
              <template slot-scope="scoped">
                <el-tag
                  v-if="scoped.row.server_group__name !== undefined"
                  type="success"
                >{{ scoped.row.server_group__name }}</el-tag>
                <el-tag
                  v-else
                  type="danger"
                >
                  暂无挂载点</el-tag>
              </template>
            </el-table-column>
            <el-table-column
              label="是否监控"
              prop="enable"
            >
              <template slot-scope="scoped">
                <el-tag
                  v-if="scoped.row.enable==1"
                  type="success"
                >是</el-tag>
                <el-tag
                  v-else
                  type="danger"
                >否</el-tag>
              </template>
            </el-table-column>
            <el-table-column
              label="操作"
              prop="options"
              width="180px;"
            >
              <template slot-scope="scoped">
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="查看监控"
                  placement="top"
                >
                  <el-button
                    :disabled="scoped.row.enable == 0 || scoped.row.server_group == null"
                    type="success"
                    icon="el-icon-monitor"
                    size="mini"
                    @click="view_machine_chart(scoped.row)"
                  ></el-button>
                </el-tooltip>
                <el-button
                  v-if="checkPermission(['admin','ops'])"
                  type="primary"
                  icon="el-icon-edit"
                  size="mini"
                  @click="update_instance(scoped.row)"
                ></el-button>
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="查看标签"
                  placement="top"
                  style="margin-left: 10px;"
                >
                  <el-popover
                    placement="bottom-end"
                    width="100"
                    trigger="click"
                  >
                    <el-tag
                      v-for="item in scoped.row.labels"
                      :key="item.id"
                      size="small"
                      style="margin-top: 2px;"
                    >{{ item.name + '=' + item.value }}
                    </el-tag>
                    <el-button
                      slot="reference"
                      type="info"
                      size="mini"
                      icon="el-icon-price-tag"
                    ></el-button>
                  </el-popover>
                </el-tooltip>
              </template>
            </el-table-column>
          </el-table>
          <pagination
            v-show="machine_list_total>0"
            :total="machine_list_total"
            :page-sizes="[15, 30, 45, 50, 100, 200]"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_machine_list"
          >
          </pagination>
        </el-tab-pane>
        <!-- kubernetes对象-------------------------------------------------- -->
        <el-tab-pane
          label="Kubernetes"
          name="kubernetes_obj"
        >
          <div>
            <el-input
              v-model="k8s_input_content"
              placeholder="搜点啥"
              size="small"
              clearable
              @keyup.enter.native="search_k8s"
            >
              <el-select
                slot="prepend"
                v-model="k8s_select_input"
                size="small"
              >
                <el-option
                  label="集群名称"
                  value="name"
                ></el-option>
                <el-option
                  label="集群ID"
                  value="endpoint"
                ></el-option>
                <el-option
                  label="内网IP"
                  value="private_ip"
                ></el-option>
              </el-select>
              <el-button
                slot="append"
                icon="el-icon-search"
                @click="search_k8s"
              ></el-button>
            </el-input>
            <el-button
              icon="el-icon-circle-plus-outline"
              type="primary"
              size="small"
              style="margin-left: 10px;"
              @click="create_k8s"
            >添加集群</el-button>
          </div>
          <el-table
            ref="k8s_list_table_refs"
            :data="k8s_list"
            :row-key="get_row_key"
            size="small"
            border
          >
            <el-table-column
              type="selection"
              width="55"
            ></el-table-column>
            <el-table-column
              label="集群名称"
              prop="name"
            ></el-table-column>
            <el-table-column
              label="Endpoint"
              prop="endpoint"
            ></el-table-column>
            <el-table-column
              label="内网IP"
              prop="private_ip"
            ></el-table-column>
            <el-table-column
              label="所属产品"
              prop="product__name"
            ></el-table-column>
            <el-table-column
              label="监控节点"
              prop="server_group__name"
            >
              <template slot-scope="scoped">
                <el-tag
                  v-if="scoped.row.server_group__name !== undefined"
                  type="success"
                >{{ scoped.row.server_group__name }}</el-tag>
                <el-tag
                  v-else
                  type="danger"
                >
                  暂无挂载点</el-tag>
              </template>
            </el-table-column>
            <el-table-column
              label="是否监控"
              prop="enable"
            >
              <template slot-scope="scoped">
                <el-tag
                  v-if="scoped.row.enable==1"
                  type="success"
                >是</el-tag>
                <el-tag
                  v-else
                  type="danger"
                >否</el-tag>
              </template>
            </el-table-column>
            <el-table-column
              label="操作"
              prop="options"
              width="180px;"
            >
              <template slot-scope="scoped">
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="查看监控"
                  placement="top"
                >
                  <el-button
                    :disabled="scoped.row.enable == 0 || scoped.row.server_group == null"
                    type="success"
                    icon="el-icon-monitor"
                    size="mini"
                    @click="view_k8s_chart(scoped.row)"
                  ></el-button>
                </el-tooltip>
                <el-button
                  v-if="checkPermission(['admin','ops'])"
                  type="primary"
                  icon="el-icon-edit"
                  size="mini"
                  @click="update_k8s(scoped.row)"
                ></el-button>
                <el-popconfirm
                  v-if="checkPermission(['admin','ops'])"
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left:10px"
                  @confirm="delete_k8s(scoped.row)"
                  @cancel="cancel_delete"
                >
                  <el-button
                    slot="reference"
                    type="danger"
                    icon="el-icon-delete"
                    size="mini"
                  ></el-button>
                </el-popconfirm>
                <!-- <el-tooltip
                  class="item"
                  effect="dark"
                  content="查看标签"
                  placement="top"
                  style="margin-left: 10px;"
                >
                  <el-popover
                    placement="bottom-end"
                    width="100"
                    trigger="click"
                  >
                    <el-tag
                      v-for="item in scoped.row.labels"
                      :key="item.id"
                      size="small"
                      style="margin-top: 2px;"
                    >{{ item.name + '=' + item.value }}
                    </el-tag>
                    <el-button
                      slot="reference"
                      type="info"
                      size="mini"
                      icon="el-icon-price-tag"
                    ></el-button>
                  </el-popover>
                </el-tooltip> -->
              </template>
            </el-table-column>
          </el-table>
          <pagination
            v-show="k8s_list_total>0"
            :total="k8s_list_total"
            :page-sizes="[15, 30, 45, 50, 100, 200]"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_k8s_list"
          >
          </pagination>
        </el-tab-pane>
        <!-- 日志对象--------------------------------------------------  -->
        <!-- <el-tab-pane
          label="日志服务"
          name="sls_obj"
          disabled
        >
          <div>
            <el-input
              v-model="sls_name_content"
              placeholder="日志项目名称"
              size="small"
              suffix-icon="el-icon-search"
              clearable
              style="width: 300px;"
              @input="search_sls($event)"
            >
            </el-input>
            <el-button
              v-if="checkPermission(['admin','ops'])"
              type="primary"
              icon="el-icon-circle-plus-outline"
              size="small"
              style="margin-left: 10px;"
              @click="create_sls"
            >添加</el-button>
          </div>
          <el-table
            ref="sls_list_refs"
            :data="sls_list"
            size="small"
            border
          >
            <el-table-column
              label="项目名称"
              prop="project_name"
            ></el-table-column>
            <el-table-column
              label="项目描述"
              prop="desc"
            ></el-table-column>
            <el-table-column
              label="日志库"
              prop="logsearch"
            ></el-table-column>
            <el-table-column
              label="所属产品"
              prop="product__name"
            ></el-table-column>
            <el-table-column
              label="云账户"
              prop="factory__name"
            ></el-table-column>
            <el-table-column
              label="操作"
              width="180px;"
            >
              <template slot-scope="scoped">
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="查询日志"
                  placement="top"
                >
                  <el-button
                    :disabled="scoped.row.factory__name == null"
                    type="success"
                    icon="el-icon-data-analysis"
                    size="mini"
                    @click="view_sls(scoped.row)"
                  ></el-button>
                </el-tooltip>
                <el-button
                  v-if="checkPermission(['admin','ops'])"
                  type="primary"
                  icon="el-icon-edit"
                  size="mini"
                  @click="update_sls(scoped.row)"
                ></el-button>
                <el-popconfirm
                  v-if="checkPermission(['admin','ops'])"
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left:10px"
                  @confirm="delete_sls(scoped.row)"
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
            v-show="sls_list_total>0"
            :total="sls_list_total"
            :page-sizes="[15, 30, 45, 50, 100, 200]"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_sls_list"
          >
          </pagination>
        </el-tab-pane> -->
        <!-- MySQL对象-------------------------------------------------- -->
        <el-tab-pane
          label="MySQL"
          name="mysql_obj"
        >
          <div>
            <el-input
              v-model="input_content"
              placeholder="搜点啥"
              size="small"
              clearable
              @keyup.enter.native="search_mysql"
            >
              <el-select
                slot="prepend"
                v-model="select_input"
                size="small"
              >
                <el-option
                  label="实例名称"
                  value="name"
                ></el-option>
                <el-option
                  label="实例ID"
                  value="endpoint"
                ></el-option>
              </el-select>
              <el-button
                slot="append"
                icon="el-icon-search"
                @click="search_mysql"
              ></el-button>
            </el-input>
            <el-button
              v-if="checkPermission(['admin','ops'])"
              type="primary"
              icon="el-icon-circle-plus-outline"
              size="small"
              style="margin-left: 10px;"
              @click="allocate_product"
            >批量分产品</el-button>
          </div>
          <el-table
            id="mysql_list_table"
            ref="mysql_list_table_refs"
            :data="mysql_list"
            :row-key="get_row_key"
            size="small"
            border
            @selection-change="handleSelectionChange"
          >
            <el-table-column
              type="selection"
              width="55"
            ></el-table-column>
            <el-table-column
              label="实例名称"
              prop="name"
            ></el-table-column>
            <el-table-column
              label="Endpoint"
              prop="endpoint"
            ></el-table-column>
            <el-table-column
              label="所属产品"
              prop="product__name"
            ></el-table-column>
            <el-table-column
              label="操作"
              prop="options"
              width="80px;"
            >
              <template slot-scope="scoped">
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="查看监控"
                  placement="top"
                >
                  <el-button
                    :disabled="scoped.row.product == null"
                    type="success"
                    icon="el-icon-monitor"
                    size="mini"
                    @click="view_mysql_chart(scoped.row)"
                  ></el-button>
                </el-tooltip>
              </template>
            </el-table-column>
          </el-table>
          <pagination
            v-show="mysql_list_total>0"
            :total="mysql_list_total"
            :page-sizes="[15, 30, 45, 50, 100, 200]"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_mysql_list"
          >
          </pagination>
        </el-tab-pane>
        <!-- Redis对象-------------------------------------------------- -->
        <el-tab-pane
          label="Redis"
          name="redis_obj"
        >
          <div>
            <el-input
              v-model="input_content"
              placeholder="搜点啥"
              size="small"
              clearable
              @keyup.enter.native="search_redis"
            >
              <el-select
                slot="prepend"
                v-model="select_input"
                size="small"
              >
                <el-option
                  label="实例名称"
                  value="name"
                ></el-option>
                <el-option
                  label="实例ID"
                  value="endpoint"
                ></el-option>
              </el-select>
              <el-button
                slot="append"
                icon="el-icon-search"
                @click="search_redis"
              ></el-button>
            </el-input>
            <el-button
              v-if="checkPermission(['admin','ops'])"
              type="primary"
              icon="el-icon-circle-plus-outline"
              size="small"
              style="margin-left: 10px;"
              @click="allocate_product"
            >批量分产品</el-button>
          </div>
          <el-table
            id="redis_list_table"
            ref="redis_list_table_refs"
            :data="redis_list"
            :row-key="get_row_key"
            size="small"
            border
            @selection-change="handleSelectionChange"
          >
            <el-table-column
              type="selection"
              width="55"
            ></el-table-column>
            <el-table-column
              label="实例名称"
              prop="name"
            ></el-table-column>
            <el-table-column
              label="Endpoint"
              prop="endpoint"
            ></el-table-column>
            <el-table-column label="版本">
              <template slot-scope="scoped">
                <el-tag
                  v-if="scoped.row.instance_type__name === 'redis_cluster'"
                  type="primary"
                  size="small"
                >集群版</el-tag>
                <el-tag
                  v-else
                  size="small"
                >标准版</el-tag>
              </template>
            </el-table-column>
            <el-table-column
              label="所属产品"
              prop="product__name"
            ></el-table-column>
            <el-table-column
              label="操作"
              prop="options"
              width="80px;"
            >
              <template slot-scope="scoped">
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="查看监控"
                  placement="top"
                >
                  <el-button
                    :disabled="scoped.row.product == null"
                    type="success"
                    icon="el-icon-monitor"
                    size="mini"
                    @click="view_redis_chart(scoped.row)"
                  ></el-button>
                </el-tooltip>
              </template>
            </el-table-column>
          </el-table>
          <pagination
            v-show="redis_list_total>0"
            :total="redis_list_total"
            :page-sizes="[15, 30, 45, 50, 100, 200]"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_redis_list"
          >
          </pagination>
        </el-tab-pane>
        <!-- MongoDB对象-------------------------------------------------- -->
        <el-tab-pane
          label="MongoDB"
          name="mongodb_obj"
        >
          <div>
            <el-input
              v-model="input_content"
              placeholder="搜点啥"
              size="small"
              clearable
              @keyup.enter.native="search_mongo"
            >
              <el-select
                slot="prepend"
                v-model="select_input"
                size="small"
              >
                <el-option
                  label="实例名称"
                  value="name"
                ></el-option>
                <el-option
                  label="实例ID"
                  value="endpoint"
                ></el-option>
              </el-select>
              <el-button
                slot="append"
                icon="el-icon-search"
                @click="search_mongo"
              ></el-button>
            </el-input>
            <el-button
              v-if="checkPermission(['admin','ops'])"
              type="primary"
              icon="el-icon-circle-plus-outline"
              size="small"
              style="margin-left: 10px;"
              @click="allocate_product"
            >批量分产品</el-button>
          </div>
          <el-table
            id="mongodb_list_table"
            ref="mongodb_list_table_refs"
            :data="mongodb_list"
            :row-key="get_row_key"
            size="small"
            border
            @selection-change="handleSelectionChange"
          >
            <el-table-column
              type="selection"
              width="55"
            ></el-table-column>
            <el-table-column
              label="实例名称"
              prop="name"
            ></el-table-column>
            <el-table-column
              label="Endpoint"
              prop="endpoint"
            ></el-table-column>
            <el-table-column label="版本">
              <template slot-scope="scoped">
                <el-tag
                  v-if="scoped.row.instance_type__name === 'mongo_sharding'"
                  type="primary"
                  size="small"
                >分片</el-tag>
                <el-tag
                  v-else
                  size="small"
                >副本</el-tag>
              </template>
            </el-table-column>
            <el-table-column
              label="所属产品"
              prop="product__name"
            ></el-table-column>
            <el-table-column
              label="操作"
              prop="options"
              width="80px;"
            >
              <template slot-scope="scoped">
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="查看监控"
                  placement="top"
                >
                  <el-button
                    :disabled="scoped.row.product == null"
                    type="success"
                    icon="el-icon-monitor"
                    size="mini"
                    @click="view_mongodb_chart(scoped.row)"
                  ></el-button>
                </el-tooltip>
              </template>
            </el-table-column>
          </el-table>
          <pagination
            v-show="mongodb_list_total>0"
            :total="mongodb_list_total"
            :page-sizes="[15, 30, 45, 50, 100, 200]"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_mongodb_list"
          >
          </pagination>
        </el-tab-pane>
        <!-- PolarDB对象-------------------------------------------------- -->
        <!-- <el-tab-pane
          label="PolarDB"
          name="polardb_obj"
          disabled
        >
          <div>
            <el-button
              type="primary"
              icon="el-icon-circle-plus-outline"
              size="small"
              @click="allocate_product"
            >批量分产品</el-button>
          </div>
          <el-table
            id="polardb_list_table"
            ref="polardb_list_table_refs"
            :data="polardb_list"
            :row-key="get_row_key"
            size="small"
            border
            @selection-change="handleSelectionChange"
          >
            <el-table-column
              type="selection"
              width="55"
            ></el-table-column>
            <el-table-column
              label="实例名称"
              prop="name"
            ></el-table-column>
            <el-table-column
              label="Endpoint"
              prop="endpoint"
            ></el-table-column>
            <el-table-column
              label="所属产品"
              prop="product__name"
            ></el-table-column>
            <el-table-column
              label="操作"
              prop="options"
              width="80px;"
            >
              <template slot-scope="scoped">
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="查看监控"
                  placement="top"
                >
                  <el-button
                    :disabled="scoped.row.enable == 0 || scoped.row.server_group == null"
                    type="success"
                    icon="el-icon-monitor"
                    size="mini"
                    @click="view_polardb_chart(scoped.row)"
                  ></el-button>
                </el-tooltip>
              </template>
            </el-table-column>
          </el-table>
          <pagination
            v-show="polardb_list_total>0"
            :total="polardb_list_total"
            :page-sizes="[15, 30, 45, 50, 100, 200]"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_polardb_list"
          >
          </pagination>
        </el-tab-pane> -->
        <!-- 负载均衡对象-------------------------------------------------- -->
        <el-tab-pane
          label="负载均衡"
          name="slb_obj"
        >
          <div>
            <el-input
              v-model="input_content"
              placeholder="搜点啥"
              size="small"
              clearable
              @keyup.enter.native="search_slb"
            >
              <el-select
                slot="prepend"
                v-model="select_input"
                size="small"
              >
                <el-option
                  label="实例名称"
                  value="name"
                ></el-option>
                <el-option
                  label="实例ID"
                  value="endpoint"
                ></el-option>
              </el-select>
              <el-button
                slot="append"
                icon="el-icon-search"
                @click="search_slb"
              ></el-button>
            </el-input>
            <el-button
              v-if="checkPermission(['admin','ops'])"
              type="primary"
              icon="el-icon-circle-plus-outline"
              size="small"
              style="margin-left: 10px;"
              @click="allocate_product"
            >批量分产品</el-button>
          </div>
          <el-table
            :data="slb_list"
            border
            size="small"
          >
            <el-table-column
              type="selection"
              width="55"
            ></el-table-column>
            <el-table-column
              label="实例名称"
              prop="name"
            ></el-table-column>
            <el-table-column
              label="实例地址"
              prop="public_ip"
            ></el-table-column>
            <el-table-column
              label="Endpoint"
              prop="endpoint"
            ></el-table-column>
            <el-table-column
              label="所属产品"
              prop="product__name"
            ></el-table-column>
            <el-table-column
              label="操作"
              prop="options"
              width="80px;"
            >
              <template slot-scope="scoped">
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="查看监控"
                  placement="top"
                >
                  <!-- :disabled="scoped.row.product == null" -->
                  <el-button
                    type="success"
                    icon="el-icon-monitor"
                    size="mini"
                    @click="view_slb_chart(scoped.row)"
                  ></el-button>
                </el-tooltip>
              </template>
            </el-table-column>
          </el-table>
          <pagination
            v-show="slb_list_total>0"
            :total="slb_list_total"
            :page-sizes="[15, 30, 45, 50, 100, 200]"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_slb_list"
          >
          </pagination>
        </el-tab-pane>
        <!-- 域名对象-------------------------------------------------- -->
        <!-- <el-tab-pane
          label="域名"
          name="domain_obj"
          disabled
        >
          <div>
            <el-button
              type="primary"
              icon="el-icon-circle-plus-outline"
              size="small"
            >新增域名</el-button>
          </div>
          <el-table
            :data="domain_list"
            border
            size="small"
          >
            <el-table-column label="域名"></el-table-column>
            <el-table-column label="Endpoint"></el-table-column>
            <el-table-column label="所属产品"></el-table-column>
            <el-table-column label="监控节点"></el-table-column>
            <el-table-column label="是否监控"></el-table-column>
            <el-table-column label="操作"></el-table-column>
          </el-table>
        </el-tab-pane> -->
      </el-tabs>
    </el-card>

    <!-- 机器对象Dialog-------------------------------------------------- -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="instance_dialog"
      width="50%"
    >
      <el-form
        ref="instance_formRefs"
        :model="instance_form"
        label-width="100px"
      >
        <el-form-item
          label="是否监控"
          prop="enable"
        >
          <el-radio-group v-model="instance_form.enable">
            <el-radio :label="1">要监控</el-radio>
            <el-radio :label="0">不监控</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item
          label="监控方式"
          prop="use_public_ip"
        >
          <el-radio-group v-model="instance_form.use_public_ip">
            <el-radio :label="0">内网监控</el-radio>
            <el-radio :label="1">外网监控</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item
          label="采集点"
          prop="server_group"
        >
          <el-select
            v-model="instance_form.server_group"
            placeholder="请选择采集点"
            clearable
            size="small"
            style="width: 250px;"
          >
            <el-option
              v-for="(item) in server_group_list"
              :key="item.id"
              :label="item.name"
              :value="item.id"
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
          @click="instance_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_instance"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 批量不监控的Dialog-------------------------------------------------- -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="batch_disable_monitor_dialog"
      width="50%"
    >
      <el-form
        ref="batch_disable_monitor_formRefs"
        :model="batch_disable_monitor_form"
        label-width="100px"
      >
        <el-form-item
          label="是否监控"
          prop="enable"
        >
          <el-radio-group v-model="batch_disable_monitor_form.enable">
            <el-radio :label="1">要监控</el-radio>
            <el-radio :label="0">不监控</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="batch_disable_monitor_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_batch_disable_monitor"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 批量用外网的Dialog-------------------------------------------------- -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="batch_use_public_dialog"
      width="50%"
    >
      <el-form
        ref="batch_use_public_formRefs"
        :model="batch_use_public_form"
        label-width="100px"
      >
        <el-form-item
          label="是否外网"
          prop="use_public_ip"
        >
          <el-radio-group v-model="batch_use_public_form.use_public_ip">
            <el-radio :label="1">用外网</el-radio>
            <el-radio :label="0">用内网</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="batch_use_public_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_batch_use_public"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 批量挂载采集点的Dialog-------------------------------------------------- -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="batch_mount_server_dialog"
      width="50%"
    >
      <el-form
        ref="batch_mount_server_formRefs"
        :model="batch_mount_server_form"
        label-width="100px"
      >
        <el-form-item
          label="采集点"
          prop="server_group"
        >
          <el-select
            v-model="batch_mount_server_form.server_group"
            placeholder="请选择采集点"
            size="small"
            style="width: 250px;"
          >
            <el-option
              v-for="(item) in server_group_list"
              :key="item.id"
              :label="item.name"
              :value="item.id"
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
          @click="batch_mount_server_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_batch_mount_server"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 批量录入实例的Dialog-------------------------------------------------- -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="create_instance_dialog"
      width="50%"
    >
      <el-form
        ref="create_instance_formRefs"
        :model="create_instance_form"
        label-width="100px"
      >
        <el-form-item
          label="实例类型"
          prop="instance_type"
        >
          <el-select
            v-model="create_instance_form.instance_type"
            placeholder="请选择实例类型"
            size="small"
            style="width: 300px;"
          >
            <el-option
              v-for="(item) in instance_type_list"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          label="实例列表"
          prop="instance_list"
        >
          <el-input
            v-model="create_instance_form.instance_list"
            :rows="4"
            type="textarea"
            :placeholder="'格式：实例名称 实例Endpoint 实例IP地址\n例如：tsh-devops-qa-kongzz i-uf6afcl6fih9v56i9apu 10.10.10.10'"
            style="width: 500px;"
          ></el-input>
        </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="create_instance_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_create_instance"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 批量分配产品的Dialog-------------------------------------------------- -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="batch_allocate_product_dialog"
      width="50%"
    >
      <el-form
        ref="batch_allocate_product_formRefs"
        :model="batch_allocate_product_form"
        label-width="100px"
      >
        <el-form-item
          label="所属产品"
          prop="product"
        >
          <el-select
            v-model="batch_allocate_product_form.product"
            placeholder="请选择产品"
            size="small"
            style="width: 250px;"
          >
            <el-option
              v-for="(item) in product_list"
              :key="item.id"
              :label="item.name"
              :value="item.id"
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
          @click="batch_allocate_product_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_batch_allocate_product"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 负载均衡对象Dialog-------------------------------------------------- -->
    <!-- MySQL对象Dialog-------------------------------------------------- -->
    <!-- Redis对象Dialog-------------------------------------------------- -->
    <!-- MongoDB对象Dialog-------------------------------------------------- -->
    <!-- kubernetes对象Dialog-------------------------------------------------- -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="k8s_dialog"
      width="50%"
    >
      <el-form
        ref="k8s_formRefs"
        :model="k8s_form"
        :rules="k8s_form_rules"
        label-width="100px"
        size="small"
      >
        <el-form-item
          label="集群名称"
          prop="name"
        >
          <el-input
            v-model="k8s_form.name"
            placeholder="请输入集群名称"
            style="width: 300px;"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="Endpoint"
          prop="endpoint"
        >
          <el-input
            v-model="k8s_form.endpoint"
            placeholder="请输入集群ID"
            style="width: 300px;"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="入口IP"
          prop="private_ip"
        >
          <el-input
            v-model="k8s_form.private_ip"
            placeholder="请输入集群入口IP"
            style="width: 300px;"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="所属产品"
          prop="product"
        >
          <el-select
            v-model="k8s_form.product"
            placeholder="请选择产品"
            size="small"
            style="width: 300px;"
          >
            <el-option
              v-for="(item) in product_list"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          label="采集点"
          prop="server_group"
        >
          <el-select
            v-model="k8s_form.server_group"
            placeholder="请选择采集点"
            clearable
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
          label="实例类型"
          prop="instance_type"
        >
          <el-select
            v-model="k8s_form.instance_type"
            placeholder="请选择实例类型"
            size="small"
            style="width: 300px;"
          >
            <el-option
              v-for="(item) in instance_type_list"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          label="是否监控"
          prop="enable"
        >
          <el-radio-group v-model="k8s_form.enable">
            <el-radio :label="1">要监控</el-radio>
            <el-radio :label="0">不监控</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="k8s_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_k8s"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 日志服务对象dialog--------------------------------------------------  -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="sls_dialog"
      width="50%"
    >
      <el-form
        ref="sls_formRefs"
        :model="sls_form"
        :rules="sls_form_rules"
        label-width="100px"
        size="small"
      >
        <el-form-item
          label="项目"
          prop="project_name"
        >
          <el-input
            v-model="sls_form.project_name"
            placeholder=""
            style="width: 300px;"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="描述"
          prop="desc"
        >
          <el-input
            v-model="sls_form.desc"
            placeholder=""
            style="width: 300px;"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="日志库"
          prop="logsearch"
        >
          <el-input
            v-model="sls_form.logsearch"
            placeholder=""
            style="width: 300px;"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="所属产品"
          prop="product"
        >
          <el-select
            v-model="sls_form.product"
            placeholder="请选择产品"
            size="small"
            style="width: 300px;"
          >
            <el-option
              v-for="(item) in product_list"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          label="所属云厂"
          prop="factory"
        >
          <el-select
            v-model="sls_form.factory"
            placeholder="请选择产品"
            size="small"
            style="width: 300px;"
          >
            <el-option
              v-for="(item) in factory_list"
              :key="item.id"
              :label="item.name"
              :value="item.id"
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
          @click="sls_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_sls"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import FileSaver from "file-saver"
import XLSX from "xlsx"

import { mapGetters } from "vuex"
import { getProductList } from "@/api/product"
import { getFactoryList } from "@/api/factory"
import Pagination from "@/components/Pagination"
import { getServerGroupList } from "@/views/monitor/api/server_group"
import { getInstanceTypeList } from "@/views/monitor/api/instance_type"
import {
  getInstanceList,
  createInstance,
  updateInstanceByID,
  deleteInstanceByID
} from "@/views/monitor/api/instance"
import {
  getSLSList,
  createSLS,
  getSLSURL,
  updateSLSByID,
  deleteSLSByID
} from "@/views/monitor/api/sls"
import checkPermission from "@/utils/permission"
export default {
  name: "InstanceObj",
  components: {
    Pagination
  },
  data() {
    return {
      list_query: {
        page: 1,
        limit: 15,
        server_group__id: null
      },
      dialog_map: {
        update_instance: "编辑机器对象",
        batch_disable_monitor: "批量不监控",
        batch_use_public: "批量用外网",
        batch_mount_server: "批量挂载采集点",
        create_instances: "批量导入实例",
        allocate_product: "批量分配产品",
        create_k8s: "新增K8S集群",
        update_k8s: "编辑K8S集群",
        create_sls: "新增日志服务",
        update_sls: "编辑日志服务"
      },
      dialog_status: "",
      instance_type_list: [],
      instance_tag_dialog: false,
      // 机器对象相关--------------------------------------------------
      show_more_search: false,
      more_search_form: {
        product__name: null,
        server_group__name: null,
        enable: null
      },
      input_content: "",
      select_input: "name",
      active_tab_name: "machine_obj",
      machine_list: [],
      machine_list_total: 0,
      instance_dialog: false,
      instance_form: {
        id: "",
        enable: "",
        use_public_ip: "",
        server_group: null
      },
      product_list: [],
      factory_list: [],
      server_group_list: [],
      server_group_filter_list: [],
      batch_disable_monitor_dialog: false,
      batch_disable_monitor_form: {
        enable: 0
      },
      batch_use_public_dialog: false,
      batch_use_public_form: {
        use_public_ip: 0
      },
      batch_mount_server_dialog: false,
      batch_mount_server_form: {},
      create_instance_dialog: false,
      create_instance_form: {
        instance_list: null,
        instance_type: null
      },
      batch_allocate_product_dialog: false,
      batch_allocate_product_form: {},
      multi_selected_list: [],
      // 日志服务相关--------------------------------------------------
      sls_name_content: "",
      sls_list: [],
      sls_list_total: 0,
      sls_dialog: false,
      sls_form: {
        id: null,
        desc: null,
        project_name: null,
        logsearch: null,
        product: null
      },
      sls_form_rules: {
        project_name: [
          { required: true, message: "该项不能为空", trigger: "blur" }
        ],
        desc: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        logsearch: [
          { required: true, message: "该项不能为空", trigger: "blur" }
        ],
        product: [{ required: true, message: "该项不能为空", trigger: "blur" }]
      },
      // 负载均衡对象相关--------------------------------------------------
      slb_list: [],
      slb_list_total: 0,
      // MySQL对象相关--------------------------------------------------
      mysql_list: [],
      mysql_list_total: 0,
      // PolarDB 对象相关
      polardb_list: [],
      polardb_list_total: 0,
      // Redis对象相关--------------------------------------------------
      redis_list: [],
      redis_list_total: 0,
      // MongoDB对象相关--------------------------------------------------
      mongodb_list: [],
      mongodb_list_total: 0,
      // Kubernetes对象相关--------------------------------------------------
      k8s_input_content: "",
      k8s_select_input: "name",
      k8s_list: [],
      k8s_list_total: 0,
      k8s_dialog: false,
      k8s_form: {
        id: null,
        name: null,
        enable: 1,
        private_ip: null,
        endpoint: null,
        product: null,
        server_group: null,
        instance_type: null
      },
      k8s_form_rules: {
        name: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        private_ip: [
          { required: true, message: "该项不能为空", trigger: "blur" }
        ],
        endpoint: [
          { required: true, message: "该项不能为空", trigger: "blur" }
        ],
        product: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        server_group: [
          { required: true, message: "该项不能为空", trigger: "blur" }
        ],
        instance_type: [
          { required: true, message: "该项不能为空", trigger: "blur" }
        ]
      },
      // 域名对象相关--------------------------------------------------
      domain_list: []
    }
  },
  computed: {
    ...mapGetters(["current_select_product_id", "current_select_product_name"])
  },
  watch: {
    // 全局组件global-product选择变化时 自动刷新表格
    current_select_product_id: function() {
      this.get_k8s_list()
      this.get_machine_list()
    }
  },
  created() {
    this.list_query.server_group__id = this.$route.params.server_group__id
    this.instance_form.server_group = this.$route.params.server_group__id
    this.get_machine_list()
    this.get_product_list()
    this.get_server_group_list()
    this.get_instance_type_list()
  },
  methods: {
    checkPermission,
    // 标签页切换
    active_tab_click(tab) {
      if (tab.name === "machine_obj") {
        this.list_query.page = 1
        this.get_machine_list()
      } else if (tab.name === "slb_obj") {
        this.list_query.page = 1
        this.get_slb_list()
        //
      } else if (tab.name === "probe_obj") {
        this.list_query.page = 1
        //
      } else if (tab.name === "mysql_obj") {
        this.list_query.page = 1
        this.get_mysql_list()
        //
      } else if (tab.name === "redis_obj") {
        this.list_query.page = 1
        this.get_redis_list()
        //
      } else if (tab.name === "kubernetes_obj") {
        this.list_query.page = 1
        this.get_k8s_list()
      } else if (tab.name === "mongodb_obj") {
        this.list_query.page = 1
        this.get_mongodb_list()
      } else if (tab.name === "sls_obj") {
        this.get_sls_list()
      }
    },
    get_row_key(row) {
      return row.id
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
    // 获取采集组列表
    get_server_group_list() {
      getServerGroupList({ limit: 999 })
        .then(resp => {
          this.server_group_list = resp.data.results
          this.server_group_list.push({ id: -100, name: "暂无挂载点" })
          this.server_group_filter_list = []
          resp.data.results.map(item => {
            this.server_group_filter_list.push({
              text: item.name,
              value: item.name
            })
          })
          this.server_group_filter_list.push({
            text: "暂无挂载点",
            value: undefined
          })
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
      getProductList({ page: 1, limit: 999 })
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
    get_factory_list() {
      getFactoryList({ limit: 100 })
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
    // 机器对象相关--------------------------------------------------
    // 更多搜索
    more_search() {
      this.show_more_search = !this.show_more_search
      this.more_search_form.enable = null
      this.more_search_form.product__name = null
      this.more_search_form.server_group__name = null
    },
    more_search_submit() {
      // console.log(this.more_search_form, '====')
      this.list_query["enable"] = this.more_search_form.enable
      this.list_query["product__name"] = this.more_search_form.product__name
      this.list_query[
        "server_group__name"
      ] = this.more_search_form.server_group__name
      this.get_machine_list()
    },
    // 导出数据
    download_machine_list_table() {
      if (this.multi_selected_list.length <= 0) {
        this.$message({
          type: "error",
          message: "没有选择的人生是徒劳的"
        })
        return
      }
      this.machine_list = this.multi_selected_list
      var wb = XLSX.utils.table_to_book(
        document.querySelector("#machine_list_table")
      )
      var wbout = XLSX.write(wb, {
        bookType: "xlsx",
        bookSST: true,
        type: "array"
      })
      try {
        FileSaver.saveAs(
          new Blob([wbout], { type: "application/octet-stream" }),
          "machine_list_table.xlsx"
        )
      } catch (e) {
        if (typeof console !== "undefined") console.log(e, wbout)
      }
      return wbout
    },
    get_machine_list() {
      delete this.list_query["instance_type__name__contains"]

      const params = "product__id__in"
      this.list_query[params] = this.current_select_product_id
      // 如果是选择的产品是全部【0】就展示全部
      if (this.current_select_product_id === 0) {
        this.list_query[params] = ""
      } else {
        this.list_query[params] = this.current_select_product_id
      }
      const instance_type = "instance_type__name"
      this.list_query[instance_type] = "machine"
      getInstanceList(this.list_query)
        .then(resp => {
          this.machine_list = resp.data.results
          this.machine_list_total = resp.data.count
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 搜索机器实例
    search_machine() {
      // var params = this.select_input + "__contains"
      var params = ""
      if (this.select_input === "name") {
        params = this.select_input + "__contains"
      } else if (this.select_input === "private_ip") {
        params = this.select_input + "__in"
      }
      this.list_query.page = 1
      var _content = this.input_content.split(" ").join(",")
      // this.list_query[params] = this.input_content
      this.list_query[params] = _content
      this.get_machine_list()
    },
    // 打开机器实例监控图(Grafana)
    view_machine_chart(row) {
      // console.log(row)
      const grafana_url =
        process.env.VUE_APP_MACHINE +
        "var-datasource=" +
        row.server_group__name +
        "&var-endpoint=" +
        row.endpoint
      window.open(grafana_url, "_blank")
    },
    // 编辑机器实例
    update_instance(row) {
      this.instance_dialog = true
      this.dialog_status = "update_instance"
      this.instance_form = Object.assign({}, row)
    },
    // 编辑机器实例
    submit_instance() {
      updateInstanceByID(this.instance_form.id, this.instance_form)
        .then(resp => {
          this.$message({
            type: "success",
            message: "修改成功"
          })
          this.instance_dialog = false
          this.get_machine_list()
        })
        .catch(err => {
          this.$message.error(err)
          this.instance_dialog = false
          this.get_machine_list()
        })
    },
    handleSelectionChange(val) {
      this.multi_selected_list = val
    },
    handle_batch_command(command) {
      if (command === "batch_disable_monitor") {
        this.batch_disable_monitor()
      } else if (command === "batch_use_public") {
        this.batch_use_public()
      } else if (command === "batch_mount_server") {
        this.batch_mount_server()
      } else if (command === "create_instances") {
        this.create_instances()
      } else if (command === "batch_allocate_product") {
        this.allocate_product()
      } else if (command === "download_machine_list_table") {
        this.download_machine_list_table()
      }
    },
    // 批量不监控
    batch_disable_monitor() {
      if (this.multi_selected_list.length <= 0) {
        this.$message({
          type: "warning",
          message: "没有选择的人生是徒劳的"
        })
        return
      }
      this.batch_disable_monitor_dialog = true
      this.dialog_status = "batch_disable_monitor"
    },
    // 批量不监控
    submit_batch_disable_monitor() {
      for (let index = 0; index < this.multi_selected_list.length; index++) {
        updateInstanceByID(this.multi_selected_list[index].id, {
          enable: this.batch_disable_monitor_form.enable
        })
          .then(resp => {
            this.$message({
              type: "success",
              message: "修改成功"
            })
            this.batch_disable_monitor_dialog = false
            this.get_machine_list()
          })
          .catch(err => {
            this.$message.error(err)
            this.batch_disable_monitor_dialog = false
            this.get_machine_list()
          })
      }
    },
    // 批量用外网
    batch_use_public() {
      if (this.multi_selected_list.length <= 0) {
        this.$message({
          type: "warning",
          message: "没有选择的人生是徒劳的"
        })
        return
      }
      this.batch_use_public_dialog = true
      this.dialog_status = "batch_use_public"
    },
    // 批量不监控
    submit_batch_use_public() {
      for (let index = 0; index < this.multi_selected_list.length; index++) {
        updateInstanceByID(this.multi_selected_list[index].id, {
          use_public_ip: this.batch_use_public_form.use_public_ip
        })
          .then(resp => {
            this.$message({
              type: "success",
              message: "修改成功"
            })
            this.batch_use_public_dialog = false
            this.get_machine_list()
          })
          .catch(err => {
            this.$message.error(err)
            this.batch_use_public_dialog = false
            this.get_machine_list()
          })
      }
    },
    // 批量挂载实例到采集组
    batch_mount_server() {
      if (this.multi_selected_list.length <= 0) {
        this.$message({
          type: "warning",
          message: "没有选择的人生是徒劳的"
        })
        return
      }
      this.batch_mount_server_dialog = true
      this.dialog_status = "batch_mount_server"
    },
    // 批量挂载实例到采集组
    submit_batch_mount_server() {
      for (let index = 0; index < this.multi_selected_list.length; index++) {
        updateInstanceByID(this.multi_selected_list[index].id, {
          server_group: this.batch_mount_server_form.server_group
        })
          .then(resp => {
            this.$message({
              type: "success",
              message: "修改成功"
            })
            this.batch_mount_server_dialog = false
            this.get_machine_list()
          })
          .catch(err => {
            this.$message.error(err)
            this.batch_mount_server_dialog = false
            this.get_machine_list()
          })
      }
    },
    // 手动录入实例
    create_instances() {
      this.create_instance_dialog = true
      this.dialog_status = "create_instances"
    },
    // 手动录入实例
    submit_create_instance() {
      var instances = []
      for (var host of this.create_instance_form.instance_list
        .trim()
        .split("\n")) {
        var host_temp = host.split(/\s+/)
        instances.push({
          name: host_temp[0],
          endpoint: host_temp[1],
          private_ip: host_temp[2],
          instance_type: this.create_instance_form.instance_type
        })
      }
      for (let index = 0; index < instances.length; index++) {
        createInstance(instances[index])
          .then(resp => {
            this.$message({
              type: "success",
              message: "录入成功"
            })
            this.create_instance_dialog = false
            this.get_machine_list()
          })
          .catch(err => {
            this.$message.error(err)
            this.create_instance_dialog = false
            this.get_machine_list()
          })
      }
    },
    // 批量分配产品
    allocate_product() {
      if (this.multi_selected_list.length <= 0) {
        this.$message({
          type: "warning",
          message: "没有选择的人生是徒劳的"
        })
        return
      }
      this.batch_allocate_product_dialog = true
      this.dialog_status = "allocate_product"
    },
    // 批量分配产品
    submit_batch_allocate_product() {
      for (let index = 0; index < this.multi_selected_list.length; index++) {
        updateInstanceByID(this.multi_selected_list[index].id, {
          product: this.batch_allocate_product_form.product
        })
          .then(resp => {
            this.$message({
              type: "success",
              message: "修改成功"
            })
            this.batch_allocate_product_dialog = false
            this.get_machine_list()
          })
          .catch(err => {
            this.$message.error(err)
            this.batch_allocate_product_dialog = false
            this.get_machine_list()
          })
      }
    },
    // 负载均衡对象相关--------------------------------------------------
    search_slb() {
      var params = ""
      if (this.select_input === "name") {
        params = this.select_input + "__contains"
      } else if (this.select_input === "endpoint") {
        params = this.select_input + "__contains"
      }
      this.list_query[params] = this.input_content
      this.get_slb_list()
    },
    get_slb_list() {
      delete this.list_query["instance_type__name__contains"]
      const params = "product__id__in"
      this.list_query[params] = this.current_select_product_id
      // 如果是选择的产品是全部【0】就展示全部
      if (this.current_select_product_id === 0) {
        this.list_query[params] = ""
      } else {
        this.list_query[params] = this.current_select_product_id
      }
      const instance_type = "instance_type__name"
      this.list_query[instance_type] = "slb"
      getInstanceList(this.list_query)
        .then(resp => {
          this.slb_list = resp.data.results
          this.slb_list_total = resp.data.count
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 查看slb监控
    view_slb_chart(row) {
      const grafana_url =
        process.env.VUE_APP_SLB + "var-instanceName=" + row.name
      window.open(grafana_url, "_blank")
    },
    // MySQL对象相关--------------------------------------------------
    search_mysql() {
      var params = ""
      if (this.select_input === "name") {
        params = this.select_input + "__contains"
      } else if (this.select_input === "endpoint") {
        params = this.select_input + "__contains"
      }
      this.list_query[params] = this.input_content
      this.get_mysql_list()
    },
    get_mysql_list() {
      delete this.list_query["instance_type__name__contains"]
      const params = "product__id__in"
      this.list_query[params] = this.current_select_product_id
      // 如果是选择的产品是全部【0】就展示全部
      if (this.current_select_product_id === 0) {
        this.list_query[params] = ""
      } else {
        this.list_query[params] = this.current_select_product_id
      }
      const instance_type = "instance_type__name"
      this.list_query[instance_type] = "mysql"
      getInstanceList(this.list_query)
        .then(resp => {
          this.mysql_list = resp.data.results
          this.mysql_list_total = resp.data.count
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    get_polardb_list() {},
    view_mysql_chart(row) {
      const grafana_url =
        process.env.VUE_APP_MYSQL + "var-instanceName=" + row.name
      window.open(grafana_url, "_blank")
    },
    // PolarDB对象相关--------------------------------------------------
    view_polardb_chart() {},
    // Redis对象相关--------------------------------------------------
    search_redis() {
      var params = ""
      if (this.select_input === "name") {
        params = this.select_input + "__contains"
      } else if (this.select_input === "endpoint") {
        params = this.select_input + "__contains"
      }
      this.list_query[params] = this.input_content
      this.get_redis_list()
    },
    get_redis_list() {
      delete this.list_query["instance_type__name"]

      const params = "product__id__in"
      this.list_query[params] = this.current_select_product_id
      // 如果是选择的产品是全部【0】就展示全部
      if (this.current_select_product_id === 0) {
        this.list_query[params] = ""
      } else {
        this.list_query[params] = this.current_select_product_id
      }
      const instance_type = "instance_type__name__contains"
      this.list_query[instance_type] = "redis"
      getInstanceList(this.list_query)
        .then(resp => {
          this.redis_list = resp.data.results
          this.redis_list_total = resp.data.count
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    view_redis_chart(row) {
      // console.log(row, '======')
      if (row.instance_type__name === "redis_cluster") {
        const grafana_url =
          process.env.VUE_APP_REDIS_CLUSTER + "var-instanceName=" + row.name
        window.open(grafana_url, "_blank")
      } else if (row.instance_type__name === "redis_standard") {
        const grafana_url =
          process.env.VUE_APP_REDIS_STANDARD + "var-instanceName=" + row.name
        window.open(grafana_url, "_blank")
      }
    },
    // MongoDB对象相关--------------------------------------------------
    view_mongodb_chart(row) {
      if (row.instance_type__name === "mongo_replicate") {
        const grafana_url =
          process.env.VUE_APP_MONGO_REPL + "var-instanceName=" + row.name
        window.open(grafana_url, "_blank")
      }
    },
    // Kubernetes对象相关--------------------------------------------------
    search_k8s() {
      var params = this.k8s_select_input + "__contains"
      this.list_query.page = 1
      this.list_query[params] = this.k8s_input_content
      this.get_k8s_list()
    },
    create_k8s() {
      this.k8s_dialog = true
      this.dialog_status = "create_k8s"
      this.k8s_form.name = null
      this.k8s_form.private_ip = null
      this.k8s_form.endpoint = null
      this.k8s_form.product = null
      this.k8s_form.server_group = null
      this.k8s_form.instance_type = null
    },
    update_k8s(row) {
      this.k8s_dialog = true
      this.dialog_status = "update_k8s"
      this.k8s_form = Object.assign({}, row)
    },
    delete_k8s(row) {
      deleteInstanceByID(row.id)
        .then(resp => {
          this.$message({
            type: "success",
            message: "删除成功"
          })
          this.get_k8s_list()
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
          this.get_k8s_list()
        })
    },
    submit_k8s() {
      if (this.dialog_status === "create_k8s") {
        // console.log(this.k8s_form)
        createInstance(this.k8s_form)
          .then(resp => {
            this.$message({
              type: "success",
              message: "录入成功"
            })
            this.k8s_dialog = false
            this.get_k8s_list()
          })
          .catch(err => {
            this.$message.error(err)
            this.k8s_dialog = false
            this.get_k8s_list()
          })
      } else if (this.dialog_status === "update_k8s") {
        updateInstanceByID(this.k8s_form.id, this.k8s_form)
          .then(resp => {
            this.$message({
              type: "success",
              message: "修改成功"
            })
            this.k8s_dialog = false
            this.get_k8s_list()
          })
          .catch(err => {
            this.$message.error(err)
            this.k8s_dialog = false
            this.get_k8s_list()
          })
      }
    },
    view_k8s_chart(row) {
      const grafana_url =
        process.env.VUE_APP_KUBERNETES +
        "var-datasource=" +
        row.server_group__name +
        "&var-cluster_name=" +
        row.name
      window.open(grafana_url, "_blank")
    },
    get_k8s_list() {
      delete this.list_query["instance_type__name__contains"]
      const params = "product__id__in"
      this.list_query[params] = this.current_select_product_id
      // 如果是选择的产品是全部【0】就展示全部
      if (this.current_select_product_id === 0) {
        this.list_query[params] = ""
      } else {
        this.list_query[params] = this.current_select_product_id
      }
      const instance_type = "instance_type__name"
      this.list_query[instance_type] = "kubernetes"
      getInstanceList(this.list_query)
        .then(resp => {
          this.k8s_list = resp.data.results
          this.k8s_list_total = resp.data.count
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // MongoDB相关--------------------------------------------------
    search_mongo() {
      var params = ""
      if (this.select_input === "name") {
        params = this.select_input + "__contains"
      } else if (this.select_input === "endpoint") {
        params = this.select_input + "__contains"
      }
      this.list_query[params] = this.input_content
      this.get_mongodb_list()
    },
    get_mongodb_list() {
      delete this.list_query["instance_type__name"]
      delete this.list_query["instance_type__name__contains"]
      const params = "product__id__in"
      this.list_query[params] = this.current_select_product_id
      // 如果是选择的产品是全部【0】就展示全部
      if (this.current_select_product_id === 0) {
        this.list_query[params] = ""
      } else {
        this.list_query[params] = this.current_select_product_id
      }
      const instance_type = "instance_type__name__contains"
      this.list_query[instance_type] = "mongo"
      getInstanceList(this.list_query)
        .then(resp => {
          this.mongodb_list = resp.data.results
          this.mongodb_list_total = resp.data.count
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    // 日志服务相关--------------------------------------------------
    search_sls(row) {
      // console.log(row)
      var search_item = row.toLowerCase()
      var temp_data = []
      if (search_item !== "") {
        this.sls_list.filter(item => {
          if (item.logsearch.toLowerCase().indexOf(search_item) !== -1) {
            temp_data.push(item)
          }
        })
        this.sls_list = temp_data
        this.sls_list_total = temp_data.length
      } else {
        this.get_sls_list()
      }
    },
    get_sls_list() {
      delete this.list_query["instance_type__name__contains"]
      const params = "product__id__in"
      this.list_query[params] = this.current_select_product_id
      // 如果是选择的产品是全部【0】就展示全部
      if (this.current_select_product_id === 0) {
        this.list_query[params] = ""
      } else {
        this.list_query[params] = this.current_select_product_id
      }
      getSLSList(this.list_query)
        .then(resp => {
          this.sls_list = resp.data.results
          this.sls_list_total = resp.data.count
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    view_sls(row) {
      getSLSURL({
        project_name: row.project_name,
        logsearch: row.logsearch,
        factory: row.factory__name
      })
        .then(resp => {
          window.open(resp.data)
        })
        .catch(err => {
          this.$message.error(err)
        })
    },
    create_sls() {
      this.sls_dialog = true
      this.dialog_status = "create_sls"
      this.sls_form.project_name = null
      this.sls_form.logsearch = null
      this.sls_form.product = null
      this.get_product_list()
      this.get_factory_list()
    },
    update_sls(row) {
      this.sls_dialog = true
      this.dialog_status = "update_sls"
      this.sls_form = Object.assign({}, row)
      this.get_product_list()
      this.get_factory_list()
    },
    submit_sls() {
      if (this.dialog_status === "create_sls") {
        createSLS(this.sls_form)
          .then(resp => {
            this.$message({
              type: "success",
              message: "录入成功"
            })
            this.sls_dialog = false
            this.get_sls_list()
          })
          .catch(err => {
            this.$message.error(err)
            this.sls_dialog = false
            this.get_sls_list()
          })
      } else if (this.dialog_status === "update_sls") {
        updateSLSByID(this.sls_form.id, this.sls_form)
          .then(resp => {
            this.$message({
              type: "success",
              message: "更新成功"
            })
            this.sls_dialog = false
            this.get_sls_list()
          })
          .catch(err => {
            this.$message.error(err)
            this.sls_dialog = false
            this.get_sls_list()
          })
      }
    },
    delete_sls(row) {
      deleteSLSByID(row.id)
        .then(resp => {
          this.$message({
            type: "success",
            message: "删除成功"
          })
          this.sls_dialog = false
          this.get_sls_list()
        })
        .catch(err => {
          this.$message.error(err)
          this.sls_dialog = false
          this.get_sls_list()
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
.el-select {
  width: 120px;
}
.el-input {
  width: 400px;
}
.el-button {
  vertical-align: top;
}
.el-dropdown {
  vertical-align: top;
}
</style>
