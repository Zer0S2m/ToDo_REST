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
			axios.post("/note/create_file", dataFile, {
				headers: {
					'Content-Type': 'multipart/form-data'
				}
			}).then((res) => {
				data.idFile = res.data.idFile;

				axios.post("/note/create", data)
				.then((res) => {
					const note = res.data;
					note["id"] = state.getters.getNotes.length;

					state.commit("addNote", note);
				})
				.catch((error) => {
					console.error(error);
				});
			})
			.catch((error) => {
				console.error(error);
			});
		},
		editNote: function(state, data) {
			const dataFile = new FormData();
			dataFile.append("file", data.file);
			axios.post("/note/create_file", dataFile, {
				headers: {
					'Content-Type': 'multipart/form-data'
				}
			}).then((res) => {
				axios.put("/note/edit", {
					"idNote": data.note.idNote,
					"titleNote": data.titleNote,
					"textNote": data.textNote,
					"fileName": data.note.fileName,
					"newFileName": res.data.fileName,
					"newIdFile": res.data.idFile
				})
				.catch((error) => {
					console.error(error);
				});

				if ( res.data.fileName ) data.fileName = res.data.fileName;

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