<template>
  <div class="main">
    <h1>{{ msg }}</h1>
    <div class="control">
      <button class="btn" @click="btnClk($event, 'names')">P Noun</button>
      <button class="btn" @click="btnClk($event, 'ttree')">title trees</button>
      <button class="btn" @click="btnClk($event, '2')">Click</button>
      <button class="btn" @click="btnClk($event, '3')">Click</button>
      <button class="btn" @click="btnClk($event, '4')">Click</button>
    </div>
    <div class="tscroll">
      <table class="tbl tbltop">
        <tr v-for="(art, idx) in arts" :key="idx" class="tbl" @click="selArt($event, art)">
      <td class="tbl">{{ idx }}</td> 
      <!--td>{{ art._id.$oid }}</td-->
      <td class="tbl">{{ art.title }}</td>
      <td>{{ timestamp(art) }}</td>

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
    let funcs = [
      {name: 'names', func: this.namesRslt },
      {name: 'ttree', func: this.titleTrees }]
    let tf = {}
    for (let f of funcs) {
      tf[f.name] = f
    }
    this.funcs = tf
    console.log(this.funcs)
    let self = this
    axios.get('/arts/')
      .then((resp) => {
        //console.log(resp.data)
        let acts = []
        let data = resp.data.rslt
        for (let jact in data) {
          try {
            let act = JSON.parse(data[jact])
            acts.push(act)
          } catch (err) {
            console.log(err, jact)
          }
        }
        self.arts = acts
        console.log(acts)
      })
      .catch((err) => {
        console.log(err)
      })
  },
  methods: {
    timestamp (art) {
      let ts = art.ts
      if (! ts) {
        console.log(art)
        return new Date()
      } 
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
    namesRslt(data) {
        console.log(data)
    },
    titleTrees(data) {
        let arts = JSON.parse(data)
        for (let art of arts) {
          // should be parsed sentance 
          let id =  art._id
          let tree = art.tree
          let tags = art.tag 
          console.log(id, tags, tree)
        }
    },
    btnClk(evt, art) {
      console.log(art)
      let self = this
      let func = this.funcs[art]
      //console.log(this.funcs, func)
      //let id = art._id.$oid
      let id = this.selected._id.$oid
      axios.get('/arts/'+art+'/'+id)
      .then((resp) => {
        //console.log(resp.data)
        let data = resp.data.rslt
        //console.log(data)
        func.func(data)
      })
      .catch((err) => { console.log(err)})

    }
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.btn {
  margin: 1em;
}
.sticky {
  position: absolute;
  left: 0;
  width: 8em;
  top: auto;
}
.tbltop {
  border: 2px solid #000;
 }
.tscroll {
  height: 40em;
  margin-left: 8em;
  overflow-x: scroll;
  overflow-y: visible;
  text-align: left;
  border: 2px solid #000;
}
.tbl {
  border: 1px solid black;
  border-collapse: collapse;
  vertical-align: top;
}
.control {
  margin: 5px;
}

</style>
