<template>
	<header class="mb-4">
		<nav class="navbar navbar-light bg-light">
			<div class="container-fluid container">
				<router-link
					:to="{ name: 'Index' }"
					class="navbar-link"
				>
					<img src="@/assets/logo.png" alt="" width="30" height="24" class="d-inline-block align-text-top">
					<span>ToDo</span>
				</router-link>
				<div>
					<button @click="openFormAddNote" type="button" class="btn btn-primary">
  					Add note
					</button>
				</div>
			</div>
		</nav>
	</header>
</template>

<script>
import ModalForm from "./ModalForm";


export default {
	name: "NavBar",
	components: {
		ModalForm
	},
	methods: {
		openFormAddNote() {
			this.$store.commit("setShowModalForm", true);
		},
	},
}
</script>

<style scoped>
.navbar-link {
	color: #000;
	text-decoration: none;
	display: flex;
	align-items: center;
}

.navbar-link span {
	margin-left: 6px;
}
</style>