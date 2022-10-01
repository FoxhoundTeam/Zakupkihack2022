<template>
  <v-card elevation="0">
    <v-card-title>{{ label }}</v-card-title>
    <v-checkbox
      v-for="(choice, i) in choices"
      v-model="selected"
      :value="choice"
      :label="choice"
      hide-details
      :key="`${i}-${choice}-${label}`"
    ></v-checkbox>
  </v-card>
</template>

<script>
import { mapActions, mapMutations, mapState } from "vuex";
export default {
  props: ["label", "choices", "id"],
  data() {
    return {
      selected: [],
    };
  },
  computed: {
    ...mapState(["goodsFilters"]),
  },
  watch: {
    async selected(value) {
      const goodsFilters = { ...this.goodsFilters };
      if (value.length == 0) delete goodsFilters[`filter_${this.id}`];
      else goodsFilters[`filter_${this.id}`] = value.join(",");
      this.setGoodsFilters(goodsFilters);
      await this.getGoods();
    },
  },
  methods: {
    ...mapActions(["getGoods"]),
    ...mapMutations(["setGoodsFilters"]),
  },
};
</script>

<style>
</style>