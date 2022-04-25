import axios from "axios";

import router from "@/router";


export default {
	store: {
		isShowFormCategory: false
	},
	mutations: {
		setShowFormCategory(state, val) {
			state.isShowFormCategory = val;
		},
		deleteCategory(state, { category, indexArr, listProjects }) {
			listProjects.projectDetail.categories.splice(indexArr, 1);
			listProjects.projectBase.categories.splice(indexArr, 1);
		},
		createCategory(state, { newCategory, listProjects }) {
			listProjects.projectDetail.categories.push(newCategory);
			listProjects.projectBase.categories.push(newCategory);
		}
	},
	actions: {
		async getNotesCategory(state, { slugProject, slugCategory }) {
			state.commit("lockUi");
			let notes = [];

			await axios.get(`/project/${slugProject}/category/${slugCategory}`)
				.then((res) => {
					notes = res.data;
				})
				.catch((error) => {
					console.error(error);
				})

			state.commit("unlockUi");
			return notes;
		},
		async createCategory(state, { category, slugProject }) {
			const listProjects = state.getters.getProjectDetailAndBase(slugProject);
			category.projectId = listProjects.projectDetail.id;
			let errorCategory;

			await axios.post(`/project/${slugProject}/category/create`, category)
				.then((res) => {
					const newCategory = res.data;
					state.commit("createCategory", { newCategory, listProjects });
				})
				.catch((error) => {
					errorCategory = error.response.data;
				});

			return errorCategory;
		},
		deleteCategory(state, { category, slugProject, indexArr }) {
			axios.delete(`/project/${slugProject}/category/delete`, {
				data: {
					slug: category.slug
				}
			})
			.then((res) => {
				const listProjects = state.getters.getProjectDetailAndBase(slugProject);
				state.commit("deleteCategory", { category, indexArr, listProjects });
			})
			.catch((error) => {
				console.error(error);
			});
		},
	},
	getters: {
		getIsShowFormCategory: state => state.isShowFormCategory,
		getNotesByPart: state => (notes, idPart) => notes.filter(note => note.partId === idPart),
		getCategoriesByProject(state, getters) {
			const projectBase = getters.getProjectBase(router.currentRoute.value.params.slugProject);
			if ( projectBase ) return projectBase.categories;
		},
		getNotesByCategory(state, getters) {
			const currentSlugCategory = router.currentRoute.value.params.slugCategory;
			const partsDetail = getters.getPartsDetail;
			let notes = partsDetail.map(partDetail => partDetail.notes).flat();
			notes = notes.filter(note => note.category.slug === currentSlugCategory);
			return notes;
		}
	}
}