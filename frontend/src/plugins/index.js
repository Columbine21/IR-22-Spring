/* 公共引入,勿随意修改,修改时需经过确认 */
import Vue from 'vue'
import './element'
import '@/styles/vab.scss'
import '@/remixIcon'
import '@/config/permission'
import './vabIcon'
import VabPermissions from 'zx-layouts/Permissions'
import Vab from '@/utils/vab'
import VabCount from 'zx-count'

Vue.use(Vab)
Vue.use(VabPermissions)
Vue.use(VabCount)