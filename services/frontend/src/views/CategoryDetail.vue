<template>
	<div class="list-group">
		<NoteItem
			v-for="note in getNotesCategory(this.$route.params.slug)" :key="note.id"
			:note="note"
		>
		</NoteItem>
	</div>
</template>

<script>
import NoteItem from "@/components/NoteItem";

import { mapGetters } from "vuex";


export default {
	name: "CategoryDetail",
	components: {
		NoteItem
	},
	computed: {
		...mapGetters([
			"getNotesCategory"
		])
	},
}
</script>