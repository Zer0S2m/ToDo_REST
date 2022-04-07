<template>
	<div class="wrapper-notes-items w100">
		<div
			class="add-notes-area df al-it-center just-between"
			:class="classAreaAddNote"
		>
			<h6 class="add-notes-title">{{ titleLevel }}</h6>
		</div>
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
	name: "NoteItems",
	props: {
		levelImportance: Number,
		titleLevel: String,
	},
	data() {
		return {
			classAreaAddNote: `add-notes-area-${this.levelImportance}`
		}
	},
	components: {
		NoteItem
	},
	computed: {
		...mapGetters([
			"getNotes",
			"getFilteredNotesByCategories",
			"getFilteredNotesByImportanceLevel"
		]),
		returnNotes: function() {
			let notes = this.getFilteredNotesByImportanceLevel([...this.getNotes], this.levelImportance);
			notes = this.getFilteredNotesByCategories(notes);

			return notes;
		}
	},
}
</script>