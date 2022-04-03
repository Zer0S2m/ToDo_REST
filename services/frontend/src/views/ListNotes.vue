<template>
	<div class="w-75 mx-auto">
		<div class="mb-3">
			<div class="d-flex align-items-center">
				<div class="me-3">
					<Select />
				</div>
				<Categories />
			</div>
		</div>
		<div class="row">
			<NoteItem
				v-for="note in returnNotes" :key="note.id"
				:note="note"
			>
			</NoteItem>
		</div>
	</div>
</template>

<script>
import {
	mapGetters,
} from "vuex";

import NoteItem from "@/components/NoteItem";
import Select from "@/components/filters/Select";
import Categories from "@/components/filters/Categories";


export default {
	name: 'ListNotes',
	components: {
		NoteItem,
		Select,
		Categories
	},
	computed: {
		...mapGetters([
			"getNotes",
			"getFilteredNotesByImportance",
			"getFilteredNotesByCategories"
		]),
		returnNotes: function() {
			let notes = this.getFilteredNotesByImportance([...this.getNotes]);
			notes = this.getFilteredNotesByCategories(notes);
			return notes;
		}
	},
}
</script>