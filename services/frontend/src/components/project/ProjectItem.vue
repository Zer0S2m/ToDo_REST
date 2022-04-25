<template>
	<div class="project-item w100">
		<div class="project-item-wrapper df column h100">
			<h3 class="project-item-title">
				<router-link
					:to="{ name: 'ProjectDetail', params: { slugProject: project.slug } }"
					class="project-item-link"
				>
					{{ project.title }}
				</router-link>
			</h3>
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
import getPubDate from "@/filters/date";


export default {
	name: "ProjectItem",
	props: {
		project: Object
	},
	computed: {
		getPubDate() { return getPubDate(this.project.pubDate) }
	}
}
</script>