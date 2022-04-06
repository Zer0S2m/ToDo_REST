<template>
	<header class="header w100 df al-it-center">
		<div class="header__wrapper">
			<nav class="header__nav">
				<ul class="header__nav-items df">
					<li class="header__nav-item">
						<SearchInput v-if="getInLogin" />
					</li>
				</ul>
			</nav>
		</div>
	</header>
</template>

<script>
import {
	mapMutations,
	mapGetters,
	mapActions
} from "vuex";

import SearchInput from "./filters/SearchInput";


export default {
	name: "NavBar",
	components: {
		SearchInput
	},
	methods: {
		...mapMutations([
			"setShowModalForm",
			"setActionForFormNote",
			"setShowFormCategory"
		]),
		...mapActions([
			"logoutUser"
		]),
		openFormNote() {
			this.setShowModalForm(true);
			this.setActionForFormNote("create");
		},
		openFormCategory() {
			this.setShowFormCategory(true);
		}
	},
	computed: {
		...mapGetters([
			"getInLogin",
		])
	},
}
</script>