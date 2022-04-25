import { createStore } from 'vuex'
import note from "./modules/note.js"
import user from "./modules/user.js"
import category from "./modules/category.js"
import filter from "./modules/filter.js"
import project from "./modules/project.js"
import preloader from "./modules/preloader.js"


export default createStore({
	modules: {
		preloader,
		note,
		user,
		category,
		filter,
		project,
	}
})
