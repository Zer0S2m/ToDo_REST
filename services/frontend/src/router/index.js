import 'bootstrap/dist/css/bootstrap.css';

import Vue from 'vue'
import Router from 'vue-router'
import VueRouter from 'vue-router';
import Index from '@/components/Index'
import NoteDetail from '@/components/NoteDetail'


Vue.use(Router)

const routes = [
	{
		path: '/',
		name: 'Index',
		component: Index
	},
	{
		path: '/note/:id/',
		name: 'NoteDetail',
		component: NoteDetail,
	}
]

const router = new VueRouter({
	mode: 'history',
  	base: process.env.BASE_URL,
	routes,
})

export default router