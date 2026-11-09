const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("AssetBridge Smart Contracts Suite", function () {
  let owner, reviewer, buyer, seller, investorA, investorB;
  let certificateContract, tokenContract, usdtContract, escrowContract;

  beforeEach(async function () {
    [owner, reviewer, buyer, seller, investorA, investorB] = await ethers.getSigners();

    // 1. Deploy AssetBridgeCertificate
    const AssetBridgeCertificate = await ethers.getContractFactory("AssetBridgeCertificate");
    certificateContract = await AssetBridgeCertificate.deploy(owner.address);
    await certificateContract.waitForDeployment();

    // 2. Deploy MockUSDT
    const MockUSDT = await ethers.getContractFactory("MockUSDT");
    usdtContract = await MockUSDT.deploy();
    await usdtContract.waitForDeployment();

    // 3. Deploy AssetBridgeToken (e.g. 2,000 units for $20,000 asset @ 10 USDT)
    const AssetBridgeToken = await ethers.getContractFactory("AssetBridgeToken");
    tokenContract = await AssetBridgeToken.deploy(
      "AssetBridge Rolex Submariner Unit",
      "AB-RLX",
      "asset-uuid-12345",
      "Represents 1/2000th undivided economic interest in verified Rolex Submariner 16610LV",
      20000,
      2000,
      10,
      owner.address
    );
    await tokenContract.waitForDeployment();

    // 4. Deploy AssetBridgeEscrow with USDT
    const AssetBridgeEscrow = await ethers.getContractFactory("AssetBridgeEscrow");
    escrowContract = await AssetBridgeEscrow.deploy(await usdtContract.getAddress(), owner.address);
    await escrowContract.waitForDeployment();
  });

  describe("1. Verified Asset Registry & Certificate Minting", function () {
    it("mints an ERC-721 certificate with hash & valuation and records provenance", async function () {
      const tx = await certificateContract.mintCertificate(
        seller.address,
        "https://assetbridge.app/metadata/1",
        "AB-CERT-2026-001",
        "Luxury Watch",
        20000 * 10**6,
        "0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
        "EXP-REVIEWER-44"
      );
      await tx.wait();

      expect(await certificateContract.totalMinted()).to.equal(1);
      const cert = await certificateContract.getCertificate(1);
      expect(cert.certNumber).to.equal("AB-CERT-2026-001");
      expect(cert.assetCategory).to.equal("Luxury Watch");
      expect(cert.assetValueUsdt).to.equal(20000 * 10**6);

      // Record Provenance
      await certificateContract.recordProvenanceMilestone(
        1,
        "0x1111222233334444555566667777888899990000111122223333444455556666",
        "Verified by certified Horological Institute",
        "Horological Expert"
      );

      const milestones = await certificateContract.getMilestones(1);
      expect(milestones.length).to.equal(1);
      expect(milestones[0].description).to.equal("Verified by certified Horological Institute");
    });
  });

  describe("2. Tokenisation & Peer-to-Peer (P2P) Transfers", function () {
    it("distributes tokens and supports peer-to-peer transfers between wallets", async function () {
      const decimals = await tokenContract.decimals();
      const initialSupply = await tokenContract.totalSupply();
      expect(initialSupply).to.equal(ethers.parseUnits("2000", decimals));

      // Transfer 500 tokens to investorA
      await tokenContract.transfer(investorA.address, ethers.parseUnits("500", decimals));
      expect(await tokenContract.balanceOf(investorA.address)).to.equal(ethers.parseUnits("500", decimals));

      // Peer-to-Peer Transfer: investorA transfers 100 tokens to investorB
      await tokenContract.connect(investorA).transfer(investorB.address, ethers.parseUnits("100", decimals));
      expect(await tokenContract.balanceOf(investorA.address)).to.equal(ethers.parseUnits("400", decimals));
      expect(await tokenContract.balanceOf(investorB.address)).to.equal(ethers.parseUnits("100", decimals));
    });
  });

  describe("3. Stablecoin Payments & USDT Protected Escrow Demo", function () {
    it("locks USDT in escrow and releases to seller upon buyer confirmation", async function () {
      const amountUsdt = 5000 * 10**6; // 5,000 USDT

      // Fund buyer with test USDT from faucet
      await usdtContract.faucet(buyer.address, 5000);
      expect(await usdtContract.balanceOf(buyer.address)).to.equal(amountUsdt);

      // Buyer approves escrow contract
      const escrowAddress = await escrowContract.getAddress();
      await usdtContract.connect(buyer).approve(escrowAddress, amountUsdt);

      // Lock payment
      await escrowContract.connect(buyer).lockPayment(
        101,
        seller.address,
        amountUsdt,
        1
      );

      const order = await escrowContract.orders(101);
      expect(order.status).to.equal(1); // PaymentLocked
      expect(order.amountUsdt).to.equal(amountUsdt);

      // Seller dispatches item
      const tracking = ethers.encodeBytes32String("TRACK-SECURE-99");
      await escrowContract.connect(seller).dispatchAsset(101, tracking);

      // Confirm delivery
      await escrowContract.connect(buyer).confirmDelivery(101);

      // Accept and release USDT to seller
      await escrowContract.connect(buyer).acceptAndRelease(101);

      expect(await usdtContract.balanceOf(seller.address)).to.equal(amountUsdt);
    });
  });
});

