<template>
	<div class="container-content container-content--small">
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
				<div v-if="errorUsername" class="text-danger">
					<p v-text="errorUsername"></p>
				</div>
			</div>
			<div class="mb-3">
				<label for="email" class="form-label">Email</label>
				<input
					v-model="email"
					type="email"
					class="form-control"
					id="email"
				>
				<div v-if="errorEmail" class="text-danger">
					<p v-text="errorEmail"></p>
				</div>
				<div class="form-text">Email is not required</div>
			</div>
			<div class="mb-3">
				<label for="password" class="form-label">Password</label>
				<input
					v-model="password"
					type="password"
					class="form-control"
					id="password"
					autocomplete="off"
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
			username: "",
			errorUsername: "",
			errorEmail: ""
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
			})
				.then((res) => {
					this.errorUsername = "";
					this.errorEmail = "";

					if ( res && res.detail.username ) {
						this.errorUsername = res.detail.username;
					} else if ( res && res.detail.email ) {
						this.errorEmail = res.detail.email;
					};
				});
		}
	}
}
</script>