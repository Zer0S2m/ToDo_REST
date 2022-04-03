export default {
	state: {
		importanceFilter: "",
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
		getFilteredNotesByImportance: (state) => (notes) => {
			if ( state.importanceFilter === "ascending" ) notes.sort((note1, note2) => note1.importance > note2.importance ? 1 : -1)
			else if ( state.importanceFilter === "descending" ) notes.sort((note1, note2) => note1.importance < note2.importance ? 1 : -1);

			return notes;
		},
		getFilteredNotesByCategories: (state) => (notes) => {
			return ( state.categoriesFilter.length ) ? 
				notes.filter(note => state.categoriesFilter.includes(note.categorySlug)) : notes;
		}
	}
}