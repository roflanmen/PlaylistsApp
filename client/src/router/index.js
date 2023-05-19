import Vue from 'vue';
import VueRouter from 'vue-router';
import Index from '@/views/Index.vue';

Vue.use(VueRouter);

const routes = [
    {
        path: '/',
        name: 'Index',
        component: Index,
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('../views/Login.vue'),
    },
    {
        path: '/register',
        name: 'Register',
        component: () => import('../views/Register.vue'),
    },
    {
        path: '/profile',
        name: 'Profile',
        component: () => import('../views/Profile.vue'),
    },
    {
        path: '/playlist/:id',
        name: 'Playlist',
        component: () => import('../views/Playlist.vue'),
    },
    {
        path: '/search/:query',
        name: 'Search',
        component: () => import('../views/Search.vue'),
    },
    {
        path: '/profile/:id',
        name: 'Profile',
        component: () => import('../views/Profile.vue'),
    },
    {
        path: '/editprofile',
        name: 'EditProfile',
        component: () => import('../views/EditProfile.vue'),
    },
    {
        path: '/editprofile/:id/',
        name: 'EditProfile',
        component: () => import('../views/EditProfile.vue'),
    },
    {
        path: '*',
        name: 'NotFound',
        component: () => import('../views/NotFound.vue'),
    },
];

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes,
});

export default router;
