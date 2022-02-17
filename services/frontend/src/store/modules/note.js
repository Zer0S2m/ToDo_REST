import axios from "axios"


export default {
	state: {
		isShowModalForm: false,
		actionForm: false,
		notes: [],
	},
	mutations: {
		setShowModalForm: function(state, val) {
			state.isShowModalForm = val;
		},
		setActionForFormNote(state, val) {
			state.actionForm = val;
		},
		addNote: function(state, note) {
			state.notes.push(note);
		},
		deleteNote: function(state, idNote) {
			state.notes.splice(idNote, 1);
		},
		editNote: function(state, data) {
			const editNote = state.notes[data.note.id];

			editNote.titleNote = data.titleNote;
			editNote.textNote = data.textNote;
		},
		setNotes(state, notes) {
			state.notes = notes;
		},
		updateNotes(state, id) {
			for ( let i = id; i < state.notes.length; i++ ) {
				const note = state.notes[i];
				note.id -= 1;
			};
		}
	},
	actions: {
		setNotes(state, notes) {
			state.commit("setNotes", notes);
		},
		deleteNote: function(state, id) {
			const idNote = state.getters.getNote(id).idNote;

			axios.post(`note/delete`,{
				idNote: idNote
			});
			state.commit("deleteNote", id);
			state.commit("updateNotes", id);
		},
		createNote: function(state, data) {
			axios.post("/note/create", {
				titleNote: data.titleNote,
				textNote: data.textNote,
			})
			.then((res) => {
				const note = res.data;
				note["id"] = state.getters.getNotes.length;

				state.commit("addNote", note);
			})
			.catch((error) => {
				console.log(error);
			});
		},
		editNote: function(state, data) {
			axios.post("/note/edit", {
				"idNote": data.note.idNote,
				"titleNote": data.titleNote,
				"textNote": data.textNote,
			})
			.catch((error) => {
				console.log(error);
			});

			state.commit("editNote", data);
		},
	},
	getters: {
		getNotes(state) {
			return state.notes;
		},
		getNote: (state) => (idNote) => {
			return state.notes[idNote];
		},
		getShowModal(state) {
			return state.isShowModalForm;
		},
		getActionForm(state) {
			return state.actionForm;
		}
	},
}