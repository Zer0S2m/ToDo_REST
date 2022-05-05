<template>
	<div class="df just-between">
		<NoteItems :levelImportance=0 titleLevel="Usual" :slugPart=slugPart />
		<NoteItems :levelImportance=1 titleLevel="Easy" :slugPart=slugPart />
		<NoteItems :levelImportance=2 titleLevel="Important" :slugPart=slugPart />
		<NoteItems :levelImportance=3 titleLevel="Urgently" :slugPart=slugPart />
	</div>
</template>

<script>
import NoteItems from "@/components/note/NoteItems";


export default {
	name: "OpenNotes",
	components: {
		NoteItems
	},
	props: {
		slugPart: String,
		slugProject: String
	}
}
</script>