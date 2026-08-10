# Phase 2 Deployment Scripts

Deployment scripts for Sharia-compliant staking smart contracts.

## 📋 Scripts Overview

### 1. `deploy-phase2-staking.ts`

Deploys `PlatformRevenueOracle` and `CareStakingHalal` contracts.

**Usage:**

```bash
npx hardhat run scripts/deploy-phase2-staking.ts --network somniaTestnet
```

**Environment Variables:**

```bash
# Phase 1 contracts (required)
export CARE_TOKEN_ADDRESS="0x..."
export CARE_TOKEN_CONTROLLER_ADDRESS="0x..."

# Governance addresses
export ADMIN_ADDRESS="0x..."
export SHARIAH_BOARD_ADDRESS="0x..."

# Finance team (5 members for 3-of-5 multi-sig)
export FINANCE_TEAM_1="0x..."
export FINANCE_TEAM_2="0x..."
export FINANCE_TEAM_3="0x..."
export FINANCE_TEAM_4="0x..."
export FINANCE_TEAM_5="0x..."

# Auditors (at least 1)
export AUDITOR_1="0x..."
```

**Output:**

```bash
📋 Contract Addresses:
   PlatformRevenueOracle: 0x1234567890123456789012345678901234567890
   CareStakingHalal: 0xabcdefabcdefabcdefabcdefabcdefabcdefabcd

💾 Deployment info saved to: deployments/phase2-staking-somniaTestnet-1234567890.json
```

---

### 2. `fund-staking-contract.ts`

Transfers 150M CARE tokens to the staking contract.

**Usage:**

```bash
# Set staking contract address
export CARE_STAKING_HALAL_ADDRESS="0x..."

# Run funding script
npx hardhat run scripts/fund-staking-contract.ts --network somniaTestnet
```

**Features:**

- Auto-loads addresses from latest deployment file
- Checks current balance before transferring
- Mints from controller if deployer lacks funds
- Verifies final balance

**Output:**

```bash
💵 Final staking contract balance: 150000000.0 CARE
✅ Staking contract fully funded!
```

---

## 🚀 Complete Deployment Workflow

### Prerequisites

1. **Phase 1 Contracts Deployed:**
   - CareToken
   - CareTokenController
   - CareTeamVesting
   - CarePartnerVesting
   - CareLiquidityLock

2. **Wallet Setup:**
   - Deployer wallet with ETH for gas
   - 5 finance team wallet addresses
   - 1+ auditor wallet addresses
   - Admin wallet address
   - Shariah board wallet address

3. **Network Configuration:**

   ```typescript
   // hardhat.config.ts
   networks: {
     somniaTestnet: {
       url: "https://testnet-rpc.somnia.network",
       accounts: [process.env.PRIVATE_KEY],
       chainId: 50311
     },
     somniaMainnet: {
       url: "https://rpc.somnia.network",
       accounts: [process.env.PRIVATE_KEY],
       chainId: 50312
     }
   }
   ```

---

### Step-by-Step Deployment

#### Step 1: Set Environment Variables

Create `.env` file in `blockchain/` directory:

```bash
# Network
SOMNIA_RPC_URL=https://testnet-rpc.somnia.network
PRIVATE_KEY=0x...

# Phase 1 Contracts
CARE_TOKEN_ADDRESS=0x1111111111111111111111111111111111111111
CARE_TOKEN_CONTROLLER_ADDRESS=0x2222222222222222222222222222222222222222

# Governance
ADMIN_ADDRESS=0x3333333333333333333333333333333333333333
SHARIAH_BOARD_ADDRESS=0x4444444444444444444444444444444444444444

# Finance Team (5 members)
FINANCE_TEAM_1=0x5555555555555555555555555555555555555555
FINANCE_TEAM_2=0x6666666666666666666666666666666666666666
FINANCE_TEAM_3=0x7777777777777777777777777777777777777777
FINANCE_TEAM_4=0x8888888888888888888888888888888888888888
FINANCE_TEAM_5=0x9999999999999999999999999999999999999999

# Auditors
AUDITOR_1=0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

#### Step 2: Deploy Contracts

```bash
cd blockchain

# Install dependencies
npm install

# Compile contracts
npx hardhat compile

# Deploy to testnet
npx hardhat run scripts/deploy-phase2-staking.ts --network somniaTestnet
```

**Expected Output:**

```bash
🚀 Starting Phase 2 Staking Deployment...

📝 Deployer address: 0x...
💰 Deployer balance: 1.5 ETH

📋 Configuration:
  CARE Token: 0x1111...
  CARE Controller: 0x2222...
  Admin: 0x3333...
  Shariah Board: 0x4444...
  Finance Team: 0x5555..., 0x6666..., 0x7777..., 0x8888..., 0x9999...
  Auditors: 0xaaaa...

🔍 Verifying Phase 1 contracts...
  ✅ CareToken found: CARE Token (CARE)
  ✅ CareTokenController found

📦 Deploying PlatformRevenueOracle...
  ✅ PlatformRevenueOracle deployed to: 0xabcd1234...
  📝 Deployment tx: 0xdef56789...

📦 Deploying CareStakingHalal...
  ✅ CareStakingHalal deployed to: 0x5678abcd...
  📝 Deployment tx: 0x9012efgh...

🔗 Updating PlatformRevenueOracle with CareStakingHalal address...
  ✅ Oracle updated with staking address
  📝 Update tx: 0xijkl3456...

🔐 Verifying role assignments...
  Oracle has REVENUE_ORACLE_ROLE: ✅
  Admin has DEFAULT_ADMIN_ROLE: ✅
  Shariah Board has SHARIAH_BOARD_ROLE: ✅

🔍 Verifying initial state...
  Current month: 202510 (YYYYMM format)
  Allocation: 150000000.0 CARE (150M expected)
  Wakala fee: 1000 bps (10%)
  Bronze tier: 1000.0 CARE min, 60% profit share
  Silver tier: 10000.0 CARE min, 70% profit share
  Gold tier: 50000.0 CARE min, 80% profit share
  Platinum tier: 100000.0 CARE min, 90% profit share

💾 Deployment info saved to: deployments/phase2-staking-somniaTestnet-1730073600000.json

✅ Phase 2 Staking Deployment Complete!

📋 Contract Addresses:
   PlatformRevenueOracle: 0xabcd1234...
   CareStakingHalal: 0x5678abcd...

🔜 Next Steps:
   1. Verify contracts on block explorer
   2. Transfer 150M CARE tokens to staking contract
   3. Set up backend revenue tracker service
   4. Configure CareWellness contract address (when deployed)
   5. Test staking flow end-to-end
   6. Set up multi-sig wallet for finance team
   7. Submit to Shariah Advisory Board for certification

📝 Environment Variables for Backend:
   PLATFORM_REVENUE_ORACLE_ADDRESS=0xabcd1234...
   CARE_STAKING_HALAL_ADDRESS=0x5678abcd...
```

#### Step 3: Fund Staking Contract

```bash
# Set staking address from deployment
export CARE_STAKING_HALAL_ADDRESS=0x5678abcd...

# Run funding script
npx hardhat run scripts/fund-staking-contract.ts --network somniaTestnet
```

**Expected Output:**

```bash
💰 Funding CareStakingHalal Contract...

📝 Deployer address: 0x...
💰 Deployer balance: 1.4 ETH

📋 Contract Addresses:
  CARE Token: 0x1111...
  CARE Controller: 0x2222...
  CARE Staking: 0x5678abcd...

📊 Required allocation: 150000000.0 CARE (150M)

💵 Current staking contract balance: 0.0 CARE
📤 Amount to transfer: 150000000.0 CARE

💰 Deployer CARE balance: 200000000.0 CARE

📤 Transferring CARE tokens to staking contract...
  ✅ Transfer successful
  📝 Transfer tx: 0xmnop7890...

💵 Final staking contract balance: 150000000.0 CARE
✅ Staking contract fully funded!

💾 Funding info saved to: deployments/staking-funding-somniaTestnet-1730073660000.json

🎉 Funding Complete!

🔜 Next Steps:
   1. Users can now stake CARE tokens
   2. Set up backend revenue tracker
   3. Submit first monthly profit report
```

#### Step 4: Verify Contracts (Optional)

```bash
# Install verification plugin
npm install --save-dev @nomicfoundation/hardhat-verify

# Verify PlatformRevenueOracle
npx hardhat verify --network somniaTestnet \
  0xabcd1234... \
  "0x5678abcd..." \
  "0x3333..." \
  "0x3333..." \
  '["0x5555...","0x6666...","0x7777...","0x8888...","0x9999..."]' \
  '["0xaaaa..."]'

# Verify CareStakingHalal
npx hardhat verify --network somniaTestnet \
  0x5678abcd... \
  "0x1111..." \
  "0x2222..." \
  "0xabcd1234..." \
  "0x4444..." \
  "0x3333..."
```

---

## 📂 Deployment Files

All deployments are saved to `deployments/` directory:

### phase2-staking-{network}-{timestamp}.json

```json
{
  "network": "somniaTestnet",
  "timestamp": "2025-10-28T01:00:00.000Z",
  "platformRevenueOracle": "0xabcd1234...",
  "careStakingHalal": "0x5678abcd...",
  "config": {
    "careToken": "0x1111...",
    "careTokenController": "0x2222...",
    "admin": "0x3333...",
    "shariahBoard": "0x4444...",
    "financeTeam": ["0x5555...", ...],
    "auditors": ["0xaaaa..."]
  },
  "transactions": {
    "oracleDeployTx": "0xdef56789...",
    "stakingDeployTx": "0x9012efgh...",
    "grantOracleRoleTx": "0xijkl3456..."
  }
}
```

### staking-funding-{network}-{timestamp}.json

```json
{
  "network": "somniaTestnet",
  "timestamp": "2025-10-28T01:01:00.000Z",
  "careStakingHalal": "0x5678abcd...",
  "amountTransferred": "150000000.0",
  "finalBalance": "150000000.0",
  "transactionHash": "0xmnop7890..."
}
```

---

## 🧪 Testing After Deployment

### Test Staking

```bash
# Create test script: scripts/test-staking.ts
npx hardhat run scripts/test-staking.ts --network somniaTestnet
```

```typescript
// Test script example
const careToken = await ethers.getContractAt("CareToken", CARE_TOKEN_ADDRESS);
const staking = await ethers.getContractAt("CareStakingHalal", STAKING_ADDRESS);

// Approve staking contract
await careToken.approve(STAKING_ADDRESS, ethers.parseEther("10000"));

// Stake 10K CARE in Silver tier
await staking.stake(ethers.parseEther("10000"), 1);

// Check stake
const stakes = await staking.getUserStakes(deployer.address);
console.log("User stakes:", stakes);
```

---

## 🚨 Troubleshooting

### Error: "CARE_TOKEN_ADDRESS not set"

**Solution:**

```bash
export CARE_TOKEN_ADDRESS="0x..."
export CARE_TOKEN_CONTROLLER_ADDRESS="0x..."
```

### Error: "Must have exactly 5 finance team members"

**Solution:**

```bash
export FINANCE_TEAM_1="0x..."
export FINANCE_TEAM_2="0x..."
export FINANCE_TEAM_3="0x..."
export FINANCE_TEAM_4="0x..."
export FINANCE_TEAM_5="0x..."
```

### Error: "Insufficient funds for gas"

**Solution:**

```bash
# Check deployer balance
npx hardhat run scripts/check-balance.ts --network somniaTestnet

# Send ETH to deployer address
```

---

## 📚 Related Documentation

- **Technical Specs:** `docs/PHASE_2_TECHNICAL_SPECIFICATIONS.md`
- **Oracle Spec:** `docs/PLATFORM_REVENUE_ORACLE_SPEC.md`
- **Sharia Design:** `docs/SHARIA_COMPLIANT_STAKING_DESIGN.md`
- **Backend Setup:** `docs/REVENUE_TRACKER_SETUP.md`

---

## 🔐 Security Notes

- ✅ All role assignments verified automatically
- ✅ Deployment info saved for audit trail
- ✅ Contracts pausable for emergency stops
- ✅ Multi-sig required for profit distribution
- ⚠️  Never commit private keys to git
- ⚠️  Always verify contracts on mainnet
- ⚠️  Test thoroughly on testnet first

---

**For support:** <dev@health-aicare.com>
