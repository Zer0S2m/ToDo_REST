<template>
	<div class="popup" v-show="getIsShowFormComment">
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
					<h3 class="popup-title">Add comment</h3>
					<form
						@submit.prevent="submit"
						class="popup-form"
					>
						<div
							class="popup-form-block df column"
							:class="{'primary-error-block': error.text}"
						>
							<label for="text-comment" class="primary-label popup-form-label">Text</label>
							<input
								required
								id="text-comment"
								v-model="textComment"
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
	name: "CommentForm",
	data() {
		return {
			textComment: "",
			error: {}
		}
	},
	methods: {
		...mapMutations([
			"setIsShowFormComment",
			"setActionFormComment",
			"setEditDataComment"
		]),
		...mapActions([
			"editProjectComment",
			"createProjectComment"
		]),
		submit() {
			const action = this.getActionFormComment;

			if ( action === "edit" ) {
				const data = this.getEditDataComment;
				data.text = this.textComment;
				this.editProjectComment(data);
			} else if ( action === "create" ) {
				const data = this.getDataForCreateComment;
				data.text = this.textComment;
				this.createProjectComment(data);
			};

			this.closeForm();
		},
		closeForm() {
			this.setIsShowFormComment(false);
			this.setActionFormComment(null);
			this.setEditDataComment(null);
			this.textComment = "";
			this.error = {};
		}
	},
	computed: {
		...mapGetters([
			"getIsShowFormComment",
			"getActionFormComment",
			"getEditDataComment",
			"getDataForCreateComment"
		])
	},
	watch: {
		getIsShowFormComment(isShow) {
			if ( isShow && this.getActionFormComment === "edit" ) {
				const editData = this.getEditDataComment;
				this.textComment = editData.text;
			};
		},
	}
}
</script>