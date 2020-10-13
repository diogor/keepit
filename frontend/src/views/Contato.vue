<template>
    <p v-if="loading">Carregando...</p>
    <div v-if="contato.id">
        <p>{{contato.retorno}} - {{showDate(contato.created_at)}}</p>
        <p>{{contato.texto}}</p>
        <p>
            <a href="#" @click.prevent="deleteContato">delete</a>
        </p>
    </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useStore } from 'vuex'
import router from '@/router'
import { showDate, fetchContact, deleteContact } from '@/api'

export default {
    setup() {
        const store = useStore()
        const loading = ref(true)
        const contato = reactive({})
        const { params } = useRoute()

        onMounted(async () => {
            const c = await fetchContact(params.id, store.state.token)
            loading.value = false
            Object.assign(contato, c)
        })

        const deleteContato = async () => {
            await deleteContact(contato.id, store.state.token)
            router.push("/")            
        }

        return {contato, showDate, loading, deleteContato}
    }
}
</script>

<style lang="sass" scoped>
p
    padding: 10px
</style>