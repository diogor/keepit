<template>
  <div class="app">
    <router-view/>
  </div>
</template>

<style lang="sass">
*
  border: none
  margin: 0px
  padding: 0px
.app
  display: grid
input, button, .contato
  margin: 10px
  padding: 10px
  outline: 1px solid #ccc
  &:focus
    outline: 1px solid #000
</style>
