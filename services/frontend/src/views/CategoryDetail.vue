<template>
	<div class="w-75 mx-auto">
		<div class="mb-3">
			<div class="d-flex align-items-center">
				<div class="me-3">
					<Select />
				</div>
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
import Select from "@/components/filters/Select";


export default {
	name: "CategoryDetail",
	components: {
		NoteItem,
		Select
	},
	computed: {
		...mapGetters([
			"getNotesCategory",
			"getFilteredNotesByImportance"
		]),
		getNotes: function() {
			let notes = this.getNotesCategory(this.$route.params.slug);
			notes = this.getFilteredNotesByImportance(notes);
			return notes;
		}
	},
}
</script>