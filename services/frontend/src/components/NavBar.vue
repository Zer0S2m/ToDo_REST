<template>
	<header class="mb-4">
		<nav class="navbar navbar-light bg-light">
			<div class="container-fluid container">
				<div class="d-flex">
					<router-link
						:to="{ name: 'Index' }"
						class="navbar-link me-3"
					>
						<img src="@/assets/logo.png" alt="" width="30" height="24" class="d-inline-block align-text-top">
						<span>ToDo</span>
					</router-link>
					<router-link
						v-if="getInLogin"
						:to="{ name: 'ListCategories' }"
						class="link"
					>
						<span>Categoires</span>
					</router-link>
				</div>
				<div>
					<router-link
						:to="{ name: 'UserAuth' }"
						class="btn btn-primary me-2"
						v-if="!getInLogin"
					>
						<span>Auth</span>
					</router-link>
					<router-link
						:to="{ name: 'UserSignUp' }"
						class="btn btn-primary"
						v-if="!getInLogin"
					>
						<span>Sign up</span>
					</router-link>
					<button
						v-if="getInLogin"
						@click="openFormCategory"
						type="button"
						class="btn btn-primary me-2"
					>
  					Add Category
					</button>
					<button
						v-if="getInLogin"
						@click="openFormNote"
						type="button"
						class="btn btn-primary me-2"
					>
  					Add note
					</button>
					<button
						v-if="getInLogin"
						@click="logoutUser"
						type="button"
						class="btn btn-primary"
					>
						Logout
					</button>
				</div>
			</div>
		</nav>
	</header>
</template>

<script>
import {
	mapMutations,
	mapGetters,
	mapActions
} from "vuex";

import ModalForm from "./ModalForm";


export default {
	name: "NavBar",
	components: {
		ModalForm
	},
	methods: {
		...mapMutations([
			"setShowModalForm",
			"setActionForFormNote",
			"setShowFormCategory"
		]),
		...mapActions([
			"logoutUser"
		]),
		openFormNote() {
			this.setShowModalForm(true);
			this.setActionForFormNote("create");
		},
		openFormCategory() {
			this.setShowFormCategory(true);
		}
	},
	computed: {
		...mapGetters([
			"getInLogin",
		])
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