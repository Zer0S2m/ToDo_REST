export default function(value) {
	const options = {
		day: 'numeric',
		weekday: 'short',
		month: "short"
	};
	const date = new Intl.DateTimeFormat("en-US", options).format(new Date(value));
	return date;
}