export default {
	state: {
		importanceFilter: 0,
		categoriesFilter: []
	},
	mutations: {
		setImportanceFilter: function(state, importance) {
			state.importanceFilter = importance;
		},
		setCategoriesFilter: function(state, categories) {
			state.categoriesFilter = categories;
		},
	},
	getters: {
		getImportnceFilter(state) {
			return state.importanceFilter;
		},
		getCategoriesFilter(state) {
			return state.categoriesFilter;
		},
		getFilteredNotesByCategories: (state) => (notes) => {
			return ( state.categoriesFilter.length ) ? 
				notes.filter(note => state.categoriesFilter.includes(note.categorySlug)) : notes;
		},
		getFilteredNotesByImportanceLevel: (state) => (notes, level) => {
			return notes.filter(note => note.importance === level);
		}
	}
}