from concurrent.futures import ProcessPoolExecutor
from django.forms import NullBooleanField
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse

from .models import Organization

import asyncio
import multiprocessing as mp

from .utils import *

import ipfshttpclient

from time import sleep

import ast

ipfsClient = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')

# Create your views here.
userMetaMaskAddress = "0x00"
userAccountBalance = 0
chainID = 0


def index(request):
    return render(request, "marketApp/main.html")


def createNFT(request):

    organizationRend = Organization.objects.filter(
        active='Y').order_by('organizationName')
    context = {}

    if request.method == "POST":
        if request.POST.get("upload-btn"):

            print("inside POST button")
            image = request.FILES['image']
            name = request.POST['name']
            description = request.POST['description']
            quantity = int(request.POST['quantity'])
            price = request.POST['price']
            organization = request.POST.getlist("organization")[0]

            charityAddress = Organization.objects.values_list(
                'metaAddress', flat=True).get(organizationName=organization)

            try:
                imageURL, tokenURL, data = asyncio.run(
                    runUploadImage(image, name, description))
            except KeyboardInterrupt:
                print("Error Message: Keyboard Interrupt")

            print("NFTdeployedAddress from views.py=", NFTdeployedAddress)
            context = {
                "organizations": organizationRend,
                "imageURL": imageURL,
                "tokenURL": tokenURL,
                "name": name,
                "description": description,
                "itemID": 0,
                "tokenID": 0,
                "quantity": quantity,
                "price": price,
                "charityAddress": charityAddress,
                "message": "You have uploaded your NFT",
                "NFTdeployedAddress": NFTdeployedAddress,
                "MarketplaceDeployedAddress": MarketplaceDeployedAddress
            }
        if request.POST.get("mint-nft-btn"):
            print("back to views")
            sleep(20)
            tokenID = getCurrentTokenID()
            print("tokenID=", tokenID)

            imageURL = request.POST['imageURL']
            name = request.POST['name']
            description = request.POST['description']
            quantity = int(request.POST['quantity'])
            price = request.POST['price']
            charityAddress = request.POST['charityAddress']

            context = {
                "organizations": organizationRend,
                "imageURL": imageURL,
                "name": name,
                "description": description,
                "itemID": 0,
                "tokenID": tokenID,
                "quantity": quantity,
                "price": price,
                "charityAddress": charityAddress,
                "message": "You have successfully minted your NFT",
                "NFTdeployedAddress": NFTdeployedAddress,
                "MarketplaceDeployedAddress": MarketplaceDeployedAddress
            }
        if request.POST.get("list-btn"):
            context = {
                "organizations": organizationRend,
                "message": "You have listed your NFT!",
            }
        return render(request, "marketApp/createNFT.html", context)

    else:
        organizations = Organization.objects.filter(active='Y')
        return render(request, "marketApp/createNFT.html", {
            "organizations": organizations
        })


async def runUploadImage(image, name, description):
    MAX_WORKER = 5
    with ProcessPoolExecutor(max_workers=MAX_WORKER) as pool:
        loop = asyncio.get_running_loop()

        imageURL, tokenURL, data = await loop.run_in_executor(None, uploadImage, image, name, description)

        #debugging statements
        print("upload image; imageURL=", imageURL) 
        print("upload image; tokenURL=", tokenURL)
        print("upload image; data=", data)

        return imageURL, tokenURL, data


def uploadImage(image, name, description):
    res = ipfsClient.add(image)
    hashKey = res["Hash"]
    imageURL = "https://ipfs.infura.io/ipfs/" + hashKey

    data = json.dumps({"name": name, "description": description, "image": imageURL})

    res = ipfsClient.add_json(data)
    tokenURL = "https://ipfs.infura.io/ipfs/" + res
    return imageURL, tokenURL, data


def connect(request):
    if request.method == "POST":
        print("here in post connect")
        global userMetaMaskAddress
        global userAccountBalance
        global chainID
        print("address: " + userMetaMaskAddress)

        if len(request.POST["userMetaMaskAddress"]) > 10:
            print("here inside if statement")
            userMetaMaskAddress = web3.toChecksumAddress(
                request.POST["userMetaMaskAddress"])
            # account balance
            # chain ID
            print("after", userMetaMaskAddress)

        organizations = Organization.objects.filter(
            active='Y').order_by('organizationName')

    return render(request, "marketApp/main.html", {
        "login": userMetaMaskAddress,
    })


def mynft(request):
    print("here in mynft function")
    print("userMetaMaskAddress=", userMetaMaskAddress)
    if request.method == "POST":
        print("In views.py mft")
        itemID = request.POST["purchasedItemID"]
        print("itemID=", itemID)
    try:
        nfts = asyncio.run(runGetMyNFT())
    except KeyboardInterrupt:
        print('Keyboard Interrupt')

    userAccountBalance = getAccountBalance(userMetaMaskAddress)
    chainID = getChainID()
    print("userAccountBalance=", userAccountBalance)
    print("chainID=", chainID)

    context = {
        "nfts": nfts,
        "userMetaMaskAddress": userMetaMaskAddress,
        "userAccountBalance": userAccountBalance,
        "chainID": chainID,
        "NFTdeployedAddress": NFTdeployedAddress,
        "MarketplaceDeployedAddress": MarketplaceDeployedAddress
    }

    return render(request, "marketApp/mynft.html", context)


async def runGetMyNFT():
    print("inside runGetMyNFT")
    MAX_WORKER = 5
    with ProcessPoolExecutor(max_workers=MAX_WORKER) as pool:
        loop = asyncio.get_running_loop()
        print("inside loop")

        data = await loop.run_in_executor(None, downloadMyNFT)
        nfts = await loop.run_in_executor(None, getMyNFT, data)

        print("nfts from runGetMyNFT=", nfts)
        return nfts


def downloadMyNFT():
    data = getItemsOwned(userMetaMaskAddress)
    print("data=", data)
    return data


def getMyNFT(data):
    nfts = []

    print("here in getMyNFT function")

    if len(data) > 0:
        for item in data:
            tokenURI = getTokenURI(item[1])
            print("printing from updated code")
            print("tokenURI=", tokenURI)
            print("tokenURI length=", len(tokenURI))
            print("tokenURI [28]=", tokenURI[28])
            print("tokenURI [29]=", tokenURI[29])
            # print("tokenURI last 2nd to last=", tokenURI[len(tokenURI)-1])
            res = ipfsClient.get_json(tokenURI[28:])
            #res = ipfsClient.get_json(tokenURI[29:len(tokenURI)-1])
            print("res=", res)

            print("res=", res)

            res2 = ast.literal_eval(res)

            price = item[7]/10**18

            nfts.append({"nftAddress": item[0], "tokenID": item[1], "itemID": item[2], "creatorAddress": item[3], "sellerAddress": item[4], "ownerAddress": item[5],
                        "organizationAddress": item[6], "price": price, "isListed": item[8], "quantity": 1, "image": res2["image"], "name": res2["name"], "description": res2["description"]})
    print("nfts=", nfts)
    return nfts


def nfts(request, category='None'):

    userAccountBalance = getAccountBalance(userMetaMaskAddress)
    chainID = getChainID()

    data = getListedItems()

    nfts = []

    if len(data) > 0:
        for item in data:
            tokenURI = getTokenURI(item[1])
            res = ipfsClient.get_json(tokenURI[28:])
            #res = ipfsClient.get_json(tokenURI[29:len(tokenURI)-1])
            print("res=", res)

            res2 = ast.literal_eval(res)

            creatorSplice = item[3]
            print("creatorpslice=" + creatorSplice)
            creatorSplice = creatorSplice[0:7] + "..." + creatorSplice[37:]
            print("creatorpslice2=" + creatorSplice)

            price = item[7]/10**18
            print("price of nft in views is ", price)

            nfts.append({"nftAddress": item[0], "tokenID": item[1], "itemID": item[2], "creatorAddress": item[3], "sellerAddress": item[4], "ownerAddress": item[5],
                        "organizationAddress": item[6], "price": price, "isListed": item[8], "image": res2["image"], "name": res2["name"], "description": res2["description"], "creatorSplice": creatorSplice})

    addressSplice = MarketplaceDeployedAddress[0:7] + "..." + MarketplaceDeployedAddress[37:]

    context = {
        "nfts": nfts,
        "NFTdeployedAddress": NFTdeployedAddress,
        "MarketplaceDeployedAddress": MarketplaceDeployedAddress,
        "userMetaMaskAddress": userMetaMaskAddress,
        "chainID": chainID,
        "addressSplice": addressSplice,
    }

    return render(request, "marketApp/nfts.html", context)

def list_market(request, id=0):
    userAccountBalance =  getAccountBalance(userMetaMaskAddress)
    chainID = getChainID()

    msg = ""
    if request.method == "POST":
        if request.POST.get("list-btn"):
            msg = "NFT has been listed!"
        if request.POST.get("delist-btn"):
            msg = "NFT was de-listed!"

    try:
        nfts = asyncio.run(runGetMyNFT())
    except KeyboardInterrupt:
        print("Keyboard interrupt")
    
    context = {
        "nfts": nfts,
        "message": msg,
        "NFTdeployedAddress": NFTdeployedAddress,
        "MarketplaceDeployedAddress": MarketplaceDeployedAddress,
        "userMetaMaskAddress": userMetaMaskAddress,
        "chainID": chainID,
    }
    return render(request, "marketApp/mynft.html", context)

# userMetaMaskAddress
# userAccountBalance
# chainID
# organizations
