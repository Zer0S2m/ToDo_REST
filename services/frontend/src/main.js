import Vue from 'vue'
import App from './App';
import axios from 'axios';
import router from './router'


Vue.config.productionTip = false

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:5000/';

new Vue({
	router,
	render: h => h(App)
}).$mount('#app');
