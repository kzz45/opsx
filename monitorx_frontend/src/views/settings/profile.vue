这里是用户Profile的页面

<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-row :gutter="20">
        <el-col :span="8">
          <el-card :body-style="{ padding: '0px' }">
            <img
              src="@/assets/kongzz.png"
              class="image"
              style="width:400px; height:380px"
            >
          </el-card>
          <div style="padding: 14px;">
            <span>{{ name }}</span>
            <el-button
              size="small"
              style="margin-left: 200px"
              @click="edit_user_profile"
            >修改用户</el-button>
          </div>
        </el-col>
        <el-col
          v-show="edit_profile"
          :span="8"
        >
          <el-card
            class="image"
            style="width:400px; height:380px"
          >
            <el-form
              ref="user_formRefs"
              :model="user_form"
              :rules="user_form_rules"
              label-width="80px"
              size="small"
            >
              <el-form-item
                label="用户名"
                prop="username"
              >
                <el-input v-model="user_form.username"></el-input>
              </el-form-item>
              <el-form-item
                label="密码"
                prop="password"
              >
                <el-input
                  v-model="user_form.password"
                  show-password
                ></el-input>
              </el-form-item>
              <el-form-item
                label="电话"
                prop="iphone"
              >
                <el-input v-model="user_form.iphone"></el-input>
              </el-form-item>
              <el-form-item
                label="活跃"
                prop="is_active"
              >
                <el-switch
                  v-model="user_form.is_active"
                  active-color="#13ce66"
                  inactive-color="#ff4949"
                >
                </el-switch>
              </el-form-item>
              <el-form-item
                label="超管"
                prop="is_superuser"
              >
                <el-switch
                  v-model="user_form.is_superuser"
                  active-color="#13ce66"
                  inactive-color="#ff4949"
                >
                </el-switch>
              </el-form-item>
              <el-form-item>
                <el-button
                  size="small"
                  @click="cancle_edit_user"
                >取 消</el-button>
                <el-button
                  size="small"
                  type="primary"
                  @click="edit_user_submit"
                >确 定</el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: "Profile",
  data() {
    return {
      user_form: {},
      user_form_rules: {},
      edit_profile: false,
      currentDate: new Date()
    }
  },
  computed: {
    ...mapGetters(['name'])
  },
  methods: {
    edit_user_profile() {
      this.edit_profile = true
    },
    edit_user_submit() {
    },
    cancle_edit_user() {
      this.edit_profile = false
    }
  }
}
</script>

<style lang="scss" scoped>
.image {
  width: 100%;
  display: block;
}
.el-row {
  margin-bottom: 20px;
  &:last-child {
    margin-bottom: 0;
  }
}
.el-col {
  border-radius: 4px;
}
</style>
