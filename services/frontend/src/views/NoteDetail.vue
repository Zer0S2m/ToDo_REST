<template>
	<div class="card">
		<h5 class="card-header">Note</h5>
		<div class="card-body">
			<h5 class="card-title">{{ note.titleNote }}</h5>
			<p class="card-text mb-0">
				{{ note.textNote }}
			</p>
			<button
				type="button"
				@click.prevent="
					downloadItem()
				"
				class="card-link d-flex mt-2 mb-3 card-btn"
			>
			{{ note.fileName }}
			</button>
			<button @click="editNote" type="button" class="btn btn-primary me-2">Edit</button>
			<button @click="toDeleteNote" type="button" class="btn btn-danger">Delete</button>
		</div>
		<div class="card-footer text-muted">
			{{ note.pubDate }}
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
			"setShowModalForm"
		]),
		toDeleteNote() {
			this.deleteNote(this.note.id);
		},
		editNote() {
			this.setShowModalForm(true);
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
			"getNote"
		])
	},
	created() {
		this.note = this.getNote(this.$route.params.id);
	}
}
</script>

<style scoped>
.card-btn {
	outline: none;
	border: none;
	background-color: transparent;
	padding: 0;
	color: #0d6efd;
  text-decoration: underline;
}
</style>