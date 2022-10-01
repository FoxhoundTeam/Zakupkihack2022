<template>
  <v-card>
    <v-card-title>Добавление товара</v-card-title>
    <v-card-text>
      <v-autocomplete
        label="Категория"
        :items="categories"
        v-model="category_id"
        item-text="name"
        item-value="id"
        append-outer-icon="mdi-plus"
        @click:append-outer="showAddCategoryModal = true"
      ></v-autocomplete>
      <v-autocomplete
        label="Товар"
        v-if="category_id"
        :items="goods"
        item-text="name"
        item-value="id"
        v-model="good_id"
        append-outer-icon="mdi-plus"
        @click:append-outer="showAddGoodModal = true"
      ></v-autocomplete>
      <v-text-field label="Цена" v-model="price" v-if="good_id"></v-text-field>
    </v-card-text>
    <v-card-actions>
      <v-btn
        color="primary"
        large
        :disabled="!price"
        @click="create"
        :loading="creating"
        >Создать</v-btn
      >
    </v-card-actions>
    <create-good-modal v-model="showAddGoodModal" />
    <create-category-modal v-model="showAddCategoryModal" />
  </v-card>
</template>

<script>
import CreateGoodModal from "../modals/CreateGoodModal.vue";
import http from "../../http";
import CreateCategoryModal from "../modals/CreateCategoryModal.vue";
import { mapMutations, mapState } from "vuex";
export default {
  components: { CreateGoodModal, CreateCategoryModal },
  data() {
    return {
      price: 0,
      showAddGoodModal: false,
      showAddCategoryModal: false,
      creating: false,
    };
  },
  computed: {
    ...mapState([
      "createCategoryId",
      "createGoodId",
      "createGoodsList",
      "user",
    ]),
    ...mapState({ categoriesFromState: "categories" }),
    category_id: {
      get() {
        return this.createCategoryId;
      },
      set(value) {
        this.setCreateCategoryId(value);
      },
    },
    good_id: {
      get() {
        return this.createGoodId;
      },
      set(value) {
        this.setCreateGoodId(value);
      },
    },
    goods: {
      get() {
        return this.createGoodsList;
      },
      set(value) {
        this.setCreateGoodsList(value);
      },
    },
    categories: {
      get() {
        return this.categoriesFromState;
      },
      set(value) {
        this.setCategories(value);
      },
    },
  },
  watch: {
    async category_id(value) {
      if (!value) return;
      this.goods = (
        await http.getList("GoodList", { category_id: value }, true)
      ).data;
    },
    // "$store.state.categories"() {
    //   this.categories = this.$store.state.categories;
    // },
  },
  // mounted() {
  //   this.categories = this.$store.state.categories;
  // },
  methods: {
    ...mapMutations([
      "setCreateCategoryId",
      "setCreateGoodId",
      "setCreateGoodsList",
      "setCategories",
      "showSnackbar",
    ]),
    async create() {
      this.creating = true;
      let response = await http.createItem(
        `/api/good/${this.good_id}/create_for_company/`,
        {
          price: this.price,
          user_id: this.user.id,
        }
      );
      if (response == {}) return;
      this.goods = [];
      this.categories = [];
      this.good_id = null;
      this.category_id = null;
      this.showSnackbar("Товар успешно добавлен");
      this.creating = false;
      this.$router.replace({ name: "Index" });
    },
  },
};
</script>

<style>
</style>