import request from '@/utils/request'

export function keywordSearch(data) {
  return request({
    url: '/keywordSearch',
    method: 'post',
    data,
  })
}
