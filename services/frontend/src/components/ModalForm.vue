<template>
	<div v-if="this.$store.state.note.isShowModalForm" class="modal fade show" id="exampleModal" style="display: block;">
		<div class="modal-dialog modal-dialog modal-dialog-centered">
			<div class="modal-content">
				<div class="modal-header">
					<h5 class="modal-title" id="exampleModalLabel">Modal title</h5>
					<button type="button" @click="closeModal" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
				</div>
				<div class="modal-body">
					<form id="create-note-form">
						<div class="mb-3">
							<label for="exampleInputTitle1" class="form-label">Title</label>
							<input v-model="titleNote" type="text" class="form-control" id="exampleInputTitle1" aria-describedby="emailHelp">
							<div id="emailHelp" class="form-text">header is not required</div>
						</div>
						<div class="mb-3">
							<label for="exampleFormControlTextarea1" class="form-label">Text</label>
							<textarea v-model="textNote" class="form-control" id="exampleFormControlTextarea1" rows="3" required></textarea>
						</div>
				</form>
				</div>
				<div class="modal-footer">
					<button @click="closeModal" type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
					<button @click="createNote" type="submit" form="create-note-form" class="btn btn-primary">Add note</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import axios from 'axios';


export default {
	name: "ModalForm",
	data() {
		return {
			titleNote: "",
			textNote: "",
			note: "",
		}
	},
	methods: {
		closeModal() {
			this.$store.commit("setShowModalForm", false);
		},
		createNote() {
			if ( !this.textNote ) {
				return;
			};

			this.closeModal();

			axios.post("/note/create", {
				titleNote: this.titleNote,
				textNote: this.textNote,
			})
			.then((res) => {
				const note = res.data;
				this.$store.commit("addNote", note);

				this.redirectToNote(note.idNote);
			})	
			.catch((error) => {
				console.log(error);
			});

			this.titleNote = "";
			this.textNote = "";
		},
		redirectToNote(idNote) {
			this.$router.push({
				name: "NoteDetail",
				params: {
					id: idNote
				},
			});
		},
	},
}
</script>

<style scoped>
#exampleModal {
	background-color: rgba(0, 0, 0, 0.5);
}
</style>