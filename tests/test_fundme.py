from brownie import FundMe, accounts, network, exceptions

from scripts.help_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fundme

import pytest

def test_can_fund_withdraw():
    account = get_account()
    fundme = deploy_fundme()
    entrance_fee = fundme.getEntranceFee()
    txn = fundme.fund({'from': account, 'value': entrance_fee})
    txn.wait(1)
    assert fundme.addressToAmountFunded(account.address) == entrance_fee
    txn2 = fundme.withdraw({'from': account})
    txn2.wait(1)
    assert fundme.addressToAmountFunded(account.address) == 0

def test_only_owner_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip('only for local testing')
    fundme = deploy_fundme()
    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fundme.withdraw({'from': bad_actor})
        
