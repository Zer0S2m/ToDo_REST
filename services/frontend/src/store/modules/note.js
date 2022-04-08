import axios from "axios"


export default {
	state: {
		isShowNoteForm: false,
		actionForm: false,
		notes: [],
		dataEdit: {
			titleNote: "",
			textNote: "",
			categorySlug: "",
			importance: 0
		}
	},
	mutations: {
		setShowNoteForm: function(state, val) {
			state.isShowNoteForm = val;
		},
		setActionForFormNote: function(state, val) {
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
			editNote.categorySlug = data.categorySlug;
			editNote.importance = data.importance;
			if ( data.fileName ) editNote.fileName = data.fileName;
		},
		setNotes(state, notes) {
			state.notes = notes;
		},
		updateNotes(state, id) {
			for ( let i = id; i < state.notes.length; i++ ) {
				const note = state.notes[i];
				note.id -= 1;
			};
		},
		deleteCategoryInNotes(state, categorySlug) {
			state.notes.map((note) => {
				if ( note.categorySlug === categorySlug ) note.categorySlug = null;
			});
		},
		setDataEdit(state, data) {
			state.dataEdit = data;
		},
		cleanDataEdit(state) {
			state.dataEdit = {
				titleNote: "",
				textNote: "",
				categorySlug: "",
				importance: 0
			}
		},
	},
	actions: {
		deleteNote: function(state, id) {
			const idNote = state.getters.getNote(id).idNote;

			axios.delete(`note/delete`, {
				data: {
					"idNote": idNote
				}
			})
			.then((res) => {
				state.commit("deleteNote", id);
				state.commit("updateNotes", id);
			})
			.catch(error => {
				console.error(error)
			});
		},
		getNotes: function(state) {
			axios.get("/note")
				.then((res) => {
					const values = Object.values(res.data.notes);
					for ( let i = 0; i < values.length; i++ ) {
						values[i].id = i;
					};

					state.commit("setNotes", values);
				})
				.catch((error) => {
					state.dispatch("logoutUser");
				});
		},
		getNote: async function(state, id) {
			let resNote;

			await axios.get(`note/${id}`)
			.then((res) => {
				resNote = res.data;
			})
			.catch((error) => {
				console.error(error);
			});

			const notes = state.getters.getNotes;
			const idNoteInArray = notes.find(note => note.idNote === resNote.idNote).id;

			resNote.id = idNoteInArray;

			return resNote;
		},
		createNote: function(state, data) {
			const dataFile = new FormData();
			dataFile.append("file", data.file);
			delete data.file;

			axios.post("/note/create", dataFile, {params: {
				titleNote: data.titleNote,
				textNote: data.textNote,
				categorySlug: data.categorySlug,
				importance: data.importance
			}})
			.then((res) => {
				const note = res.data;
				note["id"] = state.getters.getNotes.length;
				
				if ( !note.fileName ) note.fileName = null;

				state.commit("addNote", note);
			})
			.catch((error) => {
				console.error(error);
			});
		},
		editNote: function(state, data) {
			const dataFile = new FormData();
			dataFile.append("file", data.file);

			axios.put("/note/edit", dataFile, {
				params: {
					"idNote": data.note.idNote,
					"titleNote": data.titleNote,
					"textNote": data.textNote,
					"fileName": data.note.fileName,
					"categorySlug": data.categorySlug,
					"importance": data.importance
			}})
			.then((res) => {
				data.fileName = res.data.fileName;
				state.commit("editNote", data);
			})
			.catch((error) => {
				console.error(error);
			});
		},
	},
	getters: {
		getNotes(state) {
			return state.notes;
		},
		getNote: (state) => (idNote) => {
			return state.notes[idNote];
		},
		getShowNoteForm(state) {
			return state.isShowNoteForm;
		},
		getActionForm(state) {
			return state.actionForm;
		},
		getDataEdit(state) {
			return state.dataEdit;
		}
	},
}