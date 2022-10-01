<template>
  <v-dialog v-model="showModal">
    <v-card>
      <v-card-title>Редактирование категории</v-card-title>
      <v-card-text>
        <v-text-field label="Название" v-model="category.name"></v-text-field>
        <v-select v-model="category.status" :items="statuses"></v-select>
        <v-container>
          <v-row v-for="(tag, i) in category.filters" :key="i">
            <v-col class="my-0 py-0" cols="4">
              <v-select
                :items="types"
                v-model="category.filters[i].type"
                rounded
                label="Тип"
                filled
                item-text="name"
                item-value="value"
              ></v-select>
            </v-col>
            <v-col class="my-0 py-0" cols="4">
              <v-text-field
                rounded
                label="Название"
                filled
                v-model="category.filters[i].label"
                v-if="category.filters[i].type != 'range'"
              >
              </v-text-field>
              <v-text-field
                rounded
                label="Название"
                filled
                v-model="category.filters[i].label"
                v-else
                @click:append="deleteItem(i)"
                append-icon="delete"
              >
              </v-text-field>
            </v-col>
            <v-col
              class="my-0 py-0"
              cols="4"
              v-if="category.filters[i].type != 'range'"
            >
              <v-combobox
                multiple
                rounded
                clearable
                label="Варианты значений"
                chips
                deletable-chips
                filled
                v-model="category.filters[i].choices"
                @click:append="deleteItem(i)"
                append-icon="delete"
              >
              </v-combobox>
            </v-col>
          </v-row>
          <v-row>
            <v-col
              ><v-btn class="mx-1" icon @click="addItem()">
                <v-icon color="gray"> add </v-icon>
              </v-btn></v-col
            >
          </v-row>
        </v-container>
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
import http from "@/http";
import { STATUSES } from "../../consts";
import { mapMutations } from "vuex";
export default {
  props: ["value", "category"],
  data() {
    return {
      types: [
        {
          name: "Несколько элементов",
          value: "checkbox",
        },
        {
          name: "Один элемент",
          value: "radio",
        },
        {
          name: "Диапазон",
          value: "range",
        },
      ],
      statuses: STATUSES,
      saving: false,
    };
  },
  computed: {
    showModal: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit("input", value);
      },
    },
  },
  methods: {
    ...mapMutations(["showSnackbar"]),
    async save() {
      this.saving = true;
      let response = await http.updateItem(
        "Category",
        this.category.id,
        this.category,
        true
      );
      if (response == {}) return;
      this.showSnackbar("Категория успешно обновлена");
      this.saving = false;
      this.showModal = false;
    },
    addItem() {
      let filters = [...this.category.filters];
      filters.push({ type: "checkbox", label: "", choices: [] });
      this.$set(this.category, "filters", filters);
    },
    deleteItem(ind) {
      this.category.filters.splice(ind, 1);
    },
  },
};
</script>

<style>
</style>