import Vue from "vue"
import Vuex from "vuex"


Vue.use(Vuex)


export const store = new Vuex.Store({
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
			delete state.notes[idNote];
		}
	},
	actions: {
		setNotes({ state }, notes) {
			state.notes = notes;
		}
	},
})
