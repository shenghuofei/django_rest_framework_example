import * as types from './mutation-types.js'

const mutations = {
  [types.AUTHORIZE] (state, payload) {
    state.authorized = payload.authorized
    state.username = payload.username
  }
}

export default mutations
