<template>
	<div class="container user">
		<div class="user__content">
			<h2 class="user__title">Login</h2>
			<div class="user__back-form">
				<form
					@submit.prevent="submit"
					class="user__form"
				>
					<div class="primary-error-form" v-if="error">
						<p>
							{{ error }}
						</p>
					</div>
					<div class="user__form-block">
						<label for="username-user" class="user__form-label primary-label">Username</label>
						<input
							type="text"
							class="user__form-input primary-input"
							id="username-user"
							v-model="username"
							required
						>
					</div>
					<div class="user__form-block">
						<label for="password-user" class="user__form-label primary-label">Password</label>
						<input
							type="password"
							class="user__form-input primary-input"
							id="password-user"
							v-model="password"
							required
						>
					</div>
					<div class="user__form-block">
						<button
							type="submit"
							class="primary-btn-form"
						>
							Login
						</button>
					</div>
				</form>
			</div>
		</div>
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