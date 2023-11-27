<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-select
        v-model="select_product"
        placeholder="请选择"
        clearable
        filterable
      >
        <el-option
          v-for="(item, index) in product_list"
          :key="index"
          :value="item.id"
          :label="item.name"
        ></el-option>
      </el-select>
    </el-card>
  </div>
</template>

<script>
import { getProductList } from "@/views/settings/apis/product"
export default {
  data() {
    return {
      select_product: "",
      product_list: []
    }
  },
  created() {
    this.get_product_list()
  },
  methods: {
    get_product_list() {
      getProductList({ limit: 100 })
        .then((resp) => {
          this.product_list = resp.data.results
          this.select_product = this.product_list[0].id
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: err
          })
        })
    }
  }
}
</script>
