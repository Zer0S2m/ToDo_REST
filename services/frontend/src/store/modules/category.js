import axios from "axios";


export default {
	store: {
		categories: [],
		isShowFormCategory: false
	},
	mutations: {
		setCategories: function(state, val) {
			state.categories = val;
		},
		setShowFormCategory: function(state, val) {
			state.isShowFormCategory = val;
		},
		addCategory: function(state, category) {
			state.categories.push(category);
		},
		deleteCategory: function(state, id) {
			state.categories.splice(id, 1);
		}
	},
	actions: {
		createCategory: async function(state, data) {
			let errorCategory;

			await axios.post("/category/create", data)
			.then((res) => {
				state.commit("addCategory", res.data);
			})
			.catch((error) => {
				errorCategory = error.response.data;
			});

			return errorCategory;
		},
		deleteCategory: function(state, category) {
			axios.delete("/category/delete", {
				data: {
					slug: category.slug
				}
			})
			.then((res) => {
				const resCategoryId = state.getters.getCategory(category.slug);
				state.commit("deleteCategory", resCategoryId);
				state.commit("deleteCategoryInNotes", category.slug);
			})
			.catch((error) => {
				console.error(error);
			});
		},
		getCategories: function(state) {
			axios.get("/category")
			.then((res) => {
				state.commit("setCategories", res.data.categories)
			})
			.catch((error) => {
				state.dispatch("logoutUser");
			});
		},
	},
	getters: {
		getCategories(state) {
			return state.categories;
		},
		getIsShowFormCategory(state) {
			return state.isShowFormCategory;
		},
		getCategory: (state) => (slug) => {
			return state.categories.indexOf(state.categories.find(category => category.slug === slug));
		},
	}
}