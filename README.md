# Hatch

I performed an automated security review of Hatch using Slither, a Solidity static analysis framework written in Python 3 (Trail of Bits); and created unit tests to run in Brownie, a Python-based testing framework (Pytest), to verify that the smart contract functionalities work as expected (Brownie).
Testing focused on smart contracts in the Visual Studio Code repository:
1) Nft.sol: Mints an ERC-1155 token to a user’s wallet, and sets approval for MarketPlace.sol to list NFTs.
2) MarketPlace.sol: Initializes marketplace variables and enables a user to list and purchase NFTs.

I identified the following priorities for review: 1) Identify and remediate Smart Contracts’ security vulnerabilities; and 2) Verify that the behavior of the Smart Contracts was consistent with specifications.

Results are covered in the slither folder.
