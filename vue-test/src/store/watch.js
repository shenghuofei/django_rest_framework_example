const watch = (store) => {
  console.log('store', store)
  store.watch(
    (state) => state.authorized,
    (authorized) => {
      console.log(authorized)
      if (!authorized) {
        const next = window.location.href.replace(window.location.origin, '')
        // window.location = `/users/sso/?next=${encodeURIComponent(next)}`
        window.location = `/api-auth/login/?next=${encodeURIComponent(next)}`
      }
    }
  )
}

export default watch
