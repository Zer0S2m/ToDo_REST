<template>
	<div class="container">
		<div class="df project-items">
			<ProjectItem
				v-for="(project, index) in getProjects" :key="index"
				:project="project"
			>
			</ProjectItem>
		</div>
	</div>
</template>

<script>
import { mapGetters } from "vuex";

import ProjectItem from "@/components/project/ProjectItem";


export default {
	name: "ListProject",
	components: {
		ProjectItem
	},
	computed: {
		...mapGetters([
			"getProjects"
		])
	}
}
</script>