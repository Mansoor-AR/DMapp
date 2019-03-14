const { Transaction } = require('./node_modules/@zilliqa-js/account');
const { BN, Long, bytes, units } = require('./node_modules/@zilliqa-js/util');
const { Zilliqa } = require('./node_modules/@zilliqa-js/zilliqa');
const CP = require ('./node_modules/@zilliqa-js/crypto');

//const zilliqa = new Zilliqa('https://dev-api.zilliqa.com/');
const zilliqa = new Zilliqa('http://127.0.0.1:4200');
// These are set by the core protocol, and may vary per-chain.
// These numbers are JUST AN EXAMPLE. They will NOT WORK on the developer testnet
// or mainnet.
// For more information: https://apidocs.zilliqa.com/?shell#getnetworkid
const CHAIN_ID = 2;//333 for devnet; 2 for kaya
const MSG_VERSION = 1;
const VERSION = bytes.pack(CHAIN_ID, MSG_VERSION);

// Populate the wallet with an account
const privkey = '0145055f8484bb66683ddb30b4915e70f63e9d8ef4ce0e1807b5c680084c5c0f';
const recipientPubKey = 'e780f1f2e9890f42f2519a00edefd562c4653ff8';
zilliqa.wallet.addByPrivateKey(
  privkey
);

const address = CP.getAddressFromPrivateKey(privkey);
console.log("Sender account address is:%");
console.log(`0x${address}%`);
console.log("Receiver account address is:%");
console.log(`0x${recipientPubKey}%`);

async function testBlockchain() {
  try {

    // Get Balance
    const balance = await zilliqa.blockchain.getBalance(address);
    const rbal = await zilliqa.blockchain.getBalance(recipientPubKey)
    // Get Minimum Gas Price from blockchain
    const minGasPrice = await zilliqa.blockchain.getMinimumGasPrice();
    console.log(`Sender account balance is:%`);
    console.log(balance.result);
    console.log(`%Receiver balance is:%`);
    console.log(rbal.result)
    
  } catch (err) {
      console.log("Something went wrong with Kaya")
    console.log(err);
  }
}

testBlockchain();
