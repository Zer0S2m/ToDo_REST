<template>
	<div class="container">
		<ul class="notes-items">
			<NoteItem
				v-for="note in returnNotes" :key="note.id"
				:note="note"
			>
			</NoteItem>
		</ul>
	</div>
</template>

<script>
import {
	mapGetters,
} from "vuex";

import NoteItem from "@/components/NoteItem";


export default {
	name: 'ListNotes',
	components: {
		NoteItem,
	},
	computed: {
		...mapGetters([
			"getNotes",
			"getFilteredNotesByImportance",
			"getFilteredNotesByCategories",
			"getFilteredNotesByImportanceLevels"
		]),
		returnNotes: function() {
			let notes = this.getFilteredNotesByImportance([...this.getNotes]);
			notes = this.getFilteredNotesByCategories(notes);
			notes = this.getFilteredNotesByImportanceLevels(notes);
			return notes;
		}
	},
}
</script>