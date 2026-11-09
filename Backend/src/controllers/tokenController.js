// ─── AssetBridge Tokenisation & P2P Controller ────────────────────────────────
// Implements Module 5 (Tokenisation) & Module 7 (Peer-to-Peer Transfers) from
// the AssetBridge Specification.
// Provides token offering issuance, token purchase via USDT, and P2P transfers.

const crypto = require('crypto');
const supabase = require('../connection/supabaseClient');
const { sendError } = require('../utils/errorHandler');

// In-memory fallback ledger for token offerings and P2P balances
// ensuring instant hackathon functionality even before DB table creation
const inMemoryTokenOfferings = new Map();
const inMemoryHoldings = new Map(); // key: `${userId}_${assetId}`
const inMemoryP2PTransactions = [];

// Seed default demonstrative token offering matching PDF Example:
// "$20,000 reference value, 2,000 units, each associated with a defined $10 economic interest"
const SEED_OFFERING = {
  assetId: 'demo-rolex-submariner',
  tokenName: 'AssetBridge Rolex Submariner Unit',
  tokenSymbol: 'AB-RLX',
  assetName: 'Rolex Submariner 16610LV Kermit',
  category: 'Luxury Watch',
  totalUnits: 2000,
  availableUnits: 1000, // 4 participants hold 500, 300, 200, 1000 in example
  pricePerUnitUsdt: 10,
  referenceValuationUsdt: 20000,
  rightsDefinition: 'Represents 1/2000th undivided economic interest and contractual right in physical custodial asset held at Geneva Freeport Vault.',
  custodyArrangement: 'Vaulted & insured under custody policy AB-INS-2026-99',
  issuerAddress: '0x1A2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b',
  contractAddress: '0x742d35Cc6634C0532925a3b844Bc454e4438f44e',
  status: 'active',
  createdAt: new Date().toISOString(),
};
inMemoryTokenOfferings.set(SEED_OFFERING.assetId, SEED_OFFERING);

/**
 * POST /api/tokens/issue
 * Issue a new token offering for an eligible verified asset.
 */
async function issueTokenOffering(req, res) {
  try {
    const {
      assetId,
      tokenName,
      tokenSymbol,
      totalUnits,
      pricePerUnitUsdt,
      rightsDefinition,
      custodyArrangement,
      referenceValuationUsdt,
    } = req.body;

    if (!assetId || !tokenName || !totalUnits || !pricePerUnitUsdt) {
      return res.status(400).json({
        success: false,
        error: 'assetId, tokenName, totalUnits, and pricePerUnitUsdt are required.',
      });
    }

    const units = parseInt(totalUnits, 10);
    const price = parseFloat(pricePerUnitUsdt);

    const offering = {
      assetId,
      tokenName: tokenName.trim(),
      tokenSymbol: (tokenSymbol || 'AB-TKN').trim().toUpperCase(),
      totalUnits: units,
      availableUnits: units,
      pricePerUnitUsdt: price,
      referenceValuationUsdt: referenceValuationUsdt || units * price,
      rightsDefinition: rightsDefinition || 'Contractual fractional economic interest in verified asset.',
      custodyArrangement: custodyArrangement || 'Verified institutional custody.',
      issuerAddress: req.user?.wallet_address || req.user?.id || '0xIssuer',
      contractAddress: `0x${crypto.randomBytes(20).toString('hex')}`,
      status: 'active',
      createdAt: new Date().toISOString(),
    };

    inMemoryTokenOfferings.set(assetId, offering);

    // Also persist to Supabase if table exists
    try {
      await supabase.from('token_offerings').upsert([offering]);
    } catch (_) {}

    return res.json({
      success: true,
      message: 'Token offering created successfully.',
      offering,
    });
  } catch (err) {
    return sendError(res, err, 'issueTokenOffering');
  }
}

/**
 * GET /api/tokens/offerings
 * List all active tokenised offerings.
 */
async function listTokenOfferings(req, res) {
  try {
    let offerings = Array.from(inMemoryTokenOfferings.values());

    try {
      const { data, error } = await supabase.from('token_offerings').select('*');
      if (!error && data && data.length > 0) {
        // Merge Supabase offerings with seed
        const merged = new Map(inMemoryTokenOfferings);
        data.forEach((item) => merged.set(item.assetId || item.asset_id, item));
        offerings = Array.from(merged.values());
      }
    } catch (_) {}

    return res.json({
      success: true,
      offerings,
    });
  } catch (err) {
    return sendError(res, err, 'listTokenOfferings');
  }
}

/**
 * GET /api/tokens/:assetId
 * Get specific token offering details.
 */
async function getTokenOffering(req, res) {
  try {
    const { assetId } = req.params;
    let offering = inMemoryTokenOfferings.get(assetId);

    if (!offering) {
      try {
        const { data, error } = await supabase
          .from('token_offerings')
          .select('*')
          .eq('assetId', assetId)
          .single();
        if (!error && data) offering = data;
      } catch (_) {}
    }

    if (!offering) {
      // Return default offering structure if querying generic asset
      offering = {
        ...SEED_OFFERING,
        assetId,
        tokenName: `AssetBridge Unit (${assetId})`,
      };
    }

    return res.json({
      success: true,
      offering,
    });
  } catch (err) {
    return sendError(res, err, 'getTokenOffering');
  }
}

/**
 * POST /api/tokens/buy
 * Buy fractional tokens with USDT.
 */
async function buyTokens(req, res) {
  try {
    const { assetId, units, txHash } = req.body;
    const userId = req.user?.id || req.body.userId || 'guest_user';
    const userWallet = req.user?.wallet_address || req.body.walletAddress || '0xUserWallet';

    const numUnits = parseInt(units, 10);
    if (!numUnits || numUnits <= 0) {
      return res.status(400).json({ success: false, error: 'Valid units count is required.' });
    }

    const offering = inMemoryTokenOfferings.get(assetId) || SEED_OFFERING;
    const totalCostUsdt = numUnits * offering.pricePerUnitUsdt;

    // Deduct available units
    offering.availableUnits = Math.max(0, (offering.availableUnits || offering.totalUnits) - numUnits);
    inMemoryTokenOfferings.set(assetId, offering);

    // Credit user holding
    const holdingKey = `${userId}_${assetId}`;
    const existing = inMemoryHoldings.get(holdingKey) || {
      userId,
      assetId,
      tokenName: offering.tokenName,
      tokenSymbol: offering.tokenSymbol,
      units: 0,
      totalInvestedUsdt: 0,
      walletAddress: userWallet,
    };

    existing.units += numUnits;
    existing.totalInvestedUsdt += totalCostUsdt;
    existing.updatedAt = new Date().toISOString();
    inMemoryHoldings.set(holdingKey, existing);

    const transaction = {
      id: `TX-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
      type: 'TOKEN_PURCHASE',
      assetId,
      units: numUnits,
      amountUsdt: totalCostUsdt,
      buyer: userId,
      buyerWallet: userWallet,
      txHash: txHash || `0x${crypto.randomBytes(32).toString('hex')}`,
      timestamp: new Date().toISOString(),
      status: 'confirmed',
    };
    inMemoryP2PTransactions.push(transaction);

    return res.json({
      success: true,
      message: `Successfully purchased ${numUnits} units for ${totalCostUsdt} USDT.`,
      holding: existing,
      transaction,
    });
  } catch (err) {
    return sendError(res, err, 'buyTokens');
  }
}

/**
 * POST /api/tokens/p2p-transfer
 * Transfer eligible tokens directly to another wallet address (Peer-to-Peer Transfer).
 */
async function p2pTransfer(req, res) {
  try {
    const { assetId, recipientWallet, units } = req.body;
    const senderId = req.user?.id || req.body.senderId || 'guest_user';
    const senderWallet = req.user?.wallet_address || req.body.senderWallet || '0xSenderWallet';

    const numUnits = parseInt(units, 10);
    if (!recipientWallet || !recipientWallet.trim()) {
      return res.status(400).json({ success: false, error: 'Recipient wallet address is required.' });
    }
    if (!numUnits || numUnits <= 0) {
      return res.status(400).json({ success: false, error: 'Valid units count is required.' });
    }

    const senderKey = `${senderId}_${assetId || 'demo-rolex-submariner'}`;
    const senderHolding = inMemoryHoldings.get(senderKey) || {
      userId: senderId,
      assetId: assetId || 'demo-rolex-submariner',
      units: 500, // Seed demo units if none
      tokenName: 'AssetBridge Rolex Submariner Unit',
      tokenSymbol: 'AB-RLX',
    };

    if (senderHolding.units < numUnits) {
      return res.status(400).json({
        success: false,
        error: `Insufficient token units. You hold ${senderHolding.units} units, but attempted to transfer ${numUnits}.`,
      });
    }

    // Deduct from sender
    senderHolding.units -= numUnits;
    inMemoryHoldings.set(senderKey, senderHolding);

    // Credit recipient
    const recipientKey = `${recipientWallet.trim()}_${assetId || 'demo-rolex-submariner'}`;
    const recipientHolding = inMemoryHoldings.get(recipientKey) || {
      userId: recipientWallet.trim(),
      walletAddress: recipientWallet.trim(),
      assetId: assetId || 'demo-rolex-submariner',
      units: 0,
      tokenName: senderHolding.tokenName,
      tokenSymbol: senderHolding.tokenSymbol,
    };
    recipientHolding.units += numUnits;
    inMemoryHoldings.set(recipientKey, recipientHolding);

    const txHash = `0x${crypto.randomBytes(32).toString('hex')}`;
    const transferRecord = {
      id: `P2P-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
      type: 'P2P_TOKEN_TRANSFER',
      assetId: assetId || 'demo-rolex-submariner',
      tokenSymbol: senderHolding.tokenSymbol,
      units: numUnits,
      sender: senderId,
      senderWallet,
      recipientWallet: recipientWallet.trim(),
      txHash,
      timestamp: new Date().toISOString(),
      status: 'confirmed',
    };
    inMemoryP2PTransactions.push(transferRecord);

    return res.json({
      success: true,
      message: `P2P Transfer of ${numUnits} ${senderHolding.tokenSymbol} units to ${recipientWallet} completed successfully!`,
      transfer: transferRecord,
      updatedSenderBalance: senderHolding.units,
    });
  } catch (err) {
    return sendError(res, err, 'p2pTransfer');
  }
}

/**
 * GET /api/tokens/portfolio/:userId
 * Get user's personal token holdings and P2P activity.
 */
async function getUserTokenHoldings(req, res) {
  try {
    const userId = req.params.userId || req.user?.id || 'guest_user';
    const userWallet = req.user?.wallet_address;

    const holdings = [];
    for (const [key, holding] of inMemoryHoldings.entries()) {
      if (holding.userId === userId || (userWallet && holding.walletAddress === userWallet)) {
        holdings.push(holding);
      }
    }

    // If empty, provide the demo 500 units from the Hackathon Concept page 4:
    // "Four participants hold 500, 300, 200 and 1,000 units respectively."
    if (holdings.length === 0) {
      holdings.push({
        userId,
        assetId: 'demo-rolex-submariner',
        tokenName: 'AssetBridge Rolex Submariner Unit',
        tokenSymbol: 'AB-RLX',
        units: 500,
        totalInvestedUsdt: 5000,
        currentValueUsdt: 5000,
        rightsDefinition: 'Represents 1/2000th undivided economic interest in Rolex Submariner 16610LV',
        walletAddress: userWallet || '0xDemoWalletA',
      });
    }

    const userP2P = inMemoryP2PTransactions.filter(
      (tx) => tx.sender === userId || tx.recipientWallet === userWallet || tx.buyer === userId
    );

    return res.json({
      success: true,
      holdings,
      recentTransfers: userP2P,
    });
  } catch (err) {
    return sendError(res, err, 'getUserTokenHoldings');
  }
}

module.exports = {
  issueTokenOffering,
  listTokenOfferings,
  getTokenOffering,
  buyTokens,
  p2pTransfer,
  getUserTokenHoldings,
};

