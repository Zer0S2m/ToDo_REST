<template>
	<div>
		<router-link
			:to="{ name: 'NoteDetail', params: { id: id } }"
			class="list-group-item list-group-item-action"
		>
			<div class="d-flex w-100 justify-content-between">
				<h5 class="mb-1">{{ title }}</h5>
				<small>{{ pubDate }}</small>
			</div>
			<p class="mb-1">{{ text }}</p>
		</router-link>
	</div>
</template>

<script>
export default {
	name: "NoteDetail",
	props: {
		id: Number,
		title: String,
		text: String,
		pubDate: String
	},
}
</script>

<style scoped>

</style>