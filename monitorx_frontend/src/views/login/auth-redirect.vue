<script>
export default {
  name: 'AuthRedirect',
  created() {
    if (this.$route.query.code) {
      // console.log(this.$route.query.code)
      this.$store.dispatch("user/social_login", this.$route.query.code).then(() => {
        this.$outer.push({ path: "/" })
      })
    } else {
      this.$outer.push({ path: "/" })
    }
  }
}
</script>
