import { createWebHistory, createRouter } from 'vue-router'
import VocalyticsHome from '../views/VocalyticsHome.vue'
import HisTory from '../views/HisTory.vue'
import AllTranscripts from '../views/AllTranscripts.vue'
import HomePage from '../views/HomePage.vue'
import SignUp from '../authorization/SignUp.vue'
import UserInsights from '../views/UserInsights.vue'
import AdminInsights from '../views/AdminInsights.vue'
import SearchResults from '../views/SearchResults.vue'
import ABout from '../views/ABout.vue'
import ConTact from '../views/ConTact.vue'


const routes = [
    {
        path: '/',
        name: 'VocalyticsHome',
        component: VocalyticsHome
    },
    {
        path: '/register',
        name: 'SignUp',
        component: SignUp
    },
    {
        path: '/home',
        name: 'HomePage',
        component: HomePage
    },
    {
        path: '/history',
        name: 'HisTory',
        component: HisTory
    },
    {
        path: '/searchresults',
        name: 'SearchResults',
        component: SearchResults
    },
    {
        path: '/alltranscripts',
        name: 'AllTranscripts',
        component: AllTranscripts
    },
    {
        path: '/insights',
        name: 'UserInsights',
        component: UserInsights
    },
    {
        path: '/admininsights',
        name: 'AdminInsights',
        component: AdminInsights
    },
    {
        path: '/about',
        name: 'ABout',
        component: ABout
    },
    {
        path: '/contact',
        name: 'ConTact',
        component: ConTact
    },
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
  })
  
  export default router