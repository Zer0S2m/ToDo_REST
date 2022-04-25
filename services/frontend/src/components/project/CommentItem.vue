<template>
	<div class="comment w100">
		<div class="comment__wrapper df column just-between h100">
			<div class="comment__text">
				<p>
					{{ comment.text }}
				</p>
			</div>
			<div class="comment__area df al-it-center just-between w100">
				<div class="comment__btns df">
					<div class="comment__back-btn df">
						<button
							class="comment__btn primary-btn"
							type="button"
							@click="editNote"
						>
							<img src="@/assets/img/edit.svg" alt="" class="comment__btn-img">
						</button>
					</div>
					<div class="comment__back-btn df">
						<button
							class="comment__btn primary-btn red-btn"
							type="button"
							@click="deleteProjectComment({
								idUrl: comment.id,
								slugProject: slugProject,
								idIndex,
							})"
						>
							<img src="@/assets/img/trash-can.svg" alt="" class="comment__btn-img">
						</button>
					</div>
				</div>
				<div class="comment__date df">
					<time>{{ getPubDate }}</time>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import {
	mapActions,
	mapMutations
} from "vuex";

import getPubDate from "@/filters/date";


export default {
	name: "CommentItem",
	props: {
		comment: Object,
		idIndex: Number,
		slugProject: String
	},
	methods: {
		...mapActions([
			"deleteProjectComment"
		]),
		...mapMutations([
			"setActionFormComment",
			"setEditDataComment",
			"setIsShowFormComment"
		]),
		editNote() {
			this.setEditDataComment({
				idUrl: this.comment.id,
				slugProject: this.$route.params.slugProject,
				idIndex: this.idIndex,
				text: this.comment.text,
			});
			this.setActionFormComment("edit");
			this.setIsShowFormComment(true);
		}
	},
	computed: {
		getPubDate() { return getPubDate(this.comment.pubDate) }
	}
}
</script>