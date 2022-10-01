<template>
  <v-card
    class="h-100"
    outlined
    rounded
    :to="{ name: 'Company', params: { id: company.id } }"
    link
  >
    <v-card-title>{{ company.name }}</v-card-title>
    <v-card-text>
      <p v-if="company.address">Адрес: {{ company.address }}</p>
      <p v-if="company.phone">Телефон: {{ company.phone }}</p>
      <p v-if="company.site">Сайт: {{ company.site }}</p>
      <p v-if="company.email">Почта: {{ company.email }}</p>
      <p v-if="company.username">ИНН: {{ company.username }}</p>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: ["company"],
};
</script>

<style>
</style>