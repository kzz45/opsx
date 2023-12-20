<template>
  <div :class="{'has-logo':showLogo}">
    <logo
      v-if="showLogo"
      :collapse="isCollapse"
    />
    <el-scrollbar wrap-class="scrollbar-wrapper">
      <el-menu
        :default-active="activeMenu"
        :collapse="isCollapse"
        :background-color="variables.menuBg"
        :text-color="variables.menuText"
        :unique-opened="true"
        :active-text-color="variables.menuActiveText"
        :collapse-transition="false"
        mode="vertical"
      >
        <sidebar-item
          v-for="route in routes"
          :key="route.path"
          :item="route"
          :base-path="route.path"
        />
      </el-menu>
    </el-scrollbar>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Logo from './Logo'
import SidebarItem from './SidebarItem'
import variables from '@/styles/variables.scss'
import checkPermission from "@/utils/permission"
export default {
  components: { SidebarItem, Logo },
  data() {
    return {
      routes: [],
      levelOne: ["/settings"],
      levelTwoSpec: ["bill"],
      levelTwo: ["bill", "resources", "settings", "config", "silence"]
    }
  },
  computed: {
    ...mapGetters([
      'sidebar'
    ]),
    // routes() {
    //   return this.routes
    // },
    activeMenu() {
      const route = this.$route
      const { meta, path } = route
      // if set path, the sidebar will highlight the path you set
      if (meta.activeMenu) {
        return meta.activeMenu
      }
      return path
    },
    showLogo() {
      return this.$store.state.settings.sidebarLogo
    },
    variables() {
      return variables
    },
    isCollapse() {
      return !this.sidebar.opened
    }
  },
  mounted() {
    // 必须延迟更新，不然数据更新不上去
    setTimeout(() => {
      this.get_routes()
    }, 500)
  },
  methods: {
    checkPermission,
    get_routes() {
      console.log("roles", this.$store.getters.roles)
      const rou = this.$router.options.routes
      for (let i = 0; i < rou.length; i++) {
        if (this.levelOne.includes(rou[i].path) && !checkPermission(['admin', 'ops'])) {
          rou[i].hidden = true
        }
        for (var key in rou[i].children) {
          if (this.levelTwo.includes(rou[i].children[key].path) && !checkPermission(['admin', 'ops'])) {
            rou[i].children[key].hidden = true
          }
          if (this.levelTwoSpec.includes(rou[i].children[key].path) && checkPermission(['finance', 'readonly'])) {
            rou[i].children[key].hidden = false
          }
        }
      }
      this.routes = this.$router.options.routes
      this.$forceUpdate()
    }
  }
}
</script>
