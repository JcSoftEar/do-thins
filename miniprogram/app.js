App({
  onLaunch() {
    // 检查登录状态
    const token = wx.getStorageSync('token');
    if (!token) {
      // 模拟登录
      this.login();
    }
  },

  login() {
    // 模拟登录
    wx.login({
      success: (res) => {
        if (res.code) {
          // TODO: 调用后端API获取token
          // 暂时使用模拟token
          wx.setStorageSync('token', 'mock_token_' + res.code);
          wx.setStorageSync('userInfo', {
            id: 'user_001',
            nickname: '习惯达人',
            avatar: '/images/default-avatar.png'
          });
        }
      }
    });
  },

  globalData: {
    userInfo: null,
    token: '',
    apiBaseUrl: 'https://api.example.com'  // 后端API占位符
  }
})
