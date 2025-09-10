// server/security.js
const crypto = require('crypto');
const bcrypt = require('bcrypt');
const speakeasy = require('speakeasy');
const jwt = require('jsonwebtoken');

// --- Encriptación de datos sensibles ---
function encryptData(data) {
  const cipher = crypto.createCipheriv(
    'aes-256-cbc',
    Buffer.from(process.env.ENCRYPT_KEY, 'hex'),
    Buffer.from(process.env.ENCRYPT_IV, 'hex')
  );
  let encrypted = cipher.update(data, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  return encrypted;
}

function decryptData(encrypted) {
  const decipher = crypto.createDecipheriv(
    'aes-256-cbc',
    Buffer.from(process.env.ENCRYPT_KEY, 'hex'),
    Buffer.from(process.env.ENCRYPT_IV, 'hex')
  );
  let decrypted = decipher.update(encrypted, 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  return decrypted;
}

// --- 2FA (Google Authenticator) ---
function generate2FASecret() {
  return speakeasy.generateSecret({ length: 20 });
}

function verify2FAToken(secret, token) {
  return speakeasy.totp.verify({ secret, encoding: 'base32', token });
}

// --- Hash de contraseña ---
async function hashPassword(password) {
  return await bcrypt.hash(password, 12);
}

async function comparePassword(password, hash) {
  return await bcrypt.compare(password, hash);
}

// --- Middleware JWT ---
function authenticateJWT(req, res, next) {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.sendStatus(401);
  jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
    if (err) return res.sendStatus(403);
    req.user = user;
    next();
  });
}

module.exports = {
  encryptData,
  decryptData,
  generate2FASecret,
  verify2FAToken,
  hashPassword,
  comparePassword,
  authenticateJWT
};
