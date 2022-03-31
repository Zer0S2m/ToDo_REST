import Index from '@/views/Index'
import NoteDetail from '@/views/NoteDetail'
import UserSignUp from '@/views/UserSignUp'
import UserAuth from '@/views/UserAuth'
import ListCategories from '@/views/ListCategories'
import CategoryDetail from '@/views/CategoryDetail'

import axios from "axios"
import store from "@/store"
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
		meta: { 
			requiresAuth: true
		}
	},
	{
		path: '/note/:id',
		name: 'NoteDetail',
		component: NoteDetail,
		meta: { 
			requiresAuth: true
		}
	},
	{
		path: "/category",
		name: "ListCategories",
		component: ListCategories,
		meta: { 
			requiresAuth: true
		}
	},
	{
		path: "/category/:slug",
		name: "CategoryDetail",
		component: CategoryDetail,
		meta: { 
			requiresAuth: true
		}
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
  history: createWebHashHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  if( to.matched.some(record => record.meta.requiresAuth )) {
    if ( store.getters.getInLogin ) {
      next();
      return;
    };
    router.push({
			name: "UserAuth"
		});
  } else {
    next() ;
  };
});


export default router
