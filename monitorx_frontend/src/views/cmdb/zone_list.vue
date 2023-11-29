<template>
  <div class="app-container">
    <el-card class="box-card">
      <div>
        <el-button
          size="small"
          icon="el-icon-back"
          @click="go_back"
        >返回</el-button>
        <el-input
          v-model="listQuery.name__contains"
          placeholder="可用区名称"
          class="filter-item"
          clearable
          size="small"
          @change="clear_refresh"
          @keyup.enter.native="search_filter"
        >
          <el-button
            slot="append"
            icon="el-icon-search"
            @click="search_filter"
          ></el-button>
        </el-input>
      </div>

      <el-table
        :data="zone_list"
        style="width: 100%"
        border
        size="small"
      >
        <el-table-column
          prop="name"
          label="可用区名称"
        >
        </el-table-column>
        <!-- <el-table-column
          prop="alias_name"
          label="可用区别名"
        >
        </el-table-column> -->
        <el-table-column
          prop="zone_id"
          label="可用区ID"
        >
        </el-table-column>
        <!-- <el-table-column
          prop="desc"
          label="描述"
        >
        </el-table-column> -->
        <el-table-column
          prop="region__name"
          label="地域"
        >
        </el-table-column>
        <el-table-column
          prop="factory__name"
          label="来源"
        >
        </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="{ row }">
            <el-button
              v-if="checkPermission(['admin','ops'])"
              type="primary"
              icon="el-icon-edit"
              size="mini"
              @click="edit_zone_info(row)"
            ></el-button>

          </template>
        </el-table-column>
      </el-table>

      <pagination
        v-show="total>0"
        :total="total"
        :page.sync="listQuery.page"
        :limit.sync="listQuery.limit"
        @pagination="get_zone_list"
      ></pagination>

      <el-dialog
        title="编辑可用区"
        :visible.sync="dialogFormVisible"
        width="50%"
      >
        <el-form
          :model="zone_info_form"
          label-width="100px"
        >
          <el-form-item
            label="可用区ID"
            prop="region_id"
          >
            <el-input
              v-model="zone_info_form.zone_id"
              size="small"
              disabled
            ></el-input>
          </el-form-item>
          <el-form-item
            label="可用区名称"
            prop="name"
          >
            <el-input
              v-model="zone_info_form.name"
              size="small"
            ></el-input>
          </el-form-item>
          <el-form-item
            label="描述"
            style="width:300px"
            prop="desc"
          >
            <el-input
              v-model="zone_info_form.desc"
              size="small"
            ></el-input>
          </el-form-item>
          <el-form-item
            label="来源"
            prop="factory__name"
          >
            <el-input
              v-model="zone_info_form.factory__name"
              size="small"
              disabled
            ></el-input>
          </el-form-item>
        </el-form>
        <span
          slot="footer"
          class="dialog-footer"
        >
          <el-button
            size="small"
            @click="dialogFormVisible = false"
          >取 消</el-button>
          <el-button
            type="primary"
            size="small"
            @click="submit_zone_info"
          >确 定</el-button>
        </span>
      </el-dialog>

    </el-card>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import { getZoneList, updateZoneByID } from '@/views/cmdb/api/zone'
import checkPermission from "@/utils/permission"
export default {
  name: 'ZoneList',
  components: { Pagination },
  data() {
    return {
      listQuery: {
        page: 1,
        limit: 15,
        name__contains: '',
        region: this.$route.params.region
      },
      total: 0,
      zone_list: [],
      zone_info_form: {
        id: null,
        region: '',
        name: '',
        desc: '',
        factory__name: '',
        region__name: ''
      },
      image_dialog: false,
      dialogFormVisible: false,
      sync_loading: false
    }
  },
  computed: {
  },

  created() {
    // console.log(this.$route.params.region)
    this.get_zone_list()
  },
  methods: {
    checkPermission,
    get_zone_list() {
      getZoneList(this.listQuery)
        .then(response => {
          this.zone_list = response.data.results
          this.total = response.data.count
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
    edit_zone_info(param) {
      this.dialogFormVisible = true
      this.zone_info_form.id = param.id
      this.zone_info_form.zone_id = param.zone_id
      this.zone_info_form.name = param.name
      this.zone_info_form.factory__name = param.factory__name
      this.zone_info_form.desc = param.desc
      this.zone_info_form.region = param.region
    },
    submit_zone_info() {
      updateZoneByID(this.zone_info_form.id, this.zone_info_form)
        .then(() => {
          this.$message({
            type: "success",
            message: "编辑成功"
          })
          this.dialogFormVisible = false
          this.get_zone_list()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
      this.get_zone_list()
      this.dialogFormVisible = false
    },
    search_filter() {
      this.get_zone_list()
    },
    clear_refresh() {
      this.get_zone_list()
    },
    go_back() {
      this.$router.push({ name: "Other", params: { active_tab_name: 'region_resource' } })
    }
  }
}
</script>

<style scoped>
.el-table {
  margin-top: 15px;
}
.el-input {
  width: 300px;
  margin-left: 10px;
}
.el-button {
  vertical-align: top;
}
</style>
