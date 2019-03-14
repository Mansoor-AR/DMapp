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

async function testBlockchain() {
  try {

    // Get Minimum Gas Price from blockchain
    const minGasPrice = await zilliqa.blockchain.getMinimumGasPrice();
    const myGasPrice = units.toQa('1000', units.Units.Li); // Gas Price that will be used by all transactions
    //console.log('Sufficient Gas Price?');
    //console.log(myGasPrice.gte(new BN(minGasPrice.result))); // Checks if your gas price is less than the minimum gas price
    const tx = await zilliqa.blockchain.createTransaction(
        zilliqa.transactions.new({
          version: VERSION,
          toAddr: recipientPubKey,
          amount: new BN(units.toQa("1", units.Units.Zil)), // Sending an amount in Zil (1) and converting the amount to Qa
          gasPrice: myGasPrice, // Minimum gasPrice veries. Check the `GetMinimumGasPrice` on the blockchain
          gasLimit: Long.fromNumber(1)
        })
      );

    
  } catch (err) {
      console.log("Something went wrong with Kaya")
    console.log(err);
  }
}

testBlockchain();
