<template>
  <v-card elevation="0">
    <v-card-title><h1>{{ label }}</h1></v-card-title>
    <v-row v-if="loading">
      <v-col :cols="12 / columns" v-for="(part, i) in parts" :key="i">
        <v-list dense>
          <v-list-item-group>
            <v-skeleton-loader
                v-for="i in 3"
                :key="`category-skeleton-${i}`"
                class="mx-auto"
                type="list-item"
              ></v-skeleton-loader>
          </v-list-item-group>
        </v-list>
      </v-col>
    </v-row>
    <v-row v-else>
      <v-col :cols="12 / columns" v-for="(part, i) in parts" :key="i">
        <v-list dense>
          <v-list-item-group>
            <v-list-item
              link
              :to="{ name: 'Search', query: getFilters(category) }"
              v-for="(category, i) in part"
              :key="`${i}-${category.id}`"
            >
              <v-list-item-content>
                <v-list-item-title v-text="category.name"></v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import { mapState } from 'vuex';
export default {
    props: {
        label: {
            type: String,
            default: "Категории",
        },
        columns: {
            type: Number,
            default: 4,
        },
        categories: {
            default: []
        },
        loading: {
            default: false
        }
    },
  computed: {
    ...mapState(["search"]),
    parts() {
      const total = this.categories.length;
      const part = Math.round(total / 4);
      const parts = [];
      for (const i of [...Array(this.columns).keys()]) {
        parts.push(
          this.categories.slice(i * part, i * part + part)
        );
      }
      return parts;
    },
  },
  methods: {
    getFilters(category) {
        const filters = {category_id: category.id};
        if (this.search) {
            filters.q = this.search;
        }
        return filters
    }
  }
};
</script>

<style>
</style>