<template>
  <v-card>
    <v-skeleton-loader
      class="mx-auto"
      type="card-heading"
      v-if="loading"
    ></v-skeleton-loader>
    <v-card-title v-else>
      <h3>{{ good.name }}</h3></v-card-title
    >
    <v-card-text>
      <v-skeleton-loader
        class="mx-auto"
        type="table-thead, table-tbody"
        v-if="loading"
      ></v-skeleton-loader>
      <v-simple-table v-else>
        <template v-slot:default>
          <thead>
            <tr>
              <th class="text-left">Информация о товаре</th>
              <th class="text-left"></th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Категория</td>
              <td>{{ category.name }}</td>
            </tr>
            <tr
              v-for="(value, i) in good.props"
              :key="`${i}-${value.category_filter_id}-${good.id}`"
            >
              <td>{{ getPropLabel(value.category_filter_id) }}</td>
              <td>{{ value.value }}</td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
      <v-card v-if="good.description" elevation="0"
        ><v-card-title>Описание</v-card-title
        ><v-card-text>{{ good.description }}</v-card-text></v-card
      >
      <h3 class="mt-5 text-dark">Производители</h3>
      <v-skeleton-loader
        class="mx-auto"
        type="table-thead, table-tbody"
        v-if="loading"
      ></v-skeleton-loader>
      <v-simple-table v-else>
        <template v-slot:default>
          <thead>
            <tr>
              <th class="text-left">Компания</th>
              <th class="text-left">Цена</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(company, i) in good.users"
              :key="`${company.user_id}-${i}-${good.id}-${company.price}`"
              @click="
                $router.push({
                  name: 'Company',
                  params: { id: company.user_id },
                })
              "
            >
              <td>{{ companyById(company.user_id).name }}</td>
              <td>{{ company.price || "-" }}</td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-card-text>
  </v-card>
</template>

<script>
import http from "../../http";
import { mapActions, mapGetters } from "vuex";
export default {
  data() {
    return {
      good: {
        props: {},
      },
      loading: true,
    };
  },
  computed: {
    ...mapGetters(["categoryById", "companyById"]),
    category() {
      return this.categoryById(this.good.category_id) || {};
    },
  },
  methods: {
    ...mapActions(["getCompany"]),
    getPropLabel(id) {
      return this.category?.filters?.find((v) => v.id == id)?.label;
    },
    async getCompanyObj(id) {
      let company = this.companyById(id);
      if (company) return company;
      await this.getCompany(id);
      return this.companyById(id);
    },
  },
  async mounted() {
    this.good = (await http.getItem("Good", this.$route.params.id, true)).data;
    for (const company of this.good.users) {
      await this.getCompanyObj(company.user_id);
    }
    this.loading = false;
  },
};
</script>

<style>
</style>