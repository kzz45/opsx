<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-button
        type="primary"
        size="small"
        @click="create_user_group"
      >权限调整</el-button>
      <el-table
        :data="user_group_list"
        border
        style="width: 100%;margin-top: 10px"
        size="small"
      >
        <template slot="empty">
          <span>不好意思啊</span>
        </template>
        <el-table-column
          prop="name"
          label="组名"
        ></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scoped">
            <el-button
              type="primary"
              icon="el-icon-edit"
              size="mini"
              @click="edit_user_group(scoped.row)"
            ></el-button>
          </template>
        </el-table-column>
      </el-table>
      <!-- <el-transfer
        v-model="target_perm_list"
        :data="source_perm_list"
        :titles="['可用 权限', '选中 权限']"
        filter-placeholder="请输入权限名称"
        filterable
        :format="{noChecked: '${total}',hasChecked: '${checked}/${total}'}"
        style="text-align: left; display: inline-block"
      >
        <el-button
          slot="left-footer"
          class="transfer-footer"
          size="small"
        >操作</el-button>
        <el-button
          slot="right-footer"
          class="transfer-footer"
          size="small"
        >操作</el-button>
      </el-transfer> -->
      <!-- <el-transfer
        v-model="target_perm_list"
        :data="source_perm_list"
        :titles="['可用 权限', '选中 权限']"
        filter-placeholder="请输入权限名称"
        :format="{noChecked: '${total}',hasChecked: '${checked}/${total}'}"
        filterable
      >
      </el-transfer> -->
      <!-- <el-tree
        ref="treeRef"
        :props="tree_props"
        :data="tree_data"
        show-checkbox
        empty-text="啥也木有"
        :check-on-click-node="true"
      >
      </el-tree> -->

    </el-card>
    <el-dialog
      :title="perm_text_map[perm_dialog_status]"
      :visible.sync="perm_dialog"
      width="60%"
    >
      <el-form
        ref="add_user_group_formRef"
        :model="add_user_group_form"
        label-width="100px"
      >
        <el-form-item
          label="用户组名称"
          prop="name"
        >
          <el-input
            v-model="add_user_group_form.name"
            size="small"
            style="width: 580px;"
          ></el-input>
        </el-form-item>
        <el-form-item
          label="权限"
          prop="permissions"
        >
          <el-transfer
            v-model="target_perm_list"
            :right-default-checked="target_perm_list"
            :data="source_perm_list"
            :titles="['可用 权限', '选中 权限']"
            filter-placeholder="请输入权限名称"
            :format="{noChecked: '${total}',hasChecked: '${checked}/${total}'}"
            filterable
          ></el-transfer>
        </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="perm_dialog = false"
        >取 消</el-button>
        <el-button
          type="primary"
          size="small"
          @click="submit_perm"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { getProductList } from '@/api/product'
import { getPermList } from '@/api/perm'
import { getHostGroupList } from '@/api/host_group'
import { getUserGroups, updateUserGroup } from '@/api/user'

export default {
  data() {
    return {
      list_query: {
        page: 1,
        limit: 15
      },
      test_dialog: false,
      test_form: {},
      product_id: '',
      script_id: '',
      product_list: [],
      script_list: [],
      target_perm_list: [],
      target_perm_temp_list: [],
      source_perm_list: [],
      source_perm_temp_list: [],
      source_perm_total: 0,
      tree_data: [],
      tree_props: {
        id: 'key',
        label: 'label',
        children: 'children'
      },
      perm_dialog: false,
      perm_text_map: {
        create_perm: "新增用户组权限",
        update_perm: "编辑用户组权限"
      },
      perm_dialog_status: "",
      add_user_group_form: {
        name: "",
        target_perm_list: [],
        source_perm_list: []
      },
      user_group_list: []
    }
  },
  computed: {
    ...mapGetters(['current_select_product_id', 'current_select_product_name'])
  },
  watch: {
  },
  created() {
    // this.get_product_list()
    this.get_perm_list()
    this.get_machine_group_list()
    this.get_user_group()
  },
  methods: {
    add() {
      this.test_dialog = true
      // console.log(this.$refs.test_formRefs)
    },
    get_product_list() {
      getProductList(this.list_query).then(resp => {
        this.product_list = resp.data.results
      })
    },
    get_perm_list() {
      this.list_query.limit = 999
      getPermList(this.list_query).then(resp => {
        this.source_perm_temp_list = Object.keys(resp.data.results).map(function (key) {
          return { key: resp.data.results[key]["id"], label: resp.data.results[key]["name"] }
        })
        this.source_perm_total = resp.data.count
        this.source_perm_list = this.source_perm_temp_list
      })
    },
    create_user_group() {
      this.perm_dialog_status = "create_perm"
      this.perm_dialog = true
      // this.add_user_group_form.source_perm_list = this.source_perm_list
    },
    edit_user_group(row) {
      this.perm_dialog_status = "update_perm"
      this.perm_dialog = true
      this.add_user_group_form = Object.assign({}, row)
      this.target_perm_temp_list = Object.keys(row.permissions).map(function (key) {
        return row.permissions[key]["id"]
      })
      this.target_perm_list = this.target_perm_temp_list
    },
    submit_perm() {
      if (this.perm_dialog_status === "update_perm") {
        this.add_user_group_form.permissions = this.target_perm_list
        // console.log(this.target_perm_list.length, '====')
        // console.log(this.add_user_group_form, '====')
        updateUserGroup(this.add_user_group_form.id, this.add_user_group_form)
          .then(() => {
            this.$message({
              type: "success",
              message: "更新用户组成功"
            })
            this.user_group_dialog = false
            this.get_user_group()
          })
          .catch((err) => {
            this.$message({
              type: "error",
              message: err.message
            })
            this.user_group_dialog = false
            this.get_user_group()
          })
      }
    },
    get_user_group() {
      getUserGroups(this.listQuery).then(response => {
        this.user_group_list = response.data.results
      })
    },
    get_machine_group_list() {
      getHostGroupList().then(resp => {
        var resp_data = resp.data.results
        this.tree_data = Object.keys(resp_data).map(function (key) {
          return {
            id: resp_data[key]["id"],
            label: resp_data[key]["name"],
            children: Object.keys(resp_data[key]["machine_list"]).map(function (skey) {
              return { id: resp_data[key]["machine_list"][skey]["id"], label: resp_data[key]["machine_list"][skey]["external_uuid"] }
            })
          }
        })
        // console.log(this.tree_data[0]['children'], '========')
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.el-transfer-panel {
  width: 400px;
}
// .el-tree {
//   width: 400px;
//   height: auto;
//   border: 1px solid #e4e4e4;
//   background-color: white;
//   box-shadow: 0 0 10px #e8f4ff;
//   border-radius: 3px;
// }
// .el-transfer__buttons {
//   font-size: 12px !important;
//   border-radius: 3px !important;
//   padding: 9px 15px !important;
// }
// .el-button--primary {
//   border-radius: 3px !important;
//   padding: 9px 15px !important;
// }
.custom-tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  padding-right: 8px;
}
</style>
