<template>
	<div class="project-item w100">
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
							@click="toEditProject"
						>
							<img src="@/assets/img/edit-blue.svg" alt="">
							<span>Project editing</span>
						</button>
					</li>
					<li class="card-menu-item">
						<button
							type="button"
							class="card-menu-item-btn df al-it-center"
							@click="toDeleteProject"
						>
							<img src="@/assets/img/delete.svg" alt="">
							<span>Delete</span>
						</button>
					</li>
				</ul>
			</div>
		</div>
		<div class="project-item-wrapper df column h100">
			<div class="project-item-area df just-between w100">
				<h3 class="project-item-title">
					<router-link
						:to="{ name: 'ProjectDetail', params: { slugProject: project.slug } }"
						class="project-item-link"
					>
						{{ project.title }}
					</router-link>
				</h3>
				<button
					type="button"
					class="project-item-btn-menu df"
					@click="openMenu()"
				>
					<img src="@/assets/img/menu.svg" alt="" class="project-item-btn-menu-img">
				</button>
			</div>
			<div class="project-item-text">
				<p>
					{{ project.description }}
				</p>
			</div>
			<div class="project-item-description df al-it-cen">
				<div class="project-item-description-wrapper df al-it-center">
					<div class="project-item-description-block df al-it-center">
						<img src="@/assets/img/category.svg" alt="">
						<h4 class="project-item-description-block-title">{{ project.categories.length }}</h4>
					</div>
					<div class="project-item-description-block df al-it-center">
						<img src="@/assets/img/part.svg" alt="">
						<h4 class="project-item-description-block-title">{{ project.parts.length }}</h4>
					</div>
					<div class="project-item-description-block df al-it-center">
						<img src="@/assets/img/comment.svg" alt="">
						<h4 class="project-item-description-block-title">{{ project.comments.length }}</h4>
					</div>
				</div>
				<div class="project-item-date">
					<time>{{ getPubDate }}</time>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import {
	mapMutations,
	mapActions
} from "vuex";

import getPubDate from "@/filters/date";


export default {
	name: "ProjectItem",
	props: {
		project: Object
	},
	data() {
		return {
			isShowMenu: false
		}
	},
	computed: {
		getPubDate() { return getPubDate(this.project.pubDate) }
	},
	methods: {
		...mapActions([
			"editProject",
			"deleteProject"
		]),
		...mapMutations([
			"setEditDataProject",
			"setShowFormProject",
			"setActionFormProject"
		]),
		openMenu() {
			if ( this.isShowMenu ) this.isShowMenu = false;
			else this.isShowMenu = true;
		},
		toEditProject() {
			this.isShowMenu = false;

			this.setEditDataProject({
				id: this.project.id,
				description: this.project.description,
				title: this.project.title,
				slug: this.project.slug
			});
			this.setShowFormProject(true);
			this.setActionFormProject("edit")
		},
		toDeleteProject() {
			this.isShowMenu = false;
			this.deleteProject(this.project.slug);
		}
	}
}
</script>