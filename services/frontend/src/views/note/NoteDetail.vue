<template>
	<AppLoader v-if="isUiLocked" />
	<div class="container note-detail-importance" v-if="!isUiLocked" :class="createClassImportance">
		<div class="note-detail">
			<h3 class="note-detail__title">{{ note.titleNote }}</h3>
			<div class="note-detail__text">
				<p>
					{{ note.textNote }}
				</p>
			</div>
			<div class="note-detail__category" v-if="note.category && note.category.title">
				<h3 class="note-detail__category-title">
					<span>Category: </span>
					<router-link
						:to="{
							name: 'CategoryDetail',
							params: {
								slugProject: slugProject,
								slugCategory: note.category.slug
							}
						}"
						class="note-detail__category-link"
					>
						{{ note.category.title }}
					</router-link>
				</h3>
			</div>
			<div class="df note-detail__back-file" v-if="note.fileName">
				<button
					type="button"
				 	class="note-detail__file df al-it-center"
				 	@click="downloadItem"
				>
			 		<span>{{ note.fileName }}</span>
					<img src="@/assets/img/file-black.svg" alt="">
				</button>
			</div>
			<div class="df al-it-center note-detail__btns">
				<button
					type="button"
					class="note-detail__btn primary-btn"
					@click="editNote"
				>
					Edit
				</button>
				<button
					type="button"
					class="note-detail__btn primary-btn red-btn"
					@click="toDeleteNote"
				>
					Delete
				</button>
			</div>
		</div>
	</div>
</template>

<script>
import {
	mapActions,
	mapMutations,
	mapGetters
} from "vuex";

import axios from "axios";

import AppLoader from "@/components/AppLoader.vue";


export default {
	name: "NoteDetail",
	data() {
		return {
			note: {},
		}
	},
	props: {
		slugProject: String,
		idNote: String,
	},
	components: {
		AppLoader
	},
	methods: {
		...mapActions([
			"deleteNote",
			"getNote"
		]),
		...mapMutations([
			"setActionForFormNote",
			"setShowFormNote",
			"setDataEditNote",
			"setAdditionalDataForm"
		]),
		toDeleteNote() {
			this.deleteNote({
				slugProject: this.$route.params.slugProject,
				idNote: this.note.idNote,
				idPart: this.note.partId,
				levelImportance: this.note.importance
			});
			this.$router.push({
				name: "ProjectDetail",
				params: {
					slugProject: this.$route.params.slugProject
				}
			});
		},
		editNote() {
			this.setAdditionalDataForm({
				partId: this.note.partId,
				projectId: this.note.projectId,
				idNote: this.note.idNote
			});
			this.setDataEditNote({
				titleNote: this.note.titleNote,
				textNote: this.note.textNote,
				categoryId: this.note.category.id,
				importance: this.note.importance
			});
			this.setShowFormNote(true);
			this.setActionForFormNote("edit");
		},
    forceFileDownload(response){
      const url = window.URL.createObjectURL(
				new Blob([response.data])
			);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', this.note.fileName);
      document.body.appendChild(link);
      link.click();
    },
		downloadItem(url) {
			url = `/project/${this.slugProject}/note/file/${this.note.fileName}`
      axios.get(url, {
				responseType: 'arraybuffer'
			})
      .then((response) => {
        this.forceFileDownload(response);
      })
      .catch((error) => {
				console.error(error);
			});
		}
	},
	computed: {
		...mapGetters([
			"getNoteFromPart",
			"isUiLocked"
		]),
		createClassImportance() {
			return `note-detail-importance-${this.note.importance}`;
		}
	},
	async created() {
		const note = this.getNoteFromPart;

		if ( !note ) {
			await this.getNote({
				slugProject: this.slugProject,
				id: this.idNote
			})
				.then((res) => {
					this.note = res;
				})
				.catch((error) => {
					console.error(error);
				});
		} else {
			this.note = note;
		};
	}
}
</script>