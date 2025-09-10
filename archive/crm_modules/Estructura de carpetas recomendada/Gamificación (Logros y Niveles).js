// backend/src/models/Achievement.js
import { DataTypes } from 'sequelize';
import db from '../config/db.js';

const Achievement = db.define('achievement', {
  userId: { type: DataTypes.INTEGER, allowNull: false },
  title: { type: DataTypes.STRING, allowNull: false },
  description: { type: DataTypes.STRING },
  points: { type: DataTypes.INTEGER, defaultValue: 0 },
  unlocked: { type: DataTypes.BOOLEAN, defaultValue: false },
});

export default Achievement;
