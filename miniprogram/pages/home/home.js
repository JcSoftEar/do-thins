// pages/home/home.js
const app = getApp();

Page({
  data: {
    habits: [],
    userInfo: null,
    statistics: {
      totalDays: 0,
      currentStreak: 0,
      completedToday: 0
    }
  },

  onLoad() {
    this.setData({
      userInfo: app.globalData.userInfo || wx.getStorageSync('userInfo')
    });
  },

  onShow() {
    this.loadHabits();
    this.loadStatistics();
  },

  loadHabits() {
    // TODO: 调用后端API获取习惯列表
    // 暂时使用模拟数据
    const mockHabits = [
      {
        id: '1',
        name: '每日阅读',
        description: '每天阅读30分钟',
        icon: '📚',
        color: '#4A90E2',
        targetDays: 30,
        completedDays: 12,
        currentStreak: 5,
        isCheckedIn: false
      },
      {
        id: '2',
        name: '早起打卡',
        description: '每天7点前起床',
        icon: '🌅',
        color: '#FF9500',
        targetDays: 21,
        completedDays: 8,
        currentStreak: 3,
        isCheckedIn: false
      },
      {
        id: '3',
        name: '运动健身',
        description: '每天运动30分钟',
        icon: '💪',
        color: '#34C759',
        targetDays: 30,
        completedDays: 15,
        currentStreak: 7,
        isCheckedIn: false
      }
    ];
    this.setData({ habits: mockHabits });
  },

  loadStatistics() {
    // TODO: 调用后端API获取统计数据
    this.setData({
      statistics: {
        totalDays: 35,
        currentStreak: 7,
        completedToday: 2
      }
    });
  },

  goToGenerate() {
    wx.navigateTo({
      url: '/pages/generate/generate'
    });
  },

  goToDetail(e) {
    const { id } = e.currentTarget.dataset;
    wx.navigateTo({
      url: `/pages/detail/detail?id=${id}`
    });
  },

  onShareAppMessage() {
    return {
      title: '和我一起养成好习惯',
      path: '/pages/home/home',
      imageUrl: '/images/share.png'
    };
  }
});
