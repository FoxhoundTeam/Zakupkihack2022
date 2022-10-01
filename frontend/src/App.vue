<template>
  <div id="app">
    <v-app style="min-height: 100vh">
      <nav-bar />
      <v-main class="m-2">
        <router-view></router-view>
      </v-main>
      <v-dialog v-model="showErrorModal" max-width="300">
        <v-card>
          <v-card-title class="text-h5"> Ошибка </v-card-title>

          <v-card-text>
            {{ modalContent }}
          </v-card-text>

          <v-card-actions>
            <v-btn color="green darken-1" text @click="showErrorModal = false">
              OK
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-overlay :value="appLoading">
        <v-progress-circular indeterminate size="64"></v-progress-circular>
      </v-overlay>
    </v-app>
  </div>
</template>

<script>
import NavBar from "./components/NavBar.vue";
import ErrorModal from "./plugins/ErrorModal";

export default {
  components: { NavBar },
  name: "app",
  data() {
    return {
      showErrorModal: false,
      modalContent: null,
      appLoading: true,
    };
  },
  async mounted() {
    ErrorModal.ErrorEvent.$on("show", (params) => {
      this.modalContent = params.data;
      this.showErrorModal = true;
    });
    this.appLoading = false;
  },
};
</script>
<style>
a {
  text-decoration: none !important;
}
</style>
