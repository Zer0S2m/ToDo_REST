<template>
	<div v-show="getIsShowFormCategory" v-if="getInLogin" class="popup">
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
					<h3 class="popup-title">Add category</h3>
					<form
						@submit.prevent="submit"
						class="popup-form"
					>
						<div class="primary-error-form" v-if="error.server">
							<p>
								{{ error.server }}
							</p>
						</div>
						<div
							class="popup-form-block df column"
							:class="{'primary-error-block': error.title}"
						>
							<label for="title-category" class="primary-label popup-form-label">Title</label>
							<input
								required
								id="title-category"
								v-model="titleCategory"
								type="text"
								class="primary-input popup-form-input"
								placeholder="Title"
								@input="validateTitle"
							>
							<div class="primary-error-body">
								<p>
									{{ error.title }}
								</p>
							</div>
						</div>
						<div
							class="popup-form-block df column"
							:class="{'primary-error-block': error.slug}"
						>
							<label for="slug-category" class="primary-label popup-form-label">Slug</label>
							<input
								required
								id="slug-category"
								v-model="slugCategory"
								type="text"
								class="primary-input popup-form-input"
								placeholder="Slug"
								@input="validateSlug"
							>
							<div class="primary-error-body">
								<p>
									{{ error.slug }}
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
	mapGetters,
	mapMutations,
	mapActions
} from "vuex";


export default {
	name: "CategoryForm",
	data() {
		return {
			titleCategory: "",
			slugCategory: "",
			error: {},
			isValidate: false
		}
	},
	methods: {
		...mapMutations([
			"setShowFormCategory"
		]),
		...mapActions([
			"createCategory"
		]),
		submit() {
			if ( !(this.titleCategory && this.slugCategory) || !this.isValidate ) {
				return;
			};

			this.createCategory({
				category: {
					slug: this.slugCategory,
					title: this.titleCategory
				},
				slugProject: this.$route.params.slugProject
			})
			.then((res) => {
				if ( res ) {
					this.error.server = res.detail;
				} else  {
					this.closeForm();
				};
			});
		},
		closeForm() {
			this.setShowFormCategory(false);
			this.titleCategory = "";
			this.slugCategory = "";
			this.error = {};
			this.isValidate = false;
		}
	},
	computed: {
		...mapGetters([
			"getIsShowFormCategory",
			"getInLogin"
		]),
		validateTitle() {
			if ( this.titleCategory.length > 50 ) {
				this.error.title = "The maximum number of characters for the title is - 50";
				this.isValidate = false;
			}
			else {
				this.error.title = "";
				this.isValidate = true;
			}
		},
		validateSlug() {
			if ( this.slugCategory.length > 50 ) {
				this.error.slug = "The maximum number of characters for the slug is - 50";
				this.isValidate = false;
			}
			else {
				this.error.slug = "";
				this.isValidate = true;
			}
		}
	}
}
</script>