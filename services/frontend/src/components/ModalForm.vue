<template>
	<div v-if="getShowModal" class="modal fade show" id="exampleModal" style="display: block;">
		<div class="modal-dialog modal-dialog modal-dialog-centered">
			<div class="modal-content">
				<div class="modal-header">
					<h5 class="modal-title" id="exampleModalLabel">Create note</h5>
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
						<label for="category-note" class="form-label">Category</label>
						<select class="form-select" id="category-note" v-model="categorySlug">
							<option value="" selected>Select a category</option>
							<option
								v-for="category in getCategories" :key="category.id"
								:value="category.slug"
							>
								{{ category.title }}
							</option>
						</select>
						<div class="form-text">Category is not required</div>
					</div>
					<div class="mb-3">
						<label for="" class="form-label">Degree of importance</label>
						<div class="d-flex align-items-center justify-content-around">
							<input
								class="d-flex align-items-center justify-content-center importance-radio importance-radio-1"
								name="importance-note"
								type="radio"
								label="!"
								value="1"
								v-model="importance"
								@click="checkIsInputRadio"
							>
							<input
								class="d-flex align-items-center justify-content-center importance-radio importance-radio-2"
								name="importance-note"
								type="radio"
								label="!!"
								value="2"
								v-model="importance"
								@click="checkIsInputRadio"
							>
							<input
								class="d-flex align-items-center justify-content-center importance-radio importance-radio-3"
								name="importance-note"
								type="radio"
								label="!!!"
								value="3"
								v-model="importance"
								@click="checkIsInputRadio"
							>
						</div>
						<div class="form-text">Importance is not required</div>
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
			categorySlug: "",
			importance: 0
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
				file: this.file,
				titleNote: this.titleNote,
				textNote: this.textNote,
				categorySlug: this.categorySlug,
				importance: this.importance
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
		checkIsInputRadio() {
			if ( parseInt(this.importance) === parseInt(event.currentTarget.value) ) {
				event.currentTarget.checked = false;
				this.importance = 0;
			};
		},
		closeModal() {
			this.setShowModalForm(false);
			this.setActionForFormNote(false);

			this.titleNote = "";
			this.textNote = "";
			this.file = "";
			this.categorySlug = "";
			this.importance = 0;
		},
	},
	computed: {
		...mapGetters([
			"getShowModal",
			"getActionForm",
			"getNotes",
			"getNote",
			"getCategories"
		])
	},
}
</script>

<style lang="scss" scoped>
#exampleModal {
	background-color: rgba(#000000, 0.5);
}

.importance-radio {
	width: 100%;
	max-width: 40px;
  height: 40px;
  appearance: none;
  outline: 0;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
	color: #ffffff;
  text-transform: uppercase;
  transition: $animate;

	&::before {
		content: attr(label);
	}

	&:checked {
		max-width: 100px;
	}

	&.importance-radio-1 {
		background-color: $color-importance-1;
	}
	&.importance-radio-2 {
		background-color: $color-importance-2;
	}
	&.importance-radio-3 {
		background-color: $color-importance-3;
	}
}
</style>