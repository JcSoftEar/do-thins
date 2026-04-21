// utils/util.js

/**
 * 格式化日期
 * @param {Date|number} date 日期
 * @param {string} format 格式
 */
function formatDate(date, format = 'YYYY-MM-DD') {
  const d = new Date(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  const hours = String(d.getHours()).padStart(2, '0');
  const minutes = String(d.getMinutes()).padStart(2, '0');
  const seconds = String(d.getSeconds()).padStart(2, '0');

  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hours)
    .replace('mm', minutes)
    .replace('ss', seconds);
}

/**
 * 获取本周开始和结束日期
 */
function getWeekRange() {
  const now = new Date();
  const dayOfWeek = now.getDay() || 7;
  const start = new Date(now);
  start.setDate(now.getDate() - dayOfWeek + 1);
  const end = new Date(start);
  end.setDate(start.getDate() + 6);
  return {
    start: formatDate(start),
    end: formatDate(end)
  };
}

/**
 * 获取本月开始和结束日期
 */
function getMonthRange() {
  const now = new Date();
  const start = new Date(now.getFullYear(), now.getMonth(), 1);
  const end = new Date(now.getFullYear(), now.getMonth() + 1, 0);
  return {
    start: formatDate(start),
    end: formatDate(end)
  };
}

/**
 * 计算连续天数
 */
function calculateStreak(checkinHistory) {
  if (!checkinHistory || checkinHistory.length === 0) return 0;
  
  let streak = 0;
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  // 从今天开始往前计算
  for (let i = checkinHistory.length - 1; i >= 0; i--) {
    const checkDate = new Date(checkinHistory[i].date);
    checkDate.setHours(0, 0, 0, 0);
    
    const diffDays = Math.floor((today - checkDate) / (1000 * 60 * 60 * 24));
    
    if (diffDays === streak) {
      if (checkinHistory[i].isCompleted) {
        streak++;
      } else {
        break;
      }
    } else if (diffDays > streak) {
      break;
    }
  }

  return streak;
}

/**
 * 节流函数
 */
function throttle(fn, delay = 300) {
  let timer = null;
  return function(...args) {
    if (timer) return;
    timer = setTimeout(() => {
      fn.apply(this, args);
      timer = null;
    }, delay);
  };
}

/**
 * 防抖函数
 */
function debounce(fn, delay = 300) {
  let timer = null;
  return function(...args) {
    if (timer) clearTimeout(timer);
    timer = setTimeout(() => {
      fn.apply(this, args);
    }, delay);
  };
}

module.exports = {
  formatDate,
  getWeekRange,
  getMonthRange,
  calculateStreak,
  throttle,
  debounce
};
