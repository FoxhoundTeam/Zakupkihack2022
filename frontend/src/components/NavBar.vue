<template>
  <v-app-bar app>
    <v-app-bar-title
      ><router-link
        :to="{ name: 'Index' }"
        class="text-decoration-none text-dark"
        >FoxТорг</router-link
      ></v-app-bar-title
    >
    <v-btn
      v-if="$route.name != 'SearchCompany'"
      link
      text
      :to="{ name: 'SearchCompany' }"
      class="text-dark"
      dark
      >Поиск производителей</v-btn
    >
    <v-btn
      v-if="!['Search', 'Index'].includes($route.name)"
      link
      text
      :to="{ name: 'Search' }"
      class="text-dark"
      dark
      >Поиск товаров</v-btn
    >
    <search-field
      v-if="$route.name == 'Search'"
      class="ml-5 mt-5 py-0"
      :dense="true"
    />
    <v-spacer></v-spacer>
    <v-btn v-if="!isAuthenticated" color="primary" :to="{ name: 'Login' }"
      >Войти</v-btn
    >
    <div v-else>
      <v-btn
        v-if="isCompany(user)"
        link
        text
        :to="{ name: 'MyGoods' }"
        class="text-dark"
        dark
        >Мои товары</v-btn
      >
      <v-btn
        v-if="isCompany(user)"
        link
        text
        :to="{ name: 'AddGood' }"
        class="text-dark"
        dark
        >Добавить товар</v-btn
      >
      <v-btn
        v-if="isAdminOrModerator(user)"
        link
        text
        :to="{ name: 'AdminCategory' }"
        class="text-dark"
        dark
        >Настроить категории</v-btn
      >
      <v-btn
        v-if="isAdminOrModerator(user)"
        link
        text
        :to="{ name: 'AdminGood' }"
        class="text-dark"
        dark
        >Настроить товары</v-btn
      >
      <v-menu open-on-hover bottom offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn text class="text-dark" dark v-bind="attrs" v-on="on"
            ><v-icon left dark> mdi-account </v-icon>
            {{ user.name }}
          </v-btn>
        </template>

        <v-list>
          <div v-if="isCompany(user)">
            <v-list-item v-if="user.username">
              <v-list-item-title>ИНН: {{ user.username }}</v-list-item-title>
            </v-list-item>
            <v-list-item v-if="user.phone">
              <v-list-item-title>Телефон: {{ user.phone }}</v-list-item-title>
            </v-list-item>
            <v-list-item v-if="user.email">
              <v-list-item-title>Почта: {{ user.email }}</v-list-item-title>
            </v-list-item>
            <v-divider />
          </div>
          <v-list-item link>
            <v-list-item-title @click="logout">Выйти</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </div>
  </v-app-bar>
</template>

<script>
import SearchField from "./fields/SearchField.vue";
import { mapActions, mapState } from "vuex";
import { isCompany, isAdminOrModerator } from "../helpers";

export default {
  components: { SearchField },
  data() {
    return {
      isCompany: isCompany,
      isAdminOrModerator: isAdminOrModerator,
    };
  },
  computed: {
    ...mapState(["user", "isAuthenticated"]),
  },
  methods: {
    async logout() {
      await this.logoutDispatch();
      this.$router.replace({ name: "Index" });
    },
    ...mapActions({
      logoutDispatch: "logout",
    }),
  },
};
</script>

<style>
</style>