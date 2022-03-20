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
		}
	},
	actions: {
		setNotes(state, notes) {
			state.commit("setNotes", notes);
		},
		deleteNote: function(state, id) {
			const idNote = state.getters.getNote(id).idNote;

			axios.delete(`note/delete`,{
				data: {
					"idNote": idNote
				}
			}).catch(error => {
				console.error(error)
			});
			state.commit("deleteNote", id);
			state.commit("updateNotes", id);
		},
		getNotes: function(state) {
			axios.get("/note")
				.then((res) => {
					const values = Object.values(res.data.notes);
					for ( let i = 0; i < values.length; i++ ) {
						values[i].id = i;
					};
		
					state.dispatch("setNotes", values);
				})
				.catch((error) => {
					console.error(error);
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
		getShowModal(state) {
			return state.isShowModalForm;
		},
		getActionForm(state) {
			return state.actionForm;
		}
	},
}