import * as types from './mutation-types.js'
import axios from 'axios'

export const login = ({ commit }) => {
  console.log('get profile')
  axios({
    method: 'get',
    url: '/accounts/profile/'
  }).then(response => {
    console.log(response)
    if (response.data !== 'failed') {
      const payload = {
        authorized: true,
        username: response.data
      }
      commit(types.AUTHORIZE, payload)
      console.log('ok')
    } else {
      const payload = {
        authorized: false,
        username: response.data
      }
      commit(types.AUTHORIZE, payload)
      console.log('err')
    }
  }).catch(function (error) {
    const payload = {
      authorized: false,
      username: ''
    }
    commit(types.AUTHORIZE, payload)
    console.log(error)
  })
  /* const payload = {
    authorized: true,
    username: 'bbbbbb'
  }
  window.localStorage.setItem('budget.profile', JSON.stringify(payload))
  console.log(JSON.parse(window.localStorage.getItem('budget.profile')))
  commit(types.AUTHORIZE, payload)
  */
}
