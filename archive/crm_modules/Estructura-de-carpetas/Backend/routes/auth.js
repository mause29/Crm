const express = require('express');
const router = express.Router();
const User = require('../models/User');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { body, validationResult } = require('express-validator');
const speakeasy = require('speakeasy');
const nodemailer = require('nodemailer');

// Registro
router.post('/register', body('email').isEmail(), async (req,res)=>{
    const errors = validationResult(req);
    if(!errors.isEmpty()) return res.status(400).json({errors: errors.array()});
    const { name, email, password } = req.body;
    let user = await User.findOne({ email });
    if(user) return res.status(400).json({ msg: 'Usuario ya existe' });
    user = new User({ name, email, password });
    await user.save();
    res.json({ msg: 'Usuario creado' });
});

// Login + 2FA
router.post('/login', async (req,res)=>{
    const { email, password, token2FA } = req.body;
    const user = await User.findOne({ email });
    if(!user) return res.status(400).json({ msg: 'Usuario no encontrado' });
    const isMatch = await bcrypt.compare(password, user.password);
    if(!isMatch) return res.status(400).json({ msg: 'Contraseña incorrecta' });
    if(user.twoFA.enabled){
        const verified = speakeasy.totp.verify({
            secret: user.twoFA.secret,
            encoding: 'base32',
            token: token2FA
        });
        if(!verified) return res.status(400).json({ msg: '2FA inválido' });
    }
    const payload = { id: user.id, role: user.role };
    const token = jwt.sign(payload, process.env.JWT_SECRET, { expiresIn: '1d' });
    res.json({ token });
});

module.exports = router;
