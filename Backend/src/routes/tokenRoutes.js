// ─── AssetBridge Token & P2P Routes ──────────────────────────────────────────
// Routes for Tokenisation & Peer-to-Peer Transfers

const express = require('express');
const router = express.Router();
const tokenController = require('../controllers/tokenController');
const { requireAuth } = require('../middlewares/authMiddleware');

// Public listing of token offerings
router.get('/offerings', tokenController.listTokenOfferings);
router.get('/offering/:assetId', tokenController.getTokenOffering);

// Token Purchase with USDT
router.post('/buy', tokenController.buyTokens);

// Peer-to-Peer (P2P) Token Transfer between wallets
router.post('/p2p-transfer', tokenController.p2pTransfer);

// Issue new token offering (admin or verified issuer)
router.post('/issue', tokenController.issueTokenOffering);

// Portfolio holdings for user
router.get('/portfolio/:userId', tokenController.getUserTokenHoldings);
router.get('/portfolio', tokenController.getUserTokenHoldings);

module.exports = router;

