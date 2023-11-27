<template>
  <div>
    <el-button
      type="primary"
      size="small"
      icon="el-icon-circle-plus"
      @click="create_receiver"
    >新增</el-button>
    <el-table
      ref="receiver_list_table_refs"
      :data="receiver_list"
      empty-text="啥也没有"
      size="small"
      border
    >
      <el-table-column
        label="名称"
        prop="name"
      ></el-table-column>
      <el-table-column
        label="通知渠道"
        prop="channel"
      ></el-table-column>
      <el-table-column
        label="机器人"
        prop="webhook"
      ></el-table-column>
      <el-table-column
        label="产品"
        prop="product__name"
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
            @click="update_receiver(scoped.row)"
          ></el-button>
          <el-popconfirm
            title="确定删除吗？"
            confirm-button-text="确定"
            cancel-button-text="不了"
            style="margin-left: 10px"
            @confirm="delete_receiver(scoped.row)"
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
      v-show="receiver_list_total>0"
      :total="receiver_list_total"
      :page.sync="list_query.page"
      :limit.sync="list_query.limit"
      @pagination="get_receiver_list"
    ></pagination>
    <!-- 告警接收管理--------------------------------------------------  -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="receiver_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="50%"
    >
      <el-form
        ref="receiver_formRef"
        :model="receiver_form"
        :rules="receiver_form_rules"
        size="small"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="名称"
              prop="name"
            >
              <el-input
                v-model="receiver_form.name"
                clearable
                placeholder="接收者名称"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="通知渠道"
              prop="channel"
            >
              <el-select
                v-model="receiver_form.channel"
                placeholder="选择渠道"
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
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="通知模版"
              prop="template"
            >
              <el-select
                v-model="receiver_form.template"
                placeholder="通知模版"
              >
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="机器人"
              prop="webhook"
            >
              <el-input
                v-model="receiver_form.webhook"
                clearable
                placeholder="机器人webhook"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="关联产品"
              prop="product"
            >
              <el-select
                v-model="receiver_form.product"
                placeholder="请选择产品"
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
        </el-row>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="receiver_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_receiver"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"
import { getProductList } from '@/views/monitor/apis/product'
import { getReceiverList, createReceiver, updateReceiver, deleteReceiver } from '@/views/monitor/apis/receiver'

export default {
  name: "ReceiverConfig",
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
        create_receiver: "新增告警接收",
        update_receiver: "编辑告警接收"
      },
      dialog_status: "",
      product_list: [],
      // 告警接收--------------------------------------------------
      receiver_list: [],
      receiver_list_total: 0,
      receiver_dialog: false,
      receiver_form: {
        id: null,
        name: null,
        channel: null,
        webhook: null,
        product: null
      },
      receiver_form_rules: {
        name: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        channel: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        webhook: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        product: [{ required: true, message: "该项不能为空", trigger: "blur" }]
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
    // 告警接收--------------------------------------------------
    create_receiver() {
      this.dialog_status = "create_receiver"
      this.receiver_dialog = true
      this.receiver_form.name = null
      this.receiver_form.channel = null
      this.receiver_form.webhook = null
      this.receiver_form.product = null
      this.get_product_list()
    },
    update_receiver(row) {
      this.dialog_status = "update_receiver"
      this.receiver_dialog = true
      this.receiver_form = Object.assign({}, row)
      this.get_product_list()
    },
    delete_receiver(row) {
      deleteReceiver(row.id)
        .then(resp => {
          this.$message({
            type: "success",
            message: "删除成功"
          })
          this.get_receiver_list()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
          this.get_receiver_list()
        })
    },
    submit_receiver() {
      if (this.dialog_status === "create_receiver") {
        this.$refs.receiver_formRef.validate((valid) => {
          if (valid) {
            createReceiver(this.receiver_form)
              .then((resp) => {
                this.$message({
                  type: "success",
                  message: "新增成功"
                })
                this.receiver_dialog = false
                this.get_receiver_list()
              })
              .catch((err) => {
                this.$message({
                  type: "error",
                  message: err
                })
                this.receiver_dialog = false
                this.get_receiver_list()
              })
          }
        })
      } else if (this.dialog_status === "update_receiver") {
        updateReceiver(this.receiver_form.id, this.receiver_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新成功"
            })
            this.receiver_dialog = false
            this.get_receiver_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.receiver_dialog = false
            this.get_receiver_list()
          })
      }
    },
    get_receiver_list() {
      getReceiverList(this.list_query)
        .then(resp => {
          this.receiver_list = resp.data.results
          this.receiver_list_total = resp.data.count
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
.el-button {
  vertical-align: top;
}
.el-table {
  width: 100%;
  margin-top: 10px;
}
</style>
