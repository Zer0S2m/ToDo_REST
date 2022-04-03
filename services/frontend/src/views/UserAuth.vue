<template>
	<div class="container-content container-content--small">
		<h2 class="text-center">Login</h2>
		<form
			@submit.prevent=submit
		>
			<div v-if="error">
				<p v-text="error" class="text-danger fs-5"></p>
			</div>
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
			<button type="submit" class="btn btn-primary">login</button>
		</form>
	</div>
</template>

<script>
import { mapActions } from "vuex";


export default {
	name: "UserSignUp",
	data(){
    return {
      username : "",
      password : "",
			error: ""
    }
  },
	methods: {
		...mapActions([
			"loginUser"
		]),
		submit() {
			this.loginUser({
				username: this.username,
				password: this.password
			})
				.then((res) => {
					this.error = "";

					if ( res ) {
						this.error = res.detail;
					};
				});
		},
	}
}
</script>