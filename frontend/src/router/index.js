import { createRouter, createWebHistory } from 'vue-router'
import api from '@/utils/axiosConfig';
import Home from '@/views/Home.vue'
import Dashboard from '@/views/Dashboard.vue'
import GitHubCallback from '@/views/GitHubCallback.vue'
import GithubLogin from '@/views/GitHubLogin.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },

  {
    path: '/login',
    name: 'login',
    component: GithubLogin,
    meta: { requiresAuth: false }
  },

  {
    path: '/doGithub',
    name: 'GitHubCallback',
    component: GitHubCallback
  },


]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router;
