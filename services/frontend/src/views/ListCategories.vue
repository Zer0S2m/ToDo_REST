<template>
	<ol class="list-group list-group-numbered w-50 mx-auto">
		<CategoryItem
			v-for="category in getCategories" :key="category"
			:category="category"
		>
		</CategoryItem>
	</ol>
</template>

<script>
import { mapGetters } from "vuex";

import CategoryItem from "@/components/CategoryItem";


export default {
	name: "ListCategories",
	components: {
		CategoryItem
	},
	computed: {
		...mapGetters([
			"getCategories"
		])
	}
}
</script>