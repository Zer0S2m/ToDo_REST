<template>
	<div class="w-75 mx-auto">
		<div class="mb-3">
			<div class="d-flex align-items-center">
				<div class="me-3">
					<select v-model="importance" @change="selectImportance" class="form-select" aria-label="Default select example">
						<option value="" selected>Sort by importance notes</option>
						<option value="ascending">ascending</option>
						<option value="descending">descending</option>
					</select>
				</div>
				<div class="d-flex align-items-center">
					<h6 class="my-0 me-2">Categories:</h6>
					<select v-model="categories" @change="selectCategries" class="form-select" size="1" multiple>
						<option
							v-for="category in getCategories" :key="category.id"
							:value="category.slug"
						>
							{{ category.title }}
						</option>
					</select>
				</div>
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
import { mapGetters } from "vuex";

import NoteItem from "@/components/NoteItem";


export default {
	name: 'ListNotes',
	data() {
		return {
			notes: [],
			importance: "",
			categories: []
		}
	},
	components: {
		NoteItem
	},
	methods: {
		selectImportance: function() {
			if ( this.importance === "ascending" ) this.notes.sort((a, b) => a.importance > b.importance ? 1 : -1)
			else if ( this.importance === "descending" ) this.notes.sort((a, b) => a.importance < b.importance ? 1 : -1);
		},
		selectCategries: function() {
			if ( this.categories.length !== 0 ) {
				const notesFilter = this.getNotes.filter(note => this.categories.includes(note.categorySlug));
				this.notes = notesFilter;
				this.selectImportance();
			} else {
				this.notes = [...this.getNotes];
				this.selectImportance();
			};
		},
	},
	computed: {
		...mapGetters([
			"getNotes",
			"getCategories",
		]),
		returnNotes: function() {
			if ( this.notes.length === 0 && this.categories.length === 0 ) this.notes = [...this.getNotes];
			return this.notes;
		}
	},
}
</script>