const MarketplaceABI = [{
        "inputs": [{
            "internalType": "uint256",
            "name": "royalty",
            "type": "uint256"
        }],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": false,
        "inputs": [{
                "indexed": true,
                "internalType": "address",
                "name": "nftAddress",
                "type": "address"
            },
            {
                "indexed": true,
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256"
            },
            {
                "indexed": true,
                "internalType": "uint256",
                "name": "itemId",
                "type": "uint256"
            },
            {
                "indexed": false,
                "internalType": "address",
                "name": "creator",
                "type": "address"
            },
            {
                "indexed": false,
                "internalType": "address",
                "name": "seller",
                "type": "address"
            },
            {
                "indexed": false,
                "internalType": "address",
                "name": "owner",
                "type": "address"
            },
            {
                "indexed": false,
                "internalType": "address",
                "name": "charity",
                "type": "address"
            },
            {
                "indexed": false,
                "internalType": "uint256",
                "name": "price",
                "type": "uint256"
            },
            {
                "indexed": false,
                "internalType": "bool",
                "name": "isListed",
                "type": "bool"
            }
        ],
        "name": "ItemListed",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [{
                "indexed": true,
                "internalType": "address",
                "name": "previousOwner",
                "type": "address"
            },
            {
                "indexed": true,
                "internalType": "address",
                "name": "newOwner",
                "type": "address"
            }
        ],
        "name": "OwnershipTransferred",
        "type": "event"
    },
    {
        "inputs": [{
            "internalType": "uint256",
            "name": "_itemId",
            "type": "uint256"
        }],
        "name": "delistItem",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{
            "internalType": "address",
            "name": "ownerAddress",
            "type": "address"
        }],
        "name": "getItemsOwned",
        "outputs": [{
            "components": [{
                    "internalType": "address",
                    "name": "nftAddress",
                    "type": "address"
                },
                {
                    "internalType": "uint256",
                    "name": "tokenId",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "itemId",
                    "type": "uint256"
                },
                {
                    "internalType": "address",
                    "name": "creator",
                    "type": "address"
                },
                {
                    "internalType": "address payable",
                    "name": "seller",
                    "type": "address"
                },
                {
                    "internalType": "address payable",
                    "name": "owner",
                    "type": "address"
                },
                {
                    "internalType": "address payable",
                    "name": "charity",
                    "type": "address"
                },
                {
                    "internalType": "uint256",
                    "name": "price",
                    "type": "uint256"
                },
                {
                    "internalType": "bool",
                    "name": "isListed",
                    "type": "bool"
                }
            ],
            "internalType": "struct marketplace.Item[]",
            "name": "",
            "type": "tuple[]"
        }],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getListedItems",
        "outputs": [{
            "components": [{
                    "internalType": "address",
                    "name": "nftAddress",
                    "type": "address"
                },
                {
                    "internalType": "uint256",
                    "name": "tokenId",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "itemId",
                    "type": "uint256"
                },
                {
                    "internalType": "address",
                    "name": "creator",
                    "type": "address"
                },
                {
                    "internalType": "address payable",
                    "name": "seller",
                    "type": "address"
                },
                {
                    "internalType": "address payable",
                    "name": "owner",
                    "type": "address"
                },
                {
                    "internalType": "address payable",
                    "name": "charity",
                    "type": "address"
                },
                {
                    "internalType": "uint256",
                    "name": "price",
                    "type": "uint256"
                },
                {
                    "internalType": "bool",
                    "name": "isListed",
                    "type": "bool"
                }
            ],
            "internalType": "struct marketplace.Item[]",
            "name": "",
            "type": "tuple[]"
        }],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{
                "internalType": "address",
                "name": "nftAddress",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "_charity",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "_tokenId",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "_quantity",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "_price",
                "type": "uint256"
            }
        ],
        "name": "listItemsForSale",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{
                "internalType": "address",
                "name": "",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            },
            {
                "internalType": "uint256[]",
                "name": "",
                "type": "uint256[]"
            },
            {
                "internalType": "uint256[]",
                "name": "",
                "type": "uint256[]"
            },
            {
                "internalType": "bytes",
                "name": "",
                "type": "bytes"
            }
        ],
        "name": "onERC1155BatchReceived",
        "outputs": [{
            "internalType": "bytes4",
            "name": "",
            "type": "bytes4"
        }],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{
                "internalType": "address",
                "name": "",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            },
            {
                "internalType": "bytes",
                "name": "",
                "type": "bytes"
            }
        ],
        "name": "onERC1155Received",
        "outputs": [{
            "internalType": "bytes4",
            "name": "",
            "type": "bytes4"
        }],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [{
            "internalType": "address",
            "name": "",
            "type": "address"
        }],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{
                "internalType": "address",
                "name": "nftAddress",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "_itemId",
                "type": "uint256"
            }
        ],
        "name": "purchaseItem",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [{
                "internalType": "address",
                "name": "nftAddress",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "_itemId",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "listPrice",
                "type": "uint256"
            }
        ],
        "name": "relistItem",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "renounceOwnership",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "royalties",
        "outputs": [{
            "internalType": "uint256",
            "name": "",
            "type": "uint256"
        }],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{
            "internalType": "bytes4",
            "name": "interfaceId",
            "type": "bytes4"
        }],
        "name": "supportsInterface",
        "outputs": [{
            "internalType": "bool",
            "name": "",
            "type": "bool"
        }],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{
            "internalType": "address",
            "name": "newOwner",
            "type": "address"
        }],
        "name": "transferOwnership",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

function listNFT(id) {

    window.alert("inside listNFT")

    let tokenID = id;
    //window.alert("tokenid=" + tokenID)
    var web3 = new Web3(window.ethereum);

    //window.alert("step 1")

    let NFTdeployedAddress = document.getElementById("NFTdeployedAddress").textContent;
    let MarketplaceDeployedAddress = document.getElementById("MarketplaceDeployedAddress").textContent;

    //window.alert("step 2")

    let quantity_ID = 'quantity-val-' + tokenID;
    let price_ID = 'price-val-' + tokenID;
    let itemID_ID = 'itemID-val-' + tokenID;
    let charityAddress_ID = 'charityAddress-val-' + tokenID;

    //window.alert("step 3")

    let quantity = document.getElementById(quantity_ID).textContent;
    let price = document.getElementById(price_ID).textContent;

    let itemID = document.getElementById(itemID_ID).textContent;
    let charityAddress = document.getElementById(charityAddress_ID).textContent;

    // window.alert("step 4")

    tokenID = parseInt(tokenID);
    quantity = parseInt(quantity);
    itemID = parseInt(itemID);

    // window.alert("step 5")

    var priceInWei = web3.utils.toWei(price.toString(), 'ether');

    //window.alert("step 6: converted eth to wei")

    const marketplace = new web3.eth.Contract(MarketplaceABI, MarketplaceDeployedAddress);

    //window.alert("step 7, initialized marketplace")
    marketplace.setProvider(window.ethereum);
    //window.alert("step 8: set provider")

    let isListed_Id = 'isListed-input-value-' + tokenID;

    document.getElementById(isListed_Id).value = 'Y'

    if (itemID == 0) {
        window.alert("inside if statement for itemID == 0")
        window.alert("tokenID=" + tokenID);
        marketplace.methods.listItemsForSale(NFTdeployedAddress, charityAddress, tokenID, quantity, priceInWei).send({ from: ethereum.selectedAddress });
    } else {
        //window.alert("Relist Items")
        let newPrice_ID = 'new-price-' + tokenID;
        let newPrice = document.getElementById(newPrice_ID).value;
        var newPriceInWei = web3.utils.toWei(newPrice.toString(), 'ether');
        window.alert("newprice=" + newPrice);
        marketplace.methods.relistItem(NFTdeployedAddress, itemID, newPriceInWei).send({ from: ethereum.selectedAddress });
    }
}

function listNFT(id) {

    window.alert("inside listNFT")

    let tokenID = id;
    //window.alert("tokenid=" + tokenID)
    var web3 = new Web3(window.ethereum);

    //window.alert("step 1")

    let NFTdeployedAddress = document.getElementById("NFTdeployedAddress").textContent;
    let MarketplaceDeployedAddress = document.getElementById("MarketplaceDeployedAddress").textContent;

    //window.alert("step 2")

    let quantity_ID = 'quantity-val-' + tokenID;
    let price_ID = 'price-val-' + tokenID;
    let itemID_ID = 'itemID-val-' + tokenID;
    let charityAddress_ID = 'charityAddress-val-' + tokenID;

    //code was cut out for figure purposes

    if (itemID == 0) {
        window.alert("inside if statement for itemID == 0")
        window.alert("tokenID=" + tokenID);
        marketplace.methods.listItemsForSale(NFTdeployedAddress, charityAddress, tokenID, quantity, priceInWei).send({ from: ethereum.selectedAddress });
    } else {
        //window.alert("Relist Items")
        let newPrice_ID = 'new-price-' + tokenID;
        let newPrice = document.getElementById(newPrice_ID).value;
        var newPriceInWei = web3.utils.toWei(newPrice.toString(), 'ether');
        window.alert("newprice=" + newPrice);
        marketplace.methods.relistItem(NFTdeployedAddress, itemID, newPriceInWei).send({ from: ethereum.selectedAddress });
    }
}