<template>
  <div>
    <img src="@/assets/logout.png" style="display: block; margin: auto;">
  </div>
</template>

<script>
export default {
  created() {
    const logout_url = process.env.VUE_APP_IDAAS_LOGOUT
    window.open(logout_url, "_blank")
  },
  methods: {
    login() {
      this.$router.push(`/login`)
    }
  }
}
</script>
