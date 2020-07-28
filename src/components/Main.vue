<template>
  <div class="main">
    <h1>{{ msg }}</h1>
    <button @click="btnClk($event, selected)">Click</button>
    <div class="tscroll">
      <table class="tbl tbltop">
        <tr v-for="(art, idx) in arts" :key="idx" class="tbl" @click="selArt($event, art)">
      <td class="tbl">{{ idx }}</td> 
      <!--td>{{ art._id.$oid }}</td-->
      <td class="tbl">{{ art.title }}</td>
      <td>{{ timestamp(art.ts) }}</td>

        </tr>
      </table>
    </div>
  </div>
</template>

<script>
import * as axios from 'axios'

export default {
  name: 'Main',
  props: {
    msg: String
  },
  data () {
    return {
      arts: [],
      clkrslt: 0,
      tstrslt: 0,
      selected: null
    }
  },
  created() {
    let self = this
    axios.get('/arts/')
      .then((resp) => {
        //console.log(resp.data)
        let acts = []
        let data = resp.data.rslt
        for (let jact in data) {
          let act = JSON.parse(data[jact])
          acts.push(act)
        }
        self.arts = acts
        console.log(acts)
      })
      .catch((err) => {
        console.log(err)
      })
  },
  methods: {
    timestamp (ts) {
      let t =  new Date(0)
      let its = Math.round(ts)
      t.setUTCSeconds(its)
      return t.toISOString().substring(0,19)
    },
    selArt(evt, art) {
      let id = art._id.$oid
      this.selected = art
      console.log(id)
      let self = this
      axios.get('/arts/'+id)
      .then((resp) => {
        console.log(resp.data)
        self.clkrslt = JSON.parse(resp.data.rslt)
      })
      .catch((err) => { console.log(err)})
    },
    btnClk(evt, art) {
      let self = this
      //let id = art._id.$oid
      let id = this.selected._id.$oid
      axios.get('/arts/tst/'+id)
      .then((resp) => {
        //console.log(resp.data)
        console.log(self.tstrslt)
        self.tstrslt = resp.data.rslt
      })
      .catch((err) => { console.log(err)})

    }
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.sticky {
  position: absolute;
  left: 0;
  width: 8em;
  top: auto;
}
.tbltop {
 }
.tscroll {
  height: 40em;
  margin-left: 8em;
  overflow-x: scroll;
  overflow-y: visible;
  text-align: left;
}
.tbl {
  border: 1px solid black;
  border-collapse: collapse;
  vertical-align: top;
}

</style>
