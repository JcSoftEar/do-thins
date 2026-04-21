// pages/detail/detail.js
Page({
  data: {
    habit: null,
    checkinHistory: [],
    statistics: {
      totalDays: 0,
      completionRate: 0,
      longestStreak: 0
    }
  },

  onLoad(options) {
    if (options.id) {
      this.loadHabitDetail(options.id);
    }
  },

  loadHabitDetail(id) {
    // TODO: 调用后端API获取习惯详情
    const habits = wx.getStorageSync('habits') || [];
    const habit = habits.find(h => h.id === id);
    
    if (habit) {
      // 生成模拟打卡历史
      const history = this.generateMockHistory(habit);
      
      this.setData({
        habit: habit,
        checkinHistory: history,
        statistics: {
          totalDays: habit.completedDays,
          completionRate: Math.round((habit.completedDays / habit.targetDays) * 100),
          longestStreak: habit.currentStreak
        }
      });
    }
  },

  generateMockHistory(habit) {
    // 生成最近30天的模拟打卡记录
    const history = [];
    const today = new Date();
    
    for (let i = 29; i >= 0; i--) {
      const date = new Date(today);
      date.setDate(date.getDate() - i);
      
      // 模拟部分完成
      const isCompleted = Math.random() > 0.3;
      
      history.push({
        date: date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' }),
        isCompleted: isCompleted,
        weekDay: ['日', '一', '二', '三', '四', '五', '六'][date.getDay()]
      });
    }
    
    return history;
  },

  goToCheckin() {
    const { habit } = this.data;
    if (habit) {
      wx.switchTab({ url: '/pages/checkin/checkin' });
    }
  },

  editHabit() {
    const { habit } = this.data;
    if (habit) {
      wx.navigateTo({
        url: `/pages/generate/generate?id=${habit.id}`
      });
    }
  },

  shareToFriend() {
    const { habit } = this.data;
    wx.showShareMenu({
      withShareTicket: true,
      menus: ['shareAppMessage', 'shareTimeline']
    });
  },

  onShareAppMessage() {
    const { habit } = this.data;
    return {
      title: habit ? `我正在坚持「${habit.name}」，快来监督我！` : '和我一起养成好习惯',
      path: `/pages/detail/detail?id=${habit.id}`,
      imageUrl: '/images/share.png'
    };
  }
});
