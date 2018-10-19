from hashlib import sha256
import json
import time

from flask import Flask, request
import requests


# All the transactions are packaged in blocks and their information are hashed
# the blocks are chained with their hash, that is the reason that we are using
# it in the __init__ method as a parameter
class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0

    def compute_hash(self):
        """
        This function returns the hash of the block contents
        :return:
        """
        # dumps allows us to serialize obj to a JSON formatted str
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


class BlockChain:
    # difficulty of our PoW algorithm
    difficulty = 2

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        A function to generate genesis block and appends it to the chain.
        The block has index 0, previous_hash as 0, and a valid hash
        :return:
        """
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)
