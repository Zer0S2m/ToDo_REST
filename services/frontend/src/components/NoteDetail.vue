<template>

</template>

<script>
import axios from 'axios';


export default {
	name: "NoteDetail",
	data() {
		return {
			note: ""
		}
	},
	methods: {
		getNote() {
			axios.get(`/note/${this.$route.params.id}/`)
				.then((res) => {
					this.note = res.data;
				})
				.catch((error) => {
					console.error(error);
				});
		},
	},
	created() {
		this.getNote();
	},
}
</script>

<style scoped>

</style>