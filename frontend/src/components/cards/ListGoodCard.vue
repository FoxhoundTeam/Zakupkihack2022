<template>
  <v-card
    class="h-100 border border-success"
    rounded
    outlined
    :to="router_link"
    @click="$emit('click')"
  >
    <v-card-title>{{ good.name }}</v-card-title>
    <v-card-text>
      <p v-if="show_category">Категория: {{ category.name }}</p>
      <p v-if="show_status">Статус: {{ getStatus(good.status) }}</p>
      <p v-for="(value, i) in good.props" :key="`${i}-${value}-${good.id}`">
        {{ getPropLabel(value.category_filter_id) }}: {{ value.value }}
      </p>
      <v-text-field
        outlined
        rounded
        label="Цена"
        v-if="allow_edit_price"
        v-model="price"
        @blur="updatePrice"
      ></v-text-field>
      <h4 v-else-if="good.price">Цена {{ good.price }}</h4>
    </v-card-text>
  </v-card>
</template>

<script>
import http from "@/http";
import { mapGetters, mapMutations, mapState } from "vuex";
import { status_mapper } from "../../consts";
export default {
  props: {
    good: {
      type: Object,
    },
    show_category: {
      type: Boolean,
      default: false,
    },
    show_status: {
      type: Boolean,
      default: false,
    },
    allow_edit_price: {
      type: Boolean,
      default: false,
    },
    to: {
      type: String,
    },
  },
  data() {
    return {
      price: this.good.price,
    };
  },
  computed: {
    ...mapGetters(["categoryById"]),
    ...mapState(["user"]),
    category() {
      return this.categoryById(this.good.category_id) || {};
    },
    router_link() {
      if (this.to !== undefined) return this.to;

      return { name: "Good", params: { id: this.good.id } };
    },
  },
  methods: {
    ...mapMutations(["showSnackbar"]),
    getPropLabel(filter_id) {
      return this.category?.filters?.find((v) => v.id == filter_id)?.label;
    },
    getStatus(v) {
      return status_mapper(v);
    },
    async updatePrice() {
      if (this.good.price == this.price) return;
      let response = await http.createItem(
        `/api/good/${this.good.id}/create_for_company/`,
        {
          price: this.price,
          user_id: this.user.id,
        },
        true
      );
      if (response == {}) return;
      this.showSnackbar("Цена успешно обновлена");
    },
  },
};
</script>

<style>
</style>