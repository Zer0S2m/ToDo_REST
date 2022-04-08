<template>
	<div class="container note-detail-importance" :class="createClassImportance">
		<div class="note-detail">
			<h3 class="note-detail__title">{{ note.titleNote }}</h3>
			<div class="note-detail__text">
				<p>
					{{ note.textNote }}
				</p>
			</div>
			<div class="note-detail__category" v-if="note.categorySlug">
				<h3 class="note-detail__category-title">
					<span>Category: </span>
					<router-link
						:to="{ name: 'CategoryDetail', params: { slug: note.categorySlug } }"
						class="note-detail__category-link"
					>
						{{ getCategoryTitle(note.categorySlug) }}
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


export default {
	name: "NoteDetail",
	data() {
		return {
			note: {},
		}
	},
	methods: {
		...mapActions([
			"deleteNote"
		]),
		...mapMutations([
			"setActionForFormNote",
			"setShowNoteForm",
			"setDataEdit"
		]),
		toDeleteNote() {
			this.deleteNote(this.note.id);
			this.$router.push({
				name: "ListNotes"
			});
		},
		editNote() {
			this.setShowNoteForm(true);
			this.setActionForFormNote("edit");
			this.setDataEdit({
				titleNote: this.note.titleNote,
				textNote: this.note.textNote,
				categorySlug: this.note.categorySlug,
				importance: this.note.importance
			});
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
			url = `note/file/${this.note.fileName}`
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
			"getNote",
			"getCategoryTitle"
		]),
		createClassImportance: function() {
			return `note-detail-importance-${this.note.importance}`;
		},
	},
	created() {
		this.note = this.getNote(parseInt(this.$route.params.id));
	}
}
</script>