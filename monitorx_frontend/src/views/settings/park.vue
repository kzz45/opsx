<template>
  <div class="app-container">
    <el-card class="box-card">
      <div>
        <!-- <el-button
          type="primary"
          size="small"
          icon="el-icon-circle-plus"
          @click="add_park('create')"
        >新增园区</el-button> -->
        <el-button
          type="primary"
          size="small"
          icon="el-icon-circle-plus"
          @click="add_building('create')"
        >新增楼栋</el-button>
      </div>
      <el-table
        :data="building_list"
        style="width: 100%"
        border
        size="small"
      >
        <el-table-column
          prop="park__name"
          label="名称"
        >
        </el-table-column>
        <el-table-column
          prop="name"
          label="楼栋"
        >
        </el-table-column>
        <el-table-column
          prop="floor"
          label="楼层"
        >
        </el-table-column>
        <el-table-column
          label="操作"
          width="120px;"
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
              style="margin-left:10px"
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
        v-show="park_list_total>0"
        :total="park_list_total"
        :page.sync="list_query.page"
        :limit.sync="list_query.limit"
        @pagination="get_park_list"
      ></pagination>
    </el-card>
    <el-dialog
      :title="textMap[dialogStatus]"
      :visible.sync="park_dialog"
      width="50%"
    >
      <el-form
        ref="park_formRefs"
        :model="park_form"
        :rules="park_form_rules"
        label-width="100px"
      >
        <el-form-item
          label="园区名称"
          prop="name"
        >
          <el-input
            v-model="park_form.name"
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
      :title="textMap[dialogStatus]"
      :visible.sync="building_dialog"
      width="50%"
    >
      <el-form
        ref="building_formRefs"
        :model="building_form"
        :rules="building_form_rules"
        label-width="100px"
      >
        <el-form-item
          label="楼栋名称"
          prop="name"
        >
          <el-input
            v-model="building_form.name"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="楼层名称"
          prop="floor"
        >
          <el-input
            v-model="building_form.floor"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="园区"
          prop="park"
        >
          <el-select
            v-model="building_form.park"
            placeholder="请选择园区"
            size="small"
            style="width: 300px;"
          >
            <el-option
              v-for="(item) in park_list"
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
          @click="building_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_building"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import { getParkList, createPark, updateParkID } from '@/api/park'
import { getBuildingList, createBuilding, updateBuildingID, deleteBuildingByID } from '@/api/building'

export default {
  name: "Operator",
  components: {
    Pagination
  },
  data() {
    return {
      list_query: {
        page: 1,
        limit: 15
      },
      park_form: {
        id: null,
        name: null,
        building: null,
        floor: null
      },
      park_form_rules: {
        name: [{ required: true, message: '不能为空', trigger: 'blur' }]
      },
      park_dialog: false,
      textMap: {
        create_park: '新增园区',
        update_park: '编辑园区',
        create_building: "新增楼栋",
        update_building: "更新楼栋"
      },
      dialogStatus: "",
      park_list: [],
      park_list_total: 0,
      building_dialog: false,
      building_list: [],
      building_list_total: 0,
      building_form: {
        name: null,
        floor: null,
        park: null
      },
      building_form_rules: {
        name: [{ required: true, message: '不能为空', trigger: 'blur' }],
        floor: [{ required: true, message: '不能为空', trigger: 'blur' }],
        park: [{ required: true, message: '不能为空', trigger: 'blur' }]
      }
    }
  },
  created() {
    this.get_park_list()
    this.get_building_list()
  },
  methods: {
    add_park() {
      this.dialogStatus = "create_park"
      this.park_dialog = true
    },
    update_park(row) {
      this.dialogStatus = "update_park"
      this.park_dialog = true
      this.park_form = Object.assign({}, row)
    },
    submit_park() {
      if (this.dialogStatus === "create_park") {
        createPark(this.park_form)
          .then(resp => {
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
      } else if (this.dialogStatus === "update_park") {
        updateParkID(this.park_form.id, this.park_form)
          .then(resp => {
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
      getParkList(this.list_query).then(resp => {
        this.park_list = resp.data.results
        this.park_list_total = resp.data.count
      })
    },
    delete_building(row) {
      deleteBuildingByID(row.id)
        .then(resp => {
          this.$message({
            type: "success",
            message: "删除成功"
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
    },
    cancel_delete() {
      this.$message({
        type: "warning",
        message: "你考虑的很全面"
      })
    },
    add_building() {
      this.dialogStatus = "create_building"
      this.building_dialog = true
      this.building_form.name = null
      this.building_form.floor = null
      this.building_form.park = null
    },
    update_building(row) {
      this.dialogStatus = "update_building"
      this.building_dialog = true
      this.building_form = Object.assign({}, row)
    },
    submit_building() {
      if (this.dialogStatus === "create_building") {
        createBuilding(this.building_form)
          .then(resp => {
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
      } else if (this.dialogStatus === "update_building") {
        updateBuildingID(this.building_form.id, this.building_form)
          .then(resp => {
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
      getBuildingList(this.list_query).then(resp => {
        this.building_list = resp.data.results
        this.building_list_total = resp.data.count
      })
    }
  }
}
</script>

<style scoped>
.el-table {
  margin-top: 10px;
}
.el-input {
  width: 300px;
}
</style>
