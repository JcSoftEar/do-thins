// utils/request.js
const app = getApp();

/**
 * 请求封装
 * @param {Object} options 请求配置
 */
function request(options) {
  const { url, data, method = 'GET', header = {} } = options;
  
  return new Promise((resolve, reject) => {
    // 显示加载中
    if (options.showLoading !== false) {
      wx.showLoading({ title: '加载中...', mask: true });
    }

    wx.request({
      url: app.globalData.apiBaseUrl + url,
      data: data,
      method: method,
      header: {
        'Content-Type': 'application/json',
        'Authorization': wx.getStorageSync('token') || '',
        ...header
      },
      success: (res) => {
        wx.hideLoading();
        if (res.statusCode === 200) {
          if (res.data.code === 0) {
            resolve(res.data.data);
          } else {
            wx.showToast({ title: res.data.message || '请求失败', icon: 'none' });
            reject(res.data);
          }
        } else if (res.statusCode === 401) {
          // token过期，重新登录
          app.login();
          reject({ message: '登录已过期' });
        } else {
          reject(res.data);
        }
      },
      fail: (err) => {
        wx.hideLoading();
        wx.showToast({ title: '网络请求失败', icon: 'none' });
        reject(err);
      }
    });
  });
}

/**
 * GET请求
 */
function get(url, data, options = {}) {
  return request({
    url,
    data,
    method: 'GET',
    ...options
  });
}

/**
 * POST请求
 */
function post(url, data, options = {}) {
  return request({
    url,
    data,
    method: 'POST',
    ...options
  });
}

module.exports = {
  request,
  get,
  post
};
