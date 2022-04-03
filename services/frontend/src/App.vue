<template>
	<div id="app">
		<NavBar />
		<ModalForm />
		<CategoryForm />
		<h1 class="text-center mb-5">ToDo FastAPI/Python & VueJS</h1>
		<div class="container text-start">
			<router-view />
		</div>
	</div>
</template>

<script>
import NavBar from "./components/NavBar";
import ModalForm from "./components/ModalForm";
import CategoryForm from "./components/CategoryForm";


export default {
	name: 'App',
	components: {
		NavBar,
		ModalForm,
		CategoryForm
	},
}
</script>

<style lang="scss">
#app {
	font-family: 'Avenir', Helvetica, Arial, sans-serif;
	padding-bottom: 60px;
}
</style>