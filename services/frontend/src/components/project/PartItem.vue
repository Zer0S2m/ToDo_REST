<template>
	<div class="part-item w100">
		<div
			class="card-menu"
			:class="{ 'card-menu--active': isShowMenu }"
		>
			<div class="card-menu-wrapper">
				<ul class="card-menu-items">
					<li class="card-menu-item">
						<button
							type="button"
							class="card-menu-item-btn df al-it-center"
							@click="openFormNote"
						>
							<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#318ae5" viewBox="0 0 24 24"><path d="M12 2c5.514 0 10 4.486 10 10s-4.486 10-10 10-10-4.486-10-10 4.486-10 10-10zm0-2c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm6 13h-5v5h-2v-5h-5v-2h5v-5h2v5h5v2z"/></svg>
							<span>Add note</span>
						</button>
					</li>
					<li class="card-menu-item">
						<button
							type="button"
							class="card-menu-item-btn df al-it-center"
							@click="toEditPart"
						>
							<img src="@/assets/img/edit-blue.svg" alt="">
							<span>Part editing</span>
						</button>
					</li>
					<li class="card-menu-item">
						<button
							type="button"
							class="card-menu-item-btn df al-it-center"
							@click="toDeletedPart"
						>
							<img src="@/assets/img/delete.svg" alt="">
							<span>Delete</span>
						</button>
					</li>
				</ul>
			</div>
		</div>
		<div class="part-item__wrapper df column h100">
			<div class="part-item__back-title df just-between w100">
				<h4 class="part-item__title">
					<router-link
						:to='{
							name: "PartDetail",
							params: {
								slugProject: slugProject,
								slugPart: part.slug
							}
						}'
						class="part-item__link"
					>
						{{ part.title }}
					</router-link>
				</h4>
				<button
					type="button"
					class="part-item__btn-menu df"
					@click="openMenu()"
				>
					<img src="@/assets/img/menu.svg" alt="" class="part-item__btn-menu-img">
				</button>
			</div>
			<div class="part-item__text">
				<p>
					{{ part.description }}
				</p>
			</div>
			<div class="part-item__block">
				<div class="part-item__notes">
					<ul class="part-item__levels df al-it-center just-around">
						<li class="part-item__level part-item__level--0 df">
							<h5 class="part-item__level-title">{{ part.countNotesImportanceLevels[0] }}</h5>
						</li>
						<li class="part-item__level part-item__level--1 df">
							<h5 class="part-item__level-title">{{ part.countNotesImportanceLevels[1] }}</h5>
						</li>
						<li class="part-item__level part-item__level--2 df">
							<h5 class="part-item__level-title">{{ part.countNotesImportanceLevels[2] }}</h5>
						</li>
						<li class="part-item__level part-item__level--3 df">
							<h5 class="part-item__level-title">{{ part.countNotesImportanceLevels[3] }}</h5>
						</li>
					</ul>
				</div>
				<div class="part-item__area df al-">
					<div class="part-item__count-notes df al-it-center">
						<img src="@/assets/img/task.svg" alt="">
						<h5 class="part-item__count-notes-title">{{ part.countNotes }}</h5>
					</div>
					<div class="part-item__date df">
						<time>{{ getPubDate }}</time>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import {
	mapActions,
	mapMutations
} from "vuex";

import getPubDate from "@/filters/date";


export default {
	name: "PartItem",
	props: {
		part: Object,
		slugProject: String
	},
	data() {
		return {
			isShowMenu: false
		}
	},
	methods: {
		...mapMutations([
			"setShowFormNote",
			"setActionForFormNote",
			"setAdditionalDataForm",
			"setEditDataPart",
			"setShowFormPart",
			"setActionFormPart"
		]),
		...mapActions([
			"deletePart"
		]),
		openMenu() {
			if ( this.isShowMenu ) this.isShowMenu = false;
			else this.isShowMenu = true;
		},
		toDeletedPart() {
			this.isShowMenu = false;

			this.deletePart({
				slugProject: this.slugProject,
				slugPart: this.part.slug
			});
		},
		openFormNote() {
			this.isShowMenu = false;
			this.setActionForFormNote("create");
			this.setAdditionalDataForm({
				slugProject: this.slugProject,
				idPart: this.part.id,
				slugPart: this.part.slug,
			});
			this.setShowFormNote(true);
		},
		toEditPart() {
			this.setEditDataPart({
				description: this.part.description,
				title: this.part.title,
				slug: this.part.slug,
				id: this.part.id
			});
			this.isShowMenu = false;
			this.setShowFormPart(true);
			this.setActionFormPart("edit");
		}
	},
	computed: {
		getPubDate() { return getPubDate(this.part.pubDate) }
	}
}
</script>