import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

  const routes = [
  {
    path: '/',
    name: 'Učím sa',
    component: () => import('../views/Utterance.vue')
  },
  {
    path: "/intents",
    name: 'Intents',
    component: () => import('../views/Intents.vue')
  }
]

const router = new VueRouter({
  routes
})

export default router
