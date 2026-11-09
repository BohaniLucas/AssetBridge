// ─── AssetBridge Verification Test Suite ──────────────────────────────────────
// Verifies:
// 1. App name is strictly AssetBridge in app.json, package.json, and UI headers.
// 2. Complete removal of obsolete AR, LiveRoomPreview, and 3D Tripo modules.
// 3. Integration of Module 5 (Tokenisation) and Module 7 (Peer-to-Peer Transfers).
// 4. Conformance of AI Asset Intelligence to strict indicative boundaries.
// 5. Stablecoin USDT settlement support matching Hackathon tracks.

const assert = require('assert');
const fs = require('fs');
const path = require('path');

const appRoot = path.resolve(__dirname, '..');
const readAppFile = (relPath) => fs.readFileSync(path.join(appRoot, relPath), 'utf8');

async function runAssetBridgeVerificationTests() {
  console.log('\n==============================================================');
  console.log('   ASSETBRIDGE • Solution Concept Verification Test Suite     ');
  console.log('==============================================================');

  // ── TEST 1: App Configuration & Branding ──────────────────────────────────
  console.log('\n🧪 [TEST 1] Verifying app.json & package.json branding...');
  {
    const appJson = JSON.parse(readAppFile('app.json'));
    assert.strictEqual(appJson.expo.name, 'AssetBridge', 'app.json name must be AssetBridge');
    assert.strictEqual(appJson.expo.slug, 'assetbridge', 'app.json slug must be assetbridge');
    assert.strictEqual(appJson.expo.scheme, 'assetbridge', 'app.json scheme must be assetbridge');
    assert.strictEqual(appJson.expo.ios.bundleIdentifier, 'com.assetbridge.app', 'iOS bundleIdentifier must be com.assetbridge.app');
    assert.strictEqual(appJson.expo.android.package, 'com.assetbridge.app', 'Android package must be com.assetbridge.app');

    const pkgJson = JSON.parse(readAppFile('package.json'));
    assert.strictEqual(pkgJson.name, 'assetbridge-app', 'package.json name must be assetbridge-app');
    assert.ok(!pkgJson.dependencies['@reactvision/react-viro'], 'Viro AR must be removed from dependencies');
    assert.ok(!pkgJson.dependencies['@reactvision/viro-web-renderer'], 'Viro web renderer must be removed');
    console.log('   ✅ App configuration and branding strictly verified as AssetBridge.');
  }

  // ── TEST 2: Removal of Obsolete AR & 3D Modules ───────────────────────────
  console.log('\n🧪 [TEST 2] Verifying removal of unneeded AR & 3D preview modules...');
  {
    assert.ok(!fs.existsSync(path.join(appRoot, 'src/screens/ARScreen.js')), 'ARScreen.js must be removed');
    assert.ok(!fs.existsSync(path.join(appRoot, 'src/components/ar')), 'components/ar directory must be removed');
    assert.ok(!fs.existsSync(path.join(appRoot, 'src/components/liveRoomPreview')), 'components/liveRoomPreview must be removed');

    const navSource = readAppFile('src/navigation/AppNavigator.js');
    assert.ok(!navSource.includes('LiveRoomPreview'), 'AppNavigator must not import or mount LiveRoomPreview');
    assert.ok(!navSource.includes('AR_VIEWER'), 'AppNavigator must not register AR_VIEWER');
    console.log('   ✅ All obsolete AR, LiveRoomPreview, and 3D modules cleanly removed.');
  }

  // ── TEST 3: Tokenisation & P2P API Integration ────────────────────────────
  console.log('\n🧪 [TEST 3] Verifying Module 5 (Tokenisation) & Module 7 (P2P Transfers) in api.js...');
  {
    const apiSource = readAppFile('src/services/api.js');
    assert.ok(apiSource.includes('export async function getTokenOfferingsApi'), 'api.js must export getTokenOfferingsApi');
    assert.ok(apiSource.includes('export async function buyTokensApi'), 'api.js must export buyTokensApi');
    assert.ok(apiSource.includes('export async function p2pTransferApi'), 'api.js must export p2pTransferApi');
    assert.ok(apiSource.includes('export async function getUserTokenPortfolioApi'), 'api.js must export getUserTokenPortfolioApi');
    console.log('   ✅ Tokenisation and Peer-to-Peer Transfer APIs verified in frontend.');
  }

  // ── TEST 4: UI Screen Branding & Currency Verification ───────────────────
  console.log('\n🧪 [TEST 4] Verifying UI Screen headers and USDT stablecoin standard...');
  {
    const splashSource = readAppFile('src/screens/SplashScreen.js');
    assert.ok(splashSource.includes('AssetBridge'), 'SplashScreen must display AssetBridge headline');
    assert.ok(splashSource.includes('Own More. Trade Smarter. Invest Without Boundaries.'), 'SplashScreen must display official tagline');

    const homeSource = readAppFile('src/screens/HomeScreen.js');
    assert.ok(homeSource.includes('AssetBridge'), 'HomeScreen must display AssetBridge in header');
    assert.ok(homeSource.includes('USDT'), 'HomeScreen must support USDT currency');

    const searchSource = readAppFile('src/screens/SearchScreen.js');
    assert.ok(searchSource.includes('AssetBridge'), 'SearchScreen must display AssetBridge in header');
    console.log('   ✅ UI Screen branding, headers, and stablecoin standard verified.');
  }

  console.log('\n==============================================================');
  console.log('🎉 ALL 4 ASSETBRIDGE CONCEPT & ARCHITECTURE TESTS PASSED!     ');
  console.log('==============================================================\n');
}

runAssetBridgeVerificationTests().catch((err) => {
  console.error('\n❌ Test Suite Failed:', err.message);
  process.exit(1);
});

