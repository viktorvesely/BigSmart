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
  },
  {
    path: "/texts",
    name: "User utterances",
    component: () => import('../views/Validate.vue')
  }
]

const router = new VueRouter({
  routes
})

export default router
