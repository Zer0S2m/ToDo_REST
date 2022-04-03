<template>
	<div class="container-content mx-auto">
		<div class="mb-3">
			<div class="d-flex align-items-center">
				<div class="me-3">
					<SelectImportance />
				</div>
				<ImportanceLevels class="me-3" />
			</div>
		</div>
		<div class="row">
			<NoteItem
				v-for="note in getNotes" :key="note.id"
				:note="note"
			>
			</NoteItem>
		</div>
	</div>
</template>

<script>
import { mapGetters } from "vuex";

import NoteItem from "@/components/NoteItem";
import SelectImportance from "@/components/filters/SelectImportance";
import ImportanceLevels from "@/components/filters/ImportanceLevels";


export default {
	name: "CategoryDetail",
	components: {
		NoteItem,
		SelectImportance,
		ImportanceLevels
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