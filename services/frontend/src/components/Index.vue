<template>
	<div class="list-group">
		<NoteItem
			v-for="(noteKey, index) in keysNotes" v-bind:key="index"
			v-bind:id="index + 1"
			v-bind:title="notes[noteKey].titleNote"
			v-bind:text="notes[noteKey].textNote"
			v-bind:pubDate="notes[noteKey].pubDate"
		>
		</NoteItem>
	</div>
</template>

<script>
import axios from 'axios';
import NoteItem from "./NoteItem"


export default {
	name: 'Index',
	components: {
		NoteItem
	},
	data() {
		return {
			notes: '',
			keysNotes: []
		};
	},
	methods: {
		getNotes() {
			axios.get("/")
				.then((res) => {
					this.notes = res.data;
					this.keysNotes = Object.keys(this.notes);
				})	
				.catch((error) => {
					console.error(error);
				});
		},
	},
	created() {
		this.getNotes();
	},
}
</script>

<style scoped>

</style>