<template>
  <div>
    <company-card />
    <h3 class="my-5" v-if="goods.total != 0">Товары производителя</h3>
    <v-divider></v-divider>
    <v-row>
      <v-col>
        <v-row>
          <v-col
            cols="3"
            v-for="(good, i) in goods.items"
            :key="`${i}-${good.id}`"
          >
            <list-good-card :good="good" :show_category="true" />
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <v-row v-if="loading">
      <v-col cols="3" v-for="i in 4" :key="`${i}-sceleton`">
        <v-sheet elevation="2">
          <v-skeleton-loader
            class="mx-auto"
            type="card-heading, list-item-three-line, list-item"
          ></v-skeleton-loader>
        </v-sheet>
      </v-col>
    </v-row>
    <v-row v-if="length > 1">
      <v-col cols="4"> &nbsp;</v-col>
      <v-col>
        <v-pagination v-model="page" :length="length" :total-visible="7" circle></v-pagination>
      </v-col>
      <v-col cols="4"> </v-col>
    </v-row>
  </div>
</template>

<script>
import CompanyCard from "@/components/cards/CompanyCard.vue";
import ListGoodCard from "@/components/cards/ListGoodCard.vue";
import http from "@/http";
export default {
  components: { CompanyCard, ListGoodCard },
  data() {
    return {
      goods: {
        size: 12,
        total: 0,
      },
      page: 1,
      loading: true,
    };
  },
  computed: {
    length() {
      return Math.round(this.goods.total / this.goods.size) + 1;
    },
  },
  async mounted() {
    await this.setGoods();
  },
  watch: {
    async page() {
      await this.setGoods();
    },
  },
  methods: {
    async setGoods() {
      this.loading = true;
      this.goods = {items: []};
      let response = (
        await http.getList(
          `/api/companies/${this.$route.params.id}/goods/`,
          { page: this.page, size: 12 },
          true
        )
      ).data;
      this.goods = response;
      this.loading = false;
    },
  },
};
</script>

<style>
</style>