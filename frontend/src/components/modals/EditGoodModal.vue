<template>
  <v-dialog v-model="showModal" width="600">
    <v-card>
      <v-card-title>Редактирование товара</v-card-title>
      <v-card-text>
        <v-text-field v-model="good.name" label="Название" />
        <v-textarea v-model="good.description" label="Описание"></v-textarea>
        <div
          v-for="(filter, i) in category.filters"
          :key="`${filter.path}-${i}`"
        >
          <v-combobox
            v-model="good_props[filter.id].value"
            :items="filter.choices"
            :label="filter.label"
            outlined
            dense
            v-if="filter.type != 'range'"
          ></v-combobox>
          <v-text-field
            :label="filter.label"
            v-model.number="good_props[filter.id].value"
            type="number"
            v-else
          />
        </div>
        <v-select v-model="good.status" :items="statuses"></v-select>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="showModal = false" text color="red">Отменить</v-btn>
        <v-btn @click="save" text color="primary" :loading="saving"
          >Сохранить</v-btn
        >
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapGetters, mapMutations } from "vuex";
import http from "../../http";
import { STATUSES } from "../../consts";
export default {
  props: ["value", "good"],
  data() {
    return {
      statuses: STATUSES,
      saving: false,
    };
  },
  computed: {
    category() {
      return this.categoryById(this.good.category_id) || {};
    },
    showModal: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit("input", value);
      },
    },
    good_props() {
      let props = {};
      for (const prop of this.good.props || []) {
        props[prop.category_filter_id] = prop;
      }
      for (const filter of this.category.filters) {
        if (!props[filter.id])
          props[filter.id] = { category_filter_id: filter.id, value: null };
      }
      return props;
    },
    ...mapGetters(["categoryById"]),
  },
  methods: {
    ...mapMutations(["showSnackbar"]),
    async save() {
      this.saving = true;
      this.good.props = Object.values(this.good_props);
      let response = await http.updateItem(
        "Good",
        this.good.id,
        this.good,
        true
      );
      if (response == {}) return;
      this.showSnackbar("Товар успешно обновлен");
      this.saving = false;
      this.showModal = false;
    },
  },
};
</script>

<style>
</style>