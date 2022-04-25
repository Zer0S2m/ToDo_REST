export default {
	getters: {
		getFilteredNotesByImportanceLevel: state => (notes, level) => {
			return notes.filter(note => note.importance === level);
		}
	}
}