// pages/mine/mine.js
const app = getApp();

Page({
  data: {
    userInfo: null,
    statistics: {
      totalHabits: 0,
      totalCheckins: 0,
      currentStreak: 0,
      completedHabits: 0
    },
    menuItems: [
      { id: 1, icon: '📊', title: '数据统计', path: '/pages/statistics/statistics' },
      { id: 2, icon: '🏆', title: '成就中心', path: '/pages/achievement/achievement' },
      { id: 3, icon: '📝', title: '打卡记录', path: '/pages/records/records' },
      { id: 4, icon: '⚙️', title: '设置', path: '/pages/settings/settings' }
    ]
  },

  onLoad() {
    this.setData({
      userInfo: app.globalData.userInfo || wx.getStorageSync('userInfo')
    });
  },

  onShow() {
    this.loadStatistics();
  },

  loadStatistics() {
    const habits = wx.getStorageSync('habits') || [];
    
    let totalCheckins = 0;
    let completedHabits = 0;
    let maxStreak = 0;
    
    habits.forEach(h => {
      totalCheckins += h.completedDays || 0;
      maxStreak = Math.max(maxStreak, h.currentStreak || 0);
      if (h.completedDays >= h.targetDays) {
        completedHabits++;
      }
    });

    this.setData({
      statistics: {
        totalHabits: habits.length,
        totalCheckins: totalCheckins,
        currentStreak: maxStreak,
        completedHabits: completedHabits
      }
    });
  },

  goToMenuItem(e) {
    const { path } = e.currentTarget.dataset;
    wx.showToast({ title: '功能开发中', icon: 'none' });
  },

  onChooseAvatar() {
    wx.chooseMedia({
      count: 1,
      mediaType: ['image'],
      sourceType: ['album', 'camera'],
      success: (res) => {
        wx.showToast({ title: '头像更新成功', icon: 'success' });
      }
    });
  },

  logout() {
    wx.showModal({
      title: '提示',
      content: '确定要退出登录吗？',
      success: (res) => {
        if (res.confirm) {
          wx.clearStorageSync();
          wx.reLaunch({ url: '/pages/home/home' });
        }
      }
    });
  },

  onShareAppMessage() {
    return {
      title: '习惯打卡 - 和我一起养成好习惯',
      path: '/pages/home/home',
      imageUrl: '/images/share.png'
    };
  }
});
