import { createRouter, createWebHistory } from 'vue-router'


import Dashboard from '../views/Dashboard.vue'
import Profile from '../views/Profile.vue'
import Daily from '../views/Daily.vue'
import Analysis from '../views/Analysis.vue'
import AI from '../views/AI.vue'
import Goals from '../views/Goals.vue'


const router = createRouter({

    history:createWebHistory(),

    routes:[

        {
            path:'/',
            redirect:'/dashboard'
        },

        {
            path:'/dashboard',
            component:Dashboard
        },

        {
            path:'/profile',
            component:Profile
        },

        {
            path:'/daily',
            component:Daily
        },

        {
            path:'/goals',
            component:Goals
        },

        {
            path:'/analysis',
            component:Analysis
        },

        {
            path:'/ai',
            component:AI
        }

    ]

})


export default router
