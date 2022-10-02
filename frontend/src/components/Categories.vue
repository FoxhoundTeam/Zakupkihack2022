<template>
  <v-card elevation="0">
    <v-card-title><h1>{{ label }}</h1></v-card-title>
    <v-row v-if="loading">
      <v-col cols="3" v-for="(part, i) in parts" :key="i">
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
      <v-col :cols="12 / cols" v-for="(part, i) in parts" :key="i">
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
            default: "auto",
        },
        categories: {
            default: [],
        },
        loading: {
            default: false
        }
    },
  computed: {
    ...mapState(["search"]),
    cols() {
        if (this.columns !== "auto") return this.columns
        const total = this.categories.length;
        return Math.min(Math.round(total / 5), 4) || 1
    },
    parts() {
      const total = this.categories.length;
      const part = Math.round(total / this.cols);
      const parts = [];
      for (const i of [...Array(this.cols).keys()]) {
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