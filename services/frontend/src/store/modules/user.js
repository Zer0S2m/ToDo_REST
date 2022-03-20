import axios from "axios";


export default {
	state: {
		token: localStorage.getItem('token') || "",
	},
	mutations: {
		setToken: function(state, token) {
			state.token = token;
		},
		clearUser: function(state) {
			state.token = "";
		}
	},
	actions: {
		loginUser: function(state, data) {
			const { username, password } = data;
			const formData = new FormData();
			formData.append("username", username);
			formData.append("password", password);

			axios.post("/user/auth", formData)
				.then((res) => { 
					const data = res.data;
					localStorage.setItem('token', data.accessToken);

					axios.defaults.headers.common['Authorization'] = `Bearer ${data.accessToken}`;

					state.commit("setToken", data.accessToken);
					state.dispatch("getNotes");
				})
				.catch((error) => {
					console.error(error);
				});
		},
		signUpUser: function(state, data) {
			const { username, password, email } = data;

			axios.post("/user/sign-up", {
					username,
					password,
					email
			})
				.catch((error) => {
					console.error(error);
				});
		},
		logoutUser: function(state) {
			state.commit('clearUser');
			state.dispatch("setNotes", []);
			localStorage.removeItem('token');
			delete axios.defaults.headers.common['Authorization'];
		},
	},
	getters: {
		getToken(state) {
			return state.token;
		},
		getInLogin(state) {
			return !!state.token;
		}
	}
}