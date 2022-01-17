<template>
	<div>
		<h1>{{ msg }}</h1>
	</div>
</template>

<script>
import axios from 'axios';

export default {
	name: 'Index',
	data() {
		return {
			msg: '',
		};
	},
	methods: {
		getMessage() {
			axios.get("/")
				.then((res) => {
					this.msg = res.data;
					console.log(this.msg);
				})
				.catch((error) => {
					console.error(error);
				});
		},
	},
	created() {
		this.getMessage();
	},
}
</script>

<style scoped>
h1, h2 {
	font-weight: normal;
}
</style>