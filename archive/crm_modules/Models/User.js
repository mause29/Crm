const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
    name: String,
    points: { type: Number, default: 0 },
    level: { type: Number, default: 1 },
    achievements: [String],
    badges: [String],
    weeklyChallenges: { completed: Number, total: Number },
    sales: { type: Number, default: 0 }
});

module.exports = mongoose.model('User', userSchema);
