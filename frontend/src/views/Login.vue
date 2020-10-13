<template>
    <input @keyup.enter="doLogin" type="text" placeholder="Username" v-model="credentials.username">
    <input @keyup.enter="doLogin" type="password" placeholder="Password" v-model="credentials.password">
    <button @click="doLogin">Login</button>
</template>

<script>
import { reactive } from 'vue'
import { useStore } from 'vuex'
import router from '@/router'
import { login } from '@/api'

export default {
    setup() {
        const store = useStore()

        const credentials = reactive({
            username: null,
            password: null
        })

        const doLogin = async () => {
            const token = await login(credentials.username, credentials.password)

            if (token) {
                store.commit('setToken', token)
                router.push("/")
            }
        }

        return {doLogin, credentials}
    }
}
</script>
