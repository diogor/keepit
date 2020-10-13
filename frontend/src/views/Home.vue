<template>
  <p v-if="loading">Carregando...</p>
  <div class="contato" v-for="contato in contatos" :key="contato.id">
    <p>{{contato.retorno}} - {{showDate(contato.created_at)}}</p>
    <p>{{contato.texto}}</p>
    <router-link :to="{name: 'Contato', params: {id: contato.id}}">go</router-link>
  </div>
</template>

<script>
import { fetchContactList, showDate } from '@/api'
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'

export default {
  setup() {
    const store = useStore()
    const contatos = ref([])
    const loading = ref(true)

    onMounted(async () => {
      if (store.state.token) {
        contatos.value = await fetchContactList(store.state.token)
        loading.value = false
      }
    })

    return {contatos, showDate, loading}
  }
}
</script>
