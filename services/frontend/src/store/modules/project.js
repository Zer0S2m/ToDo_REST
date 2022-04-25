import axios from "axios"

import router from "@/router";


export default {
	state: {
		projects: [],
		projectsDetail: [],
		partsDetail: [],
		isShowFormComment: false,
		isShowFormProject: false,
		isShowFormPart: false,
		actionFormComment: "",
		editDataComment: {},
		dataForCreateComment: {}
	},
	mutations: {
		// Project
		setProjects(state, value) {
			state.projects = value;
		},
		createProject(state, project) {
			state.projects.push(project);
		},
		addProjectsDetail(state, project) {
			state.projectsDetail.push(project);
		},
		setShowFormProject(state, value) {
			state.isShowFormProject = value;
		},
		changeCountAllNotesInProject(state, { partInProjectPage, number }) {
			if ( partInProjectPage ) partInProjectPage.countNotes += number;
		},
		reducesCountNotesImportanceLevels(state, { part, levelImportance }) {
			if ( part ) part.countNotesImportanceLevels[levelImportance]--;
		},
		addsCountNotesImportanceLevels(state, { part, levelImportance }) {
			if ( part ) part.countNotesImportanceLevels[levelImportance]++;
		},
		changeCountNotesImportanceLevels(state, data) {
			const currentProject = state.projectsDetail.find(project => project.id === data.idProject);
			if ( currentProject ) {
				const part = currentProject.parts.find(part => part.id === data.idPart);
				part.countNotesImportanceLevels[data.lastImportance]--;
				part.countNotesImportanceLevels[data.newImportance]++;
			};
		},
		// Comment
		deleteProjectComment(state, { listProjects, idIndex }) {
			listProjects.projectDetail.comments.splice(idIndex, 1);
			listProjects.projectBase.comments.splice(idIndex, 1);
		},
		editProjectComment(state, { listProjects, newComment }) {
			listProjects.projectDetail.comments[newComment.id].text = newComment.newText;
			listProjects.projectBase.comments[newComment.id].text = newComment.newText;
		},
		setIsShowFormComment(state, value) {
			state.isShowFormComment = value;
		},
		setEditDataComment(state, data) {
			state.editDataComment = data;
		},
		setActionFormComment(state, action) {
			state.actionFormComment = action;
		},
		setDataForCreateComment(state, data) {
			state.dataForCreateComment = data;
		},
		addProjectComment(state, { newComment, listProjects }) {
			listProjects.projectDetail.comments.push(newComment);
			listProjects.projectBase.comments.push(newComment);
		},
		// Part
		addPartDetail(state, part) {
			state.partsDetail.push(part);
		},
		createPart(state, { newPart, listProjects }) {
			listProjects.projectDetail.parts.unshift(newPart);
			listProjects.projectBase.parts.unshift({
				title: newPart.title,
				slug: newPart.slug,
				id: newPart.id
			});
		},
		setShowFormPart(state, value) {
			state.isShowFormPart = value;
		},
		deletePart(state, { slugPart, listProjects }) {
			const partsProjectBase = listProjects.projectBase.parts
			for ( let indexPart = 0; indexPart < partsProjectBase.length; indexPart++ ) {
				if ( partsProjectBase[indexPart].slug === slugPart ) {
					partsProjectBase.splice(indexPart, 1);
					break;
				};
			};

			const partsProjectDetail = listProjects.projectDetail.parts
			for ( let indexPart = 0; indexPart < partsProjectDetail.length; indexPart++ ) {
				if ( partsProjectDetail[indexPart].slug === slugPart ) {
					partsProjectDetail.splice(indexPart, 1);
					break;
				};
			};

			for ( let indexPart = 0; indexPart < state.partsDetail.length; indexPart++ ) {
				const part = state.partsDetail[indexPart];
				if ( part.slug === slugPart ) {
					state.partsDetail.splice(indexPart, 1);
					break;
				};
			};
		}
	},
	actions: {
		// Project
		getProjects(state) {
			axios.get("/project")
				.then((res) => {
					state.commit("setProjects", res.data);
				})
				.catch((error) => {
					console.error(error);
				});
		},
		createProject(state, data) {
			axios.post(`/project/create`, data)
				.then((res) => {
					state.commit("createProject", res.data);
				})
				.catch((error) => {
					console.error(error);
				});
		},
		async getDetailProject(state, slug) {
			state.commit("lockUi");
			let projectDetail;

			await axios.get(`/project/${slug}`)
				.then((res) => {
					projectDetail = res.data;
					state.commit("addProjectsDetail", projectDetail);
				})
				.catch((error) => {
					console.error(error);
				});

			state.commit("unlockUi");
			return projectDetail;
		},
		// Comment
		deleteProjectComment(state, { idUrl, slugProject, idIndex }) {
			const listProjects = state.getters.getProjectDetailAndBase(slugProject);
			state.commit("deleteProjectComment", { listProjects, idIndex });

			axios.delete(`/project/${slugProject}/comment/delete`, {
				data: {
					id: idUrl
				}
			});
		},
		editProjectComment(state, dataEdit) {
			const listProjects = state.getters.getProjectDetailAndBase(dataEdit.slugProject);
			state.commit("editProjectComment", { listProjects, newComment: { id: dataEdit.idIndex, newText: dataEdit.text } });

			axios.put(`/project/${dataEdit.slugProject}/comment/edit`, {
				id: dataEdit.idUrl,
				text: dataEdit.text
			});
		},
		createProjectComment(state, data) {
			const listProjects = state.getters.getProjectDetailAndBase(data.slugProject);

			axios.post(`/project/${data.slugProject}/comment/create`, data)
				.then((res) => {
					const newComment = res.data;
					state.commit("addProjectComment", { newComment, listProjects });
				});
		},
		// Part
		createPart(state, data) {
			const listProjects = state.getters.getProjectDetailAndBase(data.slugProject);
			data.idProject = listProjects.projectBase.id;

			axios.post(`/project/${data.slugProject}/part/create`, data)
				.then((res) => {
					const newPart = res.data;
					state.commit("createPart", { newPart, listProjects });
				})
				.catch((error) => {
					console.error(error);
				});
		},
		async getDetailPart(state, { slugProject, slugPart }) {
			state.commit("lockUi");
			let detailPart;

			await axios.get(`/project/${slugProject}/part/${slugPart}`)
				.then((res) => {
					detailPart = res.data;
					state.commit("addPartDetail", detailPart);
				})
				.catch((error) => {
					console.error(error);
				});

			state.commit("unlockUi");
			return detailPart;
		},
		deletePart(state, { slugProject, slugPart }) {
			const listProjects = state.getters.getProjectDetailAndBase(slugProject);
			state.commit("deletePart", { slugPart, listProjects });

			axios.delete(`/project/${slugProject}/part/delete`, {
				data: {
					slug: slugPart
				}
			});
		},
		async getPartsInProject(state, slugProject) {
			state.commit("lockUi");
			let parts = [];

			await axios.get(`/project/${slugProject}/part`)
				.then((res) => {
					parts = res.data
				})
				.catch((error) => {
					console.error(error);
				});

			state.commit("unlockUi")
			return parts;
		}
	},
	getters: {
		// Project
		getProjects: state => state.projects,
		getProjectBase: state => slugProject => state.projects.find(project => project.slug === slugProject),
		getProjectDetail: state => slugProject => state.projectsDetail.find(project => project.slug === slugProject),
		getIsShowFormProject: state => state.isShowFormProject,
		getProjectCurrentId: state => slugProject => state.projects.find(project => project.slug === slugProject).id,
		getProjectDetailAndBase: state => slugProject => {
			return {
				projectDetail: state.projectsDetail.find(project => project.slug === slugProject),
				projectBase: state.projects.find(project => project.slug === slugProject)
			}
		},
		// Comment
		getIsShowFormComment: state => state.isShowFormComment,
		getEditDataComment: state => state.editDataComment,
		getActionFormComment: state => state.actionFormComment,
		getDataForCreateComment: state => state.dataForCreateComment,
		// Part
		getPartDetailBySlug: state => slugPart => state.partsDetail.find(part => part.slug === slugPart),
		getPartDetailById: state => id => state.partsDetail.find(part => part.id === id),
		getPartsDetail: state => state.partsDetail,
		getPartDetailInProjectPage: state => id => {
			const currentSlugProjectUrl = router.currentRoute.value.params.slugProject;
			const currentProject = state.projectsDetail.find(project => project.slug === currentSlugProjectUrl);

			if ( currentProject ) {
				const part = currentProject.parts.find(part => part.id === id);
				return part;
			};
		},
		getIsShowFormPart: state => state.isShowFormPart,
	}
}