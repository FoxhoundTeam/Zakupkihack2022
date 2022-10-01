<template>
  <categories label="Каталог" :columns="4" :categories="categories" />
</template>

<script>
import { mapState } from "vuex";
import Categories from "../components/Categories.vue";
export default {
  components: { Categories },
  computed: {
    ...mapState(["categories"]),
  },
};
</script>

<style>
</style>