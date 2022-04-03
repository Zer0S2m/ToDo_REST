<template>
	<div class="d-flex align-items-center">
		<h6 class="mb-0">Importance levels:</h6>
		<div class="d-flex flex-wrap ms-2">
			<div
				v-for="(level, index) in levels" :key="index"
				class="form-check w-50"
			>
				<input class="form-check-input" type="checkbox" :value="level.value" :id="level.value" v-model="importanceLevels">
				<label class="form-check-label" :class="level.labelClass" :for="level.value">
					{{ level.title }}
				</label>
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
	name: "ImportanceLevels",
	data() {
		return {
			levels: [
				{value: 0, title: "Usual", labelClass: "label-importance-0"},
				{value: 1, title: "easy", labelClass: "label-importance-1"},
				{value: 2, title: "Important", labelClass: "label-importance-2"},
				{value: 3, title: "Urgently", labelClass: "label-importance-3"},
			]
		}
	},
	methods: {
		...mapMutations([
			"setImportanceLevelsFilter"
		])
	},
	computed: {
		...mapGetters([
			"getImportanceLevelsFilter"
		]),
		importanceLevels: {
			get() {
				return this.getImportanceLevelsFilter;
			},
			set(value) {
				this.setImportanceLevelsFilter(value);
			}
		}
	}
}
</script>

<style lang="scss" scoped>
.label-importance-1,
.label-importance-2,
.label-importance-3 {
	text-decoration: underline;
}
.label-importance-1 {
	text-decoration-color: $color-importance-1;
}
.label-importance-2 {
	text-decoration-color: $color-importance-2;
}
.label-importance-3 {
	text-decoration-color: $color-importance-3;
}
</style>