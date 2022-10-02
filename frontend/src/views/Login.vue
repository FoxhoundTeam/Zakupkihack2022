<template>
  <b-container>
    <b-row class="mt-5">
      <b-col cols="12"><h1>FoxТорг</h1></b-col>
    </b-row>
    <b-row>
      <b-col class="my-1" sm="7" order-sm="1" order="12">
        <!-- <b-img class="w-75" :src="hackLogo"></b-img> -->
        <h3 class="mt-2">
          Площадка для поиска и аналитики по товарам, работам, услугам (ТРУ) для производителей/поставщиков и заказчиков.
        </h3></b-col
      >
      <b-col class="my-1" order-sm="12" order="1" sm="5">
        <b-card>
          <v-text-field label="Логин" v-model="username"></v-text-field>
          <v-text-field
            label="Пароль"
            v-model="password"
            type="password"
            @keyup.enter="login"
          ></v-text-field>
          <v-btn @click="login" block color="primary">Войти</v-btn>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import { mapActions, mapState } from "vuex";
export default {
  data() {
    return {
      username: "",
      password: "",
    };
  },
  computed: {
    ...mapState(["isAuthenticated"]),
  },
  methods: {
    ...mapActions({ loginDispatch: "login" }),
    async login() {
      await this.loginDispatch({
        username: this.username,
        password: this.password,
      });
      this.$router.replace({ name: "Index" });
    },
  },
  beforeMount() {
    if (this.isAuthenticated) {
      this.$router.replace({ name: "Index" });
    }
  },
};
</script>

<style>
.temp {
  width: 80px;
}
</style>