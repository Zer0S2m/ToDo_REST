<template>
	<div class="select-importance">
		<h4 class="select-importance__title">Sort by importance notes</h4>
		<div class="select-importance__wrapper">
			<div class="select-importance__back-radio">
				<div class="select-importance__radio" v-for="(filter, index) in filters" :key="index">
					<input type="radio" :value="filter.value" :id="filter.idFor" v-model="importance">
					<label :for="filter.idFor">{{ filter.title }}</label>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import {
	mapGetters,
	mapMutations
} from "vuex";


export default {
	name: "SelectImportance",
	data() {
		return {
			filters: [
				{ value: 0, title: "Default", idFor: "importance-sort-0" },
				{ value: 1, title: "Ascending", idFor: "importance-sort-up" },
				{ value: -1, title: "Descending", idFor: "importance-sort-down" },
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