import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

export default function ({ store } ) {
  const routes = [
    {
      path: '/',
      name: 'home',
      redirect:  '/dashboard',
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('layouts/MainLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        { path: '',name: 'Servidores',icon: 'las la-database', component: () => import('pages/Datasets.vue') },
        { path: 'charts',name: 'Relatórios',icon: 'las la-chart-bar', component: () => import('pages/Charts.vue') },      
        {
          path: 'logout',
          name: 'Sair',
          icon: 'las la-sign-out-alt',
          beforeEnter: (to, from, next)=>{
            store.dispatch('AuthLogout');
            next('/login');
          }
        }
      ]
    },
    {
      path: '/login',
      component: () => import('layouts/SingleLayout.vue'),
      children: [
        { path: '',name: 'Login', component: () => import('pages/Login.vue') },
      ]
    },  // Always leave this as last one
    {
      path: '/queries/:server',
      name: 'Consultas',
      icon: 'las la-terminal',
      component: () => import('pages/Queries.vue')
    },
  ]
  
  if (process.env.MODE !== 'ssr') {
    routes.push({
      path: '*',
      component: () => import('pages/Error404.vue')
    })
  }

  const Router = new VueRouter({
    scrollBehavior: () => ({ x: 0, y: 0 }),
    routes,
    mode: process.env.VUE_ROUTER_MODE,
    base: process.env.VUE_ROUTER_BASE
  })

  Router.beforeEach((to, from, next) => {
    if (to.matched.some(route => route.meta.requiresAuth)) {
      store.dispatch('AuthRequest');
      if (store.getters.isAuthenticated) {
        next();
      } else {
        next("/login");
      }
    } else {
      next();
    }
  });
  return Router
}
