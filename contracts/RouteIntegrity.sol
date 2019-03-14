//
//Author: Mansoor Ahmed
//
pragma solidity ^0.5.5;
//The first contract, this will establish the admin accounts and other "God" functions
//Install truffle and run using Remix
contract GenesisContract {
    address GlobalAdmin;    //Only global admin can secondary managers
    mapping(address => bool) public SecondaryManagers;  //There may be multiple managers
    constructor() public payable {
        //Constructor; therefore, set the global admin here
        GlobalAdmin = msg.sender; 
    }

    //Modifiers are used to limit access to functions
    modifier onlyGlobalAdmin() {
        if (msg.sender != GlobalAdmin)
            revert();
        _; //The actual function will expand inline instead of the _;
    }

    modifier onlySecondaryManagers() {
        if (!SecondaryManagers[msg.sender]) //If sender is not a secondary admin
            revert();
        _;
    }

    function addSecondaryManager (address newSM) public onlyGlobalAdmin returns (bool success) {
        if (SecondaryManagers[newSM]) //if user already exists return false
            return false;
        SecondaryManagers[newSM] = true;
        return true;
    }

    function isSecondaryManager (address checkadd) public view returns (bool result) { 
        return SecondaryManagers[checkadd];
    }
}

contract RouteIntegrity {    
    GenesisContract gencon;
    address GenconAddress;
    address GlobalAdmin; 
    mapping(bytes32 => uint) public hashmap;
    constructor() public payable {
        GlobalAdmin = msg.sender;
    }
        //Modifiers are used to limit access to functions
    modifier onlyGlobalAdmin() {
        if (msg.sender != GlobalAdmin)
            revert();
        _; //The actual function will expand inline instead of the _;
    }
    function registerGenesis (address genAd) public onlyGlobalAdmin returns (bool) { //The address should be of the already deployed genesis
        GenconAddress = genAd;
        gencon = GenesisContract(GenconAddress);
        return true;
    }
    function addHash (bytes32 toadd) public returns (bool){
        if(!(gencon.isSecondaryManager(msg.sender)))
            return false;
        if(hashmap[toadd] != 0)
            return false; //Trying to add two times.
        hashmap[toadd] = block.timestamp;
        return true;
    }
    function getHash (bytes32 toget) public view returns (uint){
        return hashmap[toget];
    }
}
