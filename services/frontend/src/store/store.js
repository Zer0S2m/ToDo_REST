import Vue from "vue"
import Vuex from "vuex"
import note from "./modules/note"


Vue.use(Vuex)


export const store = new Vuex.Store({
	modules: {
		note
	}
})
