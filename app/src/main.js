import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import VueApexCharts from 'vue-apexcharts'

import './assets/styles/sxcss/index.scss'
import './assets/styles/sxcss/reset.css'
import './assets/styles/main.scss'

Vue.use(VueApexCharts)
Vue.component('Apexchart', VueApexCharts)

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app')
