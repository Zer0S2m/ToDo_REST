<template>
	<div class="popup" v-show="getIsShowFormProject">
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
					<h3 class="popup-title">Add project</h3>
					<form
						@submit.prevent="submit"
						class="popup-form"
					>
						<div
							class="popup-form-block df column"
							:class="{'primary-error-block': error.title}"
						>
							<label for="title-project" class="primary-label popup-form-label">Title</label>
							<input
								required
								id="title-project"
								v-model="title"
								type="text"
								class="primary-input popup-form-input"
								placeholder="Text"
							>
							<div class="primary-error-body">
								<p>
									{{ error.text }}
								</p>
							</div>
						</div>
						<div
							class="popup-form-block df column"
							:class="{'primary-error-block': error.slug}"
						>
							<label for="slug-project" class="primary-label popup-form-label">Slug</label>
							<input
								required
								id="slug-project"
								v-model="slug"
								type="text"
								class="primary-input popup-form-input"
								placeholder="Text"
							>
							<div class="primary-error-body">
								<p>
									{{ error.slug }}
								</p>
							</div>
						</div>
						<div
							class="popup-form-block df column"
							:class="{'primary-error-block': error.description}"
						>
							<label for="description-project" class="primary-label popup-form-label">Description</label>
							<textarea
								id="description-project"
								cols="30"
								rows="4"
								class="primary-input popup-form-input"
								v-model="description"
								placeholder="Text"
								required
							></textarea>
							<div class="primary-error-body">
								<p>
									{{ error.description }}
								</p>
							</div>
						</div>
						<div class="popup-form-block df al-it-center">
							<button type="submit" class="primary-btn-form">
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
	mapActions,
	mapGetters,
	mapMutations
} from "vuex";


export default {
	name: "ProjectForm",
	data() {
		return {
			description: "",
			title: "",
			slug: "",
			error: {}
		}
	},
	methods: {
		...mapActions([
			"createProject"
		]),
		...mapMutations([
			"setShowFormProject"
		]),
		submit() {
			this.createProject({
				title: this.title,
				slug: this.slug,
				description: this.description,
			});
			this.closeForm();
		},
		closeForm() {
			this.setShowFormProject(false);
			this.title = "";
			this.slug = "";
			this.description = "";
		}
	},
	computed: {
		...mapGetters([
			"getIsShowFormProject"
		])
	}
}
</script>