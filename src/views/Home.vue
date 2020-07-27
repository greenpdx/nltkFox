<template>
  <div class="home">
    <!--img alt="Vue logo" src="../assets/logo.png"-->
    <Main :msg="msg"/>
  </div>
</template>

<script>
// @ is an alias to /src
import Main from '@/components/Main.vue'

export default {
  name: 'Home',
  components: {
    Main
  },
  data () {
    return {
      msg: 'Analyze FoxNews'
    }
  }
}
</script>
