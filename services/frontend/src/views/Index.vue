<template>
	<div class="list-group">
		<NoteItem
			v-for="note in getNotes" :key="note.id"
			:note="note"
		>
		</NoteItem>
	</div>
</template>

<script>
import { mapGetters } from "vuex";

import NoteItem from "@/components/NoteItem";


export default {
	name: 'Index',
	components: {
		NoteItem
	},
	computed: {
		...mapGetters([
			"getNotes"
		]),
	},
}
</script>

<style scoped>

</style>