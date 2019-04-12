import Vue from 'vue'
import Vuex from 'vuex'

import * as actions from './actions.js'
import * as getters from './getters.js'
import mutations from './mutations.js'
import watch from './watch.js'

Vue.use(Vuex)

const state = {
  authorized: true,
  username: ''
}

const store = new Vuex.Store({
  state,
  actions,
  getters,
  mutations,
  strict: process.env.NODE_ENV !== 'production'
})

watch(store)
console.log('store login')
store.dispatch('login')

export default store
