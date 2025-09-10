// backend/src/services/gamification.js
import Achievement from '../models/Achievement.js';

export async function unlockAchievement(userId, title) {
  const achievement = await Achievement.findOne({ where: { userId, title } });
  if (!achievement) {
    await Achievement.create({ userId, title, unlocked: true, points: 10 });
  } else if (!achievement.unlocked) {
    achievement.unlocked = true;
    achievement.points += 10;
    await achievement.save();
  }
}
