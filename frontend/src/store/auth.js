import Vue from 'vue'
const state = {
    status: '',
    token: localStorage.getItem('user-token') || ''
};

const mutations = {
    AuthRequest: (state) => {
        state.status = 'loading'
    },
    AuthSuccess: (state, token) => {
        state.status = 'success'
        state.token = token
    },
    AuthError: (state) => {
        state.status = 'error'
    },
    AuthLogout: (state) => {
        state.status = ''
    },
};

const getters = {
    isAuthenticated: state => state.token,
    authStatus: state => state.status,
};

const actions = {
    AuthRequest: ({commit, dispatch}) => {
        return new Promise((resolve, reject) => {
            commit('AuthRequest')
            Vue.prototype.$axios({url: '/api/check-login', method: 'GET' })
            .then(resp => {
                if(resp.data.hasOwnProperty('error')){
                    dispatch('AuthLogout');
                }else{
                    const token = resp.data.token
                    localStorage.setItem('user-token', resp.data.success) 
                    commit('AuthSuccess', resp.data.success)
                    resolve(resp)
                }
            })
            .catch(err => {
                commit('AuthError', err)
                localStorage.removeItem('user-token');
                reject(err)
            })
        })
    },
    AuthLogout: ({commit, dispatch}) => {
        return new Promise((resolve, reject) => {
            Vue.prototype.$axios({url: '/api/logout', method: 'POST' })
            commit('AuthLogout')
            localStorage.removeItem('user-token')
            resolve()
        })
    }
}
export default {state,mutations,getters,actions}