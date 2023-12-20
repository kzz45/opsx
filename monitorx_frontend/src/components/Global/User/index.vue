<template>
  <div>
    <el-select
      v-model="selected_user"
      filterable
      placeholder="选个人儿吧"
      clearable
      autocomplete="on"
      props="selected_user"
      size="small"
    >
      <el-option
        v-for="item in users"
        :key="item.id"
        :label="item.first_name"
        :value="item.id"
      >
      </el-option>
    </el-select>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { getUserList } from '@/api/user'

export default {
  name: "GlobalUser",
  data() {
    return {
      selected_user: ''
    }
  },
  computed: {
    ...mapGetters(['users'])
  },
  mounted() {
    // this.users_list = this.get_user_list()
  },
  created() {
    this.get_user_list()
  },
  methods: {
    get_user_list() {
      getUserList()
        .then(resp => {
          // this.users_list = resp.data.results
          this.$store.commit({
            type: "SET_USERS",
            users: resp.data.results
          })
        }).catch((err) => {
          this.$message({
            type: 'error',
            message: err.message
          })
        })
    }
  }
}
</script>
