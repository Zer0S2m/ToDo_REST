<template>
	<div class="card" :class="createClassImportance">
		<h5 class="card-header" :class="createClassImportance">Note</h5>
		<div class="card-body">
			<h5 class="card-title">{{ note.titleNote }}</h5>
			<p class="card-text mb-2">
				{{ note.textNote }}
			</p>
			<div
				v-if="note.categorySlug"
				class="mb-3 d-flex"
			>
				<p class="mb-0">
					<span class="fw-bold">Category</span> -
					<router-link 
						:to="{ name: 'CategoryDetail', params: { slug: note.categorySlug } }"
						class="link"
					>
						<span>{{ getCategoryTitle(note.categorySlug) }}</span>
					</router-link>
				</p>
			</div>
			<button
				v-if="note.fileName"
				type="button"
				@click.prevent="
					downloadItem()
				"
				class="card-link d-flex mb-3 card-btn"
			>
			{{ note.fileName }}
			</button>
			<button @click="editNote" type="button" class="btn btn-primary me-2">Edit</button>
			<button @click="toDeleteNote" type="button" class="btn btn-danger">Delete</button>
		</div>
		<div class="card-footer text-muted" :class="createClassImportance">
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
			"getNote",
			"getCategoryTitle"
		]),
		createClassImportance: function() {
			return `importance-${this.note.importance}`;
		},
	},
	created() {
		this.note = this.getNote(parseInt(this.$route.params.id));
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

.card.importance-1 {
	border: 1px solid rgba(110, 219, 128, 0.75);
}

.card.importance-2 {
	border: 1px solid rgba(247, 189, 64, 0.75);
}

.card.importance-3 {
	border: 1px solid rgba(224, 35, 41, 0.75);
}

.card-header.importance-1,
.card-footer.importance-1 {
	background-color: rgba(110, 219, 128, 0.15);
}
.card-header.importance-1 {
	border-bottom: 1px solid rgba(110, 219, 128, 0.75);
}
.card-footer.importance-1 {
	border-top: 1px solid rgba(110, 219, 128, 0.75);
}

.card-header.importance-2,
.card-footer.importance-2 {
	background-color: rgba(247, 189, 64, 0.15);
}
.card-header.importance-2 {
	border-bottom: 1px solid rgba(247, 189, 64, 0.75);
}
.card-footer.importance-2 {
	border-top: 1px solid rgba(247, 189, 64, 0.75);
}

.card-header.importance-3,
.card-footer.importance-3 {
	background-color: rgba(224, 35, 41, 0.15);
}
.card-header.importance-3 {
	border-bottom: 1px solid rgba(224, 35, 41, 0.75);
}
.card-footer.importance-3 {
	border-top: 1px solid rgba(224, 35, 41, 0.75);
}
</style>