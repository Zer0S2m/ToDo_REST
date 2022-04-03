<template>
	<div class="container-content mx-auto">
		<div class="mb-3">
			<div class="d-flex align-items-center">
				<div class="me-3">
					<SelectImportance />
				</div>
				<Categories class="me-3"/>
				<ImportanceLevels class="me-3" />
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
import SelectImportance from "@/components/filters/SelectImportance";
import Categories from "@/components/filters/Categories";
import ImportanceLevels from "@/components/filters/ImportanceLevels";


export default {
	name: 'ListNotes',
	components: {
		NoteItem,
		SelectImportance,
		Categories,
		ImportanceLevels
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