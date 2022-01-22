import Vue from 'vue'
import Vuex from 'vuex'
import App from './App';
import axios from 'axios';
import router from './router'


Vue.use(Vuex)

Vue.config.productionTip = false

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:5000/';


const store = new Vuex.Store({
	state: {
		isShowModalForm: false
	},
	mutations: {
		setShowModalForm(state, val) {
			state.isShowModalForm = val
		}
	},
})


new Vue({
	router,
	store: store,
	render: h => h(App)
}).$mount('#app');
