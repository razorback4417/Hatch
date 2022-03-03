// SPDX-License-Identifier: MIT
pragma solidity ^0.8.3;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";


/// @title NFT smart contract
/// @author Theo Luu
/// @notice Contract mints an ERC1155 NFT
/// @dev Contract has been tested with Slither and Brownie
contract Nft is ERC1155, Ownable, ReentrancyGuard {

    // @notice tokenIds keep track of the number of NFTs minted
    using Counters for Counters.Counter;
    Counters.Counter private tokenIds;

    // @notice address of Marketplace to list NFTs on. Initialized in the constructor
    address public marketplaceAddress;

    mapping(uint256 => string) private _uris;

    // @notice Initialize market address.
    constructor(address marketAddress) ERC1155("Market App") {
        require(marketAddress != address(0x0), 'Invalid MarketPlace Address');
        marketplaceAddress = marketAddress;
    }

    /// -------------- Mutative Functions --------------

    /// @notice Mints ERC1155 token to user wallet
    /// @dev Sets approval for MarketPlace to list NFT and sets tokenURI to uris mapping
    /// @param tokenURI Metadata of the NFT
    /// @param quantity Number of NFTs to be minted
    /// @param data Additional data with no specified format
    /// @return tokenID of the minted NFT
    function mintToken(
        string memory tokenURI,
        uint256 quantity,
        bytes memory data
    ) nonReentrant external returns (uint256) {
        tokenIds.increment();
        uint256 currentTokenId = tokenIds.current();

        _mint(msg.sender, currentTokenId, quantity, data);

        setApprovalForAll(marketplaceAddress, true);

        setTokenURI(currentTokenId, tokenURI);

        return currentTokenId;
    }

    /// @notice Sets tokenId for each minted NFT
    /// @dev setTokenURI is called by the mintToken function. setTokenURI limits one URI to one tokenId
    /// @param tokenId integer value that will be added to the NFT URI
    /// @param newURI URI that tokenId is added to
    function setTokenURI(uint tokenId, string memory newURI) public {
        bool isOwner = checkIfOwner(tokenId);
        require(isOwner, 'Function caller is not the owner of the token');
        require(bytes(_uris[tokenId]).length == 0, 'Cannot set URI twice.');
        _uris[tokenId] = newURI;
    }

    /// -------------- Read Functions --------------
    
    ///@notice Returns true or false to indicate if the sender address is the owner address of a given tokenId
    ///@dev Function is a public view
    ///@param tokenId The ID of an NFT owned by a user
    ///@return Returns true or false based on the conditional statement
    function checkIfOwner(uint tokenId) public view returns (bool) {
        if (balanceOf(msg.sender, tokenId) > 0) {
            return true;
        }
        return false;
    }

    ///@notice Returns tokenId
    ///@dev Function is an external view
    ///@return Returns currentTokenId, a non-negative integer
    function getCurrentTokenID() external view returns (uint256) {
        uint currentTokenId = tokenIds.current();
        return currentTokenId;
    }

    ///@notice Returns current token URI
    ///@dev Function is a public view
    ///@return Returns current token URI
    function getTokenURI(uint tokenId) external view returns (string memory) {
        return (_uris[tokenId]);
    }
}
