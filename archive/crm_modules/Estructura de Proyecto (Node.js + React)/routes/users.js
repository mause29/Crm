const express = require('express');
const router = express.Router();
const { getUsers, createUser } = require('../controllers/users');
const { verifyToken, checkRole } = require('../utils/authMiddleware');

router.get('/', verifyToken, checkRole(['admin']), getUsers);
router.post('/', verifyToken, checkRole(['admin']), createUser);

module.exports = router;
