<template>
  <div>
    <el-card class="box-card">
      <el-date-picker
        v-model="year_month"
        type="month"
        placeholder="按月份搜索"
        size="small"
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
        id="bar"
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

// const animationDuration = 2000
export default {
  name: "BarChart",
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
      year_month: "",
      chart: null,
      x_data: [],
      series_data: []
    }
  },
  // mounted() {
  //   this.$nextTick(() => {
  //     this.initChart()
  //   })
  // },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  },
  created() {
    this.get_bill_pie()
    setTimeout(() => {
      this.initChart()
    }, 1000)
  },
  methods: {
    get_bill_pie() {
      getDisplayList({ limit: 100 }).then(resp => {
        resp.data.results.map(element => {
          this.x_data.push(element.project__name)
          this.series_data.push(element.money)
        })
      })
    },
    initChart() {
      this.chart = this.$echarts.init(document.getElementById('bar'), 'macarons')
      // this.chart = this.$echarts.init(this.$el, 'dark')
      this.chart.setOption({
        // title: {
        //   text: '当前月份',
        //   left: 'center'
        // },
        tooltip: {
          trigger: 'axis',
          axisPointer: { // 坐标轴指示器，坐标轴触发有效
            type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
          }
        },
        grid: {
          // show: true,
          top: 10,
          left: '2%',
          right: '2%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: [{
          type: 'category',
          data: this.x_data,
          axisLabel: {
            interval: 0,
            fontSize: 12,
            rotate: "40"
          }
        }],
        yAxis: [{
          type: 'value'
        }],
        series: [{
          name: '费用',
          type: 'bar',
          data: this.series_data
        }
        ]
      })
    },
    search_month() { }
  }
}
</script>
