/**
 
 * @description router全局配置，如有必要可分文件抽离，其中asyncRoutes只有在intelligence模式下才会用到，vip文档中已提供路由的基础图标与小清新图标的配置方案，请仔细阅读
 */

import Vue from 'vue'
import VueRouter from 'vue-router'
import Layout from '@/layouts'
import { publicPath, routerMode } from '@/config'

Vue.use(VueRouter)
export const constantRoutes = []

export const asyncRoutes = [
  {
    path: '/',
    component: Layout,
    redirect: '/index',
    children: [
      {
        path: 'index',
        name: 'Index',
        component: () => import('@/views/index/index'),
        meta: {
          title: '关键词检索',
          icon: 'home',
          affix: true,
        },
      },
    ],
  },
  {
    path: '/image',
    component: Layout,
    redirect: 'noRedirect',
    children: [
      {
        path: 'upload',
        name: 'Upload',
        component: () => import('@/views/upload/index'),
        meta: {
          title: '视频帧检索',
          icon: 'shopping-cart',
          permissions: ['admin'],
          badge: 'New',
          affix: true,
        },
      },
    ],
  },
  {
    path: '',
    component: Layout,
    redirect: 'noRedirect',
    children: [
      {
        path: 'https://github.com/Columbine21',
        name: 'ExternalLink',
        meta: {
          title: 'Github 仓库',
          icon: 'users-cog',
          target: '_blank',
          permissions: ['admin', 'editor'],
          affix: true,
        },
      },
    ],
  },
]

const router = new VueRouter({
  base: publicPath,
  mode: routerMode,
  scrollBehavior: () => ({
    y: 0,
  }),
  routes: constantRoutes,
})

export default router
