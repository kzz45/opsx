<template>
  <div>
    <el-card class="box-card">
      <el-row
        :gutter="40"
        class="panel-group"
      >
        <el-col
          :span="6"
          class="card-panel-col"
        >
          <div class="card-panel">
            <div class="card-panel-icon-wrapper icon-message">
              <svg-icon
                icon-class="prometheus"
                class-name="card-panel-icon"
              ></svg-icon>
            </div>
            <div class="card-panel-description">
              <div class="card-panel-text">
                告警数量
              </div>
              <span class="card-panel-num">{{ alert_num }}</span>
            </div>
          </div>
        </el-col>
        <el-col
          :span="6"
          class="card-panel-col"
        >
          <div class="card-panel">
            <div class="card-panel-icon-wrapper icon-message">
              <svg-icon
                icon-class="ecs"
                class-name="card-panel-icon"
              ></svg-icon>
            </div>
            <div class="card-panel-description">
              <div class="card-panel-text">
                监控实例
              </div>
              <span class="card-panel-num">{{ alert_num }}</span>
            </div>
          </div>
        </el-col>
        <!-- <el-col
          :span="6"
          class="card-panel-col"
        >
          <div class="card-panel">
            <div class="card-panel-icon-wrapper icon-shopping">
              <svg-icon
                icon-class="kubernetes"
                class-name="card-panel-icon"
              ></svg-icon>
            </div>
            <div class="card-panel-description">
              <div class="card-panel-text">
                K8S项目
              </div>
              <span class="card-panel-num">{{ k8s_num }}</span>
            </div>
          </div>
        </el-col> -->
        <!-- <el-col
          :span="6"
          class="card-panel-col"
        >
          <div class="card-panel">
            <div class="card-panel-icon-wrapper icon-shopping">
              <svg-icon
                icon-class="deployment"
                class-name="card-panel-icon"
              ></svg-icon>
            </div>
            <div class="card-panel-description">
              <div class="card-panel-text">
                应用数量
              </div>
              <span class="card-panel-num">{{ k8s_num }}</span>
            </div>
          </div>
        </el-col> -->
      </el-row>
      <el-row
        :gutter="40"
        class="panel-group"
      >
        <!-- <el-col
          :span="6"
          class="card-panel-col"
        >
          <div class="card-panel">
            <div class="card-panel-icon-wrapper icon-shopping">
              <svg-icon
                icon-class="gitlab"
                class-name="card-panel-icon"
              ></svg-icon>
            </div>
            <div class="card-panel-description">
              <div class="card-panel-text">
                Git项目
              </div>
              <span class="card-panel-num">{{ k8s_num }}</span>
            </div>
          </div>
        </el-col> -->
        <!-- <el-col
          :span="6"
          class="card-panel-col"
        >
          <div class="card-panel">
            <div class="card-panel-icon-wrapper icon-shopping">
              <svg-icon
                icon-class="ip"
                class-name="card-panel-icon"
              ></svg-icon>
            </div>
            <div class="card-panel-description">
              <div class="card-panel-text">
                出口IP
              </div>
              <span class="card-panel-num">{{ k8s_num }}</span>
            </div>
          </div>
        </el-col> -->
      </el-row>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      alert_num: 0,
      k8s_num: 0
    }
  }
}
</script>

<style lang="scss" scoped>
.card-panel-lang {
  height: 108px;
  cursor: pointer;
  font-size: 18px;
  position: relative;
  overflow: hidden;
  background: #fff;
  box-shadow: 4px 4px 40px rgba(0, 0, 0, 0.05);
  border-color: rgba(0, 0, 0, 0.05);
}
.panel-group {
  margin-top: 18px;

  .card-panel-col {
    margin-bottom: 32px;
  }

  .card-panel {
    height: 108px;
    cursor: pointer;
    font-size: 12px;
    font-weight: bold;
    position: relative;
    overflow: hidden;
    color: #666;
    background: #fff;
    box-shadow: 4px 4px 40px rgba(0, 0, 0, 0.05);
    border-color: rgba(0, 0, 0, 0.05);

    &:hover {
      .card-panel-icon-wrapper {
        color: #fff;
      }

      .icon-people {
        background: #40c9c6;
      }

      .icon-message {
        background: #36a3f7;
      }

      .icon-money {
        background: #f4516c;
      }

      .icon-shopping {
        background: #34bfa3;
      }
    }

    .icon-people {
      color: #40c9c6;
    }

    .icon-message {
      color: #36a3f7;
    }

    .icon-money {
      color: #f4516c;
    }

    .icon-shopping {
      color: #34bfa3;
    }

    .card-panel-icon-wrapper {
      float: left;
      margin: 14px 0 0 14px;
      padding: 16px;
      transition: all 0.38s ease-out;
      border-radius: 6px;
    }

    .card-panel-icon {
      float: left;
      font-size: 48px;
    }

    .card-panel-description {
      float: right;
      font-weight: bold;
      margin: 26px;
      margin-left: 0px;

      .card-panel-text {
        line-height: 18px;
        color: rgba(0, 0, 0, 0.45);
        font-size: 16px;
        margin-bottom: 12px;
      }

      .card-panel-num {
        font-size: 20px;
      }
    }
  }
}

@media (max-width: 550px) {
  .card-panel-description {
    display: none;
  }

  .card-panel-icon-wrapper {
    float: none !important;
    width: 100%;
    height: 100%;
    margin: 0 !important;

    .svg-icon {
      display: block;
      margin: 14px auto !important;
      float: none !important;
    }
  }
}
</style>
