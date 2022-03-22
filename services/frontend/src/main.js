import { createApp } from 'vue'
import axios from 'axios'
import BootstrapVue3 from 'bootstrap-vue-3'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'

import App from './App.vue'
import router from './router'
import store from './store/store'


axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:5000/';

const token = localStorage.getItem("token");
if ( token ) {
	axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
};

const app = createApp(App);
app.use(store);
app.use(router);
app.use(BootstrapVue3);
app.mount('#app');
