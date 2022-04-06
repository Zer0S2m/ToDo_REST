<template>
	<div class="container user">
		<div class="user__content">
			<h2 class="user__title">Sign up</h2>
			<div class="user__back-form">
				<form 
					@submit.prevent="submit"
					class="user__form"
				>
					<div class="user__form-block">
						<label for="username-user" class="user__form-label primary-label">Username</label>
						<input
							type="text"
							class="user__form-input primary-input"
							id="username-user"
							v-model="username"
							required
						>
						<div class="user__form-error primary-input-error" v-if="errorUsername">
							<p>
								{{ errorUsername }}
							</p>
						</div>
					</div>
					<div class="user__form-block">
						<label for="email-user" class="user__form-label primary-label">Email</label>
						<input
							type="email"
							class="user__form-input primary-input"
							id="email-user"
							v-model="email"
						>
						<div class="user__form-error primary-input-error" v-if="errorEmail">
							<p>
								{{ errorEmail }}
							</p>
						</div>
						<div class="primary-text-form">
							<p>
								Email is not required
							</p>
						</div>
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
							Sign up
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