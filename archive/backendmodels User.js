// backend/models/User.js
const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
    name: String,
    email: String,
    points: { type: Number, default: 0 },
    level: { type: Number, default: 1 },
    achievements: [String],    // Badges y logros
    weeklyChallenge: { 
        challenge: String,
        progress: Number,
        completed: { type: Boolean, default: false }
    }
});

userSchema.methods.addPoints = function(points) {
    this.points += points;
    const newLevel = Math.floor(this.points / 1000) + 1;
    if(newLevel > this.level) this.level = newLevel;
    return this.save();
};

userSchema.methods.completeChallenge = function() {
    if(!this.weeklyChallenge.completed){
        this.addPoints(100); // Recompensa interna
        this.weeklyChallenge.completed = true;
        this.achievements.push(`Challenge: ${this.weeklyChallenge.challenge}`);
    }
    return this.save();
};

module.exports = mongoose.model('User', userSchema);
