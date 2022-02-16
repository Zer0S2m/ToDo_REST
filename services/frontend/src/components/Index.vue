<template>
	<div class="list-group">
		<NoteItem
			v-for="note in Object.keys(notes)" v-bind:key="note"
			v-bind:id="notes[note].idNote"
			v-bind:title="notes[note].titleNote"
			v-bind:text="notes[note].textNote"
			v-bind:pubDate="notes[note].pubDate"
		>
		</NoteItem>
	</div>
</template>

<script>
import NoteItem from "./NoteItem"


export default {
	name: 'Index',
	components: {
		NoteItem
	},
	data() {
		return {
			notes: this.$store.getters.getNotes,
		};
	},
}
</script>

<style scoped>

</style>