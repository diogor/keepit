import { createStore } from 'vuex'
import VuexPersist from 'vuex-persist'

const vuexPersist = new VuexPersist({
  key: 'keepit',
  storage: window.localStorage
})

export default createStore({
  state: {
    token: null
  },
  mutations: {
    setToken(state, token) {
      state.token = token
    }
  },
  actions: {
  },
  modules: {
  },
  plugins: [vuexPersist.plugin]
})
