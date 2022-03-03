const initialize = () => {
    const onboardButton = document.getElementById('connectButton');

    const returnAccountAddress = document.getElementById('returnAccountAddress');
    const returnAccountBalance = document.getElementById('returnAccountBalance');
    const onboareturnChainIDrdButton = document.getElementById('returnChainID');


    const isMetaMaskInstalled = () => {
        const { ethereum } = window;
        return Boolean(ethereum && ethereum.isMetaMask);
    };

    const onClickConnect = async() => {

        try {
            ethereum.request({ method: 'eth_requestAccounts' });

            window.onload = function MetaMaskClientCheck() {
                returnAccountAddress.innerHTML = "Signed In As: " + ethereum.selectedAddress;
                //console.log("returnAccountAddress.innerHTML is", returnAccountAddress.innerHTML)
            };

            returnAccountAddress.value = ethereum.selectedAddress;
            //window.ethereum.enable();
            //window.alert("the account address is " + ethereum.selectedAddress)
            //const web3 = new Web3(window.web3.currentProvider);

            //var web3 = new web3(window.ethereum);



            // await web3.eth.getBalance(ethereum.selectedAddress).then(function(result) {
            //     let accountBalance = Web3.utils.fromWei(result, "ether")

            //     returnAccountBalance.value = accountBalance;
            // });

        } catch (error) {
            window.alert("this error is from connectMM" + error)
        };

    };

    const MetaMaskClientCheck = () => {
        if (!isMetaMaskInstalled()) {
            window.alert('Please Install MetaMask');
        } else {
            onboardButton.innerText = 'Connect to MetaMask';
            onboardButton.onclick = onClickConnect;
        };
    };

    MetaMaskClientCheck()

};
window.addEventListener('DOMContentLoaded', initialize);