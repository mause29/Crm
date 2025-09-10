// backend/src/routes/auth.js
import express from 'express';
import { loginUser, registerUser, verify2FA } from '../controllers/authController.js';

const router = express.Router();
router.post('/register', registerUser);
router.post('/login', loginUser);
router.post('/verify-2fa', verify2FA);

export default router;
