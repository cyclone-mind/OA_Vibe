import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/Login.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/',
    component: () => import('@/views/layout/MainLayout.vue'),
    redirect: '/dashboard',
    children: [
      {
        path: '/dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/Dashboard.vue'),
        meta: { requiresAuth: true, title: '首页' },
      },
      {
        path: '/leave',
        name: 'Leave',
        component: () => import('@/views/leave/Leave.vue'),
        meta: { requiresAuth: true, title: '请假管理' },
      },
      {
        path: '/approval',
        name: 'Approval',
        component: () => import('@/views/approval/Approval.vue'),
        meta: { requiresAuth: true, title: '审批中心' },
      },
      {
        path: '/profile',
        name: 'Profile',
        component: () => import('@/views/profile/Profile.vue'),
        meta: { requiresAuth: true, title: '个人中心' },
      },
      // 系统管理
      {
        path: '/system/users',
        name: 'SystemUsers',
        component: () => import('@/views/system/Users.vue'),
        meta: { requiresAuth: true, title: '用户管理', adminOnly: true },
      },
      {
        path: '/system/departments',
        name: 'SystemDepartments',
        component: () => import('@/views/system/Departments.vue'),
        meta: { requiresAuth: true, title: '部门管理', adminOnly: true },
      },
      {
        path: '/system/positions',
        name: 'SystemPositions',
        component: () => import('@/views/system/Positions.vue'),
        meta: { requiresAuth: true, title: '职位管理', adminOnly: true },
      },
      {
        path: '/system/roles',
        name: 'SystemRoles',
        component: () => import('@/views/system/Roles.vue'),
        meta: { requiresAuth: true, title: '角色管理', adminOnly: true },
      },
      {
        path: '/system/menus',
        name: 'SystemMenus',
        component: () => import('@/views/system/Menus.vue'),
        meta: { requiresAuth: true, title: '菜单管理', adminOnly: true },
      },
      {
        path: '/system/permissions',
        name: 'SystemPermissions',
        component: () => import('@/views/system/Permissions.vue'),
        meta: { requiresAuth: true, title: '权限管理', adminOnly: true },
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next('/login')
  } else if (to.path === '/login' && userStore.isLoggedIn) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
