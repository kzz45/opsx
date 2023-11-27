<template>
  <div class="dashboard-container">
    <PanelGroup></PanelGroup>
  </div>
</template>

<script>
import PanelGroup from './PanelGroup'
import { mapGetters } from "vuex"

export default {
  name: "Dashboard",
  components: {
    PanelGroup
  },
  computed: {
    ...mapGetters(["name"]),
    roles() {
      return this.$store.getters.roles
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
