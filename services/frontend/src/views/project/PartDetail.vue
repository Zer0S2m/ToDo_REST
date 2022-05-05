<template>
	<AppLoader v-if="isUiLocked" />
	<div class="container part" v-if="!isUiLocked">
		<h2 class="part__title">Part - {{ part.title }}</h2>
		<div class="part__wrapper df al-it-center">
			<h4 class="part__title-note">
				<router-link
					class="part__title-note-link df"
					:to='{
						name: "PartDetail",
						params: {
							slugProject: slugProject,
							slugPart: slugPart
						}
					}'
				>
					<span>{{ getCountNotes }}</span> Open
				</router-link>
			</h4>
			<h4 class="part__title-note">
				<router-link
					class="part__title-note-link df"
					:to='{
						name: "PartClosedNotes",
						params: {
							slugProject: slugProject,
							slugPart: slugPart
						}
					}'
				>
					Closed
				</router-link>
			</h4>
		</div>
		<div>
			<router-view />
		</div>
	</div>
</template>

<script>
import {
	mapGetters,
	mapActions
} from "vuex";

import AppLoader from "@/components/AppLoader";


export default {
	name: "PartDetail",
	data() {
		return {
			part: {}
		}
	},
	props: {
		slugProject: String,
		slugPart: String
	},
	components: {
		AppLoader
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
		]),
		getCountNotes() {
			if ( this.part.notes ) return this.part.notes.length;
		},
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