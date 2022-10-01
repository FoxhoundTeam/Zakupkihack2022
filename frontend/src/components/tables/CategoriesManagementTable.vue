<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="filteredCategories"
      class="elevation-0"
      :search="search"
      @click:row="(row) => showEditCategory(row)"
    >
      <template v-slot:top>
        <h3 class="font-weight-bold text-h3 basil--text my-5 ml-5">
          Администрирование категорий
        </h3>
        <v-row class="px-4">
          <v-col cols="7">
            <v-text-field
              label="Название"
              outlined
              v-model="search"
            ></v-text-field>
          </v-col>
          <v-col cols="5">
            <div class="d-flex align-items-center justify-content-end">
              <v-select
                label="Статус"
                outlined
                clearable
                v-model="status"
                :items="statuses"
              ></v-select>
              <v-tooltip bottom open-delay="500">
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    class="mx-1 mb-5"
                    v-bind="attrs"
                    v-on="on"
                    icon
                    @click="showCreateCategory"
                  >
                    <v-icon color="gray" v-bind="attrs" v-on="on"> add </v-icon>
                  </v-btn>
                </template>
                <span>Добавить</span>
              </v-tooltip>
            </div>
          </v-col>
        </v-row>
      </template>
      <template v-slot:item.status="{ item }">
        {{ getStatus(item.status) }}
      </template>
    </v-data-table>
    <edit-category-modal v-model="showEditModal" :category="editCategory" />
    <create-category-modal v-model="showCreateModal" />
  </div>
</template>

<script>
import { status_mapper, STATUSES } from "@/consts";
import EditCategoryModal from "../modals/EditCategoryModal.vue";
import CreateCategoryModal from "../modals/CreateCategoryModal.vue";
import { mapState } from "vuex";

export default {
  components: { EditCategoryModal, CreateCategoryModal },
  data() {
    return {
      headers: [
        { text: "Название", value: "name" },
        { text: "Статус", value: "status" },
      ],
      editCategory: {},
      showEditModal: false,
      showCreateModal: false,
      search: "",
      statuses: STATUSES,
      status: null,
    };
  },
  methods: {
    showEditCategory(category) {
      this.editCategory = category;
      this.showEditModal = true;
    },
    showCreateCategory() {
      this.showCreateModal = true;
    },
    getStatus(v) {
      return status_mapper(v);
    },
  },
  computed: {
    ...mapState(["categories"]),
    filteredCategories() {
      return this.categories.filter((v) =>
        this.status ? v.status == this.status : true
      );
    },
  },
};
</script>

<style>
</style>