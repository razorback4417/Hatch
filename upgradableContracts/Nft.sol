// SPDX-License-Identifier: MIT
pragma solidity ^0.8.3;

//import './marketApp/contracts/openzeppelin-contracts-upgradeable/contracts/token/ERC1155/ERC1155Upgradeable.sol';
//import './marketApp/contracts/openzeppelin-contracts-upgradeable/contracts/security/PausableUpgradeable.sol';
//import './marketApp/contracts/openzeppelin-contracts-upgradeable/contracts/access/OwnableUpgradeable.sol';
//import './marketApp/contracts/openzeppelin-contracts-upgradeable/contracts/proxy/utils/Initializable.sol';
//import './marketApp/contracts/openzeppelin-contracts-upgradeable/contracts/proxy/utils/UUPSUpgradeable.sol';
//import './marketApp/contracts/openzeppelin-contracts-upgradeable/contracts/utils/CountersUpgradeable.sol';

import "@openzeppelin/contracts-upgradeable/token/ERC1155/ERC1155Upgradeable.sol";
import "@openzeppelin/contracts-upgradeable/security/PausableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/security/ReentrancyGuardUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/utils/CountersUpgradeable.sol";

/// @title NFT smart contract
/// @author Theo Luu
/// @notice Contract mints an ERC1155 NFT
/// @dev Contract has been tested with Slither and Brownie
contract Nft is Initializable, ERC1155Upgradeable, PausableUpgradeable, ReentrancyGuardUpgradeable, OwnableUpgradeable, UUPSUpgradeable {

    // @notice tokenIds keep track of the number of NFTs minted
    using CountersUpgradeable for CountersUpgradeable.Counter;
    CountersUpgradeable.Counter private tokenIds;

    // @notice address of Marketplace to list NFTs on. Initialized in the constructor
    address public marketplaceAddress;

    mapping(uint256 => string) private _uris;

    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() initializer {}
    
    function initialize(address marketAddress) initializer public {
        __ERC1155_init("Hatch App");
        __Pausable_init();
        __Ownable_init();
        __UUPSUpgradeable_init();
        marketplaceAddress = marketAddress;

    }


    function unpause() external onlyOwner {
        _unpause();
    }

    function pause() external onlyOwner {
        _pause();
    }

    function _authorizeUpgrade(address newImplementation)
        internal
        override
        onlyOwner {}


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
    ) nonReentrant external whenNotPaused returns (uint256) {
        tokenIds.increment();
        uint256 currentTokenId = tokenIds.current();

        _mint(msg.sender, currentTokenId, quantity, data);

        setApprovalForAll(marketplaceAddress, true);

        _setURI(tokenURI);
        // setTokenURI(currentTokenId, tokenURI);

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

    /// @notice Returns URI string for a given NFT token ID
    /// @param tokenId unique NFT token ID
    function getTokenURI(uint256 tokenId)
        public
        view
        returns (string memory)
    {
        return uri(tokenId);
    }
    
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
}
