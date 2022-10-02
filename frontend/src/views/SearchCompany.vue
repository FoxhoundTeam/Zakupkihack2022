<template>
  <div class="ml-5 mr-5">
    <v-row>
      <v-col cols="12"
        ><v-text-field
          v-model="search"
          label="Название / ИНН"
          outlined
        ></v-text-field
      ></v-col>
    </v-row>
    <v-row>
      <v-col cols="12"
        ><v-autocomplete
          outlined
          label="Категория"
          :items="categories.filter((v) => v.status == 'approved')"
          v-model="categoryId"
          item-text="name"
          item-value="id"
          clearable
        ></v-autocomplete
      ></v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-row>
          <v-col
            cols="3"
            v-for="(company, i) in companies.items"
            :key="`${i}-${company.id}`"
          >
            <list-company-card :company="company" />
          </v-col>
        </v-row>
        <v-row v-if="loading">
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
    <v-row v-if="length > 1">
      <v-col cols="4"> &nbsp;</v-col>
      <v-col>
        <v-pagination
          :disabled="loading"
          v-model="page"
          :length="length"
          :total-visible="7"
          circle
        ></v-pagination>
      </v-col>
      <v-col cols="4"> </v-col>
    </v-row>
  </div>
</template>

<script>
import ListCompanyCard from "@/components/cards/ListCompanyCard.vue";
import http from "@/http";
import { mapState } from "vuex";
export default {
  components: { ListCompanyCard },
  data() {
    return {
      categoryId: null,
      companies: {
        total: 0,
        size: 12,
        imtems: [],
      },
      page: 1,
      search: "",
      initializing: true,
      loading: true,
    };
  },
  computed: {
    ...mapState(["categories"]),
    length() {
      if (this.companies.total % this.companies.size == 0)
        return this.companies.total / this.companies.size;
      return parseInt(this.companies.total / this.companies.size) + 1 || 1;
    },
  },
  methods: {
    async getCompanies() {
      this.loading = true;
      this.companies = {
        items: [],
        total: this.companies.total,
        size: this.companies.size,
      };
      let filters = {
        page: this.page,
        size: 12,
      };
      if (this.categoryId) {
        filters.category_id = this.categoryId;
      }
      if (this.search) {
        filters.q = this.search;
      }
      this.companies = (
        await http.getList("SearchCompanies", filters, true)
      ).data;
      this.loading = false;
    },
  },
  async mounted() {
    if (this.$route.query.page) {
      this.page = Number(this.$route.query.page);
    }
    if (this.$route.query.category_id) {
      this.categoryId = Number(this.$route.query.category_id);
    }
    if (this.$route.query.q) {
      this.search = this.$route.query.q;
    }
    await this.getCompanies();
    this.initializing = false;
  },
  watch: {
    async categoryId(value) {
      this.$router.push({
        name: "SearchCompany",
        query: { ...this.$route.query, category_id: value },
      });
      if (this.initializing) {
        return;
      }
      if (this.page == 1) await this.getCompanies();
      else this.page = 1;
    },
    async search(value) {
      if (this.initializing) return;
      this.$router.push({
        name: "SearchCompany",
        query: { ...this.$route.query, q: value },
      });
      if (this.page == 1) await this.getCompanies();
      else this.page = 1;
    },
    async page(value) {
      if (this.initializing) return;
      this.$router.push({
        name: "SearchCompany",
        query: { ...this.$route.query, page: value },
      });
      await this.getCompanies();
    },
  },
};
</script>

<style>
</style>