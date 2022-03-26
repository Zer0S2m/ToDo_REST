import { createStore } from 'vuex'
import note from "./modules/note.js"
import user from "./modules/user.js"
import category from "./modules/category.js"


export default createStore({
	modules: {
		note,
		user,
		category
	}
})
