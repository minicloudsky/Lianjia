import axios from 'axios';

axios.defaults.timeout = 30000;
axios.interceptors.request.use(
    config => {
        config.data = JSON.stringify(config.data);
        return config;
    },
    error => {
        return Promise.reject(error);
    }
)

axios.interceptors.response.use(
    response => {
        return response.data;
    },
    error => {
        if (error.response) {
            switch (error.response.status) {
                case 401:
                    console.log("401")
                    break;
                default:
                    console.log('default');
            }
        }
        return Promise.reject(error);
    }
)

/**
 * 封装post请求
 * @param url
 * @param data
 * @param contentType
 * @returns {Promise}
 */
export function post(url, data = {}, contentType = "application/json") {
    return new Promise((resolve, reject) => {
        let config = {
            headers: {
                'Content-Type': contentType,
            },
            baseURL: 'http://127.0.0.1:8000',
        }
        axios.post(url, data, config).then(response => {
            resolve(response);
        }).catch(
            error => {
                return reject(error);
            }
        )
    })
}

export function get(url, params = {}, contentType = "application/json") {
    return new Promise((resolve, reject) => {
        let config = {
            headers: {
                'Content-Type': contentType,
            },
            baseURL: 'http://127.0.0.1:8000',
            params: params
        }
        axios.get(url, config).then(response => {
            resolve(response);
        }).catch(
            error => {
                return reject(error);
            }
        )
    })
}

export function put(url, data = {}, contentType = "application/json") {
    return new Promise((resolve, reject) => {
        let config = {
            headers: {
                'Content-Type': contentType,
            },
            baseURL: 'http://127.0.0.1:8000',
        }
        axios.put(url, data, config).then(response => {
            resolve(response);
        }).catch(
            error => {
                return reject(error);
            }
        )
    })
}
