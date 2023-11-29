<template>
  <div class="app-container">
    <el-card class="box-card">
      <el-alert
        :title="msg"
        type="success"
        class="marquee"
        :closable="false"
      ></el-alert>
      <!-- 步骤条1 -->
      <el-steps
        v-show="stepShow===1"
        :active="activeStepOne"
        finish-status="success"
      >
        <el-step
          title="同步地域"
          :status="step_status[0]"
        ></el-step>
        <el-step
          title="同步可用区"
          :status="step_status[1]"
        ></el-step>
        <el-step
          title="同步网络"
          :status="step_status[2]"
        ></el-step>
        <el-step
          title="同步子网"
          :status="step_status[3]"
        ></el-step>
      </el-steps>
      <!-- 步骤条2 -->
      <el-steps
        v-show="stepShow===2"
        :active="activeStepTwo"
        finish-status="success"
        style="margin-top: 10px"
      >
        <el-step
          title="同步安全组"
          :status="step_status_two[0]"
        ></el-step>
        <el-step
          title="同步镜像"
          :status="step_status_two[1]"
        ></el-step>
        <el-step
          title="同步域名"
          :status="step_status_two[2]"
        ></el-step>
        <el-step
          title="同步证书"
          :status="step_status_two[3]"
        ></el-step>
      </el-steps>
      <!-- 步骤条3 -->
      <el-steps
        v-show="stepShow===3"
        :active="activeStepThree"
        finish-status="success"
        style="margin-top: 10px"
      >
        <el-step
          title="同步机器"
          :status="step_status_three[0]"
        ></el-step>
        <el-step
          title="同步MySQL"
          :status="step_status_three[1]"
        ></el-step>
        <el-step
          title="同步Redis"
          :status="step_status_three[2]"
        ></el-step>
        <el-step
          title="同步负载均衡"
          :status="step_status_three[3]"
        ></el-step>
      </el-steps>
      <div
        v-show="activeStepOne===0"
        style="margin-top: 10px"
        class="step-container"
      >
        <el-row>
          <el-col :span="8">
            <el-card class="box-card">
              <el-select
                v-model="factory_name"
                :disabled="select_disable"
                placeholder="请选择厂商"
                size="small"
              >
                <el-option
                  v-for="item in factory_list"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                >
                </el-option>
              </el-select>
              <el-button
                size="small"
                style="margin-left: 10px"
                icon="el-icon-s-promotion"
                :loading="button_loading"
                @click="sync_region"
              ></el-button>
            </el-card>
          </el-col>
        </el-row>
      </div>
      <div
        v-show="activeStepOne===1"
        style="margin-top: 10px"
        class="step-container"
      >
        <el-row>
          <el-col
            :span="8"
            :offset="4"
          >
            <el-card class="box-card">
              <el-button
                size="small"
                :loading="button_loading"
                @click="step_back"
              >回去</el-button>
              <el-select
                v-model="factory_name"
                :disabled="select_disable"
                placeholder="请选择厂商"
                size="small"
                style="margin-left: 10px"
              >
                <el-option
                  v-for="item in factory_list"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                >
                </el-option>
              </el-select>
              <el-button
                size="small"
                style="margin-left: 10px"
                icon="el-icon-s-promotion"
                :loading="button_loading"
                @click="sync_region"
              ></el-button>
            </el-card>
          </el-col>
        </el-row>
      </div>
      <div
        v-show="activeStepOne===2"
        style="margin-top: 10px"
        class="step-container"
      >
        <el-row>
          <el-col
            :span="8"
            :offset="12"
          >
            <el-card class="box-card">
              <el-button
                size="small"
                :loading="button_loading"
                @click="step_back"
              >回去</el-button>
              <el-select
                v-model="factory_name"
                :disabled="select_disable"
                placeholder="请选择厂商"
                size="small"
                style="margin-left: 10px"
              >
                <el-option
                  v-for="item in factory_list"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                >
                </el-option>
              </el-select>
              <el-button
                size="small"
                style="margin-left: 10px"
                icon="el-icon-s-promotion"
                :loading="button_loading"
                @click="sync_region"
              ></el-button>
            </el-card>
          </el-col>
        </el-row>
      </div>
      <div
        v-show="activeStepOne===3"
        style="margin-top: 10px"
        class="step-container"
      >
        <el-row>
          <el-col
            :span="8"
            :offset="16"
          >
            <el-card class="box-card">
              <el-button
                size="small"
                :loading="button_loading"
                @click="step_back"
              >回去</el-button>
              <el-select
                v-model="factory_name"
                :disabled="select_disable"
                placeholder="请选择厂商"
                size="small"
                style="margin-left: 10px"
              >
                <el-option
                  v-for="item in factory_list"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                >
                </el-option>
              </el-select>
              <el-button
                size="small"
                style="margin-left: 10px"
                icon="el-icon-s-promotion"
                :loading="button_loading"
                @click="sync_region"
              ></el-button>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      msg: '我们正在初始化系统 我们正在初始化系统 我们正在初始化系统 我们正在初始化系统',
      stepShow: 1,
      activeStepOne: 0,
      activeStepTwo: 0,
      activeStepThree: 0,
      step_status: [],
      step_status_two: [],
      step_status_three: [],
      select_disable: false,
      step_disable: false,
      button_loading: false,
      factory_name: 'aliyun',
      factory_list: [{ label: "阿里云", value: "aliyun" }, { label: "腾讯云", value: "qcloud" }]
    }
  },
  created() {
    this.move()
  },
  methods: {
    move() {
      setInterval(() => {
        var start = this.msg.slice(0, 1)
        var end = this.msg.slice(1)
        this.msg = end + start
      }, 200)
    },
    next_step() { },
    step_back() {
      this.activeStepOne--
    },
    sync_region() {
      // console.log(this.factory_name, '=====')
      if (this.factory_name === "") {
        this.$message({
          type: "warning",
          message: "没有选择任何厂商 同步毛线"
        })
        return
      }
      this.activeStepOne++
      this.select_disable = true
    }
  }
}
</script>

<style lang="scss" scoped>
.el-button {
  vertical-align: top;
}
.marquee {
  width: 400px;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  margin: 0 auto;
}
</style>
