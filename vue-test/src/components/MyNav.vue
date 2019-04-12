<template lang="pug">
  div
    el-menu(:default-active="activeName" router=true class="el-menu-demo" mode="horizontal" @select="handleClick" background-color="#545c64" text-color="#fff" active-text-color="#ffd04b")
      el-menu-item(index="/") home
      el-menu-item(index="/bye") bye
      el-menu-item(index="/chart") chart
      div(style="text-align: right" text-color="#fff")
        el-menu-item(index="/user") 欢迎,{{ user }}
        el-menu-item(index="/logout") logout
</template>

<script>
import router from '../router/index.js'
import { mapGetters } from 'vuex'

export default {
  name: 'MyNav',
  data () {
    return {
      activeName: this.$route.path
    }
  },
  computed: {
    ...mapGetters([
      'username'
    ]),
    user () { // 名字不能和state的getter一样
      console.log(this.username)
      return this.username
    }
  },
  methods: {
    handleClick (tab, event) {
      console.log('tab:', tab, 'event:', event)
      console.log(this.activeName)
      if (tab === '/logout') {
        console.log('out')
        window.location = '/api-auth/logout/?next=/api-auth/login/>next=/'
      } else {
        router.push(this.activeName)
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang='scss' scoped>
.el-header {
  background-color: #B3C0D1;
  color: #333;
  line-height: 60px;
}
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
.action {
    color: #ddd;
      ul {
        overflow: hidden;
        li {
          float: center;
        }
      }
}
.right-click-menu{
    background: #FAFAFA;
    border: 1px solid #BDBDBD;
    box-shadow: 0 2px 2px 0 rgba(0,0,0,.14),0 3px 1px -2px rgba(0,0,0,.2),0 1px 5px 0 rgba(0,0,0,.12);
    display: block;
    list-style: none;
    margin: 0;
    padding: 0;
    position: absolute;
    width: 250px;
    float: left;
    z-index: 999999;
}

.right-click-menu li {
    border-bottom: 1px solid #E0E0E0;
    margin: 0;
    height: 40px;
    width: 100%;
    padding: 0;
    // padding: 5px 35px;
}

.right-click-menu li:last-child {
    border-bottom: none;
}

.right-click-menu li:hover {
    background: #1E88E5;
    color: #FAFAFA;
}
</style>
