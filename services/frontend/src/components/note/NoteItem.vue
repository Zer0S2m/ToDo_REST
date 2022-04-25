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
						<button
							type="button"
							class="note-delete df"
							@click="deleteNote({
								slugProject: this.$route.params.slugProject,
								idNote: note.idNote,
								idPart: note.partId,
								levelImportance: note.importance
							})"
						>
							<img src="@/assets/img/delete-note.svg" alt="" class="note-delete-img">
						</button>
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
	},
	methods: {
		...mapActions([
			"deleteNote"
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