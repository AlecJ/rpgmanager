import axios from 'axios'

const apiUrl =
    process.env.ENV === 'production'
        ? process.env.REACT_APP_PROD_API_URL
        : process.env.REACT_APP_DEV_API_URL

const client = axios.create({
    baseURL: apiUrl,
    json: true,
})

export const get = (url, params = {}) => {
    let getConfig = {
        url,
        method: 'get',
        params,
    }
    console.log(apiUrl)
    return client.request(getConfig)
}

export const post = (url, data = {}) => {
    let postConfig = {
        url,
        method: 'post',
        data,
    }
    console.log(apiUrl)
    return client.request(postConfig)
}

export const postMultipart = (url, data = {}) => {
    let postConfig = {
        method: 'post',
        headers: { 'Content-Type': 'multipart/form-data' },
    }
    return client.post(url, data, postConfig)
}

export const put = (url, data = {}) => {
    let putConfig = {
        url,
        method: 'put',
        data,
    }
    return client.request(putConfig)
}

export const deleto = (url, data = {}) => {
    let deleteConfig = {
        url,
        method: 'delete',
        data,
    }
    return client.request(deleteConfig)
}
