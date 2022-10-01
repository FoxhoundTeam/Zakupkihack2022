<template>
  <v-card elevation="0">
    <v-card-title>{{ label }}</v-card-title>
    <v-text-field
      placeholder="От"
      outlined
      type="number"
      v-model.number="min"
      @blur="filterMin"
    ></v-text-field>
    <v-text-field
      placeholder="До"
      outlined
      type="number"
      v-model.number="max"
      @blur="filterMax"
    ></v-text-field>
  </v-card>
</template>

<script>
import { mapActions, mapMutations, mapState } from "vuex";
export default {
  props: ["label", "id"],
  data() {
    return {
      min: null,
      max: null,
    };
  },
  computed: {
    ...mapState(["goodsFilters"]),
  },
  methods: {
    ...mapMutations(["setGoodsFilters"]),
    ...mapActions(["getGoods"]),
    async filterMin() {
      const goodsFilters = { ...this.goodsFilters };
      if (this.min == goodsFilters[`filter_${this.id}_gte`]) return;
      if (this.min == "") delete goodsFilters[`filter_${this.id}_gte`];
      else goodsFilters[`filter_${this.id}_gte`] = this.min;
      this.setGoodsFilters(goodsFilters);
      await this.getGoods();
    },
    async filterMax() {
      const goodsFilters = { ...this.goodsFilters };
      if (this.min == goodsFilters[`filter_${this.id}_lte`]) return;
      if (this.max == "") delete goodsFilters[`filter_${this.id}_lte`];
      else goodsFilters[`filter_${this.id}_lte`] = this.max;
      this.setGoodsFilters(goodsFilters);
      await this.getGoods();
    },
  },
};
</script>

<style>
</style>