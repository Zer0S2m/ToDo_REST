<template>
	<div id="app">
		<div class="container text-start w-50">
			<h1 class="text-center mb-5">ToDo FastAPI/Python & VueJS</h1>
			<router-view/>
		</div>
	</div>
</template>

<script>
export default {
	name: 'App'
}
</script>

<style>
#app {
	font-family: 'Avenir', Helvetica, Arial, sans-serif;
	padding: 60px 0;
}
</style>
