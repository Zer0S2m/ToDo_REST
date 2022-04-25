<template>
	<div
		v-show="getShowFormNote"
		v-if="getInLogin"
		class="popup"
	>
		<div class="popup-wrapper">
			<div class="popup-container">
				<button
					type="button"
					class="popup-close df"
					@click="closeForm"
				>
					<img src="@/assets/img/delete-note.svg" alt="" class="popup-close-img">
				</button>
				<div class="popup-area">
					<h3 class="popup-title">Add note</h3>
					<form
						class="popup-form"
						@submit.prevent=submit
					>
						<div
							class="popup-form-block df column"
							:class="{'primary-error-block': error.title}"
						>
							<label for="title-note" class="primary-label popup-form-label">Title</label>
							<input
								id="title-note"
								v-model="titleNote"
								type="text"
								class="primary-input popup-form-input"
								placeholder="Title"
								@input="validateTitle"
							>
							<div class="primary-text-form">
								<p>
									Title is not required
								</p>
							</div>
							<div class="primary-error-body">
								<p>
									{{ error.title }}
								</p>
							</div>
						</div>
						<div
							class="popup-form-block df column"
							:class="{'primary-error-block': error.text}"
						>
							<label for="text-note" class="primary-label popup-form-label">Description</label>
							<textarea
								v-model="textNote"
								id="text-note"
								cols="30"
								rows="4"
								class="primary-input popup-form-input"
								placeholder="Text"
								required
								@input="validateText"
							></textarea>
							<div class="primary-error-body">
								<p>
									{{ error.text }}
								</p>
							</div>
						</div>
						<div class="popup-form-block df column">
							<label for="category-note" class="primary-label popup-form-label">Category</label>
							<select
								v-model="categoryId"
								id="category-note"
								class="primary-select"
							>
								<option value="" selected>Select a category</option>
								<option
									v-for="category in getCategoriesByProject" :key="category.id"
									:value="category.id"
								>
									{{ category.title }}
								</option>
							</select>
							<div class="primary-text-form">
								<p>
									Category is not required
								</p>
							</div>
						</div>
						<div class="popup-form-block">
							<label for="" class="primary-label popup-form-label">Degree of importance</label>
							<div class="df al-it-center just-around back-importance">
								<input
									v-for="(importanceObj, index) in importanceSelect" :key="index"
									class="df al-it-center just-center importance-radio"
									:class="importanceObj.class"
									name="importance-note"
									type="radio"
									v-bind="{ label: importanceObj.label, value: importanceObj.value }"
									v-model="importance"
									@click="checkIsInputRadio"
								>
							</div>
							<div class="primary-text-form">
								<p>
									Importance is not required
								</p>
							</div>
						</div>
						<div class="popup-form-block">
							<label for="" class="primary-label popup-form-label">File</label>
							<div class="popup-form-back-file df al-it-center">
								<label for="file-note" class="primary-label popup-form-label popup-form-label-file primary-btn df al-it-center">
									<span>Attach file</span>
									<img src="@/assets/img/file.svg" alt="">
								</label>
								<span class="popup-form-file-text" v-text="fileText"></span>
								<input
									class="primary-file-input popup-form-file"
									type="file"
									id="file-note"
									ref="file"
									@change="uploadFile()"
								>
							</div>
							<div class="primary-text-form">
								<p>
									File is not required
								</p>
							</div>
						</div>
						<div class="popup-form-block df al-it-center">
							<button
								type="submit"
								class="primary-btn-form"
							>
								Send
							</button>
							<button
								class="primary-btn-form-cancel"
								type="button"
								@click="closeForm"
							>
								Cancel
							</button>
						</div>
					</form>
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
	name: "NoteForm",
	data() {
		return {
			titleNote: "",
			textNote: "",
			file: "",
			categoryId: "",
			importance: 0,
			importanceSelect: [
				{ value: 1, label: "!", class: "importance-radio-1" },
				{ value: 2, label: "!!", class: "importance-radio-2" },
				{ value: 3, label: "!!!", class: "importance-radio-3" }
			],
			fileTextBase: "No file choice",
			fileText: "No file choice",
			error: {
				title: "",
				text: ""
			},
			isValidate: false
		}
	},
	methods: {
		...mapMutations([
			"setShowFormNote",
			"setActionForFormNote",
			"cleanDataEdit",
			"changeCountNotesImportanceLevels",
			"setAdditionalDataForm"
		]),
		...mapActions([
			"createNote",
			"editNote"
		]),
		submit() {
			if ( !this.textNote || (this.error.title || this.error.text) ) {
				return;
			};
			const data = {
				file: this.file,
				titleNote: this.titleNote,
				textNote: this.textNote,
				categoryId: (this.categoryId) ? this.categoryId : 0,
				importance: this.importance,
				slugProject: this.$route.params.slugProject
			};

			const actionForm = this.getActionForm;

			if ( actionForm === "create" ) {
				this.createNote({...data});
			} else if ( actionForm === "edit" ) {
				const note = this.getNoteFromPart;
				this.editNote({...note, ...data});

				if ( note ) {
					this.changeCountNotesImportanceLevels({
						newImportance: data.importance,
						lastImportance: note.importance,
						idPart: note.partId,
						idProject: note.projectId
					});
				};
			};

			this.closeForm();
		},
		uploadFile() {
			this.file = this.$refs.file.files[0];

			if ( this.file ) this.fileText = this.file.name
			else this.fileText = this.fileTextBase;
		},
		checkIsInputRadio() {
			if ( parseInt(this.importance) === parseInt(event.currentTarget.value) ) {
				event.currentTarget.checked = false;
				this.importance = 0;
			};
		},
		closeForm() {
			this.setShowFormNote(false);
			this.setActionForFormNote(false);
			this.setAdditionalDataForm(false);

			this.titleNote = "";
			this.textNote = "";
			this.file = "";
			this.categoryId = "";
			this.importance = 0;
			this.fileText = this.fileTextBase;
			this.error = {};
			this.isValidate = false;
		},
	},
	computed: {
		...mapGetters([
			"getShowFormNote",
			"getActionForm",
			"getNoteFromPart",
			"getInLogin",
			"getDataEdit",
			"getCategoriesByProject"
		]),
		validateTitle() {
			if ( this.titleNote.length > 255 ) {
				this.error.title = "The maximum number of characters for the title is - 255";
			}
			else {
				this.error.title = "";
			}
		},
		validateText() {
			if ( this.textNote.length > 1000 ) {
				this.error.text = "The maximum number of characters for the text is - 1000";
			}
			else {
				this.error.text = "";
			}
		},
	},
	watch: {
		getShowFormNote(isShow) {
			const data = this.getDataEdit;
			this.titleNote = data.titleNote;
			this.textNote = data.textNote;
			this.categoryId = (data.categoryId) ? data.categoryId : "";
			this.importance = data.importance;

			this.cleanDataEdit();
		}
	}
}
</script>