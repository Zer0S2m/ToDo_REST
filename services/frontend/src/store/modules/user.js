import axios from "axios";

import router from "@/router";


export default {
	state: {
		token: localStorage.getItem('token') || "",
	},
	mutations: {
		setToken(state, token) {
			state.token = token;
		},
		clearUser(state) {
			state.token = "";
		}
	},
	actions: {
		async loginUser(state, data) {
			let errorPost;
			const { username, password } = data;
			const formData = new FormData();
			formData.append("username", username);
			formData.append("password", password);

			await axios.post("/user/auth", formData)
				.then((res) => {
					const data = res.data;
					localStorage.setItem('token', data.access_token);

					axios.defaults.headers.common['Authorization'] = `Bearer ${data.access_token}`;

					state.commit("setToken", data.access_token);
					state.dispatch("getProjects");

					router.push({
						name: "ListProject"
					});
				})
				.catch((error) => {
					errorPost = error.response.data;
				});

			return errorPost;
		},
		async signUpUser(state, data) {
			const { username, password, email } = data;
			let errorObj;

			await axios.post("/user/sign-up", {
					username,
					password,
					email
			})
				.then((res) => {
					router.push({
						name: "UserAuth"
					});
				})
				.catch((error) => {
					errorObj = error.response.data;
				});

			return errorObj;
		},
		logoutUser(state) {
			state.commit('clearUser');
			state.commit("setProjects", []);
			localStorage.removeItem('token');
			delete axios.defaults.headers.common['Authorization'];

			router.push({
				name: "UserAuth"
			});
		},
	},
	getters: {
		getToken: state => state.token,
		getInLogin: state => !!state.token,
	}
}