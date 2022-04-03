export default {
	state: {
		importanceFilter: "",
		categoriesFilter: [],
		importanceLevelsFilter: []
	},
	mutations: {
		setImportanceFilter: function(state, importance) {
			state.importanceFilter = importance;
		},
		setCategoriesFilter: function(state, categories) {
			state.categoriesFilter = categories;
		},
		setImportanceLevelsFilter: function(state, levels) {
			state.importanceLevelsFilter = levels;
		}
	},
	getters: {
		getImportnceFilter(state) {
			return state.importanceFilter;
		},
		getCategoriesFilter(state) {
			return state.categoriesFilter;
		},
		getImportanceLevelsFilter(state) {
			return state.importanceLevelsFilter;
		},
		getFilteredNotesByImportance: (state) => (notes) => {
			if ( state.importanceFilter === 1 ) notes.sort((note1, note2) => note1.importance > note2.importance ? 1 : -1)
			else if ( state.importanceFilter === -1 ) notes.sort((note1, note2) => note1.importance < note2.importance ? 1 : -1);

			return notes;
		},
		getFilteredNotesByCategories: (state) => (notes) => {
			return ( state.categoriesFilter.length ) ? 
				notes.filter(note => state.categoriesFilter.includes(note.categorySlug)) : notes;
		},
		getFilteredNotesByImportanceLevels: (state) => (notes) => {
			return ( state.importanceLevelsFilter.length ) ? 
				notes.filter(note => state.importanceLevelsFilter.includes(note.importance)) : notes;
		}
	}
}