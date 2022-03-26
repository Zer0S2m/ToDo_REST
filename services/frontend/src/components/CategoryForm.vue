<template>
		<div v-if="getIsShowFormCategory" class="modal fade show" id="exampleModal" style="display: block;">
		<div class="modal-dialog modal-dialog modal-dialog-centered">
			<div class="modal-content">
				<div class="modal-header">
					<h5 class="modal-title" id="exampleModalLabel">Create category</h5>
					<button type="button" @click="closeForm" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
				</div>
				<div class="modal-body">
					<form 
						id="create-category-form"
						@submit.prevent=submit
					>
					<div v-if="error">
						<p v-text="error" class="text-danger fs-5"></p>
					</div>
					<div class="mb-3">
						<label for="title-category" class="form-label">Title</label>
						<input
							v-model="titleCategory"
							type="text"
							class="form-control" id="title-category"
						>
					</div>
					<div class="mb-3">
						<label for="slug-category" class="form-label">Slug</label>
						<input
							v-model="slugCategory"
							type="text"
							class="form-control" id="slug-category"
						>
					</div>
				</form>
				</div>
				<div class="modal-footer">
					<button @click="closeForm" type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
					<button type="submit" form="create-category-form" class="btn btn-primary">Send</button>
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
			"getIsShowFormCategory"
		])
	}
}
</script>

<style scoped>
#exampleModal {
	background-color: rgba(0, 0, 0, 0.5);
}
</style>