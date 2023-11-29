/* eslint-disable */



const user_list = {
    state: {
        users: []
    },
    actions: {
        set_users({
                commit
            },
            val
        ) {}
    },
    mutations: {
        SET_USERS: (state, payload) => {
            state.users = payload.users
        }
    },
}

export default user_list