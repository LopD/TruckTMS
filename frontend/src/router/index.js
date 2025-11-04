import { createRouter, createWebHistory, createWebHashHistory } from 'vue-router'
import HomeView from '../views/static/HomeView.vue'
import { decodeJWT, getUserGroupsFromToken, isTokenValid, getAccessToken } from '@/JWTutils'
import { toast } from 'bulma-toast'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  // {
  //   path: '/about',
  //   name: 'about',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  // },
  {
    path: '/privacy-policy',
    name: 'privacy-policy',
    component: () => import('../views/static/PrivacyPolicy.vue')
  },
  {
    path: '/about-us',
    name: 'about-us',
    component: () => import('../views/static/AboutUsView.vue')
  },
  {
    path: '/log-in',
    name: 'log-in',
    component: () => import('../views/LogInView.vue')
  },
  {
    path: '/sign-up',
    name: 'sign-up',
    component: () => import('../views/SignUpView.vue')
  },
  {
    path: '/email-verify',
    name: 'email-verify',
    component: () => import('../views/ConfirmEmailView.vue')
  },
  // {
  //   path: '/logged-in',
  //   name: 'logged-in',
  //   component: () => import('../views/LoggedInView.vue'),
  //   meta: { requiresAuth: true },  // ← protected route
  //   redirect: { name: 'logged-in-home' },    // default child
  //   children: [
  //     {
  //       path: 'logged-in-home',
  //       name: 'logged-in-home',
  //       component: () => import('@/components/LoggedInComponents/LoggedInHome.vue'),
  //     },
  //     {
  //       path: 'hall',
  //       name: 'hall',
  //       component: () => import('@/views/ModelViews/HallView.vue'),
  //       meta: {
  //         groups: ['Managers','Maintainers']
  //       },
  //     },
  //     {
  //       path: 'hall/new',
  //       name: 'hall-form-create',
  //       component: () => import('@/components/forms/ModelForms/HallForm.vue'),
  //       meta: {
  //         groups: ['Managers'],
  //         isInNavBar: false,
  //       },
  //     },
  //     {
  //       path: 'hall/:id/edit',
  //       name: 'hall-edit',
  //       component: () => import('@/components/forms/ModelForms/HallForm.vue'),
  //       meta: {
  //         groups: ['Managers'],
  //         isInNavBar: false,
  //       },
  //     },
  //     {
  //       path: 'training-equipment',
  //       name: 'training-equipment',
  //       component: () => import('@/views/ModelViews/TrainingEquipmentView.vue'),
  //       meta: {
  //         groups: ['Managers','Maintainers','Coaches','Members'],
  //       },
  //     },
  //     {
  //       path: 'training-equipment/new',
  //       name: 'training-equipment-create',
  //       component: () => import('@/components/forms/ModelForms/TrainingEquipmentForm.vue'),
  //       meta: {
  //         groups: ['Managers'],
  //         isInNavBar: false,
  //       },
  //     },
  //     {
  //       path: 'training-equipment/:id/edit',
  //       name: 'training-equipment-edit',
  //       component: () => import('@/components/forms/ModelForms/TrainingEquipmentForm.vue'),
  //       meta: {
  //         groups: ['Managers','Maintainers'],
  //         isInNavBar: false,
  //       },
  //     },
  //     {
  //       path: 'tender',
  //       name: 'tender',
  //       component: () => import('@/views/ModelViews/TenderView.vue'),
  //       meta: {
  //         groups: ['Managers']
  //       },
  //     },
  //     {
  //       path: 'tender/new',
  //       name: 'tender-create',
  //       component: () => import('@/components/forms/ModelForms/TenderForm.vue'),
  //       meta: {
  //         groups: ['Managers'],
  //         isInNavBar: false,
  //       },
  //     },
  //     {
  //       path: 'tender/:id/edit',
  //       name: 'tender-edit',
  //       component: () => import('@/components/forms/ModelForms/TenderForm.vue'),
  //       meta: {
  //         groups: ['Managers'],
  //         isInNavBar: false,
  //       },
  //     },
  //     {
  //       path: 'supplier',
  //       name: 'supplier',
  //       component: () => import('@/views/ModelViews/SupplierView.vue'),
  //       meta: {
  //         groups: ['Managers']
  //       },
  //     },
  //     {
  //       path: 'supplier/new',
  //       name: 'supplier-create',
  //       component: () => import('@/components/forms/ModelForms/SupplierForm.vue'),
  //       meta: {
  //         groups: ['Managers'],
  //         isInNavBar: false,
  //       },
  //     },
  //     {
  //       path: 'supplier/:id/edit',
  //       name: 'supplier-edit',
  //       component: () => import('@/components/forms/ModelForms/SupplierForm.vue'),
  //       meta: {
  //         groups: ['Managers'],
  //         isInNavBar: false,
  //       },
  //     },
  //     {
  //       path: 'maintainer',
  //       name: 'maintainer',
  //       component: () => import('@/views/ModelViews/MaintainerView.vue'),
  //       meta: {
  //         groups: ['Managers','Maintainers'],
  //       },
  //     },
  //     {
  //       path: 'maintainer/new',
  //       name: 'maintainer-create',
  //       component: () => import('@/components/forms/ModelForms/MaintainerForm.vue'),
  //       meta: {
  //         groups: ['Managers'],
  //         isInNavBar: false,
  //       },
  //     },
  //     {
  //       path: 'maintainer/:id/edit',
  //       name: 'maintainer-edit',
  //       component: () => import('@/components/forms/ModelForms/MaintainerForm.vue'),
  //       meta: {
  //         groups: ['Managers','Maintainers'],
  //         isInNavBar: false,
  //       },
  //     },
  //     {
  //       path: 'maintenance-appointment',
  //       name: 'maintenance-appointment',
  //       component: () => import('@/views/ModelViews/MaintenanceAppointmentView.vue'),
  //       meta: {
  //         groups: ['Managers','Maintainers'],
  //       },
  //     },
  //     {
  //       path: 'maintenance-appointment/new',
  //       name: 'maintenance-appointment-create',
  //       component: () => import('@/components/forms/ModelForms/MaintenanceAppointmentForm.vue'),
  //       meta: {
  //         groups: ['Managers','Maintainers'],
  //         isInNavBar: false,
  //       },
  //     },
  //     {
  //       path: 'maintenance-appointment/:id/edit',
  //       name: 'maintenance-appointment-edit',
  //       component: () => import('@/components/forms/ModelForms/MaintenanceAppointmentForm.vue'),
  //       meta: {
  //         groups: ['Managers','Maintainers'],
  //         isInNavBar: false,
  //       },
  //     },
  //     {
  //       path: 'financial-record',
  //       name: 'financial-record',
  //       component: () => import('@/views/ModelViews/FinancialRecordView.vue'),
  //       meta: {
  //         groups: ['Managers']
  //       },
  //     },
  //     {
  //       path: 'financial-record/new/:type',
  //       name: 'financial-record-create',
  //       component: () => import('@/components/forms/ModelForms/FinancialRecordForm.vue'),
  //       meta: {
  //         groups: ['Managers'],
  //         isInNavBar: false,
  //       },
  //     },
  //     {
  //       path: 'financial-record/:type/:id/edit',
  //       name: 'financial-record-edit',
  //       component: () => import('@/components/forms/ModelForms/FinancialRecordForm.vue'),
  //       meta: {
  //         groups: ['Managers'],
  //         isInNavBar: false,
  //       },
  //     },
  //     {
  //       path: 'maintenance-request',
  //       name: 'maintenance-request',
  //       component: () => import('@/views/ModelViews/MaintenanceRequestView.vue'),
  //       meta: {
  //         groups: ['Managers','Maintainers','Coaches']
  //       },
  //     },
  //     {
  //       path: 'maintenance-request/new',
  //       name: 'maintenance-request-create',
  //       component: () => import('@/components/forms/ModelForms/MaintenanceRequestForm.vue'),
  //       meta: {
  //         groups: ['Managers','Maintainers','Coaches'],
  //         isInNavBar: false,
  //       },
  //     },
  //     {
  //       path: 'maintenance-request/:id/edit',
  //       name: 'maintenance-request-edit',
  //       component: () => import('@/components/forms/ModelForms/MaintenanceRequestForm.vue'),
  //       meta: {
  //         groups: ['Managers','Maintainers','Coaches'],
  //         isInNavBar: false,
  //       },
  //     },
  //     {
  //       path: 'membership-type',
  //       name: 'membership-type',
  //       component: () => import('@/views/ModelViews/MembershipTypeView.vue'),
  //       meta: {
  //         groups: ['Managers','Members','Coaches']
  //       },
  //     },
  //     {
  //       path: 'membership-type/new',
  //       name: 'membership-type-create',
  //       component: () => import('@/components/forms/ModelForms/MembershipTypeForm.vue'),
  //       meta: {
  //         groups: ['Managers'],
  //         isInNavBar: false,
  //       },
  //     },
  //     {
  //       path: 'membership-type/:id/edit',
  //       name: 'membership-type-edit',
  //       component: () => import('@/components/forms/ModelForms/MembershipTypeForm.vue'),
  //       meta: {
  //         groups: ['Managers'],
  //         isInNavBar: false,
  //       },
  //     },
  //     {
  //       path: 'membership',
  //       name: 'membership',
  //       component: () => import('@/views/ModelViews/MembershipView.vue'),
  //       meta: {
  //         groups: ['Managers','Members']
  //       },
  //     },
  //     {
  //       path: 'membership/new',
  //       name: 'membership-create',
  //       component: () => import('@/components/forms/ModelForms/MembershipForm.vue'),
  //       meta: {
  //         groups: ['Managers'],
  //         isInNavBar: false,
  //       },
  //     },
  //     {
  //       path: 'membership/:id/edit',
  //       name: 'membership-edit',
  //       component: () => import('@/components/forms/ModelForms/MembershipForm.vue'),
  //       meta: {
  //         groups: ['Managers'],
  //         isInNavBar: false,
  //       },
  //     },
  //     {
  //       path: 'financial-report',
  //       name: 'financial-report',
  //       component: () => import('@/views/ModelViews/FinancialReportView.vue'),
  //       meta: {
  //         groups: ['Managers'],
  //         isInNavBar: true,
  //       },
  //     },
  //     {
  //       path: 'membership-type-price-change-report',
  //       name: 'membership-type-price-change-report',
  //       component: () => import('@/views/ModelViews/MembershipTypePriceChangeReportView.vue'),
  //       meta: {
  //         groups: ['Managers'],
  //         isInNavBar: true,
  //       },
  //     },
  //     {
  //       path: 'user-notification',
  //       name: 'user-notification',
  //       component: () => import('@/views/ModelViews/UserNotificationView.vue'),
  //       // meta: {
  //       //   groups: ['Managers']
  //       // },
  //     },
  //     {
  //       path: 'test',
  //       name: 'test',
  //       component: () => import('@/views/ModelViews/test.vue'),
  //       // meta: {
  //       //   groups: ['Managers']
  //       // },
  //     }
  //     // {
  //     //   path: '/:catchAll(.*)',
  //     //   name: 'LoggedInViewNotFound',
  //     //   component: () => import('@/views/static/NotFoundView.vue')
  //     // }
      
  //   ]
  // },
  {
    path: '/:catchAll(.*)',
    name: 'NotFound',
    component: () => import('@/views/static/NotFoundView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes: routes
})

function showUnauthorizedNotification() {
  toast({
    message: 'Unauthorized',
    type: 'is-danger',
    dismissible: true,
    pauseOnHover: true,
    duration: 3000,
    position: 'bottom-right',
  })
}

router.beforeEach((to, from, next) => {
  const token = getAccessToken();

  if (to.meta.requiresAuth && (!token || !isTokenValid(token) ) ) {
    // Not logged in, redirect to login
    showUnauthorizedNotification()
    next({ name: 'log-in' })
  }
  
  if (to.meta.groups && to.meta.groups.length > 0 && token && isTokenValid(token) ) {
    const userGroups = getUserGroupsFromToken(token) 
    if (!userGroups.some(group => to.meta.groups.includes(group)) ) {
      showUnauthorizedNotification()
      next({ name: 'log-in' })
      return
    }
  } 

  next()
})

export default router
