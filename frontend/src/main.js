import Vue from 'vue'
import App from './App'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import axios from 'axios'
import {
    post,
    get,
    put
} from './http/main'

axios.defaults.baseURL = "http://localhost:8000"
Vue.prototype.$post = post;
Vue.prototype.$put = put;
Vue.prototype.$get = get;
Vue.use(ElementUI)

Vue.prototype.exchange = new Vue();
Vue.prototype.global = global
new Vue({
    el: '#app',
    render: h => h(App)
});
