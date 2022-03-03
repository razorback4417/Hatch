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


def test_deploy(Nft, MarketPlace, accounts):

    admin = accounts[0]

    royalty = 30

    marketplaceContract = MarketPlace.deploy(royalty, {"from": admin})
    marketplaceAddress = marketplaceContract.address

    nftContract = Nft.deploy(marketplaceAddress, {"from": admin})

    expected = marketplaceAddress
    actual = nftContract.marketplaceAddress()
    assert actual == expected

def test_mintNFT(nftContract, accounts):

    artist = accounts[1]
    # artist2 = accounts[2]
    tokenURI = "https://ipfs.infura.io/ipfs/QmcmEcjxkPkVf5hWcHMSyAFzibK78zGKHkZPfYRuSrLrqK"
    quantity = 1
    data = "0x00"

    nftContract.mintToken(tokenURI, quantity, data, {"from": artist})
    # nftContract.mintToken(tokenURI, quantity, data, {"from": artist2})

    expectedTokenID = 1
    actualTokenID = nftContract.getCurrentTokenID()
    if expectedTokenID != actualTokenID:
        assert expectedTokenID != actualTokenID
    else:
        assert expectedTokenID == actualTokenID

    expectedTokenURI = tokenURI
    actualTokenURI = nftContract.getTokenURI(actualTokenID)
    assert expectedTokenURI == actualTokenURI

    expectedOwner = True
    actualIsOwner = nftContract.checkIfOwner(actualTokenID, {"from": artist})
    if expectedOwner != actualIsOwner:
        assert expectedOwner != actualIsOwner
    else:
        assert expectedOwner == actualIsOwner

    # expectedOwner = False
    # actualIsOwner = nftContract.checkIfOwner(actualTokenID, {"from": artist2})
    # assert expectedOwner == actualIsOwner
    
    

    