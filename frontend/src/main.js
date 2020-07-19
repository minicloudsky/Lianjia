import Vue from 'vue'
import App from './App'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import axios from 'axios'
Vue.use(ElementUI)

Vue.prototype.exchange = new Vue();
Vue.prototype.global = global
Vue.prototype.$http = axios
new Vue({
  el: '#app',
  render: h => h(App)
});
