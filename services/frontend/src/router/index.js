const NoteDetail = () => import("@/views/note/NoteDetail");

const UserSignUp = () => import("@/views/UserSignUp");
const UserAuth = () => import("@/views/UserAuth");

const CategoryDetail = () => import("@/views/category/CategoryDetail");

const ListProject = () => import("@/views/project/ListProject");
const ProjectDetail = () => import("@/views/project/ProjectDetail");
const PageProject = () => import("@/views/project/PageProject");
const PartDetail = () => import("@/views/project/PartDetail");
const PartClosedNotes = () => import("@/views/project/childrenPart/ClosedNotes");
const PartOpenNotes = () => import("@/views/project/childrenPart/OpenNotes");

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
				name: "ListProject"
			};
		}
	},
	{
		path: "/project",
		component: PageProject,
		meta: {
			requiresAuth: true
		},
		children: [
			{
				path: "",
				name: "ListProject",
				component: ListProject
			},
			{
				path: ":slugProject",
				name: "ProjectDetail",
				component: ProjectDetail,
				props: true
			},
			{
				path: ":slugProject/part/:slugPart",
				name: "PartDetail",
				component: PartDetail,
				props: true,
				redirect: to => {
					return {
						name: "PartOpenNotes"
					};
				},
				children: [
					{
						path: "",
						name: "PartOpenNotes",
						component: PartOpenNotes,
						props: true
					},
					{
						path: "completed",
						name: "PartClosedNotes",
						component: PartClosedNotes,
						props: true
					},
				]
			},
			{
				path: ':slugProject/note/:idNote',
				name: 'NoteDetail',
				component: NoteDetail,
				props: true,
			},
			{
				path: ":slugProject/category/:slugCategory",
				name: "CategoryDetail",
				component: CategoryDetail,
				props: true,
			},
		]
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
