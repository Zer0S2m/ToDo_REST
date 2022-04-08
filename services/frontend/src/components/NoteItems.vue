<template>
	<div
		class="wrapper-notes-items w100"
		@drop="onDragEnd($event, levelImportance)"
    @dragenter.prevent
		@dragover.prevent
	>
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
				@dragstart="onDragStart($event, note)"
				draggable="true"
			>
			</NoteItem>
		</ul>
	</div>
</template>

<script>
import {
	mapGetters,
	mapActions
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
	methods: {
		...mapActions([
			"editNote"
		]),
		onDragStart(event, note) {
      event.dataTransfer.dropEffect = 'move';
      event.dataTransfer.effectAllowed = 'move';
			event.dataTransfer.setData("noteId", note.id.toString());
		},
		onDragEnd(event, levelImportance) {
			const noteId = parseInt(event.dataTransfer.getData("noteId"));
			const currentNote = this.getNote(noteId);

			if ( currentNote.importance !== levelImportance ) {
				this.editNote({
					...currentNote,
					importance: levelImportance,
					file: "",
					note: {
						idNote: currentNote.idNote,
						fileName: currentNote.fileName,
						id: noteId,
					}
				});
			};
		}
	},
	computed: {
		...mapGetters([
			"getNotes",
			"getNote",
			"getFilteredNotesByCategories",
			"getFilteredNotesByImportanceLevel",
			"getFilteredNotesByTextSearch"
		]),
		returnNotes: function() {
			let notes = this.getFilteredNotesByImportanceLevel(this.getNotes, this.levelImportance);
			notes = this.getFilteredNotesByCategories(notes);
			notes = this.getFilteredNotesByTextSearch(notes);

			return notes;
		}
	},
}
</script>