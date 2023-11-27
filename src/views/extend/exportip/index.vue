<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-button
        type="primary"
        size="small"
        icon="el-icon-circle-plus"
        @click="create_export_ip"
      >新增</el-button>
      <el-table
        ref="export_ip_list_table_refs"
        :data="export_ip_list"
        empty-text="啥也没有"
        size="small"
        border
      >
        <el-table-column
          type="selection"
          width="55"
        >
        </el-table-column>
        <el-table-column label="IP地址"></el-table-column>
        <el-table-column label="运营商"></el-table-column>
        <el-table-column label="园区"></el-table-column>
        <el-table-column label="楼栋"></el-table-column>
        <el-table-column label="类型"></el-table-column>
        <el-table-column label="使用"></el-table-column>
        <el-table-column label="操作"></el-table-column>
      </el-table>
      <pagination
        v-show="export_ip_list_total>0"
        :total="export_ip_list_total"
        :page.sync="list_query.page"
        :limit.sync="list_query.limit"
        @pagination="get_export_ip_list"
      ></pagination>
    </el-card>
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="export_ip_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="60%"
    >
      <el-form
        ref="export_ip_formRef"
        :model="export_ip_form"
        :rules="export_ip_form_rules"
        size="small"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="IP网段"
              prop="cidr"
            >
              <el-input v-model="export_ip_form.cidr"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="出口类型"
              prop="desc"
            >
              <el-select
                v-model="export_ip_form.desc"
                placeholder="请选择"
              >
                <el-option
                  v-for="item in export_ip_type_list"
                  :key="item.id"
                  :label="item.name"
                  :value="item.name"
                ></el-option>
              </el-select>
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
                v-model="export_ip_form.park"
                filterable
                clearable
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
          <el-col :span="12">
            <el-form-item
              label="楼栋"
              prop="building"
            >
              <el-select
                v-model="export_ip_form.building"
                filterable
                clearable
                placeholder="请选择楼栋"
              >
                <el-option
                  v-for="(item, index) in building_list"
                  :key="index"
                  :label="item.name"
                  :value="item.id"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="运营商"
              prop="operator"
            >
              <el-select
                v-model="export_ip_form.operator"
                placeholder="请选择运营商"
              >
                <el-option
                  v-for="(item) in operator_list"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="是否使用"
              prop="in_use"
            >
              <el-radio-group v-model="export_ip_form.in_use">
                <el-radio :label="true">是</el-radio>
                <el-radio :label="false">否</el-radio>
              </el-radio-group>
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
          @click="export_ip_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_export_ip"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"

export default {
  name: "ExportIP",
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
        create_export_ip: "新增IP",
        update_export_ip: "编辑IP"
      },
      dialog_status: "",
      export_ip_list: [],
      export_ip_list_total: 0,
      export_ip_type_list: [
        { id: 1, name: "国内" },
        { id: 2, name: "国际" }
      ],
      park_list: [],
      building_list: [],
      operator_list: [],
      export_ip_dialog: false,
      export_ip_form: {
        id: null,
        cidr: null,
        desc: null,
        park: null,
        in_use: true,
        building: null,
        operator: null
      },
      export_ip_form_rules: {
        cidr: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        desc: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        park: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        building: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        operator: [{ required: true, message: '不能为空', trigger: ['blur'] }],
        in_use: [{ required: true, message: '不能为空', trigger: ['blur'] }]
      }
    }
  },
  methods: {
    create_export_ip() {
      this.dialog_status = "create_export_ip"
      this.export_ip_dialog = true
    },
    update_export_ip(row) { },
    delete_export_ip(row) { },
    submit_export_ip() { },
    get_export_ip_list() { }
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
