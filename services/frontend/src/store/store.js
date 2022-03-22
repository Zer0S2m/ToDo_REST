import { createStore } from 'vuex'
import note from "./modules/note.js"
import user from "./modules/user.js"


export default createStore({
	modules: {
		note,
		user
	}
})
