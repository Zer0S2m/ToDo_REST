<template>
	<li class="category-item">
		<div class="category-item-wrapper  df al-it-center just-between">
			<router-link
				:to="{ name: 'CategoryDetail', params: { slug: category.slug } }"
				class="category-item-link"
			>
				{{ category.title }}<span>({{ setCountNotesInCategory }})</span>
			</router-link>
			<div class="df al-it-center">
				<button
					type="button"
					class="category-item__delete df"
					@click="delCategory"
				>
					<img src="@/assets/img/delete-category.svg" alt="" class="category-item__delete-img">
				</button>
			</div>
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