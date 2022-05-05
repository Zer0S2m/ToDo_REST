<template>
	<ul class="df wrap items-closed-notes">
		<NoteItem
			v-for="(note, index) in notes" :key="index"
			:note=note
			:isTakeAction='false'
		>
		</NoteItem>
	</ul>
</template>

<script>
import { mapActions } from "vuex";

import NoteItem from "@/components/note/NoteItem";


export default {
	name: "ClosedNotes",
	components: {
		NoteItem
	},
	props: {
		slugPart: String,
		slugProject: String
	},
	data() {
		return {
			notes: []
		}
	},
	methods: {
		...mapActions([
			"getCompletedNotes"
		])
	},
	async created() {
		await this.getCompletedNotes({
			slugProject: this.slugProject,
			slugPart: this.slugPart,
		})
			.then((res) => {
				this.notes = res;
			});
	}
}
</script>

<style lang="scss" scoped>
.items-closed-notes {
	margin-top: 12px;
  column-gap: 12px;

	.note {
		max-width: 24%;
	}
}
</style>