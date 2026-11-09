// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title MockUSDT
 * @dev Testnet Tether USD (USDT) token for AssetBridge Stablecoin Payments & P2P Settlement.
 * Decimals: 6 (standard USDT). Includes a public faucet for test demo payments.
 */
contract MockUSDT is ERC20, Ownable {
    constructor() ERC20("Tether USD (AssetBridge Testnet)", "USDT") Ownable(msg.sender) {
        // Mint initial supply of 1,000,000 USDT to deployer
        _mint(msg.sender, 1_000_000 * 10**6);
    }

    function decimals() public pure override returns (uint8) {
        return 6;
    }

    /**
     * @notice Demo faucet: request test USDT for testing payments and escrow.
     * @param to Recipient address
     * @param amount Amount in standard USDT units (e.g. 1000 = 1,000 USDT)
     */
    function faucet(address to, uint256 amount) external {
        require(amount <= 10_000, "Faucet limit exceeded: max 10,000 USDT per request");
        _mint(to, amount * 10**6);
    }
}

