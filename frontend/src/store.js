import Vuex from "vuex";
import http from "./http";
import Axios from "axios";
import Vue from "vue";

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    user: null,
    isAuthenticated: false,
    categories: [],
    goodsCategories: [],
    search: "",
    autocompleteItems: [],
    goods: {},
    goodsFilters: {},
    selectedCategoryId: null,
    companies: [],
    goodsPage: 1,
    createCategoryId: null,
    createGoodId: null,
    createGoodsList: [],
    showSnackbar: false,
    snackbarText: "",
    loadingGoods: false,
    loadingGoodsCategories: false,
  },
  getters: {
    categoryById: (state) => (id) => {
      return state.categories.find((v) => v.id == id);
    },
    companyById: (state) => (id) => {
      return state.companies.find((v) => v.id == id);
    },
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    setAuthenticated(state, isAuthenticated) {
      state.isAuthenticated = isAuthenticated;
    },
    setCategories(state, categories) {
      state.categories = categories;
    },
    setSearch(state, search) {
      state.search = search;
    },
    setAutocompleteItems(state, autocompleteItems) {
      state.autocompleteItems = autocompleteItems;
    },
    setGoods(state, goods) {
      state.goods = goods;
    },
    setGoodsFilters(state, goodsFilters) {
      state.goodsFilters = goodsFilters;
    },
    setSelectedCategoryId(state, selectedCategoryId) {
      state.selectedCategoryId = selectedCategoryId;
    },
    setCompanies(state, companies) {
      state.companies = companies;
    },
    setGoodsPage(state, page) {
      state.goodsPage = page;
    },
    setCreateCategoryId(state, id) {
      state.createCategoryId = id;
    },
    setCreateGoodId(state, id) {
      state.createGoodId = id;
    },
    setCreateGoodsList(state, goods) {
      state.createGoodsList = goods;
    },
    setShowSnackbar(state, showSnackbar) {
      state.showSnackbar = showSnackbar;
    },
    showSnackbar(state, snackbarText) {
      state.snackbarText = snackbarText;
      state.showSnackbar = true;
    },
    setLoadingGoods(state, loadingGoods) {
      state.loadingGoods = loadingGoods;
    },
    setLoadingGoodsCategories(state, value) {
      state.loadingGoodsCategories = value;
    },
    setGoodsCategories(state, value) {
      state.goodsCategories = value;
    },
  },
  actions: {
    async getCategories(context) {
      const response = await http.getList("Category", {}, true);
      context.commit("setCategories", response.data);
    },
    async getCompanies(context) {
      const response = await http.getList("Companies", {}, true);
      context.commit("setCompanies", response.data);
    },
    async getCompany(context, id) {
      const response = await http.getItem("Companies", id, true);
      context.commit("setCompanies", [
        ...context.state.companies,
        response.data,
      ]);
    },
    async getGoods(context) {
      context.commit("setLoadingGoods", true);
      context.commit("setGoods", {
        total: context.state.goods.total,
        size: context.state.goods.size,
      });
      let filters = {
        ...context.state.goodsFilters,
        page: context.state.goodsPage,
        size: 12,
        status: "approved",
      };
      if (context.state.search) {
        filters.name = context.state.search;
      }
      if (context.state.selectedCategoryId) {
        filters.category_id = context.state.selectedCategoryId;
      }
      const response = await http.getList("Good", filters, true);
      context.commit("setGoods", response.data);
      context.commit("setLoadingGoods", false);
    },
    async getGoodsCategories(context) {
      if (!context.state.search || context.state.selectedCategoryId) {
        context.commit("setGoodsCategories", []);
      }
      context.commit("setLoadingGoodsCategories", true);
      const response = await http.getList(
        "CategoriesByGoodName",
        { name: context.state.name },
        true
      );
      context.commit("setGoodsCategories", response.data);
      context.commit("setLoadingGoodsCategories", false);
    },
    async addItem(context, data) {
      let item_data = data.data;
      let mutation = data.mutation;
      let response = (await http.createItem(data.url, item_data, true)).data;
      let items = context.state[data.items_name];
      items.push(response);
      context.commit(mutation, items);
    },
    async updateItem(context, data) {
      let item_data = data.data;
      let mutation = data.mutation;
      let dataID = data.dataID;
      let response = (await http.updateItem(data.url, dataID, item_data, true))
        .data;
      let items = context.state[data.items_name];
      let index = items.findIndex((v) => v.id == dataID);
      if (index != -1) {
        Vue.set(items, index, response);
      }
      context.commit(mutation, items);
    },
    async login(context, creds) {
      var username = creds.username;
      var password = creds.password;
      var reg_exp_mail = /^[\w-.]+@([\w-]+\.)+[\w-]{2,4}$/;
      var login_info = {
        email: username,
        password: password,
      };
      if (username.match(reg_exp_mail) != null) {
        login_info = {
          email: username,
          password: password,
        };
      } else {
        login_info = {
          username: username,
          password: password,
        };
      }
      var status = false;
      try {
        var response = (await Axios.post("/api/auth/sign-in/", login_info))
          .data;
        localStorage.setItem("access_token", response.access_token);
        localStorage.setItem("token_type", response.token_type);
        status = true;
      } catch (error) {
        var data = error.response.data;
        if (data.non_field_errors) {
          Vue.showErrorModal(data.non_field_errors);
        } else {
          var result = "";
          for (var k in data) {
            result += `${k}: ${data[k]}\n`;
          }
          Vue.showErrorModal(result);
        }
      }
      await context.dispatch("checkAuth");
      return status;
    },
    async logout(context) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("token_type");
      context.commit("setAuthenticated", false);
      context.commit("setUser", {});
    },
    async checkAuth(context) {
      try {
        var result = await Axios.get("/api/auth/user/", {
          headers: http.getHeaders(),
        });
        if (result.status != 200) {
          context.commit("setUser", {});
          return;
        }
        context.commit("setAuthenticated", true);
        context.commit("setUser", result.data);
      } catch (e) {
        context.commit("setUser", {});
      }
    },
  },
});

export default store;
