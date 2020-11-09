import * as restAPI from './base'

export const test_get = () => {
    return restAPI.get(`/test`)
}

export const test_post = () => {
    return restAPI.post(`/test`)
}

export const test_delete = () => {
    return restAPI.deleto(`/test`)
}