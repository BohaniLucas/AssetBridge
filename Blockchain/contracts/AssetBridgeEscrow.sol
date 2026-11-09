// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

/**
 * @title AssetBridgeEscrow
 * @dev Protected Checkout / Escrow Demo for AssetBridge Real-World Assets & Collectibles.
 * Supports USDT stablecoin settlement with verified sequential lifecycle:
 * PaymentLocked -> InTransit -> Delivered -> Accepted -> ReleasedToSeller
 * With dispute resolution and refund support for authorized parties.
 */
contract AssetBridgeEscrow is Ownable, ReentrancyGuard {
    using SafeERC20 for IERC20;

    enum EscrowStatus {
        None,
        PaymentLocked,
        InTransit,
        Delivered,
        Accepted,
        Disputed,
        ReleasedToSeller,
        RefundedToBuyer
    }

    struct EscrowOrder {
        uint256 orderId;
        address buyer;
        address seller;
        uint256 amountUsdt;
        uint256 assetTokenId;
        EscrowStatus status;
        bytes32 trackingHash;
        bytes32 disputeEvidence;
        uint256 createdAt;
        uint256 shippedAt;
        uint256 deliveredAt;
        uint256 acceptedAt;
        uint256 disputedAt;
        uint256 resolvedAt;
    }

    IERC20 public immutable usdtToken;

    // Mapping from Order ID => Escrow Order
    mapping(uint256 => EscrowOrder) public orders;

    // Events
    event PaymentLocked(
        uint256 indexed orderId,
        address indexed buyer,
        address indexed seller,
        uint256 amountUsdt,
        uint256 assetTokenId
    );

    event AssetDispatched(
        uint256 indexed orderId,
        address indexed seller,
        bytes32 trackingHash,
        uint256 timestamp
    );

    event DeliveryConfirmed(
        uint256 indexed orderId,
        address indexed confirmedBy,
        uint256 timestamp
    );

    event BuyerAccepted(
        uint256 indexed orderId,
        address indexed buyer,
        uint256 timestamp
    );

    event DisputeOpened(
        uint256 indexed orderId,
        address indexed openedBy,
        bytes32 evidenceHash,
        uint256 timestamp
    );

    event FundsReleased(
        uint256 indexed orderId,
        address indexed seller,
        uint256 amountUsdt,
        uint256 timestamp
    );

    event FundsRefunded(
        uint256 indexed orderId,
        address indexed buyer,
        uint256 amountUsdt,
        uint256 timestamp
    );

    constructor(address _usdtAddress, address initialOwner) Ownable(initialOwner) {
        usdtToken = IERC20(_usdtAddress);
    }

    /**
     * @notice Locks USDT in escrow for a verified physical asset purchase.
     */
    function lockPayment(
        uint256 orderId,
        address seller,
        uint256 amountUsdt,
        uint256 assetTokenId
    ) external nonReentrant {
        require(orders[orderId].status == EscrowStatus.None, "Order ID already exists");
        require(seller != address(0) && seller != msg.sender, "Invalid seller address");
        require(amountUsdt > 0, "Amount must be greater than zero");

        usdtToken.safeTransferFrom(msg.sender, address(this), amountUsdt);

        orders[orderId] = EscrowOrder({
            orderId: orderId,
            buyer: msg.sender,
            seller: seller,
            amountUsdt: amountUsdt,
            assetTokenId: assetTokenId,
            status: EscrowStatus.PaymentLocked,
            trackingHash: bytes32(0),
            disputeEvidence: bytes32(0),
            createdAt: block.timestamp,
            shippedAt: 0,
            deliveredAt: 0,
            acceptedAt: 0,
            disputedAt: 0,
            resolvedAt: 0
        });

        emit PaymentLocked(orderId, msg.sender, seller, amountUsdt, assetTokenId);
    }

    /**
     * @notice Seller marks asset as dispatched with tracking hash.
     */
    function dispatchAsset(uint256 orderId, bytes32 trackingHash) external {
        EscrowOrder storage order = orders[orderId];
        require(order.seller == msg.sender || owner() == msg.sender, "Unauthorized dispatcher");
        require(order.status == EscrowStatus.PaymentLocked, "Invalid status for dispatch");

        order.status = EscrowStatus.InTransit;
        order.trackingHash = trackingHash;
        order.shippedAt = block.timestamp;

        emit AssetDispatched(orderId, msg.sender, trackingHash, block.timestamp);
    }

    /**
     * @notice Marks delivery as confirmed (by buyer or verified courier/reviewer).
     */
    function confirmDelivery(uint256 orderId) external {
        EscrowOrder storage order = orders[orderId];
        require(order.buyer == msg.sender || owner() == msg.sender, "Unauthorized confirmation");
        require(order.status == EscrowStatus.InTransit, "Asset is not in transit");

        order.status = EscrowStatus.Delivered;
        order.deliveredAt = block.timestamp;

        emit DeliveryConfirmed(orderId, msg.sender, block.timestamp);
    }

    /**
     * @notice Buyer accepts asset and releases USDT to seller.
     */
    function acceptAndRelease(uint256 orderId) external nonReentrant {
        EscrowOrder storage order = orders[orderId];
        require(order.buyer == msg.sender, "Only buyer can accept and release");
        require(order.status == EscrowStatus.Delivered, "Asset not delivered yet");

        order.status = EscrowStatus.ReleasedToSeller;
        order.acceptedAt = block.timestamp;
        order.resolvedAt = block.timestamp;

        usdtToken.safeTransfer(order.seller, order.amountUsdt);

        emit BuyerAccepted(orderId, msg.sender, block.timestamp);
        emit FundsReleased(orderId, order.seller, order.amountUsdt, block.timestamp);
    }

    /**
     * @notice Open dispute with evidence hash.
     */
    function openDispute(uint256 orderId, bytes32 evidenceHash) external {
        EscrowOrder storage order = orders[orderId];
        require(order.buyer == msg.sender || order.seller == msg.sender, "Only buyer or seller can dispute");
        require(
            order.status == EscrowStatus.PaymentLocked ||
            order.status == EscrowStatus.InTransit ||
            order.status == EscrowStatus.Delivered,
            "Invalid status for dispute"
        );

        order.status = EscrowStatus.Disputed;
        order.disputeEvidence = evidenceHash;
        order.disputedAt = block.timestamp;

        emit DisputeOpened(orderId, msg.sender, evidenceHash, block.timestamp);
    }

    /**
     * @notice Admin / Arbitrator resolves dispute and releases or refunds.
     */
    function resolveDispute(uint256 orderId, bool refundBuyer) external onlyOwner nonReentrant {
        EscrowOrder storage order = orders[orderId];
        require(order.status == EscrowStatus.Disputed, "Order is not in dispute");

        order.resolvedAt = block.timestamp;

        if (refundBuyer) {
            order.status = EscrowStatus.RefundedToBuyer;
            usdtToken.safeTransfer(order.buyer, order.amountUsdt);
            emit FundsRefunded(orderId, order.buyer, order.amountUsdt, block.timestamp);
        } else {
            order.status = EscrowStatus.ReleasedToSeller;
            usdtToken.safeTransfer(order.seller, order.amountUsdt);
            emit FundsReleased(orderId, order.seller, order.amountUsdt, block.timestamp);
        }
    }
}

