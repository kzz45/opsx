<template>
  <div>
    <el-card class="box-card">
      <el-row :gutter="40" class="panel-group">
        <!-- 机器数量 -->
        <el-col :span="6" class="card-panel-col">
          <div class="card-panel">
            <div class="card-panel-icon-wrapper icon-message">
              <svg-icon
                icon-class="ecs"
                class-name="card-panel-icon"
                @click="go_to_ecs_list"
              ></svg-icon>
            </div>
            <div class="card-panel-description">
              <div class="card-panel-text">
                机器数量
              </div>
              <span class="card-panel-num">{{ ecs_num }}</span>
            </div>
          </div>
        </el-col>
        <!-- MySQL数量 -->
        <el-col :span="6" class="card-panel-col">
          <div class="card-panel">
            <div class="card-panel-icon-wrapper icon-people">
              <svg-icon
                icon-class="mysql_pretty"
                class-name="card-panel-icon"
                @click="go_to_mysql_list"
              ></svg-icon>
            </div>
            <div class="card-panel-description">
              <div class="card-panel-text">
                MySQL数量
              </div>
              <span class="card-panel-num">{{ mysql_num }}</span>
            </div>
          </div>
        </el-col>
        <!-- Redis数量 -->
        <el-col :span="6" class="card-panel-col">
          <div class="card-panel">
            <div class="card-panel-icon-wrapper icon-shopping">
              <svg-icon
                icon-class="redis_red"
                class-name="card-panel-icon"
                @click="go_to_redis_list"
              ></svg-icon>
            </div>
            <div class="card-panel-description">
              <div class="card-panel-text">
                Redis数量
              </div>
              <span class="card-panel-num">{{ redis_num }}</span>
            </div>
          </div>
        </el-col>
        <!-- Mongo数量 -->
        <el-col :span="6" class="card-panel-col">
          <div class="card-panel">
            <div class="card-panel-icon-wrapper icon-shopping">
              <svg-icon
                icon-class="mongodb-tpl"
                class-name="card-panel-icon"
                @click="go_to_mongo_list"
              ></svg-icon>
            </div>
            <div class="card-panel-description">
              <div class="card-panel-text">
                Mongo数量
              </div>
              <span class="card-panel-num">{{ mongodb_num }}</span>
            </div>
          </div>
        </el-col>
        <!-- SLB数量 -->
        <el-col :span="6" class="card-panel-col">
          <div class="card-panel">
            <div class="card-panel-icon-wrapper icon-shopping">
              <svg-icon
                icon-class="slb"
                class-name="card-panel-icon"
                @click="go_to_slb_list"
              ></svg-icon>
            </div>
            <div class="card-panel-description">
              <div class="card-panel-text">
                SLB数量
              </div>
              <span class="card-panel-num">{{ slb_num }}</span>
            </div>
          </div>
        </el-col>
        <!-- 当前告警数量 -->
        <el-col :span="6" class="card-panel-col">
          <div class="card-panel">
            <div class="card-panel-icon-wrapper icon-money">
              <svg-icon
                icon-class="prometheus"
                class-name="card-panel-icon"
                @click="go_alert_list"
              ></svg-icon>
            </div>
            <div class="card-panel-description">
              <div class="card-panel-text">
                告警数量
              </div>
              <span class="card-panel-num">{{ alerts_num }}</span>
            </div>
          </div>
        </el-col>
        <!-- k8s项目 -->
        <el-col :span="6" class="card-panel-col">
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
        </el-col>
        <el-col :span="6" class="card-panel-col">
          <div class="card-panel">
            <div class="card-panel-icon-wrapper icon-shopping">
              <svg-icon
                icon-class="export_ip"
                class-name="card-panel-icon"
                @click="go_to_exportip"
              ></svg-icon>
            </div>
            <div class="card-panel-description">
              <div class="card-panel-text">
                出口IP
              </div>
              <span class="card-panel-num">{{ export_ip_num }}</span>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import { getMachineList } from "@/views/cmdb/api/machine";
import { getMySQLList } from "@/views/cmdb/api/mysql";
import { getRedisList } from "@/views/cmdb/api/redis";
import { getMongodbList } from "@/views/cmdb/api/mongodb";
import { getSLBList } from "@/views/cmdb/api/slb";
import { getAlertWallList } from "@/views/monitor/api/alert_wall";
import { getInstanceList } from "@/views/monitor/api/instance";
import { getExportIPList } from "@/api/export_ip";
// import PieChart from "./pie.vue";
export default {
  components: {
    // PieChart
  },
  data() {
    return {
      listQuery: {
        page: 1,
        limit: 15
      },
      message: "风决定要走 云该怎么挽留",
      listLoading: false,
      ecs_num: 0,
      mysql_num: 0,
      redis_num: 0,
      slb_num: 0,
      script_num: 0,
      alerts_num: 0,
      mongodb_num: 0,
      k8s_num: 0,
      export_ip_num: 0,
      resource_type_list: ["Machine", "MySQL", "Redis", "MongoDB", "SLB"],
      resource_type: "Machine",
      factory_ecs_list: [],
      factory_mysql_list: [],
      factory_redis_list: [],
      factory_mongodb_list: [],
      factory_slb_list: [],
      factory_resource_list: [],
      factory_list: [
        "阿里云",
        "腾讯云",
        "谷歌云",
        "亚马逊",
        "UCloud",
        "首都在线"
      ]
    };
  },
  computed: {
    ...mapGetters(["current_select_product_id", "current_select_product_name"])
  },
  watch: {
    // 全局组件global-product选择变化时 自动刷新表格
    current_select_product_id: function() {
      this.set_list_default();
      this.get_k8s_list();
      this.get_ecs_list();
      this.get_mongodb_list();
      this.get_mysql_list();
      this.get_redis_list();
      this.get_factory_ecs_list();
      this.get_factory_mysql_list();
      this.get_factory_redis_list();
      this.get_factory_mongodb_list();
      this.get_factory_slb_list();
    }
  },
  created() {
    this.get_ecs_list();
    this.get_mysql_list();
    this.get_redis_list();
    this.get_mongodb_list();
    this.get_slb_list();
    this.get_alert_list();
    this.get_k8s_list();
    this.get_exportip_list();
    this.set_factory_resource_list();
    this.get_factory_ecs_list();
    this.get_factory_mysql_list();
    this.get_factory_redis_list();
    this.get_factory_mongodb_list();
    this.get_factory_slb_list();
  },
  methods: {
    set_factory_resource_list() {
      this.selectType();
    },
    set_list_default() {
      this.factory_ecs_list = [];
      this.factory_mysql_list = [];
      this.factory_redis_list = [];
      this.factory_mongodb_list = [];
      this.factory_slb_list = [];
      this.selectType();
    },
    get_factory_ecs_list() {
      for (const key in this.factory_list) {
        const params = {
          external_status: "Running",
          factory__name__contains: this.factory_list[key]
        };
        if (this.current_select_product_id !== 0) {
          params["product__id__in"] = this.current_select_product_id;
        }
        getMachineList(params)
          .then(response => {
            const ecs = {
              factory: this.factory_list[key],
              count: response.data.count
            };
            this.factory_ecs_list.push(ecs);
          })
          .catch(() => {
            this.$message({
              type: "error",
              message: this.message
            });
          });
      }
    },
    get_factory_mysql_list() {
      for (const key in this.factory_list) {
        const params = {
          external_status: "Running",
          factory__name__contains: this.factory_list[key]
        };
        if (this.current_select_product_id !== 0) {
          params["project__product__id"] = this.current_select_product_id;
        }
        getMySQLList(params)
          .then(response => {
            const mysql = {
              factory: this.factory_list[key],
              count: response.data.count
            };
            this.factory_mysql_list.push(mysql);
          })
          .catch(() => {
            this.$message({
              type: "error",
              message: this.message
            });
          });
      }
    },
    get_factory_redis_list() {
      for (const key in this.factory_list) {
        const params = {
          external_status: "Running",
          factory__name__contains: this.factory_list[key]
        };
        if (this.current_select_product_id !== 0) {
          params["project__product__id"] = this.current_select_product_id;
        }
        getRedisList(params)
          .then(response => {
            const redis = {
              factory: this.factory_list[key],
              count: response.data.count
            };
            this.factory_redis_list.push(redis);
          })
          .catch(() => {
            this.$message({
              type: "error",
              message: this.message
            });
          });
      }
    },
    get_factory_mongodb_list() {
      for (const key in this.factory_list) {
        const params = {
          external_status: "Running",
          factory__name__contains: this.factory_list[key]
        };
        if (this.current_select_product_id !== 0) {
          params["project__product__id"] = this.current_select_product_id;
        }
        getMongodbList(params)
          .then(response => {
            const mongo = {
              factory: this.factory_list[key],
              count: response.data.count
            };
            this.factory_mongodb_list.push(mongo);
          })
          .catch(() => {
            this.$message({
              type: "error",
              message: this.message
            });
          });
      }
    },
    get_factory_slb_list() {
      for (const key in this.factory_list) {
        const params = {
          external_status: "Running",
          factory__name__contains: this.factory_list[key]
        };
        if (this.current_select_product_id !== 0) {
          params["product__id__in"] = this.current_select_product_id;
        }
        getSLBList(params)
          .then(response => {
            const slb = {
              factory: this.factory_list[key],
              count: response.data.count
            };
            this.factory_slb_list.push(slb);
          })
          .catch(() => {
            this.$message({
              type: "error",
              message: this.message
            });
          });
      }
    },
    get_ecs_list() {
      const params = "product__id__in";
      const req = {
        external_status: "Running"
      };
      // 如果是选择的产品是全部【0】就展示全部
      if (this.current_select_product_id === 0) {
        req[params] = "";
      } else {
        req[params] = this.current_select_product_id;
      }
      getMachineList(req)
        .then(response => {
          this.ecs_num = response.data.count;
          this.refresh_loading = true;
          setTimeout(() => {
            this.refresh_loading = false;
          }, 1.5 * 1000);
        })
        .catch(() => {
          this.$message({
            type: "error",
            message: this.message
          });
        });
    },
    go_to_ecs_list() {
      this.$router.push("/cmdb/machine");
    },
    get_mysql_list() {
      const params = "project__product__id";
      const req = {};
      if (this.current_select_product_id === 0) {
        req[params] = "";
      } else {
        req[params] = this.current_select_product_id;
      }
      getMySQLList(req)
        .then(response => {
          this.mysql_num = response.data.count;
          this.refresh_loading = true;
          setTimeout(() => {
            this.refresh_loading = false;
          }, 1.5 * 1000);
        })
        .catch(err => {
          this.$message({
            type: "error",
            message: err
          });
        });
    },
    go_to_mysql_list() {
      this.$router.push("/cmdb/mysql");
    },
    get_redis_list() {
      const params = "project__product__id";
      const req = {};
      if (this.current_select_product_id === 0) {
        req[params] = "";
      } else {
        req[params] = this.current_select_product_id;
      }
      getRedisList(req)
        .then(response => {
          this.redis_num = response.data.count;
          this.refresh_loading = true;
          setTimeout(() => {
            this.refresh_loading = false;
          }, 1.5 * 1000);
        })
        .catch(() => {
          this.$message({
            type: "error",
            message: this.message
          });
        });
    },
    get_mongodb_list() {
      const params = "project__product__id";
      const req = {};
      if (this.current_select_product_id === 0) {
        req[params] = "";
      } else {
        req[params] = this.current_select_product_id;
      }
      getMongodbList(req)
        .then(response => {
          this.mongodb_num = response.data.count;
          this.refresh_loading = true;
          setTimeout(() => {
            this.refresh_loading = false;
          }, 1.5 * 1000);
        })
        .catch(() => {
          this.$message({
            type: "error",
            message: this.message
          });
        });
    },
    go_to_mongo_list() {
      this.$router.push("/cmdb/mongodb");
    },
    get_k8s_list() {
      getInstanceList({ instance_type__name: "kubernetes" })
        .then(response => {
          this.k8s_num = response.data.count;
          this.refresh_loading = true;
          setTimeout(() => {
            this.refresh_loading = false;
          }, 1.5 * 1000);
        })
        .catch(() => {
          this.$message({
            type: "error",
            message: this.message
          });
        });
    },
    go_to_redis_list() {
      this.$router.push("/cmdb/redis");
    },
    get_slb_list() {
      delete this.listQuery["status"];
      const params = "product__id__in";
      this.listQuery[params] = this.current_select_product_id;
      // 如果是选择的产品是全部【0】就展示全部
      if (this.current_select_product_id === 0) {
        this.listQuery[params] = "";
      } else {
        this.listQuery[params] = this.current_select_product_id;
      }
      getSLBList(this.listQuery)
        .then(response => {
          this.slb_num = response.data.count;
          this.refresh_loading = false;
          setTimeout(() => {
            this.refresh_loading = false;
          }, 1.5 * 1000);
        })
        .catch(() => {
          this.$message({
            type: "error",
            message: this.message
          });
        });
    },
    go_to_slb_list() {
      this.$router.push("/cmdb/slb");
    },
    go_alert_list() {
      this.$router.push("/monitor/");
    },
    get_alert_list() {
      getAlertWallList({ by_product: 1 }).then(resp => {
        resp.data.forEach(element => {
          this.alerts_num += element.count;
          // console.log(element.count, '---')
        });
      });
    },
    get_exportip_list() {
      getExportIPList({ limit: 999 }).then(resp => {
        this.export_ip_num = resp.data.count;
      });
    },
    go_to_exportip() {
      this.$router.push("/extend/exportip");
    },
    selectType() {
      switch (this.resource_type) {
        case "Machine": {
          this.factory_resource_list = this.factory_ecs_list;
          break;
        }
        case "MySQL": {
          this.factory_resource_list = this.factory_mysql_list;
          break;
        }
        case "Redis": {
          this.factory_resource_list = this.factory_redis_list;
          break;
        }
        case "MongoDB": {
          this.factory_resource_list = this.factory_mongodb_list;
          break;
        }
        case "SLB": {
          this.factory_resource_list = this.factory_slb_list;
          break;
        }
      }
    }
  }
};
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
.el-table {
  margin-top: 15px;
}
</style>
