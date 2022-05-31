from brownie import FundMe, network, config, MockV3Aggregator
from scripts.help_scripts import deploy_mocks, get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS

def deploy_fundme():
    # account = accounts[0] # Ganache test-account
    # account = accounts.load('brownie-jason')
    # account = accounts.add(config['wallets']['from_key'])
    account = get_account()

    if(network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS):
        price_feed_address = config['networks'][network.show_active()]['eth_usd_price_feed']
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
    fundme = FundMe.deploy(
        price_feed_address,
        {'from': account},
        publish_source=config['networks'][network.show_active()].get('verify')) # Transactions ALWAYS need a "from_key" !!!
    print(f"Contract deployed to {fundme.address}")
    return fundme

def main():
    deploy_fundme()