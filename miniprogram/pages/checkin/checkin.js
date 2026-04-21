// pages/checkin/checkin.js
const app = getApp();

Page({
  data: {
    habits: [],
    todayHabits: [],
    checkedInIds: []
  },

  onLoad() {
    this.loadTodayHabits();
  },

  onShow() {
    this.loadCheckedInStatus();
  },

  loadTodayHabits() {
    // TODO: 调用后端API获取今日需要打卡的习惯
    const habits = wx.getStorageSync('habits') || [];
    
    // 筛选今日需要打卡的（有习惯且未打卡）
    const todayHabits = habits.filter(h => !h.isCheckedIn);
    
    this.setData({ 
      habits: habits,
      todayHabits: todayHabits
    });
  },

  loadCheckedInStatus() {
    // 获取今日已打卡ID列表
    const today = new Date().toDateString();
    const checkinRecord = wx.getStorageSync('checkinRecord') || {};
    const todayRecord = checkinRecord[today] || [];
    
    this.setData({ checkedInIds: todayRecord });
  },

  doCheckin(e) {
    const { id } = e.currentTarget.dataset;
    const { habits, checkedInIds } = this.data;
    
    if (checkedInIds.includes(id)) {
      wx.showToast({ title: '今日已打卡', icon: 'none' });
      return;
    }

    // 更新打卡记录
    const today = new Date().toDateString();
    const checkinRecord = wx.getStorageSync('checkinRecord') || {};
    checkinRecord[today] = [...checkedInIds, id];
    wx.setStorageSync('checkinRecord', checkinRecord);

    // 更新习惯数据
    const habitIndex = habits.findIndex(h => h.id === id);
    if (habitIndex > -1) {
      habits[habitIndex].completedDays += 1;
      habits[habitIndex].currentStreak += 1;
      habits[habitIndex].isCheckedIn = true;
      wx.setStorageSync('habits', habits);
    }

    this.setData({ 
      checkedInIds: [...checkedInIds, id],
      habits: habits,
      todayHabits: habits.filter(h => !this.data.checkedInIds.includes(h.id))
    });

    wx.showToast({ 
      title: '打卡成功！', 
      icon: 'success',
      duration: 1500
    });

    // 触发分享
    this.showShareModal(id);
  },

  showShareModal(habitId) {
    const habit = this.data.habits.find(h => h.id === habitId);
    if (!habit) return;

    wx.showModal({
      title: '打卡成功 🎉',
      content: `恭喜完成${habit.name}今日打卡！`,
      confirmText: '分享给好友',
      cancelText: '好的',
      success: (res) => {
        if (res.confirm) {
          this.shareToFriend(habit);
        }
      }
    });
  },

  shareToFriend(habit) {
    // 分享到群聊/好友
    wx.showShareMenu({
      withShareTicket: true,
      menus: ['shareAppMessage', 'shareTimeline']
    });
  },

  onShareAppMessage(res) {
    const habit = this.data.habits.find(h => h.id === res.target?.dataset?.id);
    return {
      title: habit ? `我完成了「${habit.name}」打卡，快来一起养成好习惯！` : '和我一起养成好习惯',
      path: '/pages/checkin/checkin',
      imageUrl: '/images/share.png'
    };
  }
});
