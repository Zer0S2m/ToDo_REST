<template>
	<div class="card">
		<h5 class="card-header">Note</h5>
		<div class="card-body">
			<h5 class="card-title">{{ note.titleNote }}</h5>
			<p class="card-text">
				{{ note.textNote }}
			</p>
			<button @click="editNote" type="button" class="btn btn-primary">Edit</button>
			<button @click="toDeleteNote" type="button" class="btn btn-danger">Delete</button>
		</div>
		<div class="card-footer text-muted">
			{{ note.pubDate }}
		</div>
	</div>
</template>

<script>
import {
	mapGetters,
	mapActions,
	mapMutations
} from "vuex";


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
			this.deleteNote(this.$route.params.id);
			this.$router.push({
				name: "Index"
			});
		},
		editNote() {
			this.setShowModalForm(true);
			this.setActionForFormNote("edit");
		},
	},
	computed: {
		...mapGetters([
			"getNote"
		])
	},
	created() {
		this.note = this.getNote(this.$route.params.id);
	},
}
</script>

<style scoped>

</style>