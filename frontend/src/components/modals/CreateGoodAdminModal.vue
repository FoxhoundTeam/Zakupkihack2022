<template>
  <v-dialog v-model="showModal">
    <v-card>
      <v-card-title>Добавление товара</v-card-title>
      <v-card-text>
        <v-autocomplete
          label="Категория"
          :items="categories"
          v-model="category"
          item-text="name"
          item-value="id"
          return-object
        ></v-autocomplete>
        <div v-if="category">
          <v-text-field v-model="good.name" label="Название" />
          <v-textarea v-model="good.description" label="Описание"></v-textarea>
          <div
            v-for="(filter, i) in category.filters"
            :key="`${filter.id}-${i}`"
          >
            <v-combobox
              v-model="props[filter.id].value"
              :items="filter.choices"
              :label="filter.label"
              outlined
              dense
              v-if="filter.type != 'range'"
            ></v-combobox>
            <v-text-field
              :label="filter.label"
              v-model.number="props[filter.id].value"
              type="number"
              v-else
            />
          </div>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="showModal = false" text color="red">Отменить</v-btn>
        <v-btn
          @click="create"
          :disabled="!good.name"
          text
          color="primary"
          :loading="creating"
          >Создать</v-btn
        >
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapMutations, mapState } from "vuex";
import http from "../../http";
export default {
  props: ["value"],
  data() {
    return {
      good: {
        name: "",
        category_id: null,
        description: "",
      },
      creating: false,
      category: null,
    };
  },
  computed: {
    ...mapState(["categories"]),
    showModal: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit("input", value);
      },
    },
    props() {
      let props = {};
      for (const filter of this.category.filters) {
        props[filter.id] = { category_filter_id: filter.id, value: null };
      }
      return props;
    },
  },
  methods: {
    ...mapMutations(["showSnackbar"]),
    async create() {
      this.creating = true;
      this.good.category_id = this.category.id;
      this.good.props = Object.values(this.props);
      var response = await http.createItem("Good", this.good, true);
      if (response == {}) return;
      this.$emit("created");
      this.showSnackbar("Товар успешно создан");
      this.creating = true;
      this.showModal = false;
    },
  },
};
</script>

<style>
</style>