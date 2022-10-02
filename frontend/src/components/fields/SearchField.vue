<template>
  <v-autocomplete
    @keyup.enter="doSearch(searchInput)"
    v-model="selected"
    no-filter
    :items="items"
    :loading="isLoading"
    :search-input.sync="searchInput"
    hide-selected
    hide-no-data
    label="Поиск"
    clearable
    rounded
    outlined
    append-icon=""
    append-outer-icon="mdi-magnify"
    @click:append-outer="doSearch(searchInput)"
    :dense="dense"
  >
    <template #item="{ item }">
      <v-list-item class="d-flex" @click="doSearch(item)">
        <div class="ml-2">{{ item }}</div>
      </v-list-item>
    </template>
  </v-autocomplete>
</template>

<script>
import http from "../../http";
import _debounce from "lodash/debounce";
import { mapMutations, mapState } from "vuex";
export default {
  props: {
    dense: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      searchInput: "",
      isLoading: false,
    };
  },
  methods: {
    ...mapMutations(["setAutocompleteItems", "setSearch"]),
    doSearch(value) {
      this.items = [value];
      this.selected = value;
      this.$router.push({
        name: "Search",
        query: { ...this.$route.query, q: value },
      });
    },
    autocomplete: _debounce(async function (value) {
      var response = await http.getList("Autocomplete", { q: value }, false);
      this.items = response.data;
      this.isLoading = false;
    }, 500),
  },
  computed: {
    ...mapState(["autocompleteItems", "search"]),
    items: {
      get() {
        return this.autocompleteItems;
      },
      set(value) {
        this.setAutocompleteItems(value);
      },
    },
    selected: {
      get() {
        return this.search;
      },
      set(value) {
        this.setSearch(value);
      },
    },
  },
  watch: {
    async searchInput(value) {
      if (
        !value ||
        value == this.$route.query.q ||
        this.isLoading ||
        value.length < 2
      ) {
        return;
      }
      this.isLoading = true;
      await this.autocomplete(value);
    },
    $route(value) {
      this.items = [value.query.q];
      this.selected = value.query.q;
    },
  },
  mounted() {
    this.items = [this.$route.query.q];
    this.selected = this.$route.query.q;
  },
};
</script>

<style>
</style>