<template>
	<AppLoader v-if="isUiLocked" />
	<div class="container category-page" v-if="!isUiLocked">
		<h2 class="category-page__title">Category - {{ slugCategory }}</h2>
		<div class="category-page__wrapper">
			<ul class="category-page__parts">
				<li
					class="category-page__part"
					v-for="(part, index) in parts" :key="index"
				>
					<h4 class="category-page__part-title">
						<router-link
							class="category-page__part-link"
							:to="{
								name: 'PartDetail',
								params: {
									slugProject: slugProject,
									slugPart: part.slug,
								}
							}"
						>
							{{ part.title }}
						</router-link>
					</h4>
					<ul class="category-page__part-notes df">
						<NoteItem
							v-for="(note, index) in getNotesByPart(this.getNotesByCategory, part.id)" :key="index"
							:note="note"
						/>
					</ul>
				</li>
			</ul>
		</div>
	</div>
</template>

<script>
import {
	mapActions,
	mapGetters
} from "vuex";

import AppLoader from "@/components/AppLoader";
import NoteItem from "@/components/note/NoteItem";


export default {
	name: "CategoryDetail",
	components: {
		AppLoader,
		NoteItem
	},
	data() {
		return {
			parts: []
		}
	},
	props: {
		slugProject: String,
		slugCategory: String
	},
	methods: {
		...mapActions([
			"getPartsInProject",
			"getDetailPart"
		])
	},
	computed: {
		...mapGetters([
			"isUiLocked",
			"getProjectBase",
			"getNotesByPart",
			"getPartsDetail",
			"getNotesByCategory"
		])
	},
	async created() {
		const partsDetails = this.getPartsDetail;
		const projectBase = this.getProjectBase(this.slugProject);

		if ( projectBase ) {
			this.parts = projectBase.parts;
		} else {
			await this.getPartsInProject(this.slugProject)
				.then((res) => {
					this.parts = res;
				});
		};

		for ( let partIndex = 0; partIndex < this.parts.length; partIndex++ ) {
			const part = this.parts[partIndex];
			const isPartDetail = partsDetails.find(partDetail => partDetail.slug === part.slug);
			if ( !isPartDetail ) {
				await this.getDetailPart({
					slugProject: this.slugProject,
					slugPart: part.slug
				});
			};
		};
	},
}
</script>