let BASE_URL = "";
if(process.env.NODE_ENV === "development"){
	BASE_URL = "http://127.0.0.1:8000";
}else{
	BASE_URL = "https://www.baidu.com";
}

const request = (url, options) => {
	const token = uni.getStorageSync("token");
	return new Promise((resolve, reject) => {
		uni.request({
			url: BASE_URL + url,
			header: {
				"content-type": "application/json",
				"authorization": "Bearer " + token
			},
			...options,
			success: (res) => {
				const {statusCode, data} = res;
				if(statusCode == 200){
					resolve(data);
				}else{
					let errorMsg = "请求失败";
					if (data && data.detail) {
						if (typeof data.detail === 'string') {
							errorMsg = data.detail;
						} else if (Array.isArray(data.detail) && data.detail.length > 0) {
							// 处理 FastAPI 验证错误数组
							errorMsg = data.detail[0].msg || JSON.stringify(data.detail);
						} else {
							errorMsg = JSON.stringify(data.detail);
						}
					}
					const error = new Error(errorMsg);
					error.statusCode = statusCode;
					error.data = data;
					reject(error);
				}
			},
			fail: (err) => {
				reject(new Error("服务器请求失败！"));
			}
		})
	})
}

const get = (url, data) => {
	let options = {data, method: 'GET'};
	return request(url, options);
}

const post = (url, data) => {
	let options = {data, method: "POST"};
	return request(url, options);
}

const generateName = (data) => {
	const url = "/name"
	return post(url, data);
}

const login = (email, password) => {
	let url = "/auth/login";
	return post(url, {email, password});
}

const register = (data) => {
	let url = "/auth/register";
	return post(url, data);
}

const getEmailCode = (email) => {
	let url = "/auth/code"
	return get(url, {email});
}

export default {
	request,
	get,
	post,
	login,
	register,
	getEmailCode,
	generateName
}