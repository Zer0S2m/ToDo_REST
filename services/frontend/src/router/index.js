import 'bootstrap/dist/css/bootstrap.css';

import Vue from 'vue'
import Router from 'vue-router'
import VueRouter from 'vue-router'
import Index from '@/components/Index'
import NoteDetail from '@/components/NoteDetail'

import axios from "axios"
import { store } from "../store/store.js"


Vue.use(Router)

const routes = [
	{
		path: '/',
		redirect: to => {
			return {
				name: "Index"
			};
		}
	},
	{
		path: "/note/",
		name: 'Index',
		component: Index,
	},
	{
		path: '/note/:id',
		name: 'NoteDetail',
		component: NoteDetail,
	},
]

const router = new VueRouter({
	mode: 'history',
	base: process.env.BASE_URL,
	routes,
})

router.beforeEach((to, from, next) => {
	if ( !store.getters.getNotes.length ) {
		axios.get("/note")
		.then((res) => {
			const values = Object.values(res.data.notes);
			for ( let i = 0; i < values.length; i++ ) {
				values[i].id = i;
			};

			store.dispatch("setNotes", values);
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
