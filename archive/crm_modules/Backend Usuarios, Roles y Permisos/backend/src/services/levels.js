// backend/src/services/levels.js
import User from '../models/User.js';
import Achievement from '../models/Achievement.js';

export async function updateUserLevel(userId) {
  const achievements = await Achievement.findAll({ where: { userId, unlocked: true } });
  const points = achievements.reduce((sum, a) => sum + a.points, 0);
  const level = Math.floor(points / 50) + 1; // 50 puntos por nivel
  await User.update({ level }, { where: { id: userId } });
  return level;
}

export async function getLeaderboard() {
  return await User.findAll({
    order: [['level', 'DESC']],
    attributes: ['id', 'name', 'level'],
    limit: 10,
  });
}
