async function delistNFT(id) {
    let tokenID = id
    var web3 = new Web3(window.ethereum)
        //window.alert("step 1")

    let NFTdeployedAddress = document.getElementById("NFTdeployedAddress").textContent;
    let MarketplaceDeployedAddress = document.getElementById("MarketplaceDeployedAddress").textContent;
    //window.alert("step 2")

    let itemID_ID = 'itemID-val-' + tokenID

    let itemID = document.getElementById(itemID_ID).textContent;

    itemID = parseInt(itemID);
    //window.alert("step 3")

    //window.alert("MarketplaceDeployedAddress=" + MarketplaceDeployedAddress)
    const marketplace = new web3.eth.Contract(MarketplaceABI, MarketplaceDeployedAddress);
    marketplace.setProvider(window.ethereum);
    //window.alert("step 4")

    let isListed_ID = 'isListed-input-value-' + tokenID;

    document.getElementById(isListed_ID).value = 'N';
    //window.alert("step 5")

    await marketplace.methods.delistItem(itemID).send({ from: ethereum.selectedAddress }).then(function(result) {
        console.log(result);
        //window.alert("Your transaction hash: " + result.transactionHash + "\n For more info, copy and paste it into Etherscan.")
    })
}