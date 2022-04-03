<template>
	<select v-model="importance" class="form-select">
		<option value="" selected>Sort by importance notes</option>
		<option
			v-for="(filter, index) in filters" :key="index"
			:value="filter.value"
		>
			{{ filter.title }}
		</option>
	</select>
</template>

<script>
import {
	mapGetters,
	mapMutations
} from "vuex";


export default {
	name: "Select",
	data() {
		return {
			filters: [
				{ value: "ascending", title: "Ascending" },
				{ value: "descending", title: "Descending" },
			]
		}
	},
	methods: {
		...mapMutations([
			"setImportanceFilter"
		]),
	},
	computed: {
		...mapGetters([
			"getImportnceFilter"
		]),
		importance: {
			get() {
				return this.getImportnceFilter;
			},
			set(value) {
				this.setImportanceFilter(value);
			}
		},
	}
}
</script>