<template>
	<div class="card">
		<h5 class="card-header">Note</h5>
		<div class="card-body">
			<h5 class="card-title">{{ note.title }}</h5>
			<p class="card-text">
				{{ note.text }}
			</p>
			<button type="button" class="btn btn-primary">Edit</button>
			<button @click="deleteNote" type="button" class="btn btn-danger">Delete</button>
		</div>
		<div class="card-footer text-muted">
			{{ note.pubDate }}
		</div>
	</div>
</template>

<script>
import axios from 'axios';


export default {
	name: "NoteDetail",
	data() {
		return {
			note: false
		}
	},
	methods: {
		getNote() {
			axios.get(`/note/${this.$route.params.id}`)
				.then((res) => {
					this.note = res.data;
				})
				.catch((error) => {
					console.error(error);
				});
		},
		deleteNote() {
			axios.post(`note/delete`,{
				noteId: this.$route.params.id
			})
			this.$router.push({
				name: "Index"
			});
		},
	},
	created() {
		this.getNote();
	},
}
</script>

<style scoped>

</style>