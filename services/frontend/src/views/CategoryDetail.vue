<template>
	<div class="w-75 mx-auto">
		<div class="row">
			<NoteItem
				v-for="note in getNotesCategory(this.$route.params.slug)" :key="note.id"
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