<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-tabs
        v-model="active_tab_name"
        @tab-click="active_tab_click"
      >
        <el-tab-pane
          label="账单总览"
          name="bill_chart_setting"
        >
          <el-row
            :gutter="20"
            style="margin-bottom: 10px;"
          >
            <el-col :span="12">
              <PieChart></PieChart>
            </el-col>
            <el-col :span="12">
              <ProjectTable ref="project_table_setting"></ProjectTable>
            </el-col>
          </el-row>
          <!-- <el-row :gutter="20">
            <el-col :span="12">
              <BarChart></BarChart>
            </el-col>
          </el-row> -->
        </el-tab-pane>
        <el-tab-pane
          label="账单明细"
          name="bill_detail_setting"
        >
          <BillDetail ref="bill_detail_setting"></BillDetail>
        </el-tab-pane>
        <el-tab-pane
          label="利用率"
          name="bill_ecs_utils"
        >
          <EcsUtils ref="bill_ecs_utils"></EcsUtils>
        </el-tab-pane>
        <el-tab-pane
          label="账单拆分"
          name="bill_fix_setting"
        >
          <BillSplit ref="bill_fix_setting"></BillSplit>
        </el-tab-pane>
        <el-tab-pane
          label="外部账户"
          name="bill_account_setting"
        >
          <BillAccount ref="bill_account_setting"></BillAccount>
        </el-tab-pane>
        <el-tab-pane
          label="外部产品"
          name="bill_product_setting"
        >
          <BillProduct ref="bill_product_setting"></BillProduct>
        </el-tab-pane>
        <el-tab-pane
          label="内部产品"
          name="bill_project_setting"
        >
          <BillProject ref="bill_project_setting"></BillProject>
        </el-tab-pane>
      </el-tabs>

    </el-card>
  </div>
</template>

<script>
import PieChart from './pie.vue'
import EcsUtils from './utils.vue'
import BillSplit from './split.vue'
import BillDetail from '@/views/bills/detail.vue'
import BillAccount from './account.vue'
import BillProduct from './product.vue'
import BillProject from './project.vue'
import ProjectTable from './project_table.vue'
// import ProjectBar from './project_bar.vue'

export default {
  name: "Bills",
  components: {
    PieChart,
    EcsUtils,
    BillSplit,
    BillDetail,
    BillAccount,
    BillProduct,
    BillProject,
    ProjectTable
    // ProjectBar
  },
  data() {
    return {
      list_query: {
        page: 1,
        limit: 15
      },
      active_tab_name: "bill_chart_setting",
      year_month: ""
    }
  },
  created() {
    // this.$refs.project_table_setting.get_project_list()
  },
  methods: {
    active_tab_click(tab) {
      if (tab.name === "bill_chart_setting") {
        // this.$refs.pie_chart.get_bill_pie()
      } else if (tab.name === "bill_detail_setting") {
        this.$refs.bill_detail_setting.get_bill_list()
      } else if (tab.name === "bill_ecs_utils") {
        this.$refs.bill_ecs_utils.get_utils_list()
        this.$refs.bill_ecs_utils.get_project_list()
      } else if (tab.name === "bill_fix_setting") {
        this.$refs.bill_fix_setting.get_split_list()
      } else if (tab.name === "bill_account_setting") {
        this.$refs.bill_account_setting.get_account_list()
      } else if (tab.name === "bill_product_setting") {
        this.$refs.bill_product_setting.get_product_list()
      } else if (tab.name === "bill_project_setting") {
        this.$refs.bill_project_setting.get_project_list()
      }
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
.chart-wrapper {
  background: #fff;
  padding: 16px 16px 0;
  margin-bottom: 32px;
}
</style>
