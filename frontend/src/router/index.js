import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

export default function ({ store } ) {
  const routes = [
    {
      path: '/',
      name: 'Home',
      redirect:  '/dashboard',
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: () => import('layouts/MainLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        { path: '',name: 'Fontes de dados',icon: 'icon-server-outline', component: () => import('pages/Datasets.vue') },
        { path: 'charts',name: 'Relatórios',icon: 'icon-bar-chart-outline', component: () => import('pages/Charts.vue') },      
        {
          path: 'logout',
          name: 'Sair',
          icon: 'icon-log-out-outline',
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
      icon: 'ion-terminal',
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
