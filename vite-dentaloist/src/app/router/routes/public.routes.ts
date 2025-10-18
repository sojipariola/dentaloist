// src/app/router/routes/public.routes.ts

import { lazy } from 'react'

export const publicRoutes = [

  {
    path: '/login',
    component: lazy(() => import('@/pages/auth/Login')),
  },
  {
    path: '/register',
    component: lazy(() => import('@/pages/auth/Register')),
  },
  {
    path: '/forgot-password',
    component: lazy(() => import('@/pages/auth/ForgotPassword')),
  },
  {
    path: '/reset-password/:token',
    component: lazy(() => import('@/pages/auth/ResetPassword')),
  },
  {
    path: '/health',
    component: lazy(() => import('@/pages/health/ApiStatus')),
  },

  // REMOVE the home route from here since it's defined separately in AppRouter
  // {
  //   path: '/',
  //   component: lazy(() => import('@/pages/landing/Home')),
  // },

  // Landing pages - also public
  {
    path: '/features',
    component: lazy(() => import('@/pages/landing/Features')),
  },
  {
    path: '/pricing',
    component: lazy(() => import('@/pages/landing/Pricing')),
  },
  {
    path: '/contact',
    component: lazy(() => import('@/pages/landing/Contact')),
  },
]