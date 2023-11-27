<template>
  <div>
    <el-card class="box-card">
      <el-date-picker
        v-model="year_month"
        type="month"
        placeholder="按月份搜索"
        size="small"
        value-format="yyyy-MM"
      >
      </el-date-picker>
      <el-button
        icon="el-icon-search"
        size="small"
        type="primary"
        style="margin-left: 10px;"
        @click="search_month"
      ></el-button>
      <div
        id="pie"
        :class="className"
        :style="{height:height,width:width}"
      ></div>
    </el-card>
  </div>
</template>

<script>
// import * as echarts from 'echarts'
// require('echarts/theme/macarons')
import resize from './mixins/resize'
// import { getBillPie } from '@/views/bills/apis/bill'
import { getDisplayList } from '@/views/bills/apis/display'

export default {
  name: "PieChart",
  mixins: [resize],
  props: {
    className: {
      type: String,
      default: 'chart'
    },
    width: {
      type: String,
      default: '100%'
    },
    height: {
      type: String,
      default: '300px'
    }
  },
  data() {
    return {
      list_query: {
        page: 1,
        limit: 100
      },
      year_month: "",
      chart: null,
      legend_data: [],
      series_data: []
    }
  },
  mounted() {
    this.year_month = this.formatDate(new Date())
  },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  },
  created() {
    this.get_bill_pie()
  },
  methods: {
    formatDate(date) {
      var d = new Date(date)
      var year = d.getFullYear()
      var month = "" + d.getMonth()
      if (month.length < 2) month = "0" + month
      return [year, month].join("-")
    },
    get_bill_pie() {
      getDisplayList(this.list_query).then(resp => {
        resp.data.results.map(element => {
          this.legend_data.push(element.project__name)
          this.series_data.push({
            name: element.project__name,
            value: element.money
          })
          if (this.chart) {
            this.chart.dispose()
            this.chart = null
          }
          this.chart = this.$echarts.init(
            document.getElementById("pie"),
            "macarons"
          )
          this.chart.setOption({
            tooltip: {
              trigger: "item",
              formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            series: [
              {
                name: "费用占比",
                type: "pie",
                radius: ["30%", "80%"],
                emphasis: {
                  label: {
                    show: true,
                    fontSize: "20",
                    fontWeight: "bold"
                  }
                },
                data: this.series_data
              }
            ]
          })
        })
      })
    },
    search_month() {
      const params = "ymd"
      this.list_query[params] = this.year_month
      this.legend_data = []
      this.series_data = []
      getDisplayList(this.list_query).then(resp => {
        resp.data.results.map(element => {
          this.legend_data.push(element.project__name)
          this.series_data.push({
            name: element.project__name,
            value: element.money
          })
          this.chart = this.$echarts.init(
            document.getElementById("pie"),
            "macarons"
          )
          this.chart.setOption({
            tooltip: {
              trigger: "item",
              formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            series: [
              {
                name: "费用占比",
                type: "pie",
                radius: ["30%", "80%"],
                emphasis: {
                  label: {
                    show: true,
                    fontSize: "20",
                    fontWeight: "bold"
                  }
                },
                data: this.series_data
              }
            ]
          })
        })
      })
    }
  }
}
</script>
