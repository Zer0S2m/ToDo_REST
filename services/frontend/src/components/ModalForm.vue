<template>
	<div v-if="getShowModal" class="modal fade show" id="exampleModal" style="display: block;">
		<div class="modal-dialog modal-dialog modal-dialog-centered">
			<div class="modal-content">
				<div class="modal-header">
					<h5 class="modal-title" id="exampleModalLabel">Modal title</h5>
					<button type="button" @click="closeModal" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
				</div>
				<div class="modal-body">
					<form 
						id="create-note-form"
						@submit.prevent=submit
					>
					<div class="mb-3">
						<label for="exampleInputTitle1" class="form-label">Title</label>
						<input
							v-model="titleNote"
							type="text"
							class="form-control" id="exampleInputTitle1"
						>
						<div class="form-text">Title is not required</div>
					</div>
					<div class="mb-3">
						<label for="exampleFormControlTextarea1" class="form-label">Text</label>
						<textarea
							v-model="textNote"
							class="form-control"
							id="exampleFormControlTextarea1"
							rows="3"
							required
						></textarea>
					</div>
					<div class="mb-3">
						<label for="formFileMultiple" class="form-label">Attach file</label>
						<input
							class="form-control"
							type="file"
							id="formFileMultiple"
							ref="file"
							@change="uploadFile()"
						>
						<div class="form-text">File is not required.</div>
					</div>
				</form>
				</div>
				<div class="modal-footer">
					<button @click="closeModal" type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
					<button type="submit" form="create-note-form" class="btn btn-primary">Send</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import {
	mapGetters,
	mapMutations,
	mapActions
} from "vuex";


export default {
	name: "ModalForm",
	data() {
		return {
			titleNote: "",
			textNote: "",
			file: "",
		}
	},
	methods: {
		...mapMutations([
			"setShowModalForm",
			"setActionForFormNote"
		]),
		...mapActions([
			"createNote",
			"editNote"
		]),
		submit() {
			if ( !this.textNote ) {
				return;
			};

			const data = {
				'file': this.file,
				"titleNote": this.titleNote,
				"textNote": this.textNote
			};

			const actionForm = this.getActionForm;

			if ( actionForm === "create" ) this.createNote(data)
			else if ( actionForm === "edit" ) {
				const note = this.getNote(this.$route.params.id);
				this.editNote({...data, note});
			};

			this.closeModal();
		},
		uploadFile() {
			this.file = this.$refs.file.files[0];
		},
		closeModal() {
			this.setShowModalForm(false);
			this.setActionForFormNote(false);

			this.titleNote = "";
			this.textNote = "";
		},
	},
	computed: {
		...mapGetters([
			"getShowModal",
			"getActionForm",
			"getNotes",
			"getNote",
		])
	},
}
</script>

<style scoped>
#exampleModal {
	background-color: rgba(0, 0, 0, 0.5);
}
</style>