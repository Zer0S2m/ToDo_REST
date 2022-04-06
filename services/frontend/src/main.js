import { createApp } from 'vue'
import axios from 'axios'

import '@/assets/scss/style.scss';

import App from './App.vue'
import router from './router'
import store from './store'


axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:5000/';

const token = localStorage.getItem("token");
if ( token ) {
	axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
	store.dispatch("getNotes");
	store.dispatch("getCategories");
};

const app = createApp(App);
app.use(store);
app.use(router);
app.mount('#app');
