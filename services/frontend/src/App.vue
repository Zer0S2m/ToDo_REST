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
import NavBar from "./components/NavBar";
import NoteForm from "./components/NoteForm";
import CategoryForm from "./components/CategoryForm";
import Sidebar from "./components/Sidebar";


export default {
	name: 'App',
	components: {
		NavBar,
		NoteForm,
		CategoryForm,
		Sidebar
	}
}
</script>