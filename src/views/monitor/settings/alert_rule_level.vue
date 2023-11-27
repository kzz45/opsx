<template>
  <div>
    <el-button
      type="primary"
      size="small"
      icon="el-icon-circle-plus"
      @click="create_alert_rule_level"
    >新增</el-button>
    <el-table
      ref="alert_rule_level_list_table_refs"
      :data="alert_rule_level_list"
      empty-text="啥也没有"
      size="small"
      border
    >
      <el-table-column
        label="名称"
        prop="name"
      ></el-table-column>
      <el-table-column
        label="别名"
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
            @click="update_alert_rule_level(scoped.row)"
          ></el-button>
          <el-popconfirm
            title="确定删除吗？"
            confirm-button-text="确定"
            cancel-button-text="不了"
            style="margin-left: 10px"
            @confirm="delete_alert_rule_level(scoped.row)"
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
      v-show="alert_rule_level_list_total>0"
      :total="alert_rule_level_list_total"
      :page.sync="list_query.page"
      :limit.sync="list_query.limit"
      @pagination="get_alert_rule_level_list"
    ></pagination>
    <!-- 告警等级--------------------------------------------------  -->
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="alert_rule_level_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="50%"
    >
      <el-form
        ref="alert_rule_level_formRefs"
        :model="alert_rule_level_form"
        :rules="alert_rule_level_form_rules"
        label-width="100px"
        size="small"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              label="名称"
              prop="name"
            >
              <el-input
                v-model="alert_rule_level_form.name"
                size="small"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item
              label="别名"
              prop="desc"
            >
              <el-input
                v-model="alert_rule_level_form.desc"
                size="small"
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
          @click="alert_rule_level_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_alert_rule_level"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"
import { createAlertRuleLevel, updateAlertRuleLevel, deleteAlertRuleLevel, getAlertRuleLevelList } from '@/views/monitor/apis/alert_rule_level'

export default {
  name: "AlertRuleLevelSetting",
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
        create_alert_rule_level: "新增告警等级",
        update_alert_rule_level: "编辑告警等级"
      },
      dialog_status: "",
      // 告警等级--------------------------------------------------
      alert_rule_level_list: [],
      alert_rule_level_list_total: 0,
      alert_rule_level_dialog: false,
      alert_rule_level_form: {
        id: null,
        name: null,
        desc: null
      },
      alert_rule_level_form_rules: {
        name: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        desc: [{ required: true, message: "该项不能为空", trigger: "blur" }]
      }
    }
  },
  methods: {
    // 告警等级--------------------------------------------------
    create_alert_rule_level() {
      this.dialog_status = "create_alert_rule_level"
      this.alert_rule_level_dialog = true
    },
    update_alert_rule_level(row) {
      this.dialog_status = "update_alert_rule_level"
      this.alert_rule_level_dialog = true
      this.alert_rule_level_form = Object.assign({}, row)
    },
    delete_alert_rule_level(row) {
      deleteAlertRuleLevel(row.id)
        .then(resp => {
          this.$message({
            type: "success",
            message: "删除成功"
          })
          this.get_alert_rule_level_list()
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
          this.get_alert_rule_level_list()
        })
    },
    submit_alert_rule_level() {
      if (this.dialog_status === "create_alert_rule_level") {
        this.$refs.alert_rule_level_formRefs.validate((valid) => {
          if (valid) {
            createAlertRuleLevel(this.alert_rule_level_form)
              .then((resp) => {
                this.$message({
                  type: "success",
                  message: "新增成功"
                })
                this.alert_rule_level_dialog = false
                this.get_alert_rule_level_list()
              })
              .catch((err) => {
                this.$message({
                  type: "error",
                  message: err
                })
                this.alert_rule_level_dialog = false
                this.get_alert_rule_level_list()
              })
          }
        })
      } else if (this.dialog_status === "update_alert_rule_level") {
        updateAlertRuleLevel(this.alert_rule_level_form.id, this.alert_rule_level_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新成功"
            })
            this.alert_rule_level_dialog = false
            this.get_alert_rule_level_list()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err
            })
            this.alert_rule_level_dialog = false
            this.get_alert_rule_level_list()
          })
      }
    },
    get_alert_rule_level_list() {
      getAlertRuleLevelList(this.list_query)
        .then(resp => {
          this.alert_rule_level_list = resp.data.results
          this.alert_rule_level_list_total = resp.data.count
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
.el-button {
  vertical-align: top;
}
.el-table {
  width: 100%;
  margin-top: 10px;
}
</style>
