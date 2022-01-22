<template>
	<div id="app">
		<NavBar />
		<ModalForm />
		<h1 class="text-center mb-5">ToDo FastAPI/Python & VueJS</h1>
		<div class="container text-start w-50">
			<router-view/>
		</div>
	</div>
</template>

<script>
import NavBar from "./components/NavBar";
import ModalForm from "./components/ModalForm";


export default {
	name: 'App',
	components: {
		NavBar,
		ModalForm
	},
}
</script>

<style>
#app {
	font-family: 'Avenir', Helvetica, Arial, sans-serif;
	padding-bottom: 60px;
}
</style>