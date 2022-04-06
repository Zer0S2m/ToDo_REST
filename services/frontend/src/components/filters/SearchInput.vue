<template>
	<div class="search">
		<div class="search__wrapper df al-it-center">
			<button
				type="button"
				class="search__btn df"
			>
				<img src="@/assets/img/search-btn.svg" alt="" class="search__btn-img">
			</button>
			<input
				type="text"
				class="search__input"
				placeholder="Search..."
			>
		</div>
	</div>
</template>

<script>
export default {
	name: "SearchInput"
}
</script>