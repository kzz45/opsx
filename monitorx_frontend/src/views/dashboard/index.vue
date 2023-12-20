<template>
  <div class="dashboard-editor-container">
    <panel-group></panel-group>
  </div>
</template>

<script>
import PanelGroup from './PanelGroup'

export default {
  name: 'DashboardAdmin',
  components: {
    PanelGroup
  },
  data() {
    return {
    }
  },
  methods: {
  }
}
</script>

<style lang="scss">
.dashboard-editor-container {
  padding: 32px;
  // background-color: rgb(240, 242, 245);
  position: relative;
}
</style>
