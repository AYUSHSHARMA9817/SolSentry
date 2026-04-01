// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleCFG {

    mapping(address => uint) public balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint amount) public {
        if (balances[msg.sender] >= amount) {
            _transfer(msg.sender, amount);
            balances[msg.sender] -= amount;
        }
    }

    function _transfer(address to, uint amount) internal {
        payable(to).transfer(amount);
    }

    function process(uint x) pure public returns (uint) {
        uint result = 0;

        for (uint i = 0; i < x; i++) {
            if (i % 2 == 0) {
                result += computeA(i);
            } else {
                result += computeB(i);
            }
        }

        return result;
    }

    function computeA(uint a) internal pure returns (uint) {
        return a * 2;
    }

    function computeB(uint b) internal pure returns (uint) {
        return b + 1;
    }

    function bal() public{
        (bool suc,) = msg.sender.call{value: balances[msg.sender]}("");
        require(suc);
    }
}