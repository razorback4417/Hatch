// SPDX-License-Identifier: MIT
pragma solidity ^0.8.3;

import "./marketApp/contracts/openzeppelin-contracts/contracts/token/ERC1155/ERC1155.sol";
import "./marketApp/contracts/openzeppelin-contracts/contracts/access/Ownable.sol";
import "./marketApp/contracts/openzeppelin-contracts/contracts/utils/Counters.sol";


contract nft is ERC1155, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    address public marketplaceAddress;

    mapping(uint256 => string) private _uris;

    constructor(address marketAddress) ERC1155("Market App") {
        marketplaceAddress = marketAddress;
    }

    function mintToken(
        string memory tokenURI,
        uint256 quantity,
        bytes memory data
    ) public returns (uint256) {
        _tokenIds.increment();
        uint256 currentTokenId = _tokenIds.current();

        _mint(msg.sender, currentTokenId, quantity, data);

        setApprovalForAll(marketplaceAddress, true);

        setTokenURI(currentTokenId, tokenURI);

        return currentTokenId;
    }

    function setTokenURI(uint _tokenId, string memory newURI) public {
        bool owner = checkIfOwner(_tokenId);
        require(owner ==true, 'Function claler is not the owner of the token');
        require(bytes(_uris[_tokenId]).length == 0, 'Cannot set URI twice.');
        _uris[_tokenId] = newURI;
    }

    function checkIfOwner(uint _tokenId) public view returns (bool) {
        if (balanceOf(msg.sender, _tokenId) > 0) {
            return true;
        }
        return false;
    }

    function getCurrentTokenID() public view returns (uint256) {
        uint currentTokenId = _tokenIds.current();
        return currentTokenId;
    }

    function getTokenURI(uint _tokenId) public view returns (string memory) {
        return (_uris[_tokenId]);
    }

    
}
