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
								class="sidebar__item-link df al-it-center w100"
							>
								<span>Auth</span>
						</router-link>
						</li>
						<li class="sidebar__item df" v-if="!getInLogin">
							<router-link
								active-class="sidebar__item-link--active"
								:to="{ name: 'UserSignUp' }"
								class="sidebar__item-link df al-it-center w100"
							>
								<span>Sign up</span>
							</router-link>
						</li>
						<li class="sidebar__item df" v-if="getInLogin">
							<router-link
								active-class="sidebar__item-link--active"
								:to="{ name: 'ListProject' }"
								class="sidebar__item-link df al-it-center w100"
							>
								<span class="sidebar__item-link-img df al-it-center">
									<img src="@/assets/img/project.svg" alt="">
								</span>
								<span>Projects</span>
							</router-link>
						</li>
						<li class="sidebar__item df" v-if="getInLogin">
							<button
								type="button"
								class="sidebar__item-link df al-it-center w100"
								@click="setShowFormProject(true)"
							>
								<span class="sidebar__item-link-img df al-it-center">
									<img src="@/assets/img/add.svg" alt="">
								</span>
								<span>Add project</span>
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
			"setShowFormProject"
		]),
	},
	computed: {
		...mapGetters([
			"getInLogin"
		]),
	}
}
</script>