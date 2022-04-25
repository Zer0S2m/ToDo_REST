export default {
	state: {
		lockingPool: 0
	},
	mutations: {
		lockUi(state) {
			state.lockingPool++
		},
    unlockUi(state) {
			state.lockingPool--;
		},
	},
	getters: {
		isUiLocked: state => state.lockingPool > 0
	}
}