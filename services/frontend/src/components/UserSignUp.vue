<template>
	<div>
		<h2 class="text-center">Registration</h2>
		<form
			@submit.prevent=submit
		>
			<div class="mb-3">
				<label for="username" class="form-label">Username</label>
				<input
					v-model="username"
					type="text"
					class="form-control"
					id="username"
					required
				>
			</div>
			<div class="mb-3">
				<label for="email" class="form-label">Email</label>
				<input
					v-model="email"
					type="email"
					class="form-control"
					id="email"
				>
				<div class="form-text">Email is not required</div>
			</div>
			<div class="mb-3">
				<label for="password" class="form-label">Password</label>
				<input
					v-model="password"
					type="password"
					class="form-control"
					id="password"
					required	
				>
			</div>
			<button type="submit" class="btn btn-primary">Sign up</button>
		</form>
	</div>
</template>

<script>
import { mapActions } from "vuex";


export default {
	name: "UserSignUp",
	data() {
		return {
			password: "",
			email: null,
			username: ""
		}
	},
	methods: {
		...mapActions([
			"signUpUser"
		]),
		submit() {
			this.signUpUser({
				password: this.password,
				email: this.email,
				username: this.username
			});

			this.$router.push({
				name: "UserAuth"
			});
		}
	}
}
</script>

<style scoped>

</style>