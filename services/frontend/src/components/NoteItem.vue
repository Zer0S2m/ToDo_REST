<template>
	<div>
		<router-link
			:to="{ name: 'NoteDetail', params: { id: note.id } }"
			class="list-group-item list-group-item-action"
		>
			<div class="d-flex w-100 justify-content-between">
				<h5 class="mb-1">{{ note.titleNote }}</h5>
				<small>{{ note.pubDate }}</small>
			</div>
			<p class="mb-1">{{ note.textNote }}</p>
		</router-link>
	</div>
</template>

<script>
export default {
	name: "NoteItem",
	props: {
		note: Object,
	},
}
</script>

<style scoped>

</style>