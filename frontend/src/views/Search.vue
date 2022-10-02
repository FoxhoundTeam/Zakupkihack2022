<template>
  <div fluid class="mx-5 mt-5">
    <categories
      v-if="!selectedCategoryId && search"
      :categories="goodsCategories"
      :loading="loadingGoodsCategories"
    />
    <price-chart v-if="selectedCategoryId && priceStats.labels" :labels="priceStats.labels" :data="priceStats.data"/>
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
import { mapActions, mapMutations, mapState } from "vuex";
import PriceChart from '@/components/PriceChart.vue';
export default {
  components: {
    FilterLeftSide,
    ListGoodCard,
    Categories,
    PriceChart,
  },
  async mounted() {
    if (this.$route.query.page) {
      this.page = Number(this.$route.query.page);
    } else {
      await this.getGoods(this.page);
    }
    await this.getGoodsCategories();
    await this.getPriceStats();
  },
  computed: {
    ...mapState([
      "search",
      "goods",
      "loadingGoods",
      "loadingGoodsCategories",
      "goodsCategories",
      "selectedCategoryId",
      "goodsPage",
      "priceStats",
    ]),
    length() {
      if (this.goods.total % this.goods.size == 0)
        return this.goods.total / this.goods.size;
      return parseInt(this.goods.total / this.goods.size) + 1 || 1;
    },
    page: {
      get() {
        return this.goodsPage;
      },
      set(value) {
        this.setGoodsPage(value);
      },
    },
  },
  methods: {
    ...mapActions(["getGoods", "getGoodsCategories", "getPriceStats"]),
    ...mapMutations(["setGoodsPage"]),
  },
  watch: {
    async search(value) {
      this.$router.push({
        name: "Search",
        query: { ...this.$route.query, q: value },
      });
      if (this.page == 1) {
        await this.getGoods(this.page);
      } else {
        this.page = 1;
      }
      await this.getGoodsCategories();
      await this.getPriceStats();
    },
    async page(value) {
      this.$router.push({
        name: "Search",
        query: { ...this.$route.query, page: value },
      });
      await this.getGoods(value);
    },
  },
};
</script>

<style>
</style>