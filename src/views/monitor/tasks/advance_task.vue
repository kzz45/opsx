<template>
  <div>
    <el-button
      type="primary"
      size="small"
      icon="el-icon-circle-plus"
      @click="create_advance_task"
    >新增</el-button>
    <el-table
      ref="advance_task_list_table_refs"
      :data="advance_task_list"
      empty-text="啥也没有"
      size="small"
      border
    ></el-table>
    <pagination
      v-show="advance_task_list_total>0"
      :total="advance_task_list_total"
      :page.sync="list_query.page"
      :limit.sync="list_query.limit"
      @pagination="get_advance_task_list"
    ></pagination>
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="advance_task_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="50%"
    >
      <el-form
        ref="advance_task_formRef"
        :model="advance_task_form"
        :rules="advance_task_form_rules"
        size="small"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="任务名称"
              prop="name"
            >
              <el-input v-model="advance_task_form.name"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="任务类型"
              prop="types"
            >
              <el-select
                v-model="advance_task_form.types"
                placeholder=""
              >
                <el-option
                  v-for="(item, index) in advance_task_type_list"
                  :key="index"
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
              label="产品"
              prop="product"
            >
              <el-select
                v-model="advance_task_form.product"
                placeholder="产品"
              >
                <el-option
                  v-for="(item) in product_list"
                  :key="item.id"
                  :value="item.id"
                  :label="item.name"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="挂载节点"
              prop="server"
            >
              <el-select
                v-model="advance_task_form.server"
                placeholder="挂载节点"
              >
                <el-option
                  v-for="(item) in server_list"
                  :key="item.id"
                  :value="item.id"
                  :label="item.name"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <el-form-item
              label="配置详情"
              prop="content"
            >
              <el-input
                v-model="advance_task_form.content"
                :autosize="{ minRows:10, maxRows: 20 }"
                type="textarea"
                placeholder="配置内容"
                style="width: 540px;"
              ></el-input>
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
          @click="advance_task_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_advance_task"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"
import { getProductList } from '@/views/monitor/apis/product'
import { getServerList } from '@/views/monitor/apis/server'

export default {
  name: "AdvanceTaskConfig",
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
        create_advance_task: "新增高级任务",
        update_advance_task: "编辑高级任务"
      },
      dialog_status: "",
      server_list: [],
      product_list: [],
      advance_task_list: [],
      advance_task_list_total: 0,
      advance_task_type_list: [
        { id: 1, name: "Docker Swarm" }
      ],
      advance_task_dialog: false,
      advance_task_form: {
        name: null,
        types: null,
        product: null,
        server: null,
        content: null
      },
      advance_task_form_rules: {
        name: [{ required: true, message: "该项不能为空", trigger: blur }],
        types: [{ required: true, message: "该项不能为空", trigger: blur }],
        product: [{ required: true, message: "该项不能为空", trigger: blur }],
        server: [{ required: true, message: "该项不能为空", trigger: blur }],
        content: [{ required: true, message: "该项不能为空", trigger: blur }]
      }
    }
  },
  methods: {
    get_product_list() {
      getProductList({ limit: 100 })
        .then(resp => {
          this.product_list = resp.data.results
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    get_server_list() {
      getServerList({ limit: 100 })
        .then(resp => {
          this.server_list = resp.data.results
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    create_advance_task() {
      this.dialog_status = "create_advance_task"
      this.advance_task_dialog = true
      this.get_server_list()
      this.get_product_list()
    },
    update_advance_task(row) {
      this.dialog_status = "update_advance_task"
      this.advance_task_dialog = true
      this.get_server_list()
      this.get_product_list()
    },
    delete_advance_task() { },
    submit_advance_task() { },
    get_advance_task_list() { }
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
.el-button {
  vertical-align: top;
}
.el-table {
  width: 100%;
  margin-top: 10px;
}
</style>
