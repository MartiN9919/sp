import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../store/index'
import {checkErrorStatusCode} from '@/plugins/axiosSettings'

Vue.use(VueRouter)


const routes = [
  {
    path: '/login',
    name: 'Login',
    components: {
      default: () => import('../views/LoginPage.vue'),
    },
    beforeEnter: (to, from, next) => {
      store.commit('resetState')
      next()
    },
    meta: { auth: false },
  },
  {
    path: '/map',
    name: 'Map',
    components: {
      default: () => import('../views/MapPage.vue'),
      appbar: () => import('../components/WebsiteShell/UIMainComponents/appBar.vue'),
    },
    meta: { auth: true }
  },
  {
    path: '/graph',
    name: 'Graph',
    components: {
      default: () => import('../views/GraphPage.vue'),
      appbar: () => import('../components/WebsiteShell/UIMainComponents/appBar.vue'),
    },
    meta: { auth: true }
  },
  {
    path: '/report',
    name: 'Report',
    components: {
      default: () => import('../views/ReportsPage.vue'),
      appbar: () => import('../components/WebsiteShell/UIMainComponents/appBar.vue'),
    },
    meta: { auth: true }
  },
  {
    path: '*',
    redirect:  { name: 'Login' }
  },
]

const router = new VueRouter({
  mode: 'history',
  routes
})

router.beforeResolve((to, from, next) => {
  if (to.matched.some(record => record.meta.auth))
    store.dispatch('identifyUser')
      .then(() => next())
      .catch(error => checkErrorStatusCode(error.response) ? next({ name: 'Login' }) : next())
  else
    store.dispatch('identifyUser')
      .then(() => next({ name: 'Map' }))
      .catch(() => next())
})

export default router
