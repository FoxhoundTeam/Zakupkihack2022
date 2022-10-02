<template>
  <div>
    <v-row dense v-if="!search || selectedCategoryId"
      ><v-col cols="12"
        ><v-autocomplete
          outlined
          label="Категория"
          :items="categories.filter((v) => v.status == 'approved')"
          v-model="selectedCategoryId"
          :item-text="getCategoryName"
          item-value="id"
          clearable
        ></v-autocomplete></v-col
    ></v-row>
    <v-row dense>
      <v-col
        cols="12"
        v-for="(filter, i) in selectedCategory.filters"
        :key="`${filter.id}-${i}`"
      >
        <check-box-filter
          v-if="filter.type === 'checkbox'"
          :label="filter.label"
          :choices="filter.choices"
          :id="filter.id"
        />
        <radio-button-filter
          v-else-if="filter.type === 'radio'"
          :label="filter.label"
          :choices="filter.choices"
          :id="filter.id"
        />
        <range-filter
          v-else-if="filter.type === 'range'"
          :label="filter.label"
          :id="filter.id"
        />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { mapActions, mapGetters, mapMutations, mapState } from "vuex";
import CheckBoxFilter from "./filters/CheckBoxFilter.vue";
import RadioButtonFilter from "./filters/RadioButtonFilter.vue";
import RangeFilter from "./filters/RangeFilter.vue";
export default {
  components: { CheckBoxFilter, RadioButtonFilter, RangeFilter },
  computed: {
    ...mapGetters(["categoryById"]),
    ...mapState(["categories", "search"]),
    selectedCategory() {
      return this.categoryById(this.selectedCategoryId) || {};
    },
    selectedCategoryId: {
      get() {
        return this.$store.state.selectedCategoryId;
      },
      set(value) {
        this.setSelectedCategoryId(value);
      },
    },
  },
  methods: {
    ...mapActions(["getGoods", "getGoodsCategories", "getPriceStats"]),
    ...mapMutations(["setSelectedCategoryId", "setGoodsFilters"]),
    getCategoryName(category) {
      if (category.name.length < 27) return category.name
      return category.name.slice(0, 25) + "..."
    }
  },
  watch: {
    async selectedCategoryId(value) {
      await this.getGoods();
      await this.getGoodsCategories();
      await this.getPriceStats();
      const query = { ...this.$route.query, category_id: value };
      if (!value) {
        delete query.category_id;
      }
      this.$router.replace({
        name: "Search",
        query: query,
      });
    },
    $route(value) {
      if (value.query.category_id) {
        this.selectedCategoryId = Number(value.query.category_id);
      } else {
        this.selectedCategoryId = null;
      }
    },
  },
  mounted() {
    if (this.$route.query.category_id) {
      this.selectedCategoryId = Number(this.$route.query.category_id);
    } else {
      this.selectedCategoryId = null;
    }
  },
  beforeDestroy() {
      this.setGoodsFilters({});
  }
};
</script>

<style>
</style>