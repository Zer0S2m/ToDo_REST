import axios from "axios"

import router from "@/router";


export default {
	state: {
		isShowFormNote: false,
		actionForm: false,
		dataEdit: {
			titleNote: "",
			textNote: "",
			categorySlug: "",
			importance: 0
		},
		additionalDataForm: {},
	},
	mutations: {
		setShowFormNote(state, val) {
			state.isShowFormNote = val;
		},
		setAdditionalDataForm(state, data) {
			state.additionalDataForm = data;
		},
		setActionForFormNote(state, val) {
			state.actionForm = val;
		},
		addNote(state, { partDetail, note }) {
			if ( partDetail ) partDetail.notes.unshift(note);
		},
		deleteNote(state, data) {
			if ( data.partDetail ) {
				const notes = data.partDetail.notes;
				for ( let indexNote = 0; indexNote < notes.length; indexNote++ ) {
					if ( notes[indexNote].idNote === data.idNote ) {
						notes.splice(indexNote, 1);
						break;
					};
				};
			};
		},
		editNote(state, { partDetail, newData }) {
			if ( partDetail ) {
				const editNote = partDetail.notes.find(note => note.idNote === newData.idNote);

				editNote.titleNote = newData.titleNote;
				editNote.textNote = newData.textNote;
				editNote.category = newData.category;
				editNote.importance = newData.importance;
				if ( newData.fileName ) editNote.fileName = newData.fileName;
			};
		},
		addNotesInProject(state, { project, notes }) {
			project.notes = notes;
		},
		setDataEditNote(state, data) {
			state.dataEdit = data;
		},
		cleanDataEdit(state) {
			state.dataEdit = {
				titleNote: "",
				textNote: "",
				categoryId: 0,
				importance: 0
			}
		}
	},
	actions: {
		endNote(state, data) {
			const partDetail = state.getters.getPartDetailById(data.idPart);
			const partInProjectPage = state.getters.getPartDetailInProjectPage(data.idPart);

			state.commit("deleteNote", {
				partDetail,
				idNote: data.idNote
			});
			state.commit("changeCountAllNotesInProject", {
				partInProjectPage: partInProjectPage,
				number: -1
			})
			state.commit("reducesCountNotesImportanceLevels", {
				part: partInProjectPage,
				levelImportance: data.levelImportance
			});
		},
		deleteNote(state, data) {
			axios.delete(`/project/${data.slugProject}/note/delete`, {
				data: {
					"idNote": data.idNote
				}
			})
			.then((res) => {
				state.dispatch("endNote", data);
			})
			.catch(error => {
				console.error(error);
			});
		},
		getNotes(state, { slugProject, project }) {
			axios.get(`/project/${slugProject}/note`)
				.then((res) => {
					const notes = res.data;
					state.commit("addNotesInProject", { project, notes });
					console.log(notes);
				})
				.catch((error) => {
					console.error(error);
				})
		},
		async getNote(state, { slugProject, id }) {
			state.commit("lockUi");
			let resNote;

			await axios.get(`/project/${slugProject}/note/${id}`)
			.then((res) => {
				resNote = res.data;
			})
			.catch((error) => {
				console.error(error);
			});

			state.commit("unlockUi");
			return resNote;
		},
		createNote(state, data) {
			const dataFile = new FormData();
			const additionalDataForm = state.getters.getAdditionalDataForm;
			const partDetail = state.getters.getPartDetailBySlug(additionalDataForm.slugPart);
			const currentProjectId = state.getters.getProjectCurrentId(additionalDataForm.slugProject);
			const partInProjectPage = state.getters.getPartDetailInProjectPage(additionalDataForm.idPart);

			dataFile.append("file", data.file);

			axios.post(`/project/${data.slugProject}/note/create`, dataFile, {params: {
				...data,
				partId: additionalDataForm.idPart,
				projectId: currentProjectId,
			}})
			.then((res) => {
				const note = res.data;
				state.commit("addNote", { partDetail, note });
				state.commit("addsCountNotesImportanceLevels", {
					part: partInProjectPage,
					levelImportance: data.importance
				});
				state.commit("changeCountAllNotesInProject", {
					partInProjectPage: partInProjectPage,
					number: 1
				});
			})
			.catch((error) => {
				console.error(error);
			});
		},
		editNote(state, data) {
			const partDetail = state.getters.getPartDetailById(data.partId);
			const additionalDataForm = state.getters.getAdditionalDataForm;
			const dataFile = new FormData();
			dataFile.append("file", data.file);

			axios.put(`/project/${data.slugProject}/note/edit`, dataFile, {
				params: {
					...data,
					...additionalDataForm
			}})
			.then((res) => {
				const newData = res.data;
				state.commit("editNote", { partDetail, newData });
			})
			.catch((error) => {
				console.error(error);
			});
		},
		completeNote(state, data) {
			axios.patch(`/project/${data.slugProject}/note/complete`, {
				idNote: data.idNote
			})
				.then((res) => {
					state.dispatch("endNote", data);
				})
				.catch((error) => {
					console.error(error);
				});
		}
	},
	getters: {
		getShowFormNote: state => state.isShowFormNote,
		getActionForm: state => state.actionForm,
		getDataEdit: state => state.dataEdit,
		getNoteFromPart(state, getters) {
			const parts = getters.getPartsDetail;
			const currentIdNote = parseInt(router.currentRoute.value.params.idNote);

			for ( let partIndex = 0; partIndex < parts.length; partIndex++ ) {
				const part = parts[partIndex];
				const note = part.notes.find(note => note.idNote === currentIdNote);

				if ( note ) return note;
			};
		},
		getAdditionalDataForm: state => state.additionalDataForm,
	},
}