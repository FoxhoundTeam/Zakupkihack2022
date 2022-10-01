import Vue from 'vue'
import VueRouter from 'vue-router'


Vue.use(VueRouter)

let opts = {
  routes: [
    {
      path: "/",
      name: "Index",
      component: () => import('../views/Index.vue'),
      meta: {
        requiresAuth: false
      }
    },
    {
      path: "/login",
      name: "Login",
      component: () => import('../views/Login.vue'),
      meta: {
        requiresAuth: false
      }
    },
    {
      path: "/search",
      name: "Search",
      component: () => import('../views/Search.vue'),
      meta: {
        requiresAuth: false
      },
    },
    {
      path: "/search_company",
      name: "SearchCompany",
      component: () => import('../views/SearchCompany.vue'),
      meta: {
        requiresAuth: false
      },
    },
    {
      path: "/catalog",
      name: "Catalog",
      component: () => import('../views/Catalog.vue'),
      meta: {
        requiresAuth: false
      },
    },
    {
      path: "/company/:id",
      name: "Company",
      component: () => import('../views/CompanyInfo.vue'),
      meta: {
        requiresAuth: false
      },
    },
    {
      path: "/good/create",
      name: "AddGood",
      component: () => import('../views/AddGood.vue'),
      meta: {
        requiresAuth: true,
        groups: ["company"],
      },
    },
    {
      path: "/good/my",
      name: "MyGoods",
      component: () => import('../views/CompanyGoods.vue'),
      meta: {
        requiresAuth: true,
        groups: ["company"],
      },
    },
    {
      path: "/good/admin",
      name: "AdminGood",
      component: () => import('../views/ModerateGoods.vue'),
      meta: {
        requiresAuth: true,
        groups: ["admin", "moderator"],
      },
    },
    {
      path: "/category/admin",
      name: "AdminCategory",
      component: () => import('../views/ModerateCategories.vue'),
      meta: {
        requiresAuth: true,
        groups: ["admin", "moderator"],
      },
    },
    {
      path: "/good/:id",
      name: "Good",
      component: () => import('../views/GoodInfo.vue'),
      meta: {
        requiresAuth: false
      },
    },
    // {
    //   path: "/editor",
    //   name: "Editor",
    //   component: () => import('../views/Editor.vue'),
    //   meta: {
    //     requiresAuth: false
    //   },
    //   children: [
    //     {
    //       path: "add_dataset",
    //       name: "SelectDataset",
    //       component: () => import('../components/modals/ModalSelectDataset.vue'),
    //       meta: {
    //         requiresAuth: false
    //       },
    //     },
    //     {
    //       path: "result",
    //       name: "ShowResult",
    //       component: () => import('../components/modals/ModalShowSavedRes.vue'),
    //       meta: {
    //         requiresAuth: false
    //       },
    //     }
    //   ]
    // },
  ],
  linkExactActiveClass: 'active'
};
const router = new VueRouter(opts);

export default router
