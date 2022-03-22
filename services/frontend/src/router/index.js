import Index from '@/components/Index'
import NoteDetail from '@/components/NoteDetail'
import UserSignUp from '@/components/UserSignUp'
import UserAuth from '@/components/UserAuth'

import axios from "axios"
import store from "@/store/store.js";
import {
	createRouter,
	createWebHashHistory
} from 'vue-router'


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
	{
		path: "/user/auth",
		name: "UserAuth",
		component: UserAuth
	},
	{
		path: "/user/sign-up",
		name: "UserSignUp",
		component: UserSignUp
	}
]

const router = createRouter({
	base: process.env.BASE_URL,
  history: createWebHashHistory(),
  routes
})

if ( store.getters.getToken ) {
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
		};
	});
};

export default router
