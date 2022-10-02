<template>
  <v-container>
    <v-row>
      <v-col>&nbsp;</v-col>
    </v-row>
    <v-row>
      <v-col>&nbsp;</v-col>
    </v-row>
    <v-row>
      <v-col>&nbsp;</v-col>
    </v-row>
    <v-row>
      <v-col></v-col>
      <v-col class="text-center"
        ><h1 style="font-size: 60px">FoxТорг</h1></v-col
      >
      <v-col></v-col>
    </v-row>
    <v-row>
      <v-col></v-col>
      <v-col cols="6">
        <search-field />
        <v-btn color="primary" block :to="{ name: 'Catalog' }">Каталог</v-btn>
      </v-col>
      <v-col></v-col>
    </v-row>
  </v-container>
</template>

<script>
import SearchField from "../components/fields/SearchField.vue";
export default {
  components: { SearchField },
};
</script>

<style>
</style>