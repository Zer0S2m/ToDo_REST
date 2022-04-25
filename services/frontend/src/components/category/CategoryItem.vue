<template>
	<li class="category-item">
		<div class="category-item-wrapper  df al-it-center just-between">
			<router-link
				:to="{
					name: 'CategoryDetail',
					params: {
						slugProject: slugProject,
						slugCategory: category.slug
					}
				}"
				class="category-item-link"
			>
				{{ category.title }}
			</router-link>
			<div class="df al-it-center">
				<button
					type="button"
					class="category-item__delete df"
					@click="delCategory"
				>
					<img src="@/assets/img/delete.svg" alt="" class="category-item__delete-img">
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
		category: Object,
		slugProject: String,
		indexArr: Number
	},
	methods: {
		...mapActions([
			"deleteCategory"
		]),
		delCategory() {
			this.deleteCategory({
				category: this.category,
				slugProject: this.slugProject,
				indexArr: this.indexArr
			});
		}
	},
	computed: {
		...mapGetters([

		])
	},
}
</script>