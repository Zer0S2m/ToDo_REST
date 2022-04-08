<template>
	<div class="search">
		<div class="search__wrapper df al-it-center">
			<button
				type="button"
				class="search__btn df"
				@click="setTextSearch(textSearch)"
			>
				<img src="@/assets/img/search-btn.svg" alt="" class="search__btn-img">
			</button>
			<input
				type="text"
				class="search__input"
				placeholder="Search..."
				v-model="textSearch"
				@keyup.enter="setTextSearch(textSearch)"
			>
			<button
				type="button"
				class="search__clean"
				@click="cleanData"
			>
				<img src="@/assets/img/delete-note.svg" alt="" class="search__clean-img">
			</button>
		</div>
	</div>
</template>

<script>
import { mapMutations } from "vuex";


export default {
	name: "SearchInput",
	data() {
		return {
			textSearch: ""
		}
	},
	methods: {
		...mapMutations([
			"setTextSearch"
		]),
		cleanData() {
			this.textSearch = "";
			this.setTextSearch(this.textSearch);
		}
	}
}
</script>