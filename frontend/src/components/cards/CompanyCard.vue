<template>
  <v-card>
    <v-card-title>{{ company.name }}</v-card-title>
    <v-card-text>
      <v-simple-table>
        <template v-slot:default>
          <thead>
            <tr>
              <th class="text-left">Информация о производителе</th>
              <th class="text-left"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="company.address">
              <td>Адрес</td>
              <td>{{ company.address }}</td>
            </tr>
            <tr v-if="company.phone">
              <td>Телефон</td>
              <td>
                <a :href="`tel:${company.phone}`">{{ company.phone }}</a>
              </td>
            </tr>
            <tr v-if="company.site">
              <td>Сайт</td>
              <td>
                <a :href="company.site">{{ company.site }}</a>
              </td>
            </tr>
            <tr v-if="company.email">
              <td>Почта</td>
              <td>
                <a :href="`mailto:${company.email}`">{{ company.email }}</a>
              </td>
            </tr>
            <tr v-if="company.username">
              <td>ИНН</td>
              <td>{{ company.username }}</td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-card-text>
  </v-card>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
export default {
  data() {
    return {
      company: {},
    };
  },
  computed: {
    ...mapGetters(["companyById"]),
  },
  methods: {
    ...mapActions(["getCompany"]),
  },
  async mounted() {
    if (this.companyById(this.$route.params.id))
      this.company = this.companyById(this.$route.params.id);
    else {
      await this.getCompany(this.$route.params.id);
      this.company = this.companyById(this.$route.params.id);
    }
  },
};
</script>

<style>
</style>