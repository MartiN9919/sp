import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Doc from '../views/Doc.vue'
import Info from '../views/Info.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/about',
    name: 'About',
    component: function () {
      return import(/* webpackChunkName: "about" */ '../views/About.vue')
    }
  },
  {
    path: '/doc',
    name: 'Doc',
    component: Doc,
  },
  {
    path: '/info',
    name: 'Info',
    component: Info,
  },
  {
    path: '*',
    redirect:  { name: 'Info' }
  },
]

const router = new VueRouter({
  routes
})

export default router
