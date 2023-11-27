<template>
  <div class="app-container">
    <el-card class="box-card">

    </el-card>
  </div>
</template>

<script>
export default {
  name: "JobsActions",
  data() {
    return {
      list_query: {
        page: 1,
        limit: 15
      }
    }
  },
  computed: {
  },
  created() {
  },
  methods: {

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
