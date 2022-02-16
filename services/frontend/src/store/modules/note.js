import axios from "axios"


export default {
	state: {
		isShowModalForm: false,
		notes: {},
	},
	mutations: {
		setShowModalForm: function(state, val) {
			state.isShowModalForm = val;
		},
		addNote: function(state, newNote) {
			state.notes[newNote.idNote] = {
				"idNote": newNote.idNote,
				"titleNote": newNote.titleNote,
				"textNote": newNote.textNote,
				"pubDate": newNote.pubDate
			};
		},
		deleteNote: function(state, idNote) {
			axios.post(`note/delete`,{
				idNote: idNote
			});
			delete state.notes[idNote];
		},
	},
	actions: {
		setNotes({ state }, notes) {
			state.notes = notes;
		},
	},
	getters: {
		getNotes(state) {
			return state.notes;
		},
		getNote: (state) => (idNote) => {
			return state.notes[idNote];
		},
	},
}