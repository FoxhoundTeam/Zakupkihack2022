<template>
  <div fluid class="mx-5 mt-5">
    <categories
      v-if="!selectedCategoryId && search"
      :categories="goodsCategories"
      :loading="loadingGoodsCategories"
    />
    <v-row v-if="length > 1">
      <v-col cols="4"> &nbsp;</v-col>
      <v-col>
        <v-pagination
          :disabled="loadingGoods"
          v-model="page"
          :length="length"
          :total-visible="7"
          circle
        ></v-pagination>
      </v-col>
      <v-col cols="4"> </v-col>
    </v-row>
    <v-row>
      <v-col cols="2">
        <filter-left-side />
      </v-col>
      <v-col cols="10">
        <v-row>
          <v-col
            cols="3"
            v-for="(good, i) in goods.items"
            :key="`${i}-${good.id}`"
          >
            <list-good-card :good="good" :show_category="true" />
          </v-col>
        </v-row>
        <v-row v-if="loadingGoods">
          <v-col cols="3" v-for="i in 12" :key="`${i}-skeleton`">
            <v-sheet elevation="2">
              <v-skeleton-loader
                class="mx-auto"
                type="card-heading, list-item-three-line"
              ></v-skeleton-loader>
            </v-sheet>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import FilterLeftSide from "@/components/FilterLeftSide.vue";
import ListGoodCard from "@/components/cards/ListGoodCard.vue";
import Categories from "../components/Categories.vue";
import { mapActions, mapState } from "vuex";
export default {
  components: {
    FilterLeftSide,
    ListGoodCard,
    Categories,
  },
  data() {
    return {
      page: 1,
    };
  },
  async mounted() {
    if (this.$route.query.page) {
      this.page = Number(this.$route.query.page);
    }
    await this.getGoods();
    await this.getGoodsCategories();
  },
  computed: {
    ...mapState([
      "search",
      "goods",
      "loadingGoods",
      "loadingGoodsCategories",
      "goodsCategories",
      "selectedCategoryId",
    ]),
    length() {
      return Math.round(this.goods.total / this.goods.size) + 1 || 1;
    },
  },
  methods: {
    ...mapActions(["getGoods", "getGoodsCategories"]),
  },
  watch: {
    async search(value) {
      this.$router.push({
        name: "Search",
        query: { ...this.$route.query, q: value },
      });
      if (this.page == 1) {
        await this.getGoods();
      } else {
        this.page = 1;
      }
      await this.getGoodsCategories();
    },
    async page(value) {
      await this.getGoods();
      this.$router.push({
        name: "Search",
        query: { ...this.$route.query, page: value },
      });
    },
  },
};
</script>

<style>
</style>