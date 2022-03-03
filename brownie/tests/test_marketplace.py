import brownie
import pytest

@pytest.fixture
def marketPlaceContract(accounts, MarketPlace):
    admin = accounts[0]
    royalty = 30
    
    return MarketPlace.deploy(royalty, {"from": admin})

@pytest.fixture
def nftContract(marketPlaceContract, Nft, accounts):
    admin = accounts[0]

    return Nft.deploy(marketPlaceContract.address, {"from": admin})

@pytest.fixture
def tokenURI():
    return "https://ipfs.infura.io/ipfs/QmcmEcjxkPkVf5hWcHMSyAFzibK78zGKHkZPfYRuSrLrqK"

def test_listItemsForSale(accounts, marketPlaceContract, nftContract, tokenURI):
    
    artist = accounts[1]
    charityAddress = accounts[2]

    #Deploy NFT contract
    nftAddress = nftContract.address

    quantity = 1
    price = 1
    data = "0x00"

    #Mints NFT
    nftContract.mintToken(tokenURI, quantity, data, {"from": artist})

    #Gets minted NFT token ID
    tokenId = nftContract.getCurrentTokenID()

    #Lists item for sale
    marketPlaceContract.listItemsForSale(nftAddress, charityAddress, tokenId, quantity, price, {"from": artist})

    #Sets up assert statement
    expectedItemId = 1
    actualItemId = marketPlaceContract.getCurrentItemId()
    assert actualItemId == expectedItemId

def test_listItemsForSaleRevert(accounts, marketPlaceContract, nftContract, tokenURI):
    
    artist = accounts[1]
    charityAddress = accounts[2]

    #Deploy NFT contract
    nftAddress = nftContract.address

    quantity = 1
    price = 0
    data = "0x00"

    #Mints NFT
    nftContract.mintToken(tokenURI, quantity, data, {"from": artist})

    #Gets minted NFT token ID
    tokenId = nftContract.getCurrentTokenID()

    #Reverts because the listing price is zero
    with brownie.reverts("Item price must be greater than 0"):
        marketPlaceContract.listItemsForSale(nftAddress, charityAddress, tokenId, quantity, price, {"from": artist})

def test_purchaseItem(accounts, marketPlaceContract, nftContract, tokenURI):

    #Setup parameters
    artist = accounts[1]
    buyer = accounts[2]
    charityAddress = accounts[3]
    

    #Obtain NFT contract address
    nftAddress = nftContract.address
    quantity = 1

    #Price in Wei (10 ETH)
    price = 10000000000000000000

    data = "0x00"

    #Mint NFT
    nftContract.mintToken(tokenURI, quantity, data, {"from": artist})

    #Obtain minted NFT token ID
    tokenId = nftContract.getCurrentTokenID()

    #Lists NFT on marketplace
    marketPlaceContract.listItemsForSale(nftAddress, charityAddress, tokenId, quantity, price, {"from": artist})

    #Obtains the listing item ID
    itemId = marketPlaceContract.getCurrentItemId()

    #Purchases listed NFT with given item ID
    marketPlaceContract.purchaseItem(nftAddress, itemId, {"from": buyer, "value": price})

    #Assert whether account balances are correctly updated
    assert buyer.balance() == 90000000000000000000 #90 ETH
    assert artist.balance() == 107000000000000000000 #107 ETH
    assert charityAddress.balance() == 103000000000000000000 #103 ETH


def test_deploy(accounts, MarketPlace):
    admin = accounts[0]

    royalty = 30

    marketplaceContract = MarketPlace.deploy(royalty, {"from": admin})

    expectedRoyalty = royalty
    actualRoyalty = marketplaceContract.royalties()
    assert actualRoyalty == expectedRoyalty



def test_delistItem(accounts, nftContract, marketPlaceContract):
    
    artist = accounts[1]
    buyer = accounts[2]
    charityAddress = accounts[3]

    nftAddress = nftContract.address

    tokenURI = "https://ipfs.infura.io/ipfs/QmcmEcjxkPkVf5hWcHMSyAFzibK78zGKHkZPfYRuSrLrqK"
    quantity = 1
    price = 10000000000000000000
    data = "0x00"

    nftContract.mintToken(tokenURI, quantity, data, {"from": artist})

    tokenId = nftContract.getCurrentTokenID()

    marketPlaceContract.listItemsForSale(nftAddress, charityAddress, tokenId, quantity, price, {"from": artist})

    itemId = marketPlaceContract.getCurrentItemId()

    marketPlaceContract.delistItem(itemId, {"from": artist})

    data = marketPlaceContract.getItemById(itemId)
    actualIsListed = data[8]
    assert actualIsListed == False

def test_relistItem(accounts, nftContract, marketPlaceContract):
    
    artist = accounts[1]
    buyer = accounts[2]
    charityAddress = accounts[3]
    
    nftAddress = nftContract.address

    tokenURI = "https://ipfs.infura.io/ipfs/QmcmEcjxkPkVf5hWcHMSyAFzibK78zGKHkZPfYRuSrLrqK"
    quantity = 1
    price = 10000000000000000000
    data = "0x00"

    nftContract.mintToken(tokenURI, quantity, data, {"from": artist})

    tokenId = nftContract.getCurrentTokenID()

    marketPlaceContract.listItemsForSale(nftAddress, charityAddress, tokenId, quantity, price, {"from": artist})

    itemId = marketPlaceContract.getCurrentItemId()

    marketPlaceContract.delistItem(itemId, {"from": artist})

    price = 20000000000000000000

    marketPlaceContract.relistItem(nftAddress, itemId, price, {"from": artist})

    data = marketPlaceContract.getItemById(tokenId)

    actualPrice = data[7]
    actualIsListed = data[8]

    assert actualPrice == price
    assert actualIsListed == True

def test_getCurentItemID(accounts, nftContract, marketPlaceContract):
    artist = accounts[1]
    charityAddress = accounts[3]

    nftAddress = nftContract.address

    tokenURI = "https://ipfs.infura.io/ipfs/QmcmEcjxkPkVf5hWcHMSyAFzibK78zGKHkZPfYRuSrLrqK"
    quantity = 1
    price = 1
    data = "0x00"

    nftContract.mintToken(tokenURI, quantity, data, {"from": artist})

    tokenId = nftContract.getCurrentTokenID()

    marketPlaceContract.listItemsForSale(nftAddress, charityAddress, tokenId, quantity, price, {"from": artist})

    itemId = marketPlaceContract.getCurrentItemId()

    expectedItemId = 1
    actualItemId = marketPlaceContract.getCurrentItemId()
    assert actualItemId == expectedItemId

def test_getListedItems(accounts, nftContract, marketPlaceContract):
    artist = accounts[1]
    artist2 = accounts[2]
    charityAddress = accounts[3]

    nftAddress = nftContract.address

    tokenURI = "https://ipfs.infura.io/ipfs/QmcmEcjxkPkVf5hWcHMSyAFzibK78zGKHkZPfYRuSrLrqK"
    quantity = 1
    data = "0x00"

    nftContract.mintToken(tokenURI, quantity, data, {"from": artist})

    tokenId = nftContract.getCurrentTokenID()

    price = 10000000000000000000

    marketPlaceContract.listItemsForSale(nftAddress, charityAddress, tokenId, quantity, price, {"from": artist})

    nftContract.mintToken(tokenURI, quantity, data, {"from": artist2})

    tokenId = nftContract.getCurrentTokenID()

    price = 20000000000000000000

    marketPlaceContract.listItemsForSale(nftAddress, charityAddress, tokenId, quantity, price, {"from": artist2})

    data = marketPlaceContract.getListedItems()

    actualArtist1 = data[0][5]
    actualArtist2 = data[1][5]

    assert actualArtist1 == artist
    assert actualArtist2 == artist2

def test_getItemsOwned(accounts, nftContract, marketPlaceContract):
    artist = accounts[1]
    artist2 = accounts[2]
    charityAddress = accounts[3]

    nftAddress = nftContract.address

    tokenURI = "https://ipfs.infura.io/ipfs/QmcmEcjxkPkVf5hWcHMSyAFzibK78zGKHkZPfYRuSrLrqK"
    quantity = 1
    data = "0x00"

    nftContract.mintToken(tokenURI, quantity, data, {"from": artist})

    tokenId = nftContract.getCurrentTokenID()

    price = 10000000000000000000

    marketPlaceContract.listItemsForSale(nftAddress, charityAddress, tokenId, quantity, price, {"from": artist})

    nftContract.mintToken(tokenURI, quantity, data, {"from": artist2})

    tokenId = nftContract.getCurrentTokenID()

    price = 20000000000000000000

    marketPlaceContract.listItemsForSale(nftAddress, charityAddress, tokenId, quantity, price, {"from": artist2})

    data = marketPlaceContract.getItemsOwned(artist)

    actualArtist1 = data[0][5]
    assert actualArtist1 == artist

def test_getItemById(accounts, marketPlaceContract, nftContract):
    
    artist = accounts[1]
    charityAddress = accounts[2]

    nftAddress = nftContract.address

    tokenURI = "https://ipfs.infura.io/ipfs/QmcmEcjxkPkVf5hWcHMSyAFzibK78zGKHkZPfYRuSrLrqK"
    quantity = 1
    price = 1
    data = "0x00"

    nftContract.mintToken(tokenURI, quantity, data, {"from": artist})

    tokenId = nftContract.getCurrentTokenID()

    marketPlaceContract.listItemsForSale(
        nftAddress, charityAddress, tokenId, quantity, price, {"from": artist})

    expectedItemId = 1
    actualItemId = marketPlaceContract.getCurrentItemId()
    assert actualItemId == expectedItemId

    data = marketPlaceContract.getItemById(actualItemId)

    actualNFTAddress = data[0]
    actualTokenId = data[1]
    actualItemId = data[2]
    actualCreator = data[3]
    actualSeller = data[4]
    actualOwner = data[5]
    actualCharity = data[6]
    actualPrice = data[7]
    actualIsListed = data[8]

    assert actualNFTAddress == nftAddress
    assert actualTokenId == tokenId
    assert actualItemId == expectedItemId
    assert actualCreator == artist
    assert actualSeller == artist
    assert actualOwner == artist
    assert actualCharity == charityAddress
    assert actualPrice == price
    assert actualIsListed == True