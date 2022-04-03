<template>
	<div class="col-4 mb-4">
		<router-link
			:to="{ name: 'NoteDetail', params: { id: note.id } }"
			class="list-group-item list-group-item-action"
			:class="classImportance"
		>
			<div>
				<h5 class="mb-1">{{ note.titleNote }}</h5>
				<p class="mb-0">{{ note.textNote }}</p>
			</div>
			<p class="mb-0 mt-2">
				<small>
					<time>{{ note.pubDate }}</time>
				</small>
			</p>
		</router-link>
	</div>
</template>

<script>
export default {
	name: "NoteItem",
	props: {
		note: Object,
	},
	data() {
		return {
			classImportance: `importance-${this.note.importance}`
		}
	},
}
</script>

<style lang="scss" scoped>
.list-group-item-action {
	transition: $animate;

	&:hover {
		color: initial;
	}
}

.importance-1 { @include card-note-importance($color-importance-1); }
.importance-2 { @include card-note-importance($color-importance-2); }
.importance-3 { @include card-note-importance($color-importance-3); }
</style>