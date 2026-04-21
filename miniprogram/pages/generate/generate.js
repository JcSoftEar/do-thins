// pages/generate/generate.js
Page({
  data: {
    name: '',
    description: '',
    targetDays: 30,
    selectedIcon: '📚',
    selectedColor: '#4A90E2',
    icons: ['📚', '🏃', '💪', '🌅', '💧', '🍎', '✍️', '🧘', '💤', '🎯'],
    colors: ['#4A90E2', '#FF9500', '#34C759', '#FF3B30', '#5856D6', '#FF2D55', '#00C7BE', '#AC8E68'],
    days: [7, 14, 21, 30, 60, 90, 100]
  },

  onLoad(options) {
    // 如果有id参数，说明是编辑模式
    if (options.id) {
      wx.setNavigationBarTitle({ title: '编辑习惯' });
      this.loadHabitDetail(options.id);
    }
  },

  loadHabitDetail(id) {
    // TODO: 调用后端API获取习惯详情
    // 暂时使用模拟数据
    const mockHabit = {
      id: id,
      name: '每日阅读',
      description: '每天阅读30分钟',
      targetDays: 30,
      icon: '📚',
      color: '#4A90E2'
    };
    this.setData({
      name: mockHabit.name,
      description: mockHabit.description,
      targetDays: mockHabit.targetDays,
      selectedIcon: mockHabit.icon,
      selectedColor: mockHabit.color
    });
  },

  onNameInput(e) {
    this.setData({ name: e.detail.value });
  },

  onDescriptionInput(e) {
    this.setData({ description: e.detail.value });
  },

  selectIcon(e) {
    this.setData({ selectedIcon: e.currentTarget.dataset.icon });
  },

  selectColor(e) {
    this.setData({ selectedColor: e.currentTarget.dataset.color });
  },

  selectDays(e) {
    this.setData({ targetDays: e.currentTarget.dataset.days });
  },

  saveHabit() {
    const { name, description, targetDays, selectedIcon, selectedColor } = this.data;

    if (!name.trim()) {
      wx.showToast({ title: '请输入习惯名称', icon: 'none' });
      return;
    }

    // TODO: 调用后端API保存习惯
    const habit = {
      id: Date.now().toString(),
      name,
      description,
      targetDays,
      icon: selectedIcon,
      color: selectedColor,
      completedDays: 0,
      currentStreak: 0,
      isCheckedIn: false,
      createdAt: new Date().toISOString()
    };

    // 保存到本地存储
    const habits = wx.getStorageSync('habits') || [];
    habits.push(habit);
    wx.setStorageSync('habits', habits);

    wx.showToast({ title: '创建成功', icon: 'success' });
    setTimeout(() => {
      wx.navigateBack();
    }, 1500);
  },

  onShareAppMessage() {
    return {
      title: '创建新习惯',
      path: '/pages/generate/generate'
    };
  }
});
