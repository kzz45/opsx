<template>
  <div>
    <el-row>
      <el-col :span="6">
        <el-button
          icon="el-icon-scissors"
          type="primary"
          size="small"
          @click="create_split"
        ></el-button>
      </el-col>
      <el-col :span="18">
        <el-tag type="warning">这里是实在不能划分到项目组的，所以我们定义了拆分规则，如果你不认同，请联系对应的运维</el-tag>
      </el-col>
    </el-row>

    <el-table
      ref="bill_split_table_refs"
      :data="split_list"
      empty-text="啥也没有"
      size="small"
      border
    >
      <el-table-column
        label="拆分产品"
        prop="product__name"
      ></el-table-column>
      <el-table-column
        label="拆分原则"
        prop="desc"
      ></el-table-column>
      <el-table-column
        label="拆分账期"
        prop="ymd"
      ></el-table-column>
      <el-table-column
        label="拆分金额"
        prop="money"
      ></el-table-column>
      <el-table-column
        label="拆分比例"
        prop="items"
      >

        <template slot-scope="scoped">
          <el-tag
            v-for="item in JSON.parse(scoped.row.items)"
            :key="item.id"
            size="small"
          >{{ item.name + '=' + item.value }}
          </el-tag>
        </template>
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
            @click="update_split(scoped.row)"
          ></el-button>
          <el-popconfirm
            title="确定删除吗？"
            confirm-button-text="确定"
            cancel-button-text="不了"
            style="margin-left: 10px"
            @confirm="delete_split(scoped.row)"
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
      v-show="split_list_total>0"
      :total="split_list_total"
      :page.sync="list_query.page"
      :limit.sync="list_query.limit"
      @pagination="get_split_list"
    ></pagination>

    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="bill_split_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="60%"
    >
      <el-form
        ref="bill_split_formRef"
        :model="bill_split_form"
        :rules="bill_split_form_rules"
        size="small"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="拆分说明"
              prop="desc"
            >
              <el-input
                v-model="bill_split_form.desc"
                placeholder="拆分原则说明"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="拆分账期"
              prop="ymd"
            >
              <el-input
                v-model="bill_split_form.ymd"
                placeholder="拆分账期"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="拆分产品"
              prop="product"
            >
              <el-select
                v-model="bill_split_form.product"
                placeholder="请选择需要拆分的产品"
                filterable
              >
                <el-option
                  v-for="(item, index) in product_list"
                  :key="index"
                  :value="item.id"
                  :label="item.name+':'+item.code"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="产品金额"
              prop="money"
            >
              <el-input-number v-model="bill_split_form.money"></el-input-number>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="拆分项目"
              prop="project"
            >
              <el-select
                v-model="bill_split_form.project"
                placeholder="拆分给的项目"
                filterable
              >
                <el-option
                  v-for="(item, index) in project_list"
                  :key="index"
                  :value="item.name"
                  :label="item.name"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="拆分比例"
              prop="percent"
            >
              <el-input-number v-model="bill_split_form.percent"></el-input-number>
              <el-button
                type="primary"
                icon="el-icon-plus"
                size="small"
                style="margin-left: 10px;"
                @click="add_split_percent"
              ></el-button>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <el-form-item v-if="split_info_list.length > 0">
              <el-tag
                v-for="(item, index) in split_info_list"
                :key="index"
                closable
                :disable-transitions="false"
                style="margin-left: 2px;"
                @close="delete_split_percent(item.value)"
              >{{ item.name }}拆分{{ item.value }}%</el-tag>
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
          @click="bill_split_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_split"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"
import { getProjectList } from "@/views/bills/apis/project"
import { getProductList } from "@/views/bills/apis/product"
import {
  getSplitList,
  createSplit,
  updateSplit,
  deleteSplit
} from "@/views/bills/apis/split"

export default {
  name: "BillSplit",
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
        create_split: "新增拆分",
        update_split: "更新拆分"
      },
      dialog_status: "",
      bill_split_dialog: false,
      split_list: [],
      split_list_total: 0,
      bill_split_form: {
        id: null,
        desc: null,
        product: null,
        project: "",
        percent: null,
        items: null
      },
      bill_split_form_rules: {},
      product_list: [],
      project_list: [],
      split_info_list: []
    }
  },
  methods: {
    get_product_list() {
      getProductList({ limit: 999 })
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
    get_project_list() {
      getProjectList({ limit: 999 })
        .then(resp => {
          this.project_list = resp.data.results
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    create_split() {
      this.bill_split_dialog = true
      this.dialog_status = "create_split"
      this.get_product_list()
      this.get_project_list()
    },
    add_split_percent() {
      if (
        this.bill_split_form.project === "" ||
        this.bill_split_form.percent === ""
      ) {
        return
      } else {
        this.split_info_list.push({
          name: this.bill_split_form.project,
          value: this.bill_split_form.percent
        })
        this.bill_split_form.project = null
        this.bill_split_form.percent = null
      }
    },
    delete_split_percent(tag) {
      this.split_info_list.map((item, index) => {
        if (item.value === tag) {
          this.split_info_list.splice(index, 1)
        }
      })
    },
    update_split(row) {
      this.bill_split_dialog = true
      this.dialog_status = "update_split"
      this.bill_split_form = Object.assign({}, row)
      this.$nextTick(() => {
        this.split_info_list = JSON.parse(row.items)
      })
      this.get_product_list()
      this.get_project_list()
    },
    delete_split(row) {
      deleteSplit(row.id)
        .then(() => {
          this.$message({
            type: "success",
            message: "删除成功"
          })
          this.get_split_list()
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err.message
          })
          this.get_split_list()
        })
    },
    submit_split() {
      if (this.dialog_status === "create_split") {
        var post_data = Object.assign({}, this.bill_split_form)
        post_data.items = JSON.stringify(this.split_info_list)
        createSplit(post_data)
          .then(resp => {
            this.$message({
              type: "success",
              message: "新增成功"
            })
            this.bill_split_dialog = false
            this.get_split_list()
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err
            })
            this.bill_split_dialog = false
            this.get_split_list()
          })
      } else if (this.dialog_status === "update_split") {
        var update_data = Object.assign({}, this.bill_split_form)
        update_data.items = JSON.stringify(this.split_info_list)
        updateSplit(update_data.id, update_data)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新成功"
            })
            this.bill_split_dialog = false
            this.get_split_list()
          })
          .catch(err => {
            this.$message({
              type: "error",
              message: err.message
            })
            this.bill_split_dialog = false
            this.get_split_list()
          })
      }
    },
    get_split_list() {
      getSplitList(this.list_query)
        .then(resp => {
          this.split_list = resp.data.results
          this.split_list_total = resp.data.count
        })
        .catch(err => {
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
