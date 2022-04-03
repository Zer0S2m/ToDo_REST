<template>
	<div class="d-flex align-items-center">
		<h6 class="my-0 me-2">Categories:</h6>
		<select v-model="categories" class="form-select" size="1" multiple>
			<option
				v-for="category in getCategories" :key="category.id"
				:value="category.slug"
			>
				{{ category.title }}
			</option>
		</select>
	</div>
</template>

<script>
import {
	mapGetters,
	mapMutations
} from "vuex";


export default {
	name: "Categories",
	methods: {
		...mapMutations([
			"setCategoriesFilter"
		])
	},
	computed: {
		...mapGetters([
			"getCategoriesFilter",
			"getCategories"
		]),
		categories: {
			get() {
				return this.getCategoriesFilter;
			},
			set(value) {
				this.setCategoriesFilter(value);
			}
		},
	}
}
</script>