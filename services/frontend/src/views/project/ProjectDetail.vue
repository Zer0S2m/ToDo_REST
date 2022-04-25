<template>
	<AppLoader v-if="isUiLocked" />
	<div class="container project" v-if="!isUiLocked">
		<h2 class="project__title">Project - {{ project.title }}</h2>
		<div class="project__parts">
			<h4 class="project__subtitle">Parts</h4>
			<div class="project__parts-items df">
				<PartItem
					v-for="(part, index) in project.parts" :key="index"
					:part=part
					:slugProject="slugProject"
				>
				</PartItem>
				<button type="button" @click="setShowFormPart(true)" class="project__add project__add-part df w100 al-it-center column just-center">
					<img src="@/assets/img/add-white.svg" alt="" class="project__add-img project__add-part-img">
					<span class="project__add-text project__add-part-text">Add part</span>
				</button>
			</div>
		</div>
		<div class="project__category">
			<h4 class="project__subtitle">Categories</h4>
			<ul class="project__category-items w50">
				<CategoryItem
					v-for="(category, index) in project.categories" :key="index"
					:category="category"
					:slugProject="slugProject"
					:indexArr=index
				>
				</CategoryItem>
				<button type="button" @click="setShowFormCategory(true)" class="project__add project__add-category df w100 al-it-center just-center">
					<img src="@/assets/img/add-white.svg" alt="" class="project__add-img project__add-category-img">
					<span class="project__add-text project__add-category-text">Add category</span>
				</button>
			</ul>
		</div>
		<div class="project__comments">
			<h4 class="project__subtitle">Comments</h4>
			<div class="project__comments-items df">
				<CommentItem
					v-for="(comment, index) in project.comments" :key="index"
					:comment=comment
					:idIndex=index
					:slugProject=slugProject
				>
				</CommentItem>
				<button type="button" @click="addComment" class="project__add project__add-comment df w100 al-it-center column just-center">
					<img src="@/assets/img/add-white.svg" alt="" class="project__add-img project__add-comment-img">
					<span class="project__add-text project__add-comment-text">Add comment</span>
				</button>
			</div>
		</div>
	</div>
</template>

<script>
import {
	mapActions,
	mapMutations,
	mapGetters
} from "vuex";

import CommentItem from "@/components/project/CommentItem.vue";
import PartItem from "@/components/project/PartItem.vue";
import CategoryItem from "@/components/category/CategoryItem";
import AppLoader from "@/components/AppLoader.vue";


export default {
	name: "ProjectDetail",
	props: {
		slugProject: String
	},
	data() {
		return {
			project: {}
		}
	},
	components: {
		CommentItem,
		PartItem,
		AppLoader,
		CategoryItem
	},
	methods: {
		...mapMutations([
			"setDataForCreateComment",
			"setIsShowFormComment",
			"setActionFormComment",
			"setShowFormPart",
			"setShowFormCategory"
		]),
		...mapActions([
			"getDetailProject"
		]),
		addComment() {
			this.setIsShowFormComment(true);
			this.setActionFormComment("create");
			this.setDataForCreateComment({
				slugProject: this.project.slug,
				idProject: this.project.id
			});
		},
	},
	computed: {
		...mapGetters([
			"isUiLocked",
			"getProjectDetail"
		])
	},
	async created() {
		const project = this.getProjectDetail(this.slugProject);

		if ( !Boolean(project) ) {
			await this.getDetailProject(this.slugProject).
				then((res) => {
					this.project = res;
				});
		} else {
			this.project = project;
		};
	}
}
</script>