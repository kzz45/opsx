<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-button
        type="primary"
        size="small"
        icon="el-icon-circle-plus"
        @click="create_script"
      >新增</el-button>
      <el-table
        ref="script_list_table_refs"
        :data="script_list"
        empty-text="啥也没有"
        size="small"
        border
      >
        <el-table-column label="名称"></el-table-column>
        <el-table-column label="描述"></el-table-column>
        <el-table-column label="语言"></el-table-column>
        <el-table-column label="用户组"></el-table-column>
        <el-table-column label="更新时间"></el-table-column>
        <el-table-column label="操作"></el-table-column>
      </el-table>
    </el-card>
    <el-dialog
      :title="dialog_map[dialog_status]"
      :visible.sync="script_dialog"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="50%"
    >
      <el-form
        ref="script_formRef"
        :model="script_form"
        :rules="script_form_rules"
        size="small"
        label-width="100px"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item label="脚本名称"></el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="用户组"></el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="脚本语言"></el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="是否公开"></el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label=""></el-form-item>
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
          @click="script_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_script"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "JobsScripts",
  data() {
    return {
      list_query: {
        page: 1,
        limit: 15
      },
      dialog_map: {
        create_script: "新增脚本",
        update_script: "编辑脚本"
      },
      dialog_status: "",
      script_list: [],
      script_dialog: false,
      script_form: {},
      script_form_rules: {}
    }
  },
  computed: {
  },
  created() {
  },
  methods: {
    create_script() {
      this.dialog_status = "create_script"
      this.script_dialog = true
    },
    update_script() { },
    delete_script() { },
    submit_script() { },
    get_script_list() { }
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
