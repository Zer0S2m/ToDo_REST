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
			<button
				type="button"
				class="add-notes-btn df"
				@click="openFormNote"
			>
				<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="#FFFFFF" viewBox="0 0 24 24">
					<path d="M12 2c5.514 0 10 4.486 10 10s-4.486 10-10 10-10-4.486-10-10 4.486-10 10-10zm0-2c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm6 13h-5v5h-2v-5h-5v-2h5v-5h2v5h5v2z"/>
				</svg>
			</button>
		</div>
		<ul class="notes-items">
			<NoteItem
				v-for="note in getNotesPart" :key="note.id"
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
	mapActions,
	mapMutations
} from "vuex";

import NoteItem from "@/components/note/NoteItem";


export default {
	name: "NoteItems",
	props: {
		levelImportance: Number,
		titleLevel: String,
		idPart: Number
	},
	data() {
		return {
			classAreaAddNote: `add-notes-area-${this.levelImportance}`,
		}
	},
	components: {
		NoteItem
	},
	methods: {
		...mapActions([
			"editNote"
		]),
		...mapMutations([
			"changeCountNotesImportanceLevels",
			"setActionForFormNote",
			"setShowFormNote",
			"setDataEditNote",
			"setAdditionalDataForm"
		]),
		onDragStart(event, note) {
      event.dataTransfer.dropEffect = 'move';
      event.dataTransfer.effectAllowed = 'move';
			event.dataTransfer.setData("idNote", note.idNote.toString());
			event.dataTransfer.setData("idPart", note.partId.toString());
		},
		onDragEnd(event, levelImportance) {
			const idNote = parseInt(event.dataTransfer.getData("idNote"));
			const idPart = parseInt(event.dataTransfer.getData("idPart"));

			const part = this.getPartDetailById(idPart);
			const currentNote = part.notes.find(note => note.idNote === idNote);

			if ( currentNote.importance !== levelImportance ) {
				this.changeCountNotesImportanceLevels({
					newImportance: levelImportance,
					lastImportance: currentNote.importance,
					idPart: idPart,
					idProject: currentNote.projectId
				});
				this.editNote({
					slugPart: this.$route.params.slugPart,
					slugProject: this.$route.params.slugProject,
					...currentNote,
					importance: levelImportance,
					file: "",
					note: {
						idNote: idNote,
						fileName: currentNote.fileName
					}
				});
			};
		},
		openFormNote() {
			this.setAdditionalDataForm({
				slugProject: this.$route.params.slugProject,
				slugPart: this.$route.params.slugPart,
				idPart: this.idPart
			});
			this.setActionForFormNote("create");
			this.setShowFormNote(true);
			this.setDataEditNote({
				importance: this.levelImportance
			});
		}
	},
	computed: {
		...mapGetters([
			"getFilteredNotesByImportanceLevel",
			"getPartDetailBySlug",
			"getPartDetailById"
		]),
		getNotesPart() {
			const part = this.getPartDetailBySlug(this.$route.params.slugPart);
			const notes = this.getFilteredNotesByImportanceLevel(part.notes, this.levelImportance);

			return notes;
		}
	}
}
</script>