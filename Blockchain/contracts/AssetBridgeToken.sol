// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title AssetBridgeToken
 * @dev ERC-20 Token representing defined economic or contractual interests in a verified real-world asset.
 * Aligns with AssetBridge Tokenisation & Peer-to-Peer Transfer modules.
 */
contract AssetBridgeToken is ERC20, Ownable {
    string public assetId;
    string public rightsDefinition;
    uint256 public initialValuationUsdt;
    uint256 public pricePerUnitUsdt;
    address public issuer;

    event TokensIssued(address indexed issuer, uint256 totalSupply, uint256 pricePerUnitUsdt);
    event P2PTransferCompleted(address indexed from, address indexed to, uint256 amount);

    /**
     * @param name Name of token, e.g. "AssetBridge Rolex Submariner Unit"
     * @param symbol Symbol of token, e.g. "AB-RLX"
     * @param _assetId ID of the underlying verified asset in Asset Registry
     * @param _rightsDefinition Clearly defined legal, contractual or economic rights
     * @param _initialValuationUsdt Total reference value of physical asset in USDT
     * @param _totalUnits Number of fractional units to create (e.g. 2,000 units)
     * @param _pricePerUnitUsdt Price in USDT per unit (e.g. 10 USDT)
     * @param _issuer Address of authorized issuer
     */
    constructor(
        string memory name,
        string memory symbol,
        string memory _assetId,
        string memory _rightsDefinition,
        uint256 _initialValuationUsdt,
        uint256 _totalUnits,
        uint256 _pricePerUnitUsdt,
        address _issuer
    ) ERC20(name, symbol) Ownable(_issuer) {
        assetId = _assetId;
        rightsDefinition = _rightsDefinition;
        initialValuationUsdt = _initialValuationUsdt;
        pricePerUnitUsdt = _pricePerUnitUsdt;
        issuer = _issuer;

        // Mint total units to issuer
        _mint(_issuer, _totalUnits * (10 ** decimals()));

        emit TokensIssued(_issuer, _totalUnits, _pricePerUnitUsdt);
    }

    /**
     * @notice Transfer tokens directly to another wallet (P2P Transfer).
     */
    function transfer(address to, uint256 amount) public override returns (bool) {
        bool success = super.transfer(to, amount);
        if (success) {
            emit P2PTransferCompleted(msg.sender, to, amount);
        }
        return success;
    }
}

