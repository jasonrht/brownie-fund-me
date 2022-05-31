from brownie import FundMe, network
from scripts.help_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
import pytest

def fund():
    fundme = FundMe[-1]
    account = get_account()
    entrance_fee = fundme.getEntranceFee()
    print(entrance_fee)
    print(f'The current entry fee is {entrance_fee}')
    print('Funding')
    fundme.fund({'from':account, 'value':entrance_fee})

def withdraw():
    fundme = FundMe[-1]
    account = get_account()
    fundme.withdraw({'from': account})

def main():
    fund()
    withdraw()

