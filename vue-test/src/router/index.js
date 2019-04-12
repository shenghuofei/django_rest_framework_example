import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import bye from '@/components/bye'
import hchart from '@/components/hchart'

Vue.use(Router)

export default new Router({
  // mode: (process.env.NODE_ENV === 'development') ? 'history' : 'hash',
  mode: (process.env.NODE_ENV === 'production') ? 'history' : 'hash',
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    }, {
      path: '/bye',
      component: bye
    }, {
      path: '/chart',
      component: hchart
    }, { /* 不存在的路由都跳转到根 */
      path: '*',
      redirect: '/'
    }
  ]
})
