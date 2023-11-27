<template>
  <div>
    <el-select
      v-model="selected_product"
      :selectedproduct="selected_product"
      placeholder="选择产品"
      clearable
      filterable
    >
      <el-option
        v-for="item in product_list"
        :key="item.id"
        :label="'【' + item.id + '】' + item.name"
        :value="item.id"
      >
      </el-option>
    </el-select>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { getProductList } from '@/views/container/apis/product'

export default {
  name: "GlobalProduct",
  props: {
    value: { type: Number, default: 0 }
  },
  data() {
    return {
      selected_product: 0
    }
  },
  computed: {
    ...mapGetters([
      'product_list',
      'current_select_product_id',
      'current_select_product_name'
    ])
  },
  watch: {
    selected_product: function (val) {
      if (val !== this.current_select_product_id) {
        for (var product of this.product_list) {
          if (product.id === val) {
            var current_select_product_name = product.name
          }
        }
        this.$store.commit({
          type: "SET_SELECT_PRODUCT",
          current_select_product_id: val,
          current_select_product_name: current_select_product_name
        })
        this.$emit('input', val)
        this.$emit('change', val)
      }
    },
    value: function () {
      this.selected_product = isNaN(this.value) ? 0 : Number(this.value)
    }
  },
  created() {
    if (this.value) {
      this.selected_product = this.value
    } else {
      this.selected_product = this.current_select_product_id ? parseInt(this.current_select_product_id) : 0
    }
    this.get_product_list()
  },
  methods: {
    get_product_list() {
      getProductList({ limit: 999 })
        .then(resp => {
          resp.data.results.unshift(
            { id: 0, name: '全部' }
          )
          this.$store.commit({
            type: "SET_SELECT_PRODUCT_LIST",
            product_list: resp.data.results
          })
        })
    }
  }
}
</script>
