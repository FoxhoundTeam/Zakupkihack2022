<template>
  <v-card elevation="0">
    <v-card-title>{{ label }}</v-card-title>
    <v-radio-group v-model="selected">
      <v-radio
        v-for="(choice, i) in choices"
        :value="choice"
        :label="choice"
        :key="`${i}-${choice}-${label}`"
      ></v-radio>
    </v-radio-group>
  </v-card>
</template>

<script>
import { mapActions, mapMutations, mapState } from "vuex";
export default {
  props: ["label", "choices", "id"],
  data() {
    return {
      selected: null,
    };
  },
  computed: {
    ...mapState(["goodsFilters"]),
  },
  watch: {
    async selected(value) {
      const goodsFilters = { ...this.goodsFilters };
      goodsFilters[`filter_${this.id}`] = value;
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