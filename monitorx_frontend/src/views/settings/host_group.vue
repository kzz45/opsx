产品分组页面
也是主机分组

<template>
  <div class="app-container">
    <el-card class="box-card">
      <!-- 新增或者搜索相关 -->
      <div>
        <el-button
          size="small"
          icon="el-icon-back"
          @click="go_back"
        >返回</el-button>
        <el-input
          v-model="input_select"
          placeholder="搜索"
          size="small"
          clearable
          @keyup.enter.native="search_host_group"
        >
          <el-select
            slot="prepend"
            v-model="select_input"
            size="small"
            placeholder="请选择"
          >
            <el-option
              label="分组名称"
              value="name"
            ></el-option>
          </el-select>
          <el-button
            slot="append"
            icon="el-icon-search"
            :loading="button_loading"
          ></el-button>
        </el-input>
        <el-button
          type="primary"
          size="small"
          style="margin-left: 10px"
          @click="add_host_group"
        >新增分组</el-button>
      </div>
      <div style="margin-top: 10px">
        <el-table
          :data="host_group_list"
          style="width: 100%"
          border
          size="small"
        >
          <el-table-column
            prop="name"
            label="分组名称"
          >
          </el-table-column>
          <el-table-column
            prop="desc"
            label="描述"
          >
          </el-table-column>
          <el-table-column
            prop="product__name"
            label="所属产品"
          >
          </el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scoped">
              <el-button
                type="primary"
                icon="el-icon-edit"
                size="mini"
                @click="edit_host_group(scoped.row)"
              ></el-button>
              <el-popconfirm
                title="确定删除吗？"
                confirm-button-text="确定"
                cancel-button-text="不了"
                style="margin-left:10px"
                @confirm="delete_host_group(scoped.row)"
                @cancel="cancel_delete_host_group"
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
          v-show="host_group_total>0"
          :total="host_group_total"
          :page.sync="listQuery.page"
          :limit.sync="listQuery.limit"
          @pagination="get_host_group_list"
        ></pagination>
      </div>
    </el-card>
    <!-- 新增或者编辑分组的Dialog -->
    <el-dialog
      :title="textMap[dialogStatus]"
      :visible.sync="host_group_dialog"
      width="50%"
    >
      <el-form
        ref="host_group_form"
        :model="host_group_form"
        :rules="host_group_form_rules"
        label-width="100px"
      >
        <el-form-item
          label="分组名称"
          style="width:300px"
          prop="name"
        >
          <el-input
            v-model="host_group_form.name"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="分组描述"
          style="width:300px"
          prop="desc"
        >
          <el-input
            v-model="host_group_form.desc"
            size="small"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="所属产品"
          style="width:300px"
          prop="product"
        >
          <el-input
            v-model="product_name"
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
          @click="host_group_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_host_group"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Pagination from '@/components/Pagination'
import { getHostGroupList, createHostGroup, updateHostGroupByID, deleteHostGroupByID } from '@/api/host_group'

export default {
  name: "HostGroup",
  components: {
    Pagination
  },
  data() {
    return {
      listQuery: {
        page: 1,
        limit: 15
      },
      input_select: '',
      select_input: 'name',
      button_loading: false,
      host_group_total: 0,
      host_group_list: [],
      host_group_dialog: false,
      textMap: {
        create: '新增分组',
        update: '更新分组'
      },
      dialogStatus: '',
      host_group_form: {
        id: null,
        name: null,
        desc: null,
        product: null
      },
      host_group_form_rules: {
        name: [{ required: true, message: '不能为空', trigger: 'blur' }],
        desc: [{ required: true, message: '不能为空', trigger: 'blur' }]
      },
      product_id: '',
      product_name: '',
      product_info: {
        id: null,
        name: null
      }
    }
  },
  computed: {
    ...mapGetters(['current_select_product_id', 'current_select_product_name'])
  },
  created() {
    this.product_info = JSON.parse(this.$route.query.product_info)
    console.log(this.product_info, '====')
    this.product_id = this.product_info.id
    this.product_name = this.product_info.name
    this.get_host_group_list()
  },
  methods: {
    get_host_group_list() {
      const params = "product__id__in"
      this.listQuery[params] = this.product_info.id
      getHostGroupList(this.listQuery)
        .then(response => {
          this.host_group_list = response.data.results
          this.host_group_total = response.data.count
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    search_host_group() { },
    add_host_group() {
      this.host_group_dialog = true
      this.dialogStatus = 'create'
      this.host_group_form.product = this.product_id
      // if (this.$refs.host_group_form) {
      //   this.$refs.host_group_form.resetFields()
      // }
      this.host_group_form.name = null
      this.host_group_form.desc = null
    },
    edit_host_group(row) {
      this.host_group_dialog = true
      this.dialogStatus = 'update'
      this.host_group_form = Object.assign({}, row)
    },
    submit_host_group() {
      if (this.dialogStatus === "create") {
        createHostGroup(this.host_group_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "新增产品主机分组【" + this.host_group_form.name + "】成功"
            })
            this.host_group_dialog = false
            this.get_host_group_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.host_group_dialog = false
            this.get_host_group_list()
          })
      } else if (this.dialogStatus === 'update') {
        updateHostGroupByID(this.host_group_form.id, this.host_group_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新产品主机分组【" + this.host_group_form.name + "】成功"
            })
            this.host_group_dialog = false
            this.get_host_group_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.host_group_dialog = false
            this.get_host_group_list()
          })
      }
    },
    delete_host_group(row) {
      deleteHostGroupByID(row.id)
        .then(() => {
          this.$message({
            type: "success",
            message: "删除分组【" + row.name + "】成功"
          })
          this.get_host_group_list()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
          this.get_host_group_list()
        })
    },
    cancel_delete_host_group() {
      this.$message({
        type: "warning",
        message: "想想还是算了"
      })
    },
    go_back() {
      this.$router.push({ name: "Product" })
    }
  }
}
</script>

<style scoped>
.el-input {
  width: 300px;
  margin-left: 10px;
}
.el-select {
  width: 100px;
}
.el-button {
  vertical-align: top;
}
</style>
