const express = require('express');
const router = express.Router();
const User = require('../models/User');

const getIo = (req) => req.app.get('io');

router.get('/ranking', async (req, res) => {
    const users = await User.find().sort({ points: -1 }).limit(10);
    res.json(users);
});

router.post('/updatePoints', async (req, res) => {
    const { userId, points, sales } = req.body;
    const user = await User.findById(userId);
    if(!user) return res.status(404).json({ error: 'Usuario no encontrado' });

    user.points += points || 0;
    user.sales += sales || 0;
    if(user.points >= user.level * 500) user.level += 1;
    await user.save();

    const ranking = await User.find().sort({ points: -1 }).limit(10);
    getIo(req).emit('rankingUpdate', ranking);
    getIo(req).emit('userUpdate', user);

    res.json({ success: true, user, ranking });
});

module.exports = router;
