<template>
	<CommentForm />
	<ProjectForm />
	<PartForm />
	<router-view></router-view>
</template>

<script>
import CommentForm from "@/components/project/CommentForm";
import ProjectForm from "@/components/project/ProjectForm";
import PartForm from "@/components/project/PartForm";


export default {
	name: "PageProject",
	components: {
		CommentForm,
		ProjectForm,
		PartForm
	}
}
</script>