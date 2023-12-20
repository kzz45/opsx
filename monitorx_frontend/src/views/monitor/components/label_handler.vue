<template>
  <div>
    <el-form>
      <el-form-item>
        <el-autocomplete
          v-model="label_name"
          :fetch-suggestions="query_search_label_name"
          placeholder="请选择标签名称"
          clearable
          size="small"
          style="width: 140px;"
          @select="handle_select"
        ></el-autocomplete>
        <span style="margin-left: 20px;"></span>
        <el-autocomplete
          v-model="label_value"
          :fetch-suggestions="query_search_label_value"
          placeholder="请选择标签的值"
          clearable
          size="small"
          style="width: 140px;"
        ></el-autocomplete>
        <el-button
          type="primary"
          icon="el-icon-plus"
          size="small"
          style="margin-left: 10px;"
          @click="add_condition"
        ></el-button>
      </el-form-item>
      <el-form-item v-if="label_value_list.length > 0">
        <el-tag
          v-for="(item, index) in label_value_list"
          :key="index"
          closable
          :disable-transitions="false"
          style=" margin-top: 10px; margin-left: 2px;"
          @close="delete_label_value(item.value)"
        >{{ item.name }}={{ item.value }}</el-tag>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { getLabelList } from '@/views/monitor/api/label'

export default {
  name: "LabelHandler",
  data() {
    return {
      label_id: null,
      label_name: '',
      label_value: '',
      label_name_options: [],
      label_value_options: [],
      label_value_list: []
    }
  },
  created() {
    this.get_label_name_list()
  },
  methods: {
    get_label_name_list() {
      this.label_name_options = []
      getLabelList({ limit: 999 })
        .then(resp => {
          resp.data.results.map(item => {
            this.label_name_options.push({
              id: item.id,
              mode: item.mode,
              value: item.name,
              product: item.product
            })
          })
          return this.label_name_options
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    get_label_value_list(name) {
      this.label_value_options = []
      getLabelList({ limit: 999, name: name })
        .then(resp => {
          resp.data.results.map(item => {
            this.label_value_options.push({
              id: item.id,
              mode: item.mode,
              value: item.value,
              product: item.product
            })
          })
          return this.label_value_options
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    },
    handle_select(item) {
      this.get_label_value_list(item.value)
    },
    createStateFilter(queryString) {
      return (state) => {
        return (state.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0)
      }
    },
    query_search_label_name(queryString, cb) {
      var restaurants = this.label_name_options
      var results = queryString ? restaurants.filter(this.createStateFilter(queryString)) : restaurants
      cb(results)
    },
    query_search_label_value(queryString, cb) {
      var restaurants = this.label_value_options
      var results = queryString ? restaurants.filter(this.createStateFilter(queryString)) : restaurants
      cb(results)
    },
    add_condition() {
      if (this.label_name === "" || this.label_value === "") {
        return
      }
      this.label_value_list.push({
        name: this.label_name,
        value: this.label_value
      })
      this.label_name = null
      this.label_value = null
    },
    delete_label_value(tag) {
      this.label_value_list.map((item, index) => {
        if (item.value === tag) {
          this.label_value_list.splice(index, 1)
        }
      })
    }
  }
}
</script>

<style scoped>
.el-button {
  vertical-align: top;
}
</style>
