import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../store/index'
import {checkErrorStatusCode} from '@/plugins/axios_settings'

Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginPage.vue'),
    meta: { isAuth: false },
  },
  {
    path: '/map',
    name: 'Map',
    component: () => import('../views/MapPage.vue'),
    meta: { isAuth: true }
  },
  {
    path: '/graph',
    name: 'Graph',
    component: () => import('../views/GraphPage.vue'),
    meta: { isAuth: true }
  },
  {
    path: '/report',
    name: 'Report',
    component: () => import('../views/ReportsPage.vue'),
    meta: { isAuth: true }
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
  if (to.matched.some(record => record.meta.isAuth)) {
    store.dispatch('identifyUser', {})
      .then(() => { next() })
      .catch(error => { if(checkErrorStatusCode(error.response.status)) next({ name: 'Login' }) })
  } else {
    store.dispatch('identifyUser', {})
      .then(() => { next({ name: 'Map' }) })
      .catch(() => { next() })
  }
})

export default router
