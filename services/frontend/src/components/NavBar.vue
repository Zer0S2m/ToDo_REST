<template>
	<header class="header w100 df al-it-center">
		<div class="header__wrapper">
			<nav class="header__nav">
				<ul class="header__nav-items df">
					<li class="header__nav-item">
						ToDo
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

export default {
	name: "NavBar",
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