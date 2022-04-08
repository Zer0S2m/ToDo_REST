export default {
	state: {
		importanceFilter: 0,
		categoriesFilter: [],
		textSearch: ""
	},
	mutations: {
		setImportanceFilter: function (state, importance) {
			state.importanceFilter = importance;
		},
		setCategoriesFilter: function (state, categories) {
			state.categoriesFilter = categories;
		},
		setTextSearch: function (state, text) {
			state.textSearch = text;
		}
	},
	getters: {
		getImportnceFilter(state) {
			return state.importanceFilter;
		},
		getCategoriesFilter(state) {
			return state.categoriesFilter;
		},
		getTextSearch(state) {
			return state.textSearch;
		},
		getFilteredNotesByCategories: (state) => (notes) => {
			return (state.categoriesFilter.length) ?
				notes.filter(note => state.categoriesFilter.includes(note.categorySlug)) : notes;
		},
		getFilteredNotesByImportanceLevel: (state) => (notes, level) => {
			return notes.filter(note => note.importance === level);
		},
		getFilteredNotesByTextSearch: (state) => (notes) => {
			return (state.textSearch) ?
				notes.filter(note => {
					if ( note.titleNote.includes(state.textSearch) || note.textNote.includes(state.textSearch) ) return note;
				}) : notes;
		}
	}
}