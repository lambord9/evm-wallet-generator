import pandas as pd
from eth_account import Account
from bip_utils import Bip44, Bip44Coins, Bip44Changes, Bip39MnemonicGenerator, Bip39SeedGenerator

def generate_evm_wallets(num):
    evm_wallets = []
    for i in range (num):
        mnemonic_generator = Bip39MnemonicGenerator()
        mnemonic = mnemonic_generator.FromWordsNumber(12)
        seed = Bip39SeedGenerator(mnemonic).Generate()
        bip_object = Bip44.FromSeed(seed, Bip44Coins.ETHEREUM)
        private_key = bip_object.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0).PrivateKey().Raw().ToBytes()
        account = Account.from_key(private_key)

        evm_wallets.append({
            'address': account.address,
            'private_key': private_key.hex(),
            'mnemonic': mnemonic.ToStr()
        })

    return evm_wallets

def save_to_file(wallets, file_name):
    df = pd.DataFrame(wallets, columns=[
        'address', 
        'private_key', 
        'mnemonic'
        ])
    df.to_csv(file_name, index=False)

if __name__ == '__main__':
    count = int(input('How many wallets should I generate?\n'))
    wallets = generate_evm_wallets(count)
    save_to_file(wallets, 'wallets.csv')
    print(f"\n>>> {count} wallets have been generated. Saved to wallets.csv")