import { createRouter, createWebHistory } from 'vue-router'
import home from '../views/Home.vue'
import events from '../views/Events.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: home
  },
  {
    path: '/events',
    name: 'events',
    component: events
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
