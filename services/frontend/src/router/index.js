import 'bootstrap/dist/css/bootstrap.css';

import Vue from 'vue'
import Router from 'vue-router'
import VueRouter from 'vue-router';
import Index from '@/components/Index'
import NoteDetail from '@/components/NoteDetail'

import axios from "axios"
import { store } from "../store/store"


Vue.use(Router)

const routes = [
	{
		path: '/',
		name: 'Index',
		component: Index
	},
	{
		path: '/note/:id',
		name: 'NoteDetail',
		component: NoteDetail,
	}
]

const router = new VueRouter({
	mode: 'history',
	base: process.env.BASE_URL,
	routes,
})

router.beforeEach((to, from, next) => {
	if ( !Object.keys(store.state.notes).length ) {
		axios.get("/")
		.then((res) => {
			store.dispatch("setNotes", res.data);
			next();
		})
		.catch((error) => {
			console.error(error);
		});
	} else {
		next();
	}
})

export default router
