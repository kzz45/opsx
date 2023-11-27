<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-tabs
        v-model="active_tab_name"
        @tab-click="active_tab_click"
      >
        <!-- 云厂管理--------------------------------------------------  -->
        <el-tab-pane
          label="云厂管理"
          name="factory_settings"
        >
          <el-button
            type="primary"
            size="small"
            icon="el-icon-circle-plus"
            @click="create_factory"
          >新增</el-button>
          <el-table
            ref="factory_list_table_refs"
            :data="factory_list"
            empty-text="啥也没有"
            size="small"
            border
          >
            <el-table-column
              label="云厂名称"
              prop="name"
            >
            </el-table-column>
            <el-table-column
              label="云厂描述"
              prop="desc"
            >
            </el-table-column>
            <el-table-column
              label="AccessID"
              prop="access_id"
            >
            </el-table-column>
            <el-table-column
              label="操作"
              width="120px"
            >
              <template slot-scope="scoped">
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  size="mini"
                  @click="update_factory(scoped.row)"
                ></el-button>
                <el-popconfirm
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left: 10px"
                  @confirm="delete_factory(scoped.row)"
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
            v-show="factory_list_total>0"
            :total="factory_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_factory_list"
          ></pagination>
        </el-tab-pane>
        <!-- 云厂临时角色--------------------------------------------------  -->
        <el-tab-pane
          label="临时角色"
          name="rolearn_setting"
        >
          <el-button
            type="primary"
            size="small"
            icon="el-icon-circle-plus"
            @click="create_rolearn"
          >新增</el-button>
          <el-table
            ref="rolearn_list_table_refs"
            :data="rolearn_list"
            empty-text="啥也没有"
            size="small"
            border
          >
            <el-table-column
              label="名称"
              prop="name"
            ></el-table-column>
            <el-table-column
              label="策略"
              prop="policy"
            ></el-table-column>
            <el-table-column
              label="ARN"
              prop="rolearn"
            ></el-table-column>
            <el-table-column
              label="云厂"
              prop="factory__name"
            ></el-table-column>
            <el-table-column
              label="操作"
              width="120px"
            >
              <template slot-scope="scoped">
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  size="mini"
                  @click="update_rolearn(scoped.row)"
                ></el-button>
                <el-popconfirm
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left: 10px"
                  @confirm="delete_rolearn(scoped.row)"
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
            v-show="rolearn_list_total>0"
            :total="rolearn_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_rolearn_list"
          ></pagination>
        </el-tab-pane>
      </el-tabs>
    </el-card>
    <!-- 云厂管理dialog--------------------------------------------------  -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="factory_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="60%"
    >
      <el-form
        ref="factory_formRef"
        :model="factory_form"
        :rules="factory_form_rules"
        size="small"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="云厂名称"
              prop="name"
            >
              <el-input v-model="factory_form.name"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="云厂描述"
              prop="desc"
            >
              <el-input v-model="factory_form.desc"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="AccessID"
              prop="access_id"
            >
              <el-input v-model="factory_form.access_id"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="AccessKey"
              prop="access_key"
            >
              <el-input v-model="factory_form.access_key"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="factory_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_factory"
        >确 定</el-button>
      </span>
    </el-dialog>
    <!-- 临时角色管理dialog--------------------------------------------------  -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="rolearn_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="60%"
    >
      <el-form
        ref="rolearn_formRef"
        :model="rolearn_form"
        :rules="rolearn_form_rules"
        size="small"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="名称"
              prop="name"
            >
              <el-input v-model="rolearn_form.name"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="策略"
              prop="policy"
            >
              <el-input v-model="rolearn_form.policy"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="有效时间"
              prop="duration"
            >
              <el-input-number
                v-model="rolearn_form.duration"
                placeholder="有效时间"
              ></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="角色ARN"
              prop="rolearn"
            >
              <el-input v-model="rolearn_form.rolearn"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="所属云厂"
              prop="factory"
            >
              <el-select
                v-model="rolearn_form.factory"
                placeholder="请选择云厂"
              >
                <el-option
                  v-for="(item) in factory_list"
                  :key="item.id"
                  :value="item.id"
                  :label="item.name"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12"></el-col>
        </el-row>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="rolearn_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_rolearn"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"
import permission from "@/directive/permission/index.js"
import checkPermission from '@/utils/permission'
import { mapGetters } from "vuex"
import { createFactory, getFactoryList, updateFactory, deleteFactory } from "@/views/settings/apis/factory"
import { createAssumeRole, updateAssumeRole, deleteAssumeRole, getAssumeRoleList } from '@/views/settings/apis/rolearn'

export default {
  name: "SettingsFactory",
  components: {
    Pagination
  },
  directives: {
    permission
  },
  data() {
    return {
      list_query: {
        page: 1,
        limit: 15
      },
      active_tab_name: "factory_settings",
      dialog_map: {
        create_factory: "新增云厂",
        update_factory: "编辑云厂",
        create_rolearn: "新增临时角色",
        update_rolearn: "编辑临时角色"
      },
      dialog_status: "",
      // 云厂管理--------------------------------------------------
      factory_list: [],
      factory_list_total: 0,
      factory_dialog: false,
      factory_form: {
        id: null,
        name: null,
        desc: null,
        access_id: null,
        access_key: null
      },
      factory_form_rules: {
        name: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        desc: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        access_id: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        access_key: [{ required: true, message: '不能为空', trigger: ['blur'] }]
      },
      // 临时角色--------------------------------------------------
      rolearn_list: [],
      rolearn_list_total: 0,
      rolearn_dialog: false,
      rolearn_form: {
        id: null,
        name: null,
        policy: null,
        duration: 3600,
        rolearn: null,
        factory: null
      },
      rolearn_form_rules: {}
    }
  },
  computed: {
    ...mapGetters(["user_id", "is_superuser"])
  },
  created() {
    this.get_factory_list()
  },
  methods: {
    checkPermission,
    active_tab_click(tab) {
      if (tab.name === "factory_settings") {
        this.get_factory_list()
      } else if (tab.name === "rolearn_setting") {
        this.get_rolearn_list()
      }
    },
    // 云厂管理--------------------------------------------------
    create_factory() {
      this.dialog_status = "create_factory"
      this.factory_dialog = true
      this.factory_form.name = null
      this.factory_form.desc = null
      this.factory_form.access_id = null
      this.factory_form.access_key = null
    },
    update_factory(row) {
      this.dialog_status = "update_factory"
      this.factory_dialog = true
      this.factory_form = Object.assign({}, row)
    },
    delete_factory(row) {
      deleteFactory(row.id)
        .then(() => {
          this.$message({
            type: "success",
            message: "删除成功"
          })
          this.get_factory_list()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
          this.get_factory_list()
        })
    },
    submit_factory() {
      if (this.dialog_status === "create_factory") {
        createFactory(this.factory_form)
          .then((resp) => {
            this.$message({
              type: "success",
              message: "新增成功"
            })
            this.factory_dialog = false
            this.get_factory_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.factory_dialog = false
            this.get_factory_list()
          })
      } else if (this.dialog_status === "update_factory") {
        updateFactory(this.factory_form.id, this.factory_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新成功"
            })
            this.factory_dialog = false
            this.get_factory_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.factory_dialog = false
            this.get_factory_list()
          })
      }
    },
    get_factory_list() {
      getFactoryList(this.list_query)
        .then((resp) => {
          this.factory_list = resp.data.results
          this.factory_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    create_rolearn() {
      this.dialog_status = "create_rolearn"
      this.rolearn_dialog = true
      this.get_factory_list()
    },
    update_rolearn(row) {
      this.dialog_status = "update_rolearn"
      this.rolearn_dialog = true
      this.get_factory_list()
    },
    delete_rolearn(row) {
      deleteAssumeRole(row.id)
        .then(() => {
          this.$message({
            type: "success",
            message: "删除成功"
          })
          this.get_rolearn_list()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
          this.get_rolearn_list()
        })
    },
    submit_rolearn() {
      if (this.dialog_status === "create_rolearn") {
        createAssumeRole(this.rolearn_form)
          .then((resp) => {
            this.$message({
              type: "success",
              message: "新增成功"
            })
            this.rolearn_dialog = false
            this.get_rolearn_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.rolearn_dialog = false
            this.get_rolearn_list()
          })
      } else if (this.dialog_status === "update_rolearn") {
        updateAssumeRole(this.rolearn_form.id, this.rolearn_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新成功"
            })
            this.rolearn_dialog = false
            this.get_rolearn_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.rolearn_dialog = false
            this.get_rolearn_list()
          })
      }
    },
    get_rolearn_list() {
      getAssumeRoleList(this.list_query)
        .then(resp => {
          this.rolearn_list = resp.data.results
          this.rolearn_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    cancel_delete() {
      this.$message({
        type: "warning",
        message: "你考虑的很全面"
      })
    }
  }
}
</script>

<style scoped>
.el-input {
  width: 200px;
}
.el-select {
  width: 200px;
}
.el-input-number {
  width: 200px;
}
.el-tag {
  vertical-align: middle;
}
.el-button {
  vertical-align: top;
}
.el-table {
  width: 100%;
  margin-top: 10px;
}
</style>
