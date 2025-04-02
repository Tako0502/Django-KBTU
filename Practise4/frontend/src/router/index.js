import {createRouter, createWebHistory} from "vue-router";

import Login from "../views/LoginView.vue";

import Admin from "../views/AdminView.vue";

import Register from "../views/RegisterView.vue";

import store from "../store";

const routes = [
    {path: "/", component: Login},

    {
        path: "/admin",

        component: Admin,

        meta: {requiresAdmin: true},
    },
    {path: '/register', component: Register},
];

const router = createRouter({history: createWebHistory(), routes});

router.beforeEach(async (to, from, next) => {
    if (to.meta.requiresAdmin) {
        await store.dispatch("fetchUser");

        if (store.state.user?.role === "admin") {
            next();
        } else {
            next("/");
        }
    } else {
        next();
    }
});

export default router;
