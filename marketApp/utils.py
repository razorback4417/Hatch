import asyncio
from web3 import Web3

from solcx import compile_standard, install_solc
import json

from django.conf import settings

provider = settings.PROVIDER
web3 = Web3(Web3.HTTPProvider(provider))
chain_id = settings.CHAIN_ID

my_address = settings.MY_PUBLIC_KEY
private_key = settings.MY_PRIVATE_KEY
nounce = web3.eth.getTransactionCount(my_address)

NFTdeployedAddress = settings.NFT_DEPLOYED_ADDRESS

MarketplaceDeployedAddress = settings.MARKETPLACE_DEPLOYED_ADDRESS

#compiling the nft.sol contract to extract bytecode and abi

with open(
    #"marketApp\\contracts\\nft.sol",
    "marketApp/contracts/nft.sol",

    "r"
) as file:
    nft_file = file.read()

install_solc("0.8.3")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"nft.sol": {"content": nft_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.3",
    allow_paths=[".",
                 "./marketApp/contracts/openzeppelin-contracts/contracts/token/ERC1155",
                 "./marketApp/contracts/openzeppelin-contracts/contracts/access",
                 "./marketApp/contracts/openzeppelin-contracts/contracts/utils"
                 ],
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

NFT_Bytecode = compiled_sol["contracts"]["nft.sol"]["nft"]["evm"]["bytecode"]["object"]

NFT_ABI = compiled_sol["contracts"]["nft.sol"]["nft"]["abi"]

#compiling the marketplace.sol contract to extract bytecode and abi
with open(
    "marketApp/contracts/marketplace.sol",
    "r",
) as file:
    marketplace_file = file.read()

install_solc("0.8.3")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"marketplace.sol": {"content": marketplace_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.3",
    allow_paths=[".",
                 "./marketApp/contracts/openzeppelin-contracts/contracts/token/ERC1155",
                 "./marketApp/contracts/openzeppelin-contracts/contracts/token/ERC1155/utils",
                 "./marketApp/contracts/openzeppelin-contracts/contracts/access",
                 "./marketApp/contracts/openzeppelin-contracts/contracts/security",
                 "./marketApp/contracts/openzeppelin-contracts/contracts/utils"
                 ],
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

Marketplace_Bytecode = compiled_sol["contracts"]["marketplace.sol"]["marketplace"]["evm"]["bytecode"]["object"]

Marketplace_ABI = compiled_sol["contracts"]["marketplace.sol"]["marketplace"]["abi"]

def getChainID():
    chainID = web3.eth.chain_id
    return chainID

def getAccountBalance(userAddress):
    num = web3.eth.get_balance(userAddress)
    accountBalance = round(web3.fromWei(num, 'ether'), 2)

def getItemsOwned(ownerAddress):
    marketplace_contract = web3.eth.contract(abi=Marketplace_ABI, address=MarketplaceDeployedAddress)
    itemsOwned = marketplace_contract.functions.getItemsOwned(ownerAddress).call()
    return itemsOwned

def getCurrentTokenID():
    nft_contract = web3.eth.contract(abi=NFT_ABI, address=NFTdeployedAddress)
    tokenID = nft_contract.functions.getCurrentTokenID().call()
    return tokenID

def getTokenURI(tokenID):
    nft_contract = web3.eth.contract(abi=NFT_ABI, address=NFTdeployedAddress)
    tokenURI = nft_contract.functions.getTokenURI(tokenID).call()
    return tokenURI

def getListedItems():
    marketplace_contract = web3.eth.contract(abi=Marketplace_ABI, address=MarketplaceDeployedAddress)
    listedItems =  marketplace_contract.functions.getListedItems().call()
    return listedItems