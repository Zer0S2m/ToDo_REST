<template>
	<aside class="sidebar df w100">
		<div class="sidebar__wrapper w100">
			<div class="sidebar__content df column just-between h100">
				<div class="sidebar__content-area">
					<div class="sidebar__profile df al-it-center">
						<h4 class="sidebar__profile-title w100">ToDo</h4>
					</div>
					<ul class="sidebar__items">
						<li class="sidebar__item df" v-if="!getInLogin">
							<router-link
								active-class="sidebar__item-link--active"
								:to="{ name: 'UserAuth' }"
								class="sidebar__item-link df w100"
							>
								<span>Auth</span>
						</router-link>
						</li>
						<li class="sidebar__item df" v-if="!getInLogin">
							<router-link
								active-class="sidebar__item-link--active"
								:to="{ name: 'UserSignUp' }"
								class="sidebar__item-link df w100"
							>
								<span>Sign up</span>
							</router-link>
						</li>
						<li class="sidebar__item df" v-if="getInLogin">
							<router-link
								active-class="sidebar__item-link--active"
								:to="{ name: 'ListNotes' }"
								class="sidebar__item-link df w100"
							>
								<span class="sidebar__item-link-img">
									<img src="@/assets/img/notes.svg" alt="">
								</span>
								<span>Notes</span>
							</router-link>
						</li>
						<li class="sidebar__item df" v-if="getInLogin">
							<router-link
								active-class="sidebar__item-link--active"
								:to="{ name: 'ListCategories' }"
								class="sidebar__item-link df w100"
							>
								<span class="sidebar__item-link-img">
									<img src="@/assets/img/category.svg" alt="">
								</span>
								<span>Categories</span>
							</router-link>
						</li>
						<li class="sidebar__item df" v-if="getInLogin">
							<button
								type="button"
								class="sidebar__item-link df w100"
								@click="openFormNote"
							>
								<span class="sidebar__item-link-img">
									<img src="@/assets/img/add-note.svg" alt="">
								</span>
								<span>Add note</span>
							</button>
						</li>
						<li class="sidebar__item df" v-if="getInLogin">
							<button
								type="button"
								class="sidebar__item-link df w100"
								@click="setShowFormCategory(true)"
							>
								<span class="sidebar__item-link-img">
									<img src="@/assets/img/add-category.svg" alt="">
								</span>
								<span>Add category</span>
							</button>
						</li>
					</ul>
				</div>
			</div>
		</div>
	</aside>
</template>

<script>
import {
	mapGetters,
	mapMutations
} from "vuex";


export default {
	name: "Sidebar",
	methods: {
		...mapMutations([
			"setShowNoteForm",
			"setShowFormCategory",
			"setActionForFormNote"
		]),
		openFormNote() {
			this.setShowNoteForm(true);
			this.setActionForFormNote("create");
		},
	},
	computed: {
		...mapGetters([
			"getInLogin"
		]),
	}
}
</script>