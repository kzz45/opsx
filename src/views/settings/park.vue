<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-tabs
        v-model="active_tab_name"
        @tab-click="active_tab_click"
      >
        <!-- 园区管理--------------------------------------------------  -->
        <el-tab-pane
          label="园区管理"
          name="park_setting"
        >
          <el-button
            type="primary"
            size="small"
            icon="el-icon-circle-plus"
            @click="create_park"
          >新增</el-button>
          <el-table
            ref="park_list_table_refs"
            :data="park_list"
            empty-text="啥也没有"
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
              width="120px"
            >
              <template slot-scope="scoped">
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  size="mini"
                  @click="update_park(scoped.row)"
                ></el-button>
                <el-popconfirm
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left: 10px"
                  @confirm="delete_park(scoped.row)"
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
            v-show="park_list_total>0"
            :total="park_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_park_list"
          ></pagination>
        </el-tab-pane>
        <!-- 楼栋管理--------------------------------------------------  -->
        <el-tab-pane
          label="楼栋管理"
          name="building_setting"
        >
          <el-button
            type="primary"
            size="small"
            icon="el-icon-circle-plus"
            @click="create_building"
          >新增</el-button>
          <el-table
            ref="building_list_table_refs"
            :data="building_list"
            empty-text="啥也没有"
            size="small"
            border
          >
            <el-table-column
              label="楼栋"
              prop="name"
            ></el-table-column>
            <el-table-column
              label="楼层"
              prop="floor"
            ></el-table-column>
            <el-table-column
              label="园区"
              prop="park__name"
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
                  @click="update_building(scoped.row)"
                ></el-button>
                <el-popconfirm
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left: 10px"
                  @confirm="delete_building(scoped.row)"
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
            v-show="building_list_total>0"
            :total="building_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_building_list"
          ></pagination>
        </el-tab-pane>
        <!-- 运营商管理--------------------------------------------------  -->
        <el-tab-pane
          label="运营厂商"
          name="operator_setting"
        >
          <el-button
            type="primary"
            size="small"
            icon="el-icon-circle-plus"
            @click="create_operator"
          >新增</el-button>
          <el-table
            ref="operator_list_table_refs"
            :data="operator_list"
            empty-text="啥也没有"
            size="small"
            border
          >
            <el-table-column
              label="运营商"
              prop="name"
            ></el-table-column>
            <el-table-column
              label="描述"
              prop="desc"
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
                  @click="update_operator(scoped.row)"
                ></el-button>
                <el-popconfirm
                  title="确定删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="不了"
                  style="margin-left: 10px"
                  @confirm="delete_operator(scoped.row)"
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
            v-show="operator_list_total>0"
            :total="operator_list_total"
            :page.sync="list_query.page"
            :limit.sync="list_query.limit"
            @pagination="get_operator_list"
          ></pagination>
        </el-tab-pane>
      </el-tabs>
    </el-card>
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="park_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="60%"
    >
      <el-form
        ref="park_formRef"
        :model="park_form"
        :rules="park_form_rules"
        size="small"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="名称"
              prop="name"
            >
              <el-input v-model="park_form.name"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="描述"
              prop="desc"
            >
              <el-input v-model="park_form.desc"></el-input>
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
          @click="park_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_park"
        >确 定</el-button>
      </span>
    </el-dialog>

    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="building_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="60%"
    >
      <el-form
        ref="building_formRef"
        :model="building_form"
        :rules="building_form_rules"
        size="small"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="名称"
              prop="name"
            >
              <el-input v-model="building_form.name"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="楼层"
              prop="floor"
            >
              <el-input v-model="building_form.floor"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="园区"
              prop="park"
            >
              <el-select
                v-model="building_form.park"
                placeholder="请选择园区"
              >
                <el-option
                  v-for="(item, index) in park_list"
                  :key="index"
                  :label="item.name"
                  :value="item.id"
                ></el-option>
              </el-select>
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
          @click="building_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_building"
        >确 定</el-button>
      </span>
    </el-dialog>

    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="operator_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="60%"
    >
      <el-form
        ref="operator_formRef"
        :model="operator_form"
        :rules="operator_form_rules"
        size="small"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="名称"
              prop="name"
            >
              <el-input v-model="operator_form.name"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="描述"
              prop="desc"
            >
              <el-input v-model="operator_form.desc"></el-input>
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
          @click="operator_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_operator"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"
import { createPark, updatePark, getParkList } from '@/views/settings/apis/park'
import { createBuilding, updateBuilding, getBuildingList } from '@/views/settings/apis/building'
import { createOperator, updateOperator, getOperatorList } from '@/views/settings/apis/operator'

export default {
  name: "ParkSetting",
  components: {
    Pagination
  },
  data() {
    return {
      list_query: {
        page: 1,
        limit: 15
      },
      dialog_map: {
        create_park: "新增园区",
        update_park: "编辑园区",
        create_building: "新增楼栋",
        update_building: "编辑楼栋",
        create_operator: "新增运营商",
        update_operator: "编辑运营商"
      },
      dialog_status: "",
      active_tab_name: "park_setting",
      park_list: [],
      park_list_total: 0,
      park_dialog: false,
      park_form: {
        id: null,
        name: null,
        desc: null
      },
      park_form_rules: {
        name: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        desc: [{ required: true, message: '不能为空', trigger: ['blur'] }]
      },
      building_list: [],
      building_list_total: 0,
      building_dialog: false,
      building_form: {
        id: null,
        name: null,
        floor: null,
        park: null
      },
      building_form_rules: {
        name: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        floor: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        park: [{ required: true, message: '不能为空', trigger: ['blur'] }]
      },
      operator_list: [],
      operator_list_total: 0,
      operator_dialog: false,
      operator_form: {
        id: null,
        name: null,
        desc: null
      },
      operator_form_rules: {
        name: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        desc: [{ required: true, message: '不能为空', trigger: ['blur'] }]
      }
    }
  },
  created() {
    this.get_park_list()
  },
  methods: {
    active_tab_click(tab) {
      if (tab.name === "park_setting") {
        this.get_park_list()
      } else if (tab.name === "building_setting") {
        this.get_building_list()
      } else if (tab.name === "operator_setting") {
        this.get_operator_list()
      }
    },
    create_park() {
      this.dialog_status = "create_park"
      this.park_dialog = true
      this.park_form.name = null
      this.park_form.desc = null
    },
    update_park(row) {
      this.dialog_status = "update_park"
      this.park_dialog = true
      this.park_form = Object.assign({}, row)
    },
    delete_park(row) { },
    submit_park() {
      if (this.dialog_status === "create_park") {
        createPark(this.park_form)
          .then((resp) => {
            this.$message({
              type: "success",
              message: "新增成功"
            })
            this.park_dialog = false
            this.get_park_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.park_dialog = false
            this.get_park_list()
          })
      } else if (this.dialog_status === "update_park") {
        updatePark(this.park_form.id, this.park_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新成功"
            })
            this.park_dialog = false
            this.get_park_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.park_dialog = false
            this.get_park_list()
          })
      }
    },
    get_park_list() {
      getParkList(this.list_query)
        .then((resp) => {
          this.park_list = resp.data.results
          this.park_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    create_building() {
      this.dialog_status = "create_building"
      this.building_dialog = true
      this.building_form.name = null
      this.building_form.floor = null
      this.building_form.park = null
    },
    update_building(row) {
      this.dialog_status = "update_building"
      this.building_dialog = true
      this.building_form = Object.assign({}, row)
    },
    delete_building(row) { },
    submit_building() {
      if (this.dialog_status === "create_building") {
        createBuilding(this.building_form)
          .then((resp) => {
            this.$message({
              type: "success",
              message: "新增成功"
            })
            this.building_dialog = false
            this.get_building_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.building_dialog = false
            this.get_building_list()
          })
      } else if (this.dialog_status === "update_building") {
        updateBuilding(this.building_form.id, this.building_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新成功"
            })
            this.building_dialog = false
            this.get_building_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.building_dialog = false
            this.get_building_list()
          })
      }
    },
    get_building_list() {
      getBuildingList(this.list_query)
        .then((resp) => {
          this.building_list = resp.data.results
          this.building_list_total = resp.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    create_operator() {
      this.dialog_status = "create_operator"
      this.operator_dialog = true
      this.operator_form.name = null
      this.operator_form.desc = null
    },
    update_operator(row) {
      this.dialog_status = "update_operator"
      this.operator_dialog = true
      this.operator_form = Object.assign({}, row)
    },
    delete_operator(row) { },
    submit_operator() {
      if (this.dialog_status === "create_operator") {
        createOperator(this.operator_form)
          .then((resp) => {
            this.$message({
              type: "success",
              message: "新增成功"
            })
            this.operator_dialog = false
            this.get_operator_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.operator_dialog = false
            this.get_operator_list()
          })
      } else if (this.dialog_status === "update_operator") {
        updateOperator(this.operator_form.id, this.operator_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新成功"
            })
            this.operator_dialog = false
            this.get_operator_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.operator_dialog = false
            this.get_operator_list()
          })
      }
    },
    get_operator_list() {
      getOperatorList(this.list_query)
        .then((resp) => {
          this.operator_list = resp.data.results
          this.operator_list_total = resp.data.count
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
