<template>
	<div v-show="getIsShowFormCategory && getInLogin" class="popup">
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
					<form
					@submit.prevent="submit"
						class="popup-form"
					>
						<div class="primary-error-form" v-if="error">
							<p>
								{{ error }}
							</p>
						</div>
						<div class="popup-form-block df column">
							<label for="title-category" class="primary-label popup-form-label">Title</label>
							<input
								required
								id="title-category"
								v-model="titleCategory"
								type="text"
								class="primary-input popup-form-input"
								placeholder="Title"
							>
						</div>
						<div class="popup-form-block df column">
							<label for="slug-category" class="primary-label popup-form-label">Slug</label>
							<input
								required
								id="slug-category"
								v-model="slugCategory"
								type="text"
								class="primary-input popup-form-input"
								placeholder="Slug"
							>
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
	name: "CategoryForm",
	data() {
		return {
			titleCategory: "",
			slugCategory: "",
			error: ""
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
			if ( !(this.titleCategory && this.slugCategory) ) {
				return;
			};

			this.createCategory({
				slug: this.slugCategory,
				title: this.titleCategory
			})
			.then((res) => {
				if ( res ) {
					this.error = res.detail;
				} else  {
					this.closeForm();
				};
			});
		},
		closeForm() {
			this.setShowFormCategory(false);
			this.titleCategory = "";
			this.slugCategory = "";
			this.error = "";
		}
	},
	computed: {
		...mapGetters([
			"getIsShowFormCategory",
			"getInLogin"
		])
	}
}
</script>