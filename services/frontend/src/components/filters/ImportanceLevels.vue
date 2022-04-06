<template>
	<div class="importance-level">
		<h4 class="importance-level__title">Importance levels</h4>
		<div class="importance-level__wrapper">
			<div
				v-for="(level, index) in levels" :key="index"
				class="importance-level__back-check"
			>
				<input class="importance-level__check" type="checkbox" :value="level.value" :id="level.value" v-model="importanceLevels">
				<label class="importance-level__label" :class="level.labelClass" :for="level.value">
					{{ level.title }}<span>({{ setCountNotesImportance(level.value) }})</span>
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
				{ value: 0, title: "Usual", labelClass: "label-importance-0" },
				{ value: 1, title: "easy", labelClass: "label-importance-1" },
				{ value: 2, title: "Important", labelClass: "label-importance-2" },
				{ value: 3, title: "Urgently", labelClass: "label-importance-3" },
			]
		}
	},
	methods: {
		...mapMutations([
			"setImportanceLevelsFilter"
		]),
		setCountNotesImportance: function(importance) {
			let notes = this.getNotes;
			notes = notes.filter(note => note.importance === importance);
			return notes.length;
		}
	},
	computed: {
		...mapGetters([
			"getImportanceLevelsFilter",
			"getNotes"
		]),
		importanceLevels: {
			get() {
				return this.getImportanceLevelsFilter;
			},
			set(value) {
				this.setImportanceLevelsFilter(value);
			}
		},
	}
}
</script>