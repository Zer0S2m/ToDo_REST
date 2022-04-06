<template>
	<div class="container">
		<ul class="notes-items">
			<NoteItem
				v-for="note in getNotes" :key="note.id"
				:note="note"
			>
			</NoteItem>
		</ul>
	</div>
</template>

<script>
import { mapGetters } from "vuex";

import NoteItem from "@/components/NoteItem";


export default {
	name: "CategoryDetail",
	components: {
		NoteItem,
	},
	computed: {
		...mapGetters([
			"getNotesCategory",
			"getFilteredNotesByImportance",
			"getFilteredNotesByImportanceLevels"
		]),
		getNotes: function() {
			let notes = this.getNotesCategory(this.$route.params.slug);
			notes = this.getFilteredNotesByImportance(notes);
			notes = this.getFilteredNotesByImportanceLevels(notes);
			return notes;
		}
	},
}
</script>