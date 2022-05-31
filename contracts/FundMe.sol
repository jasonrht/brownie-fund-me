//SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract FundMe {
    using SafeMath for uint256;

    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;
    address public owner;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    function fund() public payable {
        // Set minimum donation value (0.50 USD)
        uint256 minUsd = getEntranceFee();
        require(
            getConversionRate(msg.value) >= minUsd,
            "Donation amount too low ..."
        ); // If statement condition, won't continue if requirement is NOT met.
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {
        // minimumUSD
        uint256 minUsd = 0.50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (minUsd) / price;
    }

    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000);
    }

    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        return (ethPrice * ethAmount) / 10000000000;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function withdraw() public payable onlyOwner {
        payable(msg.sender).transfer(address(this).balance);
        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        funders = new address[](0);
    }
}
