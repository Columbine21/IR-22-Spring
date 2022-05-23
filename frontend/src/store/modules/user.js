/**
 
 * @description 登录、获取用户信息、退出登录、清除accessToken逻辑，不建议修改
 */

import Vue from 'vue'
import {
  getAccessToken,
  removeAccessToken,
  setAccessToken,
} from '@/utils/accessToken'

const state = () => ({
  accessToken: getAccessToken(),
  username: 'Team - III',
  avatar: 'https://i.gtimg.cn/club/item/face/img/2/15922_100.gif',
  permissions: [],
})
const getters = {
  accessToken: (state) => state.accessToken,
  username: (state) => state.username,
  avatar: (state) => state.avatar,
  permissions: (state) => state.permissions,
}
const mutations = {
  setAccessToken(state, accessToken) {
    state.accessToken = accessToken
    setAccessToken(accessToken)
  },
  setUsername(state, username) {
    state.username = username
  },
  setAvatar(state, avatar) {
    state.avatar = avatar
  },
  setPermissions(state, permissions) {
    state.permissions = permissions
  },
}
const actions = {
  setPermissions({ commit }, permissions) {
    commit('setPermissions', permissions)
  },
  async getUserInfo({ commit, state }) {
    const { data } = await getUserInfo(state.accessToken)
    if (!data) {
      Vue.prototype.$baseMessage('验证失败，请重新登录...', 'error')
      return false
    }
    let { permissions, username, avatar } = data
    if (permissions && username && Array.isArray(permissions)) {
      commit('setPermissions', permissions)
      commit('setUsername', username)
      commit('setAvatar', avatar)
      return permissions
    } else {
      Vue.prototype.$baseMessage('用户信息接口异常', 'error')
      return false
    }
  },
}
export default { state, getters, mutations, actions }
