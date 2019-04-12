<template lang="pug">
  div
    el-menu(:default-active="activeName" router=true class="el-menu-demo" mode="horizontal" @select="handleClick" background-color="#545c64" text-color="#fff" active-text-color="#ffd04b")
      el-menu-item(index="/") home
      el-menu-item(index="/bye") bye
      el-menu-item(index="/chart") chart
      div(style="text-align: right" text-color="#fff")
        el-menu-item(index="/user") 欢迎,{{ user }}
        el-menu-item(index="/logout") logout
    el-tabs(type="card" v-model="activeName" @tab-click="handleClick")
      el-tab-pane(label="all" name="/bye")
      el-tab-pane(label="home" name="/")
      el-tab-pane(label="chart" name="/chart")
    el-input(v-model:age="age" style="width: 20%" placeholder="请输入内容")
    span {{msg}}
    a(href='https://www.baidu.com' title="for tips这是百度的链接") 百度
    .action(v-if='hasRight')
      ul
        li 编辑
        li 删除

    el-container(style="height: 500px; border: 1px solid #eee")
      div(oncontextmenu="self.event.returnValue=false")
        el-input(placeholder="输入关键字进行过滤" v-model="filterText")
        el-tree(class="filter-tree" :data="treedata" :props="defaultProps" default-expand-all=false :filter-node-method="filterNode" ref="tree2" @node-click="treeclick" @node-contextmenu="mousemenu"  @contextmenu.native='contextmenuTrigger=true' style="background-color: rgb(238, 241, 246)")
      el-container
        el-header(style="text-align: right; font-size: 12px")
          span header
        div(v-for="node of activenode")
          span {{ node }}
        ul.right-click-menu(ref="menu", tabindex="-1" v-if="viewMenu" @blur="closeMenu" :style="{top:top, left:left}")
          li menu1
          li menu2
          li menu3
    div(class="el-table el-table--border")
      table(class="el-table__header-wrapper" cellspacing="0" text-align="center")
        thead
          tr
            th(class="cell") page
            th(class="cell") stage
            th(class="cell") deploy
        tbody
          template(v-for="(h, i) of current")
            tr
              td {{ h.page }}
              td
                el-checkbox(v-model="h.stage" @change="stagechange(i,$event)")
              td
                el-checkbox(v-model="h.deploy")
    el-table(border :data="current" style="width: 100%" )
      el-table-column(type="index")
      el-table-column(prop="page" label="page")
    el-pagination(background layout="prev, pager, next" :total="totalpage" @current-change="pagechange")
    el-button(round type="success" @click="bye") bye
    router-link.el-button(class="el-button is-round" :to="'/bye'") bye
</template>

<script>
import router from '../router/index.js'
import { mapGetters } from 'vuex'

export default {
  name: 'HelloWorld',
  data () {
    return {
      age: 20,
      activenode: [],
      filterText: '',
      // treedata: [],
      treedata: [{
        label: 'meituan',
        children: [{
          label: '二级 1-1',
          children: [{
            label: '三级 1-1-1'
          }, {
            label: '三级 1-1-2'
          }]
        }]
      }, {
        label: 'dianping',
        children: [{
          label: '二级 1-1',
          children: [{
            label: '三级 1-1-1'
          }, {
            label: '三级 1-1-2'
          }]
        }]
      }, {
        label: 'dba',
        children: [{
          label: '二级 1-1',
          children: [{
            label: '三级 1-1-1'
          }, {
            label: '三级 1-1-2'
          }]
        }]
      }, {
        label: 'redis',
        children: [{
          label: '二级 1-1',
          children: [{
            label: '三级 1-1-1'
          }, {
            label: '三级 1-1-2'
          }]
        }]
      }, {
        label: 'eagle',
        children: [{
          label: '二级 1-1',
          children: [{
            label: '三级 1-1-1'
          }, {
            label: '三级 1-1-2'
          }]
        }]
      }, {
        label: 'mafka',
        children: [{
          label: '二级 1-1',
          children: [{
            label: '三级 1-1-1'
          }, {
            label: '三级 1-1-2'
          }]
        }]
      }, {
        label: 'tair',
        children: [{
          label: '二级 1-1',
          children: [{
            label: '三级 1-1-1'
          }, {
            label: '三级 1-1-2'
          }]
        }]
      }, {
        label: 'nginx',
        children: [{
          label: '二级 1-1',
          children: [{
            label: '三级 1-1-1'
          }, {
            label: '三级 1-1-2'
          }]
        }]
      }, {
        label: 'databus',
        children: [{
          label: '二级 1-1',
          children: [{
            label: '三级 1-1-1'
          }, {
            label: '三级 1-1-2'
          }]
        }]
      }, {
        label: 'zookeeper',
        children: [{
          label: '二级 1-1',
          children: [{
            label: '三级 1-1-1'
          }, {
            label: '三级 1-1-2'
          }]
        }]
      }, {
        label: 'resource-pool',
        children: [{
          label: '二级 1-1',
          children: [{
            label: '三级 1-1-1'
          }, {
            label: '三级 1-1-2'
          }]
        }]
      }],
      defaultProps: {
        children: 'children',
        label: 'label'
      },
      node: {},
      current: [{'page': 1, 'stage': true, 'deploy': true}],
      totalpage: 100,
      activeName: this.$route.path,
      hasRight: true,
      msg: 'Welcome to Your Vue.js App',
      rightmenu: false,
      viewMenu: false,
      top: '0px',
      left: '0px'
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
  watch: {
    filterText (val) {
      this.$refs.tree2.filter(val)
    }
  },
  mounted () {
    // this.loadtree()
  },
  methods: {
    loadtree () {
      let { treedata } = this
      treedata = [{
        label: 'meituan',
        children: [{
          label: '二级 1-1',
          children: [{
            label: '三级 1-1-1'
          }, {
            label: '三级 1-1-2'
          }]
        }]
      }]
      this.treedata = treedata
    },
    bye () {
      router.push('/bye')
    },
    handleClick (tab, event) {
      console.log(tab, event)
      console.log(this.activeName)
      if (tab === '/logout') {
        window.location = '/api-auth/logout/?next=/api-auth/login/?next=/'
      } else {
        router.push(this.activeName)
      }
    },
    pagechange (currentPage) {
      this.current = [{'page': currentPage}]
      console.log(currentPage)
    },
    filterNode (value, data) {
      if (!value) return true
      return data.label.indexOf(value) !== -1
    },
    stagechange (index, value) {
      console.log(index, value)
      if (value) {
        this.current[index].deploy = value
      }
    },
    treeclick (data, node, tree) {
      console.log(data, node, tree)
      this.activenode = [node.label]
      for (var l = 0; l < node.level; l++) {
        var pnode = node.parent
        node = pnode
        this.activenode.unshift(pnode.label)
        console.log(pnode.label, l)
      }
      console.log(this.activenode)
    },
    setMenu (top, left) {
      /* let largestHeight = window.innerHeight - this.$refs.menu.offsetHeight - 5
      let largestWidth = window.innerWidth - this.$refs.menu.offsetWidth - 25
      console.log(largestHeight, top)
      console.log(largestWidth, left)
      if (this.$refs.menu.offsetHeight + top + 5 > window.innerHeight) {
        top = top - this.$refs.menu.offsetHeight
      }
      if (this.$refs.menu.offsetWidth + left + 5 > window.innerWidth) {
        left = left - this.$refs.menu.offsetWidth
      }
      if (top > largestHeight) top = largestHeight

      if (left > largestWidth) left = largestWidth */

      this.top = top + 'px'
      this.left = left + 'px'
    },
    closeMenu () {
      this.viewMenu = false
    },
    openMenu (e) {
      // console.log(e)
      this.viewMenu = true
      this.$nextTick(function () {
        this.$refs.menu.focus()
        this.setMenu(e.pageY, e.pageX)
      }/* .bind(this) */)
      e.preventDefault()
    },
    mousemenu (e, data, node) {
      /* this.rightmenu = true
      const menu = this.$refs.menu
      menu.style.display = 'block'
      menu.style.left = e.clientX + 'px'
      menu.style.top = e.clientY + 'px'
      console.log('mouse')
      console.log(e, e.x, e.y)
      console.log(data)
      console.log(node.label, node.level)
      return false
      */
      this.node.label = node.label
      this.node.level = node.level
      console.log('open', this.node)
      this.openMenu(e)
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
