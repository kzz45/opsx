import request from '@/utils/request'

export function setCurrentApiPrefixFromLocalStorage(provider) {
  localStorage.setItem('current_api_prefix', provider)
  return provider
}

export function getCurrentApiPrefixFromLocalStorage() {
  return localStorage.getItem('current_api_prefix')
}

export function getTemplateList(prefix, resource_type, params, id = '') {
  if (id !== '') {
    return request({
      url: '/api/cloud_manage/' + prefix + '/' + resource_type + '_template/' + id + '/',
      method: 'get',
      params: params
    })
  } else {
    return request({
      url: '/api/cloud_manage/' + prefix + '/' + resource_type + '_template/',
      method: 'get',
      params: params
    })
  }
}

export function getCloudManageApiPrefix(factory_name) {
    switch (true) {
        case /ali|阿里云|alibaba/iug.test(factory_name): {
            console.log(factory_name)
          return 'ali'
        }
        case /aws|亚马逊/iug.test(factory_name): {
            console.log(factory_name)
          return 'aws'
        }
        case /gcp|谷歌云|google/iug.test(factory_name): {
            console.log(factory_name)
          return 'gcp'
        }
        default: {
          return ''
        }
      }
  }

export function labelInstance(prefix, data) {
  return request({
      url: '/api/cloud_manage/' + prefix + '/instance/label_instances/',
      method: 'post',
      data: data
  })
}

export function createInstance(prefix, data) {
  return request({
      url: '/api/cloud_manage/' + prefix + '/instance/run_instances/',
      method: 'post',
      data: data
  })
}

export function createInstanceTemplate(prefix, data) {
  return request({
      url: '/api/cloud_manage/' + prefix + '/instance_template/',
      method: 'post',
      data: data
  })
}

export function createLoadBalancerTemplate(prefix, data) {
  return request({
      url: '/api/cloud_manage/' + prefix + '/loadbalancer_template/',
      method: 'post',
      data: data
  })
}

export function createLoadBalancer(prefix, data) {
  return request({
      url: '/api/cloud_manage/' + prefix + '/loadbalancer/create_loadbalancer/',
      method: 'post',
      data: data
  })
}

export function updateInstanceTemplate(prefix, data, id) {
  return request({
      url: '/api/cloud_manage/' + prefix + '/instance_template/' + id + '/',
      method: 'put',
      data: data
  })
}

export function updateLoadBalancerTemplate(prefix, data, id) {
  return request({
      url: '/api/cloud_manage/' + prefix + '/loadbalancer_template/' + id + '/',
      method: 'put',
      data: data
  })
}

export function startInstance(prefix, data) {
  return request({
      url: '/api/cloud_manage/' + prefix + '/instance/start_instances/',
      method: 'post',
      data: data
  })
}

export function stopInstance(prefix, data) {
  return request({
      url: '/api/cloud_manage/' + prefix + '/instance/stop_instances/',
      method: 'post',
      data: data
  })
}

export function rebootInstance(prefix, data) {
  return request({
      url: '/api/cloud_manage/' + prefix + '/instance/reboot_instances/',
      method: 'post',
      data: data
  })
}

export function deleteInstance(prefix, data) {
  return request({
      url: '/api/cloud_manage/' + prefix + '/instance/delete_instances/',
      method: 'delete',
      data: data
  })
}

export function modifyInstance(prefix, data) {
  return request({
      url: '/api/cloud_manage/' + prefix + '/instance/modify_instances/',
      method: 'post',
      data: data
  })
}

export function getResource(prefix, resource_type, params) {
  return request({
      url: '/api/cloud_manage/' + prefix + '/' + resource_type + '/' + params['id'] + '/',
      method: 'get',
      params: params
  })
}

export function getRealInstance(prefix, params) {
  return request({
    url: '/api/cloud_manage/' + prefix + '/instance/get_real_instance/',
      method: 'get',
      params: params
  })
}

export function getTemplate(prefix, resource_type, id) {
  return request({
      url: '/api/cloud_manage/' + prefix + '/' + resource_type + '_template/' + id + '/',
      method: 'get'
  })
}

export function copyTemplate(prefix, resource_type, id) {
  return request({
    url: '/api/cloud_manage/' + prefix + '/' + resource_type + '_template/' + id + '/copy_template/',
      method: 'post'
  })
}

export function getResourceGroupList() {
  return request({
    url: '/api/cloud_manage/ali/instance_template/get_resource_group_list/',
    method: 'get'
  })
}

export function deleteTemplate(prefix, resource_type, id) {
  return request({
      url: '/api/cloud_manage/' + prefix + '/' + resource_type + '_template/' + id + '/',
      method: 'delete'
  })
}

export function getResourceList(prefix, resource_type, params) {
  return request({
      url: '/api/cloud_manage/' + prefix + '/' + resource_type + '/',
      method: 'get',
      params: params
  })
}

export function getInstanceLog(prefix, resource_type, id) {
  return request({
      url: '/api/cloud_manage/' + prefix + '/' + resource_type + '/' + id + '/get_instance_log/',
      method: 'get'
  })
}

export function getLoadBalancerLog(prefix, resource_type, id) {
  return request({
      url: '/api/cloud_manage/' + prefix + '/' + resource_type + '/' + id + '/get_loadbalancer_log/',
      method: 'get'
  })
}

export function getRecordList(params) {
  return request({
      url: '/api/cloud_manage/common/record/',
      method: 'get',
      params: params
  })
}

export function getRecordCeleryLog(params) {
  return request({
      url: '/api/cloud_manage/common/record/' + params['id'] + '/get_record_celery_log/',
      method: 'get',
      params: params
  })
}

export function startLoadBalancer(prefix, data) {
  return request({
      url: '/api/cloud_manage/' + prefix + '/loadbalancer/start_loadbalancers/',
      method: 'post',
      data: data
  })
}

export function stopLoadBalancer(prefix, data) {
  return request({
      url: '/api/cloud_manage/' + prefix + '/loadbalancer/stop_loadbalancers/',
      method: 'post',
      data: data
  })
}

export function lableLoadBalancer(prefix, data) {
  return request({
      url: '/api/cloud_manage/' + prefix + '/loadbalancer/label_loadbalancers/',
      method: 'post',
      data: data
  })
}
