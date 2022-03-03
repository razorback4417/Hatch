// SPDX-License-Identifier: MIT
pragma solidity ^0.8.3;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/token/ERC1155/utils/ERC1155Holder.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/// @title MarketPlace smart contract
/// @author Theo Luu
/// @notice Contract initializes marketplace variables and enables users to list and purchase NFTs
contract MarketPlace is ERC1155Holder, Ownable, ReentrancyGuard {

    //@notice itemIds to keep track of the ID of NFTs
    using Counters for Counters.Counter;
    Counters.Counter private itemIds;

    uint256 public royalties;

    // @notice Owner of marketplace. Initalized as msg.sender in constructor
    address payable marketPlaceOwner;

    mapping(uint256 => Item) private itemsMapping;

    //@notice Initializes owner of marketplace as msg.sender and initializes proportion of royalties that will go to charity
    constructor(uint256 royalty) {
        marketPlaceOwner = payable(msg.sender);
        royalties = royalty;
    }

    ///@notice Item struct stores variables required to list an NFT on the marketplace
    struct Item {
        address nftAddress;
        uint256 tokenId;
        uint256 itemId;
        address creatorAddress;
        address payable sellerAddress;
        address payable ownerAddress;
        address payable charityAddress;
        uint256 price;
        bool isListed;
    }

    /// -------------- Events --------------

    ///@notice Event produced when an NFT is listed
    ///@param nftAddress Deployed NFT contract address
    ///@param tokenId Unique NFT ID
    ///@param itemId Unique NFT item ID
    ///@param creatorAddress Address of the NFT's creator
    ///@param sellerAddress Address of the NFT's seller
    ///@param ownerAddress Address of NFT's Owner
    ///@param charityAddress Address of charity benefiting from sell of NFT
    ///@param price Price of NFT
    ///@param isListed Listed boolean indicator

    event ItemListed(
        address indexed nftAddress,
        uint256 indexed tokenId,
        uint256 indexed itemId,
        address creatorAddress,
        address sellerAddress,
        address ownerAddress,
        address charityAddress,
        uint256 price,
        bool isListed
    );

    /// -------------- Mutative Functions --------------

    ///@notice Lists NFTs that are for sale
    ///@dev Reverts with error message if price is not positive. Transfers the NFT from owner wallet to marketplace
    ///@param nftAddress Deployed NFT contract address
    ///@param charityAddress Address of charity benefiting from sell of NFT
    ///@param tokenId Unique NFT ID
    ///@param quantity Number of NFTs to be minted
    ///@param price Price of NFT
    function listItemsForSale(
        address nftAddress,
        address charityAddress,
        uint256 tokenId,
        uint256 quantity,
        uint256 price
    ) nonReentrant external {
        require(price > 0, "Item price must be greater than 0");
        for (uint256 i = 0; i < quantity; i++) {
            listItem(nftAddress, charityAddress, tokenId, price);
        }
        IERC1155(nftAddress).safeTransferFrom(
            msg.sender,
            address(this),
            tokenId,
            1,
            "0x00"
        );
    }

    ///@notice Lists an NFT that is for sale
    ///@param nftAddress Deployed NFT contract address
    ///@param charityAddress Address of charity benefiting from sell of NFT
    ///@param tokenId Unique NFT ID
    ///@param price Price of NFT
    function listItem(
        address nftAddress,
        address charityAddress,
        uint256 tokenId,
        uint256 price
    ) internal {
        itemIds.increment();
        uint256 itemId = itemIds.current();
        itemsMapping[itemId] = Item(
            nftAddress,
            tokenId,
            itemId,
            msg.sender,
            payable(msg.sender),
            payable(msg.sender),
            payable(charityAddress),
            price,
            true
        );

        emit ItemListed(
            nftAddress,
            tokenId,
            itemId,
            msg.sender,
            msg.sender,
            address(0),
            charityAddress,
            price,
            true
        );
    }

    ///@notice Allows users to purchase NFT
    ///@dev Transfers NFT from marketplace to buyer
    ///@param nftAddress Deployed NFT contract address
    ///@param itemId Unique item ID
    function purchaseItem(address nftAddress, uint256 itemId)
        external
        payable
        nonReentrant
    {
        uint256 price = itemsMapping[itemId].price;
        uint256 tokenId = itemsMapping[itemId].tokenId;
        bool isForSale = itemsMapping[itemId].isListed;
        address ownerAddress = itemsMapping[itemId].ownerAddress;

        require(
            ownerAddress != msg.sender,
            "Buyer and Seller are the same addresses"
        );
        require(isForSale, "Item requested is not for sale.");
        require(msg.value == price, "Please submit the correct amount of ETH");

        uint256 royaltiesToCharity = ((royalties * msg.value) / 100);
        uint256 etherToSeller = msg.value - royaltiesToCharity;

        ///@dev Transfers 1 NFT token of token type tokenId from marketplace contract to the buyer, msg.sender
        IERC1155(nftAddress).safeTransferFrom(
            address(this),
            msg.sender,
            tokenId,
            1,
            "0x00"
        );

        ///@dev Grants permission to buyer to transfer caller's token
        IERC1155(nftAddress).setApprovalForAll(msg.sender, true);

        ///@dev Sets buyer to new owner
        itemsMapping[itemId].ownerAddress = payable(msg.sender);

        ///@dev Unlist purchased NFT from marketplace
        itemsMapping[itemId].isListed = false;

        ///@notice Move royalty amount to charity address
        (bool royaltiesTransferred, ) = itemsMapping[itemId].charityAddress.call{
            value: royaltiesToCharity
        }(" ");
        require(
            royaltiesTransferred,
            "Failed to transfer royalties to charity"
        );

        ///@notice Move remaining sell price to seller address
        (bool salePriceTransferred, ) = itemsMapping[itemId].sellerAddress.call{
            value: etherToSeller
        }(" ");
        require(
            salePriceTransferred,
            "Failed to transfer sale price to seller"
        );
    }


    ///@notice Deployed NFT contract address
    ///@param itemId Unique item ID
    function delistItem(uint256 itemId) external {
        require(itemsMapping[itemId].isListed, "Item not listed yet");
        address itemOwner = itemsMapping[itemId].ownerAddress;
        require(msg.sender == itemOwner, "msg sender is not owner of item");
        itemsMapping[itemId].isListed = false;
    }

    ///@notice Allows user to relist NFT
    ///@param nftAddress Deployed NFT contract address
    ///@param itemId Unique item ID
    ///@param listPrice Price of relisted item
    function relistItem(
        address nftAddress,
        uint256 itemId,
        uint256 listPrice
    ) external {
        uint256 tokenId = itemsMapping[itemId].tokenId;
        address charityAddress = itemsMapping[itemId].charityAddress;
        require(
            !(itemsMapping[itemId].isListed),
            "Item is already listed"
        );
        require(
            msg.sender == itemsMapping[itemId].ownerAddress,
            "Caller is not owner of item"
        );
        itemsMapping[itemId].isListed = true;
        itemsMapping[itemId].price = listPrice;

        emit ItemListed(
            nftAddress,
            tokenId,
            itemId,
            msg.sender,
            msg.sender,
            address(0),
            charityAddress,
            listPrice,
            true
        );
    }

    /// -------------- Read Functions --------------

    ///@notice Returns item owned by an address
    ///@param ownerAddress Address of the owner of items
    ///@return Returns item owned by ownerAddress address
    function getItemsOwned(address ownerAddress)
        external
        view
        returns (Item[] memory)
    {
        uint256 totalItemCount = itemIds.current();
        uint256 myItemsCount = 0;
        uint256 resultItemId = 0;

        for (uint256 i = 0; i < totalItemCount; i++) {
            if (itemsMapping[i + 1].ownerAddress == ownerAddress) {
                myItemsCount++;
            }
        }

        Item[] memory ownedItems = new Item[](myItemsCount);
        for (uint256 i = 0; i < totalItemCount; i++) {
            if (itemsMapping[i + 1].ownerAddress == ownerAddress) {
                uint256 thisItemId = itemsMapping[i + 1].itemId;
                Item storage thisItem = itemsMapping[thisItemId];
                ownedItems[resultItemId] = thisItem;
                resultItemId++;
            }
        }

        return ownedItems;
    }

    ///@notice Returns array of items listed in marketplace
    ///@dev First for-loop creates itemsListedCount used for size of listedItems array
    ///@return Array of items listed in marketplace
    function getListedItems() external view returns (Item[] memory) {
        uint256 totalItemCount = itemIds.current();
        uint256 itemsListedCount = 0;
        uint256 resultItemId = 0;

        for (uint256 i = 0; i < totalItemCount; i++) {
            if (itemsMapping[i + 1].isListed) {
                itemsListedCount++;
            }
        }

        Item[] memory listedItems = new Item[](itemsListedCount);
        for (uint256 i = 0; i < totalItemCount; i++) {
            if (itemsMapping[i + 1].isListed) {
                uint256 thisItemId = itemsMapping[i + 1].itemId;
                Item storage thisItem = itemsMapping[thisItemId];
                listedItems[resultItemId] = thisItem;
                resultItemId++;
            }
        }

        return listedItems;
    }


    ///@notice Gets latest ItemId on the marketplace
    ///@return Returns current itemId
    function getCurrentItemId() external view returns (uint256) {
        return itemIds.current();
    }

    ///@notice Gets item based on a given itemId
    ///@param itemId Unique NFT item ID
    ///@return Returns item information
    function getItemById(uint256 itemId) external view returns (Item memory) {
        return itemsMapping[itemId];
    }
}
