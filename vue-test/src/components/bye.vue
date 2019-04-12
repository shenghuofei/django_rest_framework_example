<template lang="pug">
  div(class="hello" style="padding-bottom: 1rem;")
    span(style="font-size: 1.2rem; font-weight: bold;") {{msg}}
    input(type='checkbox' name='agreement' v-model:checked="checked")
    el-checkbox(v-model:checked="checked") 选择?
    input(type='input' class='small' name='agreement' v-model:checked="checked")
    div.block
      span.demonstration 时间
      el-date-picker(type="datetime" placeholder="选择日期时间" value-format="yyyy-MM-dd HH:mm:ss" v-model:date="date")
    div(style="padding-bottom: 1rem;")
      label(for='email') username:
      el-input#email(type='email' style="width: 20%" placeholder='name@email.com' name='email' v-model:username="username")
    el-button(plain type="info" @click="getvue") get
    el-button(round type="danger" @click="postvue") post
    router-link.el-button.round(:to="'/'") 返回
    HelloWorld /* 使用组件 */
</template>

<script>
import HelloWorld from './HelloWorld.vue' /* 导入其他组件 */
import axios from 'axios'
export default {
  data () {
    return {
      checked: true,
      date: '',
      username: '',
      msg: 'bye App'
    }
  },
  components: {
    HelloWorld
  },
  methods: {
    getvue: async function () {
      const response = await axios({
        method: 'get',
        url: 'http://localhost:8000/vue/',
        params: {check: this.checked, username: this.username}
        // data: JSON.stringify({check: 'checked', username: 'username'})
      })
      console.log(response)
      if (response.data.errno === '0') {
        console.log('ok')
      } else {
        console.log('err')
      }
    },
    postvue () {
      axios({
        method: 'post',
        url: 'http://localhost:9000/vue/',
        params: {check: 'checked', username: 'ppppp'},
        data: JSON.stringify({check: 'checked', username: 'username', date: this.date}),
        headers: {'Content-Type': 'application/x-www-form-urlencoded'} /*  解决跨域问题 */
      })
        .then(response => { /* 必须箭头函数才能设置this的data值 */
          this.username = response.data.data
          console.log(response)
        })
        .catch(function (error) {
          console.log(error)
        })
    }
  }
}
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang='scss' scoped>
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
          float: left;
        }
      }
}
</style>
