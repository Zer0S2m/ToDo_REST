<template>
	<li
		class="note"
		:class="getClassImportance"
	>
		<div class="note-wrapper df h100">
			<div class="note-content df column just-between w100">
				<div class="note-area">
					<div class="note-date df al-it-center just-between w100">
						<time>{{ getPubDate }}</time>
						<div class="note-date-wrapper df al-it-cen" v-if="isTakeAction">
							<button
								type="button"
								class="note-complete note-btn df"
								@click="completeNote({
									slugProject: this.$route.params.slugProject,
									idNote: note.idNote,
									idPart: note.partId,
									levelImportance: note.importance
								})"
							>
								<img src="@/assets/img/complete.svg" alt="" class="note-complete-img note-btn-img">
							</button>
							<button
								type="button"
								class="note-delete note-btn df"
								@click="deleteNote({
									slugProject: this.$route.params.slugProject,
									idNote: note.idNote,
									idPart: note.partId,
									levelImportance: note.importance
								})"
							>
								<img src="@/assets/img/delete-note.svg" alt="" class="note-delete-img note-btn-img">
							</button>
						</div>
					</div>
					<h4 class="note-title">{{ note.titleNote }}</h4>
					<div class="note-text">
						<p>
							{{ note.textNote }}
						</p>
					</div>
				</div>
				<div class="note-back-link df">
					<router-link
						:to="{
							name: 'NoteDetail',
							params: {
								slugProject: this.$route.params.slugProject,
								idNote: note.idNote
							}
						}"
						class="note-link df primary-btn"
					>
						More
					</router-link>
				</div>
			</div>
		</div>
	</li>
</template>

<script>
import { mapActions } from "vuex";

import getPubDate from "@/filters/date";


export default {
	name: "NoteItem",
	props: {
		note: Object,
		isTakeAction: Boolean
	},
	methods: {
		...mapActions([
			"deleteNote",
			"completeNote"
		]),
	},
	computed: {
		getClassImportance() {
			return `importance-${this.note.importance}`;
		},
		getPubDate() { return getPubDate(this.note.pubDate) }
	}
}
</script>