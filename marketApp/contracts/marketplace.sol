// SPDX-License-Identifier: MIT
pragma solidity ^0.8.3;

import "./marketApp/contracts/openzeppelin-contracts/contracts/token/ERC1155/ERC1155.sol";
import "./marketApp/contracts/openzeppelin-contracts/contracts/token/ERC1155/utils/ERC1155Holder.sol";
import "./marketApp/contracts/openzeppelin-contracts/contracts/security/ReentrancyGuard.sol";
import "./marketApp/contracts/openzeppelin-contracts/contracts/utils/Counters.sol";
import "./marketApp/contracts/openzeppelin-contracts/contracts/access/Ownable.sol";

contract marketplace is ERC1155Holder, Ownable, ReentrancyGuard {
    using Counters for Counters.Counter;
    Counters.Counter private _itemIds;

    uint256 public royalties;

    address payable marketplaceOwner;

    mapping(uint256 => Item) private itemsMapping;

    constructor(uint256 royalty) {
        marketplaceOwner = payable(msg.sender);
        royalties = royalty;
    }

    struct Item {
        address nftAddress;
        uint256 tokenId;
        uint256 itemId;
        address creator;
        address payable seller;
        address payable owner;
        address payable charity;
        uint256 price;
        bool isListed;
    }

    event ItemListed(
        address indexed nftAddress,
        uint256 indexed tokenId,
        uint256 indexed itemId,
        address creator,
        address seller,
        address owner,
        address charity,
        uint256 price,
        bool isListed
    );

    function listItemsForSale(
        address nftAddress,
        address _charity,
        uint256 _tokenId,
        uint256 _quantity,
        uint256 _price
    ) public {
        require(_price > 0, "Item price must be greater than 0");
        for (uint256 i = 0; i < _quantity; i++) {
            listItem(nftAddress, _charity, _tokenId, _price);
        }
    }

    function listItem(
        address nftAddress,
        address _charity,
        uint256 _tokenId,
        uint256 _price
    ) internal {
        _itemIds.increment();
        uint256 itemId = _itemIds.current();
        itemsMapping[itemId] = Item(
            nftAddress,
            _tokenId,
            itemId,
            msg.sender,
            payable(msg.sender),
            payable(msg.sender),
            payable(_charity),
            _price,
            true
        );

        IERC1155(nftAddress).safeTransferFrom(
            msg.sender,
            address(this),
            _tokenId,
            1,
            "0x00"
        );
        emit ItemListed(
            nftAddress,
            _tokenId,
            itemId,
            msg.sender,
            msg.sender,
            address(0),
            _charity,
            _price,
            true
        );
    }

    function purchaseItem(address nftAddress, uint256 _itemId)
        public
        payable
        nonReentrant
    {
        uint256 price = itemsMapping[_itemId].price;
        uint256 _tokenId = itemsMapping[_itemId].tokenId;
        bool isForSale = itemsMapping[_itemId].isListed;
        address owner = itemsMapping[_itemId].owner;

        require(owner != msg.sender, "Buyer and Seller are the same addresses");
        require(isForSale == true, "Item requested is not for sale.");
        require(msg.value == price, "Please submit the correct amount of ETH");

        uint256 royaltiesToCharity = ((royalties * msg.value) / 100);
        uint256 etherToSeller = msg.value - royaltiesToCharity;

        IERC1155(nftAddress).safeTransferFrom(
            address(this),
            msg.sender,
            _tokenId,
            1,
            "0x00"
        );

        IERC1155(nftAddress).setApprovalForAll(msg.sender, true);

        itemsMapping[_itemId].owner = payable(msg.sender);

        itemsMapping[_itemId].isListed = false;

        (bool royaltiesTransferred, ) = itemsMapping[_itemId].charity.call{
            value: royaltiesToCharity
        }(" ");
        require(
            royaltiesTransferred,
            "Failed to transfer royalties to charity"
        );

        (bool salePriceTransferred, ) = itemsMapping[_itemId].seller.call{
            value: etherToSeller
        }(" ");
        require(
            salePriceTransferred,
            "Failed to transfer sale price to seller"
        );
    }

    function getItemsOwned(address ownerAddress)
        public
        view
        returns (Item[] memory)
    {
        uint totalItemCount = _itemIds.current();
        uint myItemsCount = 0;
        uint resultItemId = 0;

        for (uint i = 0; i < totalItemCount; i++) {
            if (itemsMapping[i + 1].owner == ownerAddress) {
                myItemsCount++;
            }
        }

        Item[] memory ownedItems = new Item[](myItemsCount);
        for (uint i = 0; i < totalItemCount; i++) {
            if (itemsMapping[i + 1].owner == ownerAddress) {
                uint thisItemId = itemsMapping[i + 1].itemId;
                Item storage thisItem = itemsMapping[thisItemId];
                ownedItems[resultItemId] = thisItem;
                resultItemId++;
            }
        }

        return ownedItems;
    }

    function getListedItems() public view returns (Item[] memory) {
        uint totalItemCount = _itemIds.current();
        uint itemsListedCount = 0;
        uint resultItemId = 0;

        for (uint i = 0; i < totalItemCount; i++) {
            if (itemsMapping[i+1].isListed == true) {
                itemsListedCount++;
            }
        }

        Item[] memory listedItems = new Item[](itemsListedCount);
        for (uint i = 0; i < totalItemCount; i++) {
            if (itemsMapping[i+1].isListed == true) {
                uint thisItemId = itemsMapping[i+1].itemId;
                Item storage thisItem = itemsMapping[thisItemId];
                listedItems[resultItemId] = thisItem;
                resultItemId++;
            }
        }

        return listedItems;
    }

    function delistItem(uint _itemId) public {
        require(itemsMapping[_itemId].isListed == true, 'Item not listed yet');
        address itemOwner = itemsMapping[_itemId].owner;
        require(msg.sender == itemOwner, 'msg sender is not owner of item');
        itemsMapping[_itemId].isListed = false;
    }

    function relistItem(address nftAddress, uint _itemId, uint listPrice) public {
        uint _tokenId = itemsMapping[_itemId].tokenId;
        address _charity = itemsMapping[_itemId].charity;
        require(itemsMapping[_itemId].isListed == false, 'Item is already listed');
        require(msg.sender == itemsMapping[_itemId].owner, 'Caller is not owner of item');
        itemsMapping[_itemId].isListed = true;
        itemsMapping[_itemId].price = listPrice;

        emit ItemListed(nftAddress, _tokenId, _itemId, msg.sender, msg.sender, address(0), _charity, listPrice, true);
    }
}
