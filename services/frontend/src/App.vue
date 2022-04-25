<template>
	<div>
		<div class="df">
			<Sidebar />
			<main class="main w100">
				<NavBar />
				<router-view />
			</main>
			<NoteForm />
			<CategoryForm />
		</div>
	</div>
</template>

<script>
import { mapActions } from "vuex";

import NavBar from "./components/NavBar";
import NoteForm from "./components/note/NoteForm";
import CategoryForm from "./components/category/CategoryForm";
import Sidebar from "./components/Sidebar";


export default {
	name: 'App',
	components: {
		NavBar,
		NoteForm,
		CategoryForm,
		Sidebar
	},
	methods: {
		...mapActions([
			"getProjects"
		])
	},
	created() {
		this.getProjects();
	}
}
</script>