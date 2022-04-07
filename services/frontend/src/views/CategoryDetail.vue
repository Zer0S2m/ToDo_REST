<template>
	<div class="container">
		<div class="df just-between">
			<NoteItems :levelImportance=0 title-level="Usual" />
			<NoteItems :levelImportance=1 title-level="Easy" />
			<NoteItems :levelImportance=2 title-level="Important" />
			<NoteItems :levelImportance=3 title-level="Urgently" />
		</div>
	</div>
</template>

<script>
import { mapMutations } from "vuex";

import NoteItems from "@/components/NoteItems";


export default {
	name: "CategoryDetail",
	components: {
		NoteItems,
	},
	methods: {
		...mapMutations([
			"setCategoriesFilter"
		])
	},
	created() {
		this.setCategoriesFilter([this.$route.params.slug]);
	}
}
</script>