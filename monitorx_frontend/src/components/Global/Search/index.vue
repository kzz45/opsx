<template>
  <el-input
    v-model="global_search"
    placeholder="全局搜索IP"
  ></el-input>
</template>

<script>
export default {
  name: "GlobalSearch",
  data() {
    return {
      global_search: ""
    }
  }
}
</script>
