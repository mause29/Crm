// backend/models/User.js
const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
    name: String,
    email: String,
    points: { type: Number, default: 0 },
    level: { type: Number, default: 1 },
    achievements: [String]
});

userSchema.methods.addPoints = function(points) {
    this.points += points;
    // Ejemplo: subir de nivel cada 1000 puntos
    const newLevel = Math.floor(this.points / 1000) + 1;
    if(newLevel > this.level) this.level = newLevel;
    return this.save();
}

module.exports = mongoose.model('User', userSchema);
