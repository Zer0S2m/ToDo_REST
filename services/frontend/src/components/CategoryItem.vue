<template>
	<li class="list-group-item d-flex justify-content-between align-items-start">
		<div class="ms-2 me-auto">
			<div class="fw-bold">
				<router-link
					:to="{ name: 'CategoryDetail', params: { slug: category.slug } }"
					class="link"
				>
					<span>{{ category.title }}</span>
				</router-link>
			</div>
		</div>
		<div class="d-flex align-items-center">
			<span class="badge bg-primary rounded-pill h-100 me-3">{{ setCountNotesInCategory }}</span>
			<button
				type="button"
				class="btn btn-danger py-0"
				@click="delCategory"
			>
				Del
			</button>
		</div>
	</li>
</template>

<script>
import {
	mapGetters,
	mapActions 
} from "vuex";


export default {
	name: "CategoryItem",
	props: {
		category: Object
	},
	methods: {
		...mapActions([
			"deleteCategory"
		]),
		delCategory() {
			this.deleteCategory(this.category);
		}
	},
	computed: {
		...mapGetters([
			"getNotes"
		]),
		setCountNotesInCategory: function() {
			let notes = this.getNotes;
			notes = notes.filter(note => note.categorySlug === this.category.slug);

			return notes.length;
		}
	},
}
</script>