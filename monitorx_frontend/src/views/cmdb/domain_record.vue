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
          v-model="input_content"
          placeholder="关键字"
          class="input-with-select"
          size="small"
          clearable
          style="width: 400px; margin-left: 10px"
        >
          <el-select
            slot="prepend"
            v-model="select_input"
            size="small"
            placeholder="请选择"
            style="width: 100px;"
          >
            <el-option
              label="子域名"
              value="subDomain"
            ></el-option>
            <el-option
              label="记录值"
              value="value"
            ></el-option>
          </el-select>
          <el-button
            slot="append"
            icon="el-icon-search"
            @click="search_handler"
          ></el-button>
        </el-input>
        <el-button
          v-if="checkPermission(['admin','ops'])"
          type="primary"
          size="small"
          icon="el-icon-circle-plus"
          style="margin-left: 10px"
          @click="create_record"
        >新增</el-button>
        <el-button
          type="info"
          size="small"
          style="margin-left: 10px"
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
                <el-col :span="4">
                  <el-form-item
                    label="证书状态: "
                    prop="certStatus"
                  >
                    <el-select
                      v-model="more_search_form.certStatus"
                      placeholder="选择状态"
                      size="small"
                      filterable
                      style="width: 200px"
                      @change="more_search_submit"
                    >
                      <el-option
                        label="正常"
                        value="Safe"
                      ></el-option>
                      <el-option
                        label="即将到期"
                        value="Expiring"
                      ></el-option>
                      <el-option
                        label="错误"
                        value="Wrong"
                      ></el-option>
                      <el-option
                        label="过期"
                        value="Expired"
                      ></el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>
            </div>
          </el-collapse-transition>
        </el-form>
      </div>
      <!-- 解析记录值列表 -->
      <!-- 阿里云解析 -->
      <el-table
        v-if="supplier==='ali'"
        :data="domain_record_list"
        size="small"
        style="width: 100%; margin-top: 10px"
        border
      >
        <el-table-column
          prop="rr"
          label="主机记录"
        >
        </el-table-column>
        <el-table-column
          prop="type"
          label="记录类型"
        >
        </el-table-column>
        <el-table-column
          prop="value"
          label="记录值"
        >
        </el-table-column>
        <el-table-column
          prop="line"
          label="线路"
        >
        </el-table-column>
        <el-table-column
          prop="weight"
          label="权重"
        >
        </el-table-column>
        <el-table-column
          prop="priority"
          label="MX"
        >
        </el-table-column>
        <el-table-column
          prop="status"
          label="解析状态"
        >
          <template slot-scope="scoped">
            <el-tag
              v-if="scoped.row.status === 'DISABLE'"
              type="warning"
            >暂停</el-tag>
            <el-tag
              v-if="scoped.row.status === 'ENABLE'"
              type="success"
            >启用</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="ttl"
          label="TTL(秒)"
        >
        </el-table-column>
        <el-table-column
          prop="remark"
          label="备注"
          show-overflow-tooltip
        >
        </el-table-column>
        <el-table-column
          prop="sslStatus"
          label="ssl状态"
        >
          <template slot-scope="scoped">
            <!-- <el-tag
              v-if="scoped.row.sslStatus === 0"
              type="warning"
            >停用</el-tag>
            <el-tag
              v-if="scoped.row.sslStatus === 1"
              type="success"
            >启用</el-tag> -->
            <i v-if="scoped.row.sslStatus === 0" slot="reference" class="el-icon-video-pause" style="color:orange; font-size:18px; margin-top: 12px;"></i>
            <i v-if="scoped.row.sslStatus === 1" slot="reference" class="el-icon-video-play" style="color:green; font-size:18px; margin-top: 12px;"></i>
          </template>
        </el-table-column>
        <el-table-column
          prop="certStatus"
          label="证书状态"
          :filters="[
            { text: '正常', value: 'Safe' },
            { text: '即将到期', value: 'Expiring' },
            { text: '错误', value: 'Wrong' },
            { text: '过期', value: 'Expired' },
          ]"
          :filter-method="filterHandler"
        >
          <template slot-scope="scoped">
            <el-tag
              v-if="scoped.row.certStatus === 'Wrong'"
              type="danger"
            >错误</el-tag>
            <el-tag
              v-if="scoped.row.certStatus === 'Expired'"
              type="danger"
            >过期</el-tag>
            <el-tag
              v-if="scoped.row.certStatus === 'Safe'"
              type="success"
            >正常</el-tag>
            <el-tag
              v-if="scoped.row.certStatus === 'Expiring'"
              type="warning"
            >即将到期</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="updatedOn"
          label="最后操作时间"
        >
        </el-table-column>
        <el-table-column
          prop="updatedBy"
          label="最后操作人"
        >
        </el-table-column>
        <el-table-column
          label="操作"
          width="240px"
        >
          <template slot-scope="{ row }">
            <el-popconfirm
              conirm-button-text="对的!"
              cancel-button-text="手滑, 算了!"
              icon="el-icon-info"
              icon-color="red"
              title="想好了一定要暂停解析吗?"
              @confirm="change_record_status(row, false)"
            >
              <el-button
                v-if="row.status==='ENABLE'&&checkPermission(['admin','ops'])"
                slot="reference"
                type="danger"
                size="mini"
                icon="el-icon-video-pause"
              ></el-button>
            </el-popconfirm>
            <el-popconfirm
              conirm-button-text="对的!"
              cancel-button-text="手滑, 算了!"
              icon="el-icon-info"
              icon-color="red"
              title="想好了一定要恢复解析吗?"
              @confirm="change_record_status(row, true)"
            >
              <el-button
                v-if="row.status==='DISABLE'&&checkPermission(['admin','ops'])"
                slot="reference"
                type="warning"
                size="mini"
                icon="el-icon-video-play"
              ></el-button>
            </el-popconfirm>
            <el-tooltip
              v-if="checkPermission(['admin','ops'])"
              class="item"
              effect="dark"
              content="修改记录"
              placement="top"
            >
              <el-button
                type="primary"
                icon="el-icon-edit"
                size="mini"
                style="margin-left: 10px"
                @click="edit_record(row, supplier)"
              ></el-button>
            </el-tooltip>
            <el-tooltip
              v-if="checkPermission(['admin','ops'])"
              class="item"
              effect="dark"
              content="修改权重"
              placement="top"
            >
              <el-button
                type="primary"
                icon="el-icon-setting"
                size="mini"
                @click="edit_ali_weight(row)"
              ></el-button>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>
      <!-- dnspod解析 -->
      <el-table
        v-if="supplier==='dnspod'"
        :data="domain_record_list"
        size="small"
        style="width: 100%; margin-top: 10px"
        border
      >
        <el-table-column
          prop="name"
          label="主机记录"
        >
        </el-table-column>
        <el-table-column
          prop="type"
          label="记录类型"
        >
        </el-table-column>
        <el-table-column
          prop="value"
          label="记录值"
        >
        </el-table-column>
        <el-table-column
          prop="line"
          label="线路"
        >
        </el-table-column>
        <el-table-column
          prop="mx"
          label="MX"
        >
        </el-table-column>
        <el-table-column
          prop="weight"
          label="权重"
        >
        </el-table-column>
        <el-table-column
          prop="status"
          label="解析状态"
        >
          <template slot-scope="scoped">
            <el-tag
              v-if="scoped.row.status === 'DISABLE'"
              type="warning"
            >暂停</el-tag>
            <el-tag
              v-if="scoped.row.status === 'ENABLE'"
              type="success"
            >启用</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="ttl"
          label="TTL(秒)"
        >
        </el-table-column>
        <el-table-column
          prop="remark"
          label="备注"
          show-overflow-tooltip
        >
        </el-table-column>
        <el-table-column
          prop="sslStatus"
          label="ssl状态"
        >
          <template slot-scope="scoped">
            <!-- <el-tag
              v-if="scoped.row.sslStatus === 0"
              type="warning"
            >停用</el-tag>
            <el-tag
              v-if="scoped.row.sslStatus === 1"
              type="success"
            >启用</el-tag> -->
            <i v-if="scoped.row.sslStatus === 0" slot="reference" class="el-icon-video-pause" style="color:orange; font-size:18px; margin-top: 12px;"></i>
            <i v-if="scoped.row.sslStatus === 1" slot="reference" class="el-icon-video-play" style="color:green; font-size:18px; margin-top: 12px;"></i>
          </template>
        </el-table-column>
        <el-table-column
          prop="certStatus"
          label="证书状态"
          :filters="[
            { text: '正常', value: 'Safe' },
            { text: '即将到期', value: 'Expiring' },
            { text: '错误', value: 'Wrong' },
            { text: '过期', value: 'Expired' },
          ]"
          :filter-method="filterHandler"
        >
          <template slot-scope="scoped">
            <el-tag
              v-if="scoped.row.certStatus === 'Wrong'"
              type="danger"
            >错误</el-tag>
            <el-tag
              v-if="scoped.row.certStatus === 'Expired'"
              type="danger"
            >过期</el-tag>
            <el-tag
              v-if="scoped.row.certStatus === 'Safe'"
              type="success"
            >正常</el-tag>
            <el-tag
              v-if="scoped.row.certStatus === 'Expiring'"
              type="warning"
            >即将到期</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="updatedOn"
          label="最后操作时间"
        >
        </el-table-column>
        <el-table-column
          prop="updatedBy"
          label="最后操作人"
        >
        </el-table-column>
        <el-table-column
          label="操作"
          width="120px"
        >
          <template slot-scope="{ row }">
            <el-popconfirm
              conirm-button-text="对的!"
              cancel-button-text="手滑, 算了!"
              icon="el-icon-info"
              icon-color="red"
              title="想好了一定要暂停解析吗?"
              @confirm="change_record_status(row, false)"
            >
              <el-button
                v-if="row.status==='ENABLE'&&checkPermission(['admin','ops'])"
                slot="reference"
                type="danger"
                size="mini"
                icon="el-icon-video-pause"
              ></el-button>
            </el-popconfirm>
            <el-popconfirm
              conirm-button-text="对的!"
              cancel-button-text="手滑, 算了!"
              icon="el-icon-info"
              icon-color="red"
              title="想好了一定要恢复解析吗?"
              @confirm="change_record_status(row, true)"
            >
              <el-button
                v-if="row.status==='DISABLE'&&checkPermission(['admin','ops'])"
                slot="reference"
                type="warning"
                size="mini"
                icon="el-icon-video-play"
              ></el-button>
            </el-popconfirm>
            <!-- <el-tooltip
              class="item"
              effect="dark"
              content="暂停解析"
              placement="top"
            >
              <el-button
                v-if="row.status==='ENABLE'"
                type="danger"
                icon="el-icon-video-pause"
                size="mini"
                @click="change_record_status(row, false)"
              ></el-button>
            </el-tooltip>
            <el-tooltip
              class="item"
              effect="dark"
              content="恢复解析"
              placement="top"
            >
              <el-button
                v-if="row.status==='DISABLE'"
                type="warning"
                icon="el-icon-video-play"
                size="mini"
                @click="change_record_status(row, true)"
              ></el-button> -->
            <!-- </el-tooltip> -->
            <el-tooltip
              v-if="checkPermission(['admin','ops'])"
              class="item"
              effect="dark"
              content="修改记录"
              placement="top"
            >
              <el-button
                type="primary"
                icon="el-icon-edit"
                size="mini"
                style="margin-left: 10px"
                @click="edit_record(row, supplier)"
              ></el-button>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>
      <!-- aws解析 -->
      <el-table
        v-if="supplier==='aws'"
        :data="domain_record_list"
        size="small"
        style="width: 100%; margin-top: 10px"
        border
      >
        <el-table-column
          prop="name"
          label="主机记录"
        >
        </el-table-column>
        <el-table-column
          prop="type"
          label="记录类型"
        >
        </el-table-column>
        <el-table-column
          prop="value"
          label="记录值"
        >
        </el-table-column>
        <el-table-column
          prop="ttl"
          label="TTL(秒)"
        >
        </el-table-column>
        <el-table-column
          prop="routingPolicy"
          label="路由策略"
          show-overflow-tooltip
        >
        </el-table-column>
        <el-table-column
          prop="differentiator"
          label="权重/角色/地区"
          show-overflow-tooltip
        >
        </el-table-column>
        <el-table-column
          prop="remark"
          label="备注"
          show-overflow-tooltip
        >
        </el-table-column>
        <el-table-column
          prop="sslStatus"
          label="ssl状态"
        >
          <template slot-scope="scoped">
            <!-- <el-tag
              v-if="scoped.row.sslStatus === 0"
              type="warning"
            >停用</el-tag>
            <el-tag
              v-if="scoped.row.sslStatus === 1"
              type="success"
            >启用</el-tag> -->
            <i v-if="scoped.row.sslStatus === 0" slot="reference" class="el-icon-video-pause" style="color:orange; font-size:18px; margin-top: 12px;"></i>
            <i v-if="scoped.row.sslStatus === 1" slot="reference" class="el-icon-video-play" style="color:green; font-size:18px; margin-top: 12px;"></i>
          </template>
        </el-table-column>
        <el-table-column
          prop="certStatus"
          label="证书状态"
          :filters="[
            { text: '正常', value: 'Safe' },
            { text: '即将到期', value: 'Expiring' },
            { text: '错误', value: 'Wrong' },
            { text: '过期', value: 'Expired' },
          ]"
          :filter-method="filterHandler"
        >
          <template slot-scope="scoped">
            <el-tag
              v-if="scoped.row.certStatus === 'Wrong'"
              type="danger"
            >错误</el-tag>
            <el-tag
              v-if="scoped.row.certStatus === 'Expired'"
              type="danger"
            >过期</el-tag>
            <el-tag
              v-if="scoped.row.certStatus === 'Safe'"
              type="success"
            >正常</el-tag>
            <el-tag
              v-if="scoped.row.certStatus === 'Expiring'"
              type="warning"
            >即将到期</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="updatedOn"
          label="最后操作时间"
        >
        </el-table-column>
        <el-table-column
          prop="updatedBy"
          label="最后操作人"
        >
        </el-table-column>
        <el-table-column
          label="操作"
          width="120px"
        >
          <template slot-scope="{ row }">
            <el-tooltip
              v-if="checkPermission(['admin','ops'])"
              class="item"
              effect="dark"
              content="修改记录"
              placement="top"
            >
              <el-button
                type="primary"
                icon="el-icon-edit"
                size="mini"
                @click="edit_record(row, supplier)"
              ></el-button>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>
      <!-- akamai解析 -->
      <el-table
        v-if="supplier==='akamai'"
        :data="domain_record_list"
        size="small"
        style="width: 100%; margin-top: 10px"
        border
      >
        <el-table-column
          prop="name"
          label="主机记录"
        >
        </el-table-column>
        <el-table-column
          prop="type"
          label="记录类型"
        >
        </el-table-column>
        <el-table-column
          prop="data"
          label="记录值"
        >
        </el-table-column>
        <el-table-column
          prop="ttl"
          label="TTL(秒)"
        >
        </el-table-column>
        <el-table-column
          prop="remark"
          label="备注"
          show-overflow-tooltip
        >
        </el-table-column>
        <el-table-column
          prop="sslStatus"
          label="ssl状态"
        >
          <template slot-scope="scoped">
            <!-- <el-tag
              v-if="scoped.row.sslStatus === 0"
              type="warning"
            >停用</el-tag>
            <el-tag
              v-if="scoped.row.sslStatus === 1"
              type="success"
            >启用</el-tag> -->
            <i v-if="scoped.row.sslStatus === 0" slot="reference" class="el-icon-video-pause" style="color:orange; font-size:18px; margin-top: 12px;"></i>
            <i v-if="scoped.row.sslStatus === 1" slot="reference" class="el-icon-video-play" style="color:green; font-size:18px; margin-top: 12px;"></i>
          </template>
        </el-table-column>
        <el-table-column
          prop="certStatus"
          label="证书状态"
          :filters="[
            { text: '正常', value: 'Safe' },
            { text: '即将到期', value: 'Expiring' },
            { text: '错误', value: 'Wrong' },
            { text: '过期', value: 'Expired' },
          ]"
          :filter-method="filterHandler"
        >
          <template slot-scope="scoped">
            <el-tag
              v-if="scoped.row.certStatus === 'Wrong'"
              type="danger"
            >错误</el-tag>
            <el-tag
              v-if="scoped.row.certStatus === 'Expired'"
              type="danger"
            >过期</el-tag>
            <el-tag
              v-if="scoped.row.certStatus === 'Safe'"
              type="success"
            >正常</el-tag>
            <el-tag
              v-if="scoped.row.certStatus === 'Expiring'"
              type="warning"
            >即将到期</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="updatedOn"
          label="最后操作时间"
        >
        </el-table-column>
        <el-table-column
          prop="updatedBy"
          label="最后操作人"
        >
        </el-table-column>
        <el-table-column
          label="操作"
          width="120px"
        >
          <template slot-scope="{ row }">
            <el-tooltip
              v-if="checkPermission(['admin','ops'])"
              class="item"
              effect="dark"
              content="修改记录"
              placement="top"
            >
              <el-button
                type="primary"
                icon="el-icon-edit"
                size="mini"
                @click="edit_record(row, supplier)"
              ></el-button>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>
      <!-- 分页 -->
      <pagination
        v-show="domain_record_total>0"
        :total="domain_record_total"
        :page.sync="listQuery.page"
        :limit.sync="listQuery.limit"
        @pagination="get_domain_record_list"
      ></pagination>
    </el-card>
    <!-- 修改akamai解析的Dialog -->
    <el-dialog
      v-if="supplier==='akamai'"
      title="修改解析"
      :visible.sync="editRecordDialogFormVisible"
      width="50%"
    >
      <el-form
        :model="record_edit_form"
        label-width="100px"
      >
        <el-form-item
          label="主机记录"
          style="width:600px"
          prop="name"
        >
          <el-input
            v-model="record_edit_form.subDomain"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="记录值"
          style="width:600px"
          prop="value"
        >
          <el-input
            v-model="record_edit_form.value"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="TTL(秒)"
          style="width:300px"
          prop="ttl"
        >
          <el-input
            v-model.number="record_edit_form.ttl"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="记录类型"
          style="width:300px"
          prop="type"
        >
          <el-select
            v-model="record_edit_form.recordType"
            size="small"
          >
            <el-option
              label="A"
              value="A"
            ></el-option>
            <el-option
              label="AAAA"
              value="AAAA"
            ></el-option>
            <el-option
              label="CNAME"
              value="CNAME"
            ></el-option>
            <el-option
              label="TXT"
              value="TXT"
            ></el-option>
            <el-option
              label="MX"
              value="MX"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          label="备注"
          style="width:600px"
          prop="remark"
        >
          <el-input
            v-model="record_edit_form.remark"
            size="small"
          ></el-input>
        </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="editRecordDialogFormVisible = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_edit_record"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 修改aws解析的Dialog -->
    <el-dialog
      v-if="supplier==='aws'"
      title="修改解析"
      :visible.sync="editRecordDialogFormVisible"
      width="50%"
    >
      <el-form
        :model="record_edit_form"
        label-width="120px"
      >
        <el-form-item
          label="主机记录"
          style="width:600px"
          prop="name"
        >
          <el-input
            v-model="record_edit_form.subDomain"
            size="small"
            disabled
          ></el-input>
        </el-form-item>
        <el-form-item
          label="Alias"
          style="width:600px"
          prop="alias"
        >
          <el-switch
            v-model="record_edit_form.awsAlias"
            active-color="#13ce66"
            inactive-color="#ff4949"
          >
          </el-switch>
        </el-form-item>
        <el-form-item
          v-if="record_edit_form.awsAlias===false"
          label="记录值"
          style="width:600px"
          prop="value"
        >
          <el-input
            v-model="record_edit_form.value"
            size="small"
          ></el-input>
          <i v-if="record_edit_form.recordType === 'TXT'" style="color:red;">记得加引号!!</i>
        </el-form-item>
        <el-form-item
          v-if="record_edit_form.awsAlias===true"
          label="目标区域"
          style="width:600px"
          prop="value"
        >
          <el-select
            v-model="target_region"
            size="small"
            clearable
            filterable
            style="width: 300px"
            @change="search_lb($event)"
          >
            <el-option
              v-for="item in aws_region_list_all"
              :key="item.name"
              :label="item.name"
              :value="item.name"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          v-if="record_edit_form.awsAlias===true"
          label="目标LB"
          style="width:600px"
          prop="value"
        >
          <el-select
            v-model="record_edit_form.value"
            size="small"
            clearable
            filterable
            style="width: 300px"
            @change="set_edit_target_lb($event)"
          >
            <el-option
              v-for="item in aws_lb_list"
              :key="item.DnsName"
              :label="item.DnsName"
              :value="{DnsName: item.DnsName, HostedZoneId: item.HostedZoneId}"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          label="TTL(秒)"
          style="width:300px"
          prop="ttl"
        >
          <el-input
            v-model.number="record_edit_form.ttl"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="记录类型"
          style="width:300px"
          prop="type"
        >
          <el-select
            v-model="record_edit_form.recordType"
            size="small"
          >
            <el-option
              label="A"
              value="A"
            ></el-option>
            <el-option
              label="AAAA"
              value="AAAA"
            ></el-option>
            <el-option
              label="CNAME"
              value="CNAME"
            ></el-option>
            <el-option
              label="TXT"
              value="TXT"
            ></el-option>
            <el-option
              label="MX"
              value="MX"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          label="备注"
          style="width:600px"
          prop="remark"
        >
          <el-input
            v-model="record_edit_form.remark"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item

          label="路由策略"
          style="width:300px"
          prop="routingPolicy"
        >
          <el-select
            v-model="record_edit_form.awsRoutingPolicy"
            size="small"
            @change="record_edit_form.awsDifferentiator=''"
          >
            <el-option
              label="Simple"
              value="Simple"
            ></el-option>
            <el-option
              label="Weighted"
              value="Weighted"
            ></el-option>
            <!-- <el-option
              label="Failover"
              value="Failover"
            ></el-option> -->
            <el-option
              label="Geolocation"
              value="Geolocation"
            ></el-option>
          </el-select>
        </el-form-item>
        <!-- <el-form-item
          label="路由策略"
          style="width:300px"
          prop="routingPolicy"
        >
          <el-select
            v-model="record_edit_form.awsRoutingPolicy"
            size="small"
            disabled
          >
          </el-select>
        </el-form-item> -->
        <el-form-item
          v-if="record_edit_form.awsRoutingPolicy==='Geolocation'"
          label="地区"
          style="width:300px"
          prop="differentiator"
        >
          <el-select
            v-model="record_edit_form.awsDifferentiator"
            size="small"
          >
            <el-option
              label="Default"
              value="Default"
            ></el-option>
            <el-option
              label="China"
              value="China"
            ></el-option>
          </el-select>
        </el-form-item>
        <!-- <el-form-item
          v-if="record_edit_form.awsRoutingPolicy==='Failover'"
          label="角色"
          style="width:300px"
          prop="differentiator"
        >
          <el-select
            v-model="record_edit_form.awsDifferentiator"
            size="small"
          >
            <el-option
              label="Primary"
              value="Primary"
            ></el-option>
            <el-option
              label="Secondary"
              value="Secondary"
            ></el-option>
          </el-select>
        </el-form-item> -->
        <el-form-item
          v-if="record_edit_form.awsRoutingPolicy==='Weighted'"
          label="权重"
          style="width:300px"
          prop="differentiator"
        >
          <el-input
            v-model="record_edit_form.awsDifferentiator"
            size="small"
          >
          </el-input>
        </el-form-item>
        <el-form-item
          v-if="record_edit_form.awsRoutingPolicy!=='Simple' && supplier === 'aws'"
          label="线路标识"
          style="width:300px"
          prop="identifier"
        >
          <el-input
            v-model="record_edit_form.awsIdentifier"
            size="small"
          >
          </el-input>
        </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="editRecordDialogFormVisible = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_edit_record"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 修改dnspod解析的Dialog -->
    <el-dialog
      v-if="supplier==='dnspod'"
      title="修改解析"
      :visible.sync="editRecordDialogFormVisible"
      width="50%"
    >
      <el-form
        :model="record_edit_form"
        label-width="100px"
      >
        <el-form-item
          label="主机记录"
          style="width:600px"
          prop="name"
        >
          <el-input
            v-model="record_edit_form.subDomain"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="记录值"
          style="width:600px"
          prop="value"
        >
          <el-input
            v-model="record_edit_form.value"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="线路"
          style="width:600px"
          prop="line"
        >
          <el-select
            v-model="record_edit_form.recordLine"
            size="small"
            clearable
            filterable
            style="width: 300px"
            @change="search_line($event)"
          >
            <el-option
              v-for="item in domain_line_list"
              :key="item.line"
              :label="item.line"
              :value="item.line"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          label="TTL(秒)"
          style="width:300px"
          prop="ttl"
        >
          <el-input
            v-model.number="record_edit_form.ttl"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="权重"
          style="width:300px"
          prop="weight"
        >
          <el-input
            v-model="record_edit_form.weight"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="记录类型"
          style="width:300px"
          prop="type"
        >
          <el-select
            v-model="record_edit_form.recordType"
            size="small"
          >
            <el-option
              label="A"
              value="A"
            ></el-option>
            <el-option
              label="AAAA"
              value="AAAA"
            ></el-option>
            <el-option
              label="CNAME"
              value="CNAME"
            ></el-option>
            <el-option
              label="TXT"
              value="TXT"
            ></el-option>
            <el-option
              label="MX"
              value="MX"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          v-if="record_edit_form.recordType==='MX'"
          label="MX"
          style="width:300px"
          prop="mx"
        >
          <el-input
            v-model.number="record_edit_form.mx"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="备注"
          style="width:600px"
          prop="remark"
        >
          <el-input
            v-model="record_edit_form.remark"
            size="small"
          ></el-input>
        </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="editRecordDialogFormVisible = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_edit_record"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 修改ali解析的Dialog -->
    <el-dialog
      v-if="supplier==='ali'"
      title="修改解析"
      :visible.sync="editRecordDialogFormVisible"
      width="50%"
    >
      <el-form
        :model="record_edit_form"
        label-width="100px"
      >
        <el-form-item
          label="主机记录"
          style="width:600px"
          prop="rr"
        >
          <el-input
            v-model="record_edit_form.subDomain"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="记录值"
          style="width:600px"
          prop="value"
        >
          <el-input
            v-model="record_edit_form.value"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="线路"
          style="width:600px"
          prop="line"
        >
          <el-select
            v-model="record_edit_form.recordLine"
            size="small"
            clearable
            filterable
            style="width: 300px"
            @change="search_line($event)"
          >
            <el-option
              v-for="item in domain_line_list"
              :key="item.line"
              :label="item.lineName"
              :value="item.line"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          label="TTL(秒)"
          style="width:300px"
          prop="ttl"
        >
          <el-input
            v-model.number="record_edit_form.ttl"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="记录类型"
          style="width:300px"
          prop="type"
        >
          <el-select
            v-model="record_edit_form.recordType"
            size="small"
          >
            <el-option
              label="A"
              value="A"
            ></el-option>
            <el-option
              label="AAAA"
              value="AAAA"
            ></el-option>
            <el-option
              label="CNAME"
              value="CNAME"
            ></el-option>
            <el-option
              label="TXT"
              value="TXT"
            ></el-option>
            <el-option
              label="MX"
              value="MX"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          v-if="record_edit_form.recordType==='MX'"
          label="MX"
          style="width:300px"
          prop="mx"
        >
          <el-input
            v-model.number="record_edit_form.mx"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="备注"
          style="width:600px"
          prop="remark"
        >
          <el-input
            v-model="record_edit_form.remark"
            size="small"
          ></el-input>
        </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="editRecordDialogFormVisible = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_edit_record"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 修改ali权重的Dialog -->
    <el-dialog
      title="修改权重"
      :visible.sync="editAliRecordWeightDialogFormVisible"
      width="50%"
    >
      <el-form
        :model="record_edit_form"
        label-width="100px"
      >
        <el-form-item
          label="主机记录"
          style="width:50px"
          prop="rr"
        >
          <el-input
            v-model="record_edit_form.subDomain"
            :disabled="true"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="记录值"
          style="width:50px"
          prop="value"
        >
          <el-input
            v-model="record_edit_form.value"
            :disabled="true"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="权重"
          style="width:50px"
          prop="weight"
        >
          <el-input
            v-model="record_edit_form.weight"
            size="small"
          ></el-input>
        </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="editAliRecordWeightDialogFormVisible = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_ali_weight"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 创建解析的Dialog -->
    <el-dialog
      title="新增解析"
      :visible.sync="createRecordDialogFormVisible"
      width="50%"
    >
      <el-form
        ref="record_create_formRefs"
        :model="record_create_form"
        label-width="100px"
      >
        <el-form-item
          label="主机记录"
          style="width:300px"
          prop="subDomain"
        >
          <el-input
            v-model="record_create_form.subDomain"
            placeholder="勿填写主域名"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          v-if="supplier === 'aws'"
          label="Alias"
          style="width:600px"
          prop="alias"
        >
          <el-switch
            v-model="record_create_form.awsAlias"
            active-color="#13ce66"
            inactive-color="#ff4949"
          >
          </el-switch>
        </el-form-item>
        <el-form-item
          v-if="record_create_form.awsAlias===false"
          label="记录值"
          style="width:300px"
          prop="value"
        >
          <el-input
            v-model="record_create_form.value"
            :placeholder="getPlaceholder"
            size="small"
          ></el-input>
          <i v-if="record_create_form.recordType === 'TXT'" style="color:red;">记得加引号!!</i>
        </el-form-item>
        <el-form-item
          v-if="record_create_form.awsAlias===true"
          label="目标区域"
          style="width:600px"
          prop="value"
        >
          <el-select
            v-model="target_region"
            size="small"
            clearable
            filterable
            style="width: 300px"
            @change="search_lb($event)"
          >
            <el-option
              v-for="item in aws_region_list_all"
              :key="item.name"
              :label="item.name"
              :value="item.name"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          v-if="record_create_form.awsAlias===true"
          label="目标LB"
          style="width:600px"
          prop="value"
        >
          <el-select
            v-model="record_create_form.value"
            size="small"
            clearable
            filterable
            style="width: 300px"
            @change="set_create_target_lb($event)"
          >
            <el-option
              v-for="item in aws_lb_list"
              :key="item.DnsName"
              :label="item.DnsName"
              :value="{DnsName: item.DnsName, HostedZoneId: item.HostedZoneId}"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          v-if="supplier === 'dnspod'"
          label="线路"
          style="width:600px"
          prop="recordLine"
        >
          <el-select
            v-model="record_create_form.recordLine"
            size="small"
            clearable
            filterable
            style="width: 300px"
            @change="search_line($event)"
          >
            <el-option
              v-for="item in domain_line_list"
              :key="item.line"
              :label="item.line"
              :value="item.line"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          v-if="supplier === 'ali'"
          label="线路"
          style="width:600px"
          prop="recordLine"
        >
          <el-select
            v-model="record_create_form.recordLine"
            size="small"
            clearable
            filterable
            style="width: 300px"
            @change="search_line($event)"
          >
            <el-option
              v-for="item in domain_line_list"
              :key="item.line"
              :label="item.lineName"
              :value="item.line"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          label="TTL(秒)"
          style="width:300px"
          prop="ttl"
        >
          <el-input
            v-model.number="record_create_form.ttl"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          v-if="supplier === 'dnspod'"
          label="权重"
          style="width:300px"
          prop="weight"
        >
          <el-input
            v-model="record_create_form.weight"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="记录类型"
          style="width:300px"
          prop="recordType"
        >
          <el-select
            v-model="record_create_form.recordType"
            size="small"
          >
            <el-option
              label="A"
              value="A"
            ></el-option>
            <el-option
              label="AAAA"
              value="AAAA"
            ></el-option>
            <el-option
              label="CNAME"
              value="CNAME"
            ></el-option>
            <el-option
              label="TXT"
              value="TXT"
            ></el-option>
            <el-option
              label="MX"
              value="MX"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          v-if="record_create_form.recordType==='MX' && (supplier === 'ali' || supplier === 'dnspod')"
          label="MX"
          style="width:300px"
          prop="mx"
        >
          <el-input
            v-model.number="record_create_form.mx"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          v-if="supplier === 'aws'"
          label="路由策略"
          style="width:300px"
          prop="routingPolicy"
        >
          <el-select
            v-model="record_create_form.awsRoutingPolicy"
            size="small"
            @change="record_create_form.awsDifferentiator=''"
          >
            <el-option
              label="Simple"
              value="Simple"
            ></el-option>
            <el-option
              label="Weighted"
              value="Weighted"
            ></el-option>
            <!-- <el-option
              label="Failover"
              value="Failover"
            ></el-option> -->
            <el-option
              label="Geolocation"
              value="Geolocation"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          v-if="record_create_form.awsRoutingPolicy==='Geolocation' && supplier === 'aws'"
          label="地区"
          style="width:300px"
          prop="differentiator"
        >
          <el-select
            v-model="record_create_form.awsDifferentiator"
            size="small"
          >
            <el-option
              label="Default"
              value="Default"
            ></el-option>
            <el-option
              label="China"
              value="China"
            ></el-option>
          </el-select>
        </el-form-item>
        <!-- <el-form-item
          v-if="record_create_form.awsRoutingPolicy==='Failover' && supplier === 'aws'"
          label="角色"
          style="width:300px"
          prop="differentiator"
        >
          <el-select
            v-model="record_create_form.awsDifferentiator"
            size="small"
          >
            <el-option
              label="Primary"
              value="Primary"
            ></el-option>
            <el-option
              label="Secondary"
              value="Secondary"
            ></el-option>
          </el-select>
        </el-form-item> -->
        <el-form-item
          v-if="record_create_form.awsRoutingPolicy==='Weighted' && supplier === 'aws'"
          label="权重"
          style="width:300px"
          prop="differentiator"
        >
          <el-input
            v-model="record_create_form.awsDifferentiator"
            size="small"
          >
          </el-input>
        </el-form-item>
        <el-form-item
          v-if="record_create_form.awsRoutingPolicy!=='Simple' && supplier === 'aws'"
          label="线路标识"
          style="width:300px"
          prop="identifier"
        >
          <el-input
            v-model="record_create_form.awsIdentifier"
            size="small"
          >
          </el-input>
        </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="reset_record_create_form"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_create_record"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import { getDomainRecordList, updateDomainRecord, updateDomainRecordStatus, addDomainRecord, getDomainLineList, updateAliWeight, getAwsLb } from '@/views/cmdb/api/domain_record'
import { getRegionList } from '@/views/cmdb/api/region'
import checkPermission from "@/utils/permission"
export default {
  name: "DomainRecord",
  components: { Pagination },
  data() {
    return {
      awsRegionQuery: {
        limit: 999,
        factory__name: "亚马逊"
      },
      listQuery: {
        page: 1,
        limit: 15,
        domain: JSON.parse(this.$route.query.domain_info).domain
      },
      awsLbQuery: {
        region: ''
      },
      supplier: JSON.parse(this.$route.query.domain_info).supplier,
      record_create_form: {
        domain: '',
        subDomain: '',
        recordType: 'A',
        recordLine: '默认',
        value: '',
        remark: '',
        ttl: 600,
        mx: 0,
        weight: 0,
        status: 'ENABLE',
        updatedBy: '',
        awsAlias: false,
        awsIdentifier: '',
        awsRoutingPolicy: 'Simple',
        awsDifferentiator: '',
        awsHostedZoneId: ''
      },
      target_region: '',
      aws_region_list_all: [],
      aws_lb_list: [],
      domain_line_list: [],
      domain_line_list_all: [],
      record_edit_form: {
        id: 0,
        recordId: '',
        domain: '',
        subDomain: '',
        recordType: '',
        recordLine: '',
        remark: '',
        value: '',
        ttl: 600,
        mx: 0,
        weight: 0,
        status: 'ENABLE',
        updatedBy: '',
        awsAlias: false,
        awsIdentifier: '',
        awsRoutingPolicy: 'Simple',
        awsDifferentiator: '',
        awsHostedZoneId: ''
      },
      editRecordDialogFormVisible: false,
      createRecordDialogFormVisible: false,
      editAliRecordWeightDialogFormVisible: false,
      input_content: '',
      select_input: 'subDomain',
      domain_record_list: [],
      domain_record_total: 0,
      show_more_search: false,
      more_search_form: {
        certStatus: null
      }
    }
  },
  computed: {
    getPlaceholder() {
      if (this.supplier === 'aws' && (this.record_create_form.recordType === 'TXT' || this.record_edit_form.recordType === 'TXT')) {
        return '请输入主机记录, 记得加引号'
      } else {
        return '请输入主机记录'
      }
    }
  },
  watch: {
    // 换了搜索对象就初始化记录
    select_input() {
      this.input_content = ''
      this.listQuery = new Map()
      this.listQuery["page"] = 1
      this.listQuery["limit"] = 15
      this.listQuery["domain"] = JSON.parse(this.$route.query.domain_info).domain
      this.get_domain_record_list()
    }
  },
  created() {
    this.get_domain_record_list()
    this.get_line_list()
    this.get_aws_region()
  },
  methods: {
    checkPermission,
    more_search() {
      this.show_more_search = !this.show_more_search
      this.more_search_form.certStatus = null
    },
    more_search_submit() {
      this.listQuery["certStatus"] = this.more_search_form.certStatus
      this.get_domain_record_list()
    },
    filterHandler(value, row, column) {
      // console.log("filterHandler-row", row)
      // console.log("filterHandler-column", column)
      const property = column['property']
      return row[property] === value
    },
    reset_record_create_form() {
      this.createRecordDialogFormVisible = false
      this.$refs.record_create_formRefs.resetFields()
    },
    search_handler() {
      const params = this.select_input
      this.listQuery.page = 1
      if (this.input_content !== '') {
        this.listQuery[params] = this.input_content
      } else {
        delete this.listQuery[params]
      }
      this.get_domain_record_list()
    },
    change_record_status(param, status) {
      if (status) {
        this.record_edit_form.status = 'ENABLE'
      } else {
        this.record_edit_form.status = 'DISABLE'
      }
      if (this.supplier === 'dnspod') {
        this.record_edit_form.id = param.id
        this.record_edit_form.recordId = param.recordId.toString()
        this.record_edit_form.domain = param.domain
        this.record_edit_form.subDomain = param.name
        this.record_edit_form.recordType = param.type
        this.record_edit_form.recordLine = param.line
        this.record_edit_form.value = param.value
        this.record_edit_form.ttl = param.ttl
        this.record_edit_form.mx = param.mx
        this.record_edit_form.weight = param.weight
      } else if (this.supplier === 'ali') {
        this.record_edit_form.id = param.id
        this.record_edit_form.recordId = param.recordId.toString()
        this.record_edit_form.domain = param.domainName
        this.record_edit_form.subDomain = param.rr
        this.record_edit_form.recordType = param.type
        this.record_edit_form.recordLine = param.line
        this.record_edit_form.value = param.value
        this.record_edit_form.ttl = param.ttl
        this.record_edit_form.mx = param.priority
        this.record_edit_form.weight = param.weight.toString()
      }
      this.record_edit_form.updatedBy = this.$store.getters.name
      updateDomainRecordStatus(this.record_edit_form).then(res => {
        this.$message({
          message: '操作成功',
          type: 'success'
        })
        .then(this.$router.go(0))
      })
    },
    get_domain_record_list() {
      getDomainRecordList(this.listQuery).then(response => {
        this.domain_record_list = response.data.data
        this.domain_record_total = response.data.totalNumber
      })
    },
    get_line_list() {
      getDomainLineList(this.listQuery).then(response => {
        this.domain_line_list = response.data.data
      })
    },
    get_aws_region() {
      getRegionList(this.awsRegionQuery).then(response => {
        // console.log("response", response.data.results)
        this.aws_region_list_all = response.data.results
      })
    },
    set_edit_target_lb(param) {
      this.record_edit_form.value = param.DnsName
      this.record_edit_form.awsHostedZoneId = param.HostedZoneId
      // console.log("set_edit_target_lb", this.record_edit_form)
    },
    set_create_target_lb(param) {
      this.record_create_form.value = param.DnsName
      this.record_create_form.awsHostedZoneId = param.HostedZoneId
      // console.log("set_create_target_lb", this.record_create_form)
    },
    search_lb(param) {
      var searchVal = param.toLowerCase()
      var newListData = []
      if (searchVal !== '') {
        this.awsLbQuery["region"] = searchVal
        getAwsLb(this.awsLbQuery).then(response => {
          newListData = response.data
          // console.log("getAwsLb", newListData)
          this.aws_lb_list = newListData
        })
      }
    },
    search_line(param) {
      var searchVal = param.toLowerCase()
      var newListData = []
      if (searchVal !== '') {
        this.domain_line_list_all.filter(item => {
          if (item.line.toLowerCase().indexOf(searchVal) !== -1) {
            newListData.push(item)
          }
        })
        this.domain_line_list = newListData
      } else {
        this.get_line_list()
      }
    },
    go_back() {
      this.$router.push({ name: "DomainList", params: { active_tab_name: "domain_resouce" } })
    },
    // 创建解析
    create_record() {
      this.createRecordDialogFormVisible = true
      this.record_create_form.domain = JSON.parse(this.$route.query.domain_info).domain
      this.record_create_form.updatedBy = this.$store.getters.name
    },
    // 修改解析
    edit_record(param, supplier) {
      this.editRecordDialogFormVisible = true
      if (supplier === 'akamai') {
        this.record_edit_form.id = param.id
        this.record_edit_form.domain = JSON.parse(this.$route.query.domain_info).domain
        this.record_edit_form.subDomain = param.name
        this.record_edit_form.recordType = param.type
        this.record_edit_form.value = param.data
        this.record_edit_form.ttl = param.ttl
        this.record_edit_form.remark = param.remark
      } else if (supplier === 'aws') {
        this.record_edit_form.id = param.id
        this.record_edit_form.domain = JSON.parse(this.$route.query.domain_info).domain
        this.record_edit_form.subDomain = param.name
        this.record_edit_form.recordType = param.type
        this.record_edit_form.ttl = param.ttl
        this.record_edit_form.remark = param.remark
        this.record_edit_form.awsAlias = param.alias
        this.record_edit_form.awsRoutingPolicy = param.routingPolicy
        this.record_edit_form.awsDifferentiator = param.differentiator
        this.record_edit_form.awsIdentifier = param.identifier
        if (param.alias === 'true') {
          this.record_edit_form.value = param.DnsName
          this.record_edit_form.awsHostedZoneId = param.HostedZoneId
        } else {
          this.record_edit_form.value = param.value
        }
      } else if (supplier === 'dnspod') {
        this.record_edit_form.id = param.id
        this.record_edit_form.recordId = param.recordId.toString()
        this.record_edit_form.domain = param.domain
        this.record_edit_form.subDomain = param.name
        this.record_edit_form.recordType = param.type
        this.record_edit_form.recordLine = param.line
        this.record_edit_form.value = param.value
        this.record_edit_form.ttl = param.ttl
        this.record_edit_form.mx = param.mx
        this.record_edit_form.remark = param.remark
        this.record_edit_form.weight = param.weight
      } else if (supplier === 'ali') {
        this.record_edit_form.id = param.id
        this.record_edit_form.recordId = param.recordId.toString()
        this.record_edit_form.domain = param.domainName
        this.record_edit_form.subDomain = param.rr
        this.record_edit_form.recordType = param.type
        this.record_edit_form.recordLine = param.line
        this.record_edit_form.value = param.value
        this.record_edit_form.ttl = param.ttl
        this.record_edit_form.mx = param.priority
        this.record_edit_form.remark = param.remark
        this.record_edit_form.weight = param.weight.toString()
      }
      this.record_edit_form.updatedBy = this.$store.getters.name
    },
    edit_ali_weight(param) {
      this.editAliRecordWeightDialogFormVisible = true
      this.record_edit_form.id = param.id
      this.record_edit_form.recordId = param.recordId.toString()
      this.record_edit_form.subDomain = param.rr
      this.record_edit_form.value = param.value
      this.record_edit_form.remark = param.remark
      this.record_edit_form.weight = param.weight.toString()
      this.record_edit_form.updatedBy = this.$store.getters.name
    },
    submit_ali_weight() {
      updateAliWeight(this.record_edit_form)
        .then((res) => {
          if (res.data.code !== "0") {
            this.$message({
            type: "error",
            message: res.data.message
          })
          } else {
            this.$message({
              type: "success",
              message: "修改成功"
            })
          }
          this.editAliRecordWeightDialogFormVisible = false
          this.get_domain_record_list()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
      this.get_domain_record_list()
      this.editAliRecordWeightDialogFormVisible = false
    },
    // 提交修改的解析
    submit_edit_record() {
      if (this.record_edit_form.recordType === 'TXT' && !this.record_edit_form.value.startsWith("\"")) {
          this.$message({
            type: "error",
            message: "不是让你加引号了么"
          })
        }
      if (this.supplier === 'aws' || this.supplier === 'akamai') {
        var word = this.record_edit_form.subDomain.split('.')
        var word1 = JSON.parse(this.$route.query.domain_info).domain.split('.')
        for (let i = 0; i < word1.length; i++) {
          word.splice(word.indexOf(word1[i]), 1)
        }
        let subDomain = ''
        for (let i = 0; i < word.length; i++) {
          subDomain += word[i] + '.'
        }
        subDomain = subDomain.substring(0, subDomain.lastIndexOf('.'))
        this.record_edit_form.subDomain = subDomain
      }
      // console.log(this.record_edit_form)
      updateDomainRecord(this.record_edit_form)
        .then((res) => {
          if (res.data.code !== "0") {
            this.$message({
            type: "error",
            message: res.data.message
          })
          } else {
          this.$message({
            type: "success",
            message: "修改成功"
          })
          }
          this.editRecordDialogFormVisible = false
          this.get_domain_record_list()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
      this.get_domain_record_list()
      this.editRecordDialogFormVisible = false
    },
    // 提交创建的解析
    submit_create_record() {
      if (this.record_create_form.recordType === 'TXT' && !this.record_create_form.value.startsWith("\"")) {
        this.$message({
          type: "error",
          message: "不是让你加引号了么"
        })
      } else {
        addDomainRecord(this.record_create_form)
        .then((res) => {
          if (res.data.code !== "0") {
            this.$message({
            type: "error",
            message: res.data.message
          })
          this.$refs.record_create_formRefs.resetFields()
          } else {
          this.$message({
            type: "success",
            message: "创建成功"
          })
          this.$refs.record_create_formRefs.resetFields()
          }
          this.createRecordDialogFormVisible = false
          this.get_domain_record_list()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
          this.$refs.record_create_formRefs.resetFields()
        })
      }
      this.get_domain_record_list()
      this.createRecordDialogFormVisible = false
    }
  }
}
</script>

<style scoped>
.el-select {
  width: 300px;
}
.el-input {
  width: 300px;
}
</style>
