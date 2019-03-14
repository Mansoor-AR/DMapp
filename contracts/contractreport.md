## Sūrya's Description Report

### Files Description Table


|  File Name  |  SHA-1 Hash  |
|-------------|--------------|
| RouteIntgrity.sol | 6b9c37e199baa323f36f4946eb7e3de736b4352e |


### Contracts Description Table


|  Contract  |         Type        |       Bases      |                  |                 |
|:----------:|:-------------------:|:----------------:|:----------------:|:---------------:|
|     └      |  **Function Name**  |  **Visibility**  |  **Mutability**  |  **Modifiers**  |
||||||
| **GenesisContract** | Implementation |  |||
| └ | \<Constructor\> | Public ❗️ |  💵 | |
| └ | addSecondaryManager | Public ❗️ | 🛑  | onlyGlobalAdmin |
| └ | isSecondaryManager | Public ❗️ |   |NO❗️ |
||||||
| **RouteIntegrity** | Implementation |  |||
| └ | \<Constructor\> | Public ❗️ |  💵 | |
| └ | registerGenesis | Public ❗️ | 🛑  | onlyGlobalAdmin |
| └ | addHash | Public ❗️ | 🛑  |NO❗️ |
| └ | getHash | Public ❗️ |   |NO❗️ |


### Legend

|  Symbol  |  Meaning  |
|:--------:|-----------|
|    🛑    | Function can modify state |
|    💵    | Function is payable |
