import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    instances: [],
  },
  mutations: {
    ADD_INSTANCE: (state, instance) => state.instances.push(instance),
  },
  actions: {
    createInstance: ({ commit }, instance) => {
      commit('ADD_INSTANCE', { ...instance, fixValue: +instance.fixValue })
    },
  },
  getters: {
    getInstances: (state) => state.instances,
  },
  modules: {},
})
