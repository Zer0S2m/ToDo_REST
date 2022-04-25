<template>
	<AppLoader v-if="isUiLocked" />
	<div class="container part" v-if="!isUiLocked">
		<h2 class="part__title">Part - {{ part.title }}</h2>
		<div class="df just-between">
			<NoteItems :levelImportance=0 titleLevel="Usual" :idPart=part.id />
			<NoteItems :levelImportance=1 titleLevel="Easy" :idPart=part.id />
			<NoteItems :levelImportance=2 titleLevel="Important" :idPart=part.id />
			<NoteItems :levelImportance=3 titleLevel="Urgently" :idPart=part.id />
		</div>
	</div>
</template>

<script>
import {
	mapGetters,
	mapActions
} from "vuex";

import AppLoader from "@/components/AppLoader";
import NoteItems from "@/components/note/NoteItems.vue";


export default {
	name: "PartDetail",
	data() {
		return {
			part: {}
		}
	},
	props: {
		slugProject: String,
		slugPart: String,
	},
	components: {
		AppLoader,
		NoteItems
	},
	methods: {
		...mapActions([
			"getDetailPart"
		])
	},
	computed: {
		...mapGetters([
			"isUiLocked",
			"getPartDetailBySlug",
			"getPartsDetail",
			"getProjectDetail",
		])
	},
	async created() {
		const part = this.getPartDetailBySlug(this.slugPart);

		if ( !Boolean(part) ) {
			await this.getDetailPart({
				slugProject: this.slugProject,
				slugPart: this.slugPart
			})
				.then((res) => {
					this.part = res;
				})
				.catch((error) => {
					console.error(error);
				});
		}
		else {
			this.part = part;
		};
	}
}
</script>