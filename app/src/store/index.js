import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    instances: [],
  },
  mutations: {
    ADD_INSTANCE: (state, instance) => state.instances.push(instance),
    REMOVE_INSTANCE: (state, id) => {
      state.instances = state.instances.filter((instance) => instance.id !== id)
    },
  },
  actions: {
    createInstance: ({ commit }, instance) => {
      commit('ADD_INSTANCE', { ...instance })
    },
    removeInstance: ({ commit }, id) => {
      commit('REMOVE_INSTANCE', id)
    },
  },
  getters: {
    getInstances: (state) => state.instances,
  },
  modules: {},
})
