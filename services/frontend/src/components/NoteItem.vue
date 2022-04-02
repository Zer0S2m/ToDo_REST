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

<style scoped>
.list-group-item-action {
	transition: all 0.2s ease;
}
.list-group-item-action:hover {
	color: initial;
}

.importance-1 {
	border: 1px solid rgba(110, 219, 128, 0.75);
	background-color: rgba(110, 219, 128, 0.15);
}
.importance-1:hover {
	background-color: rgba(110, 219, 128, 0.2);
}

.importance-2 {
	border: 1px solid rgba(247, 189, 64, 0.75);
	background-color: rgba(247, 189, 64, 0.15);
}
.importance-2:hover {
	background-color: rgba(247, 189, 64, 0.2);
}

.importance-3 {
	border: 1px solid rgba(224, 35, 41, 0.7);
	background-color: rgba(224, 35, 41, 0.15);
}
.importance-3:hover {
	background-color: rgba(224, 35, 41, 0.2);
}
</style>