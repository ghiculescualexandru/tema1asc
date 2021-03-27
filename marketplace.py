"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Lock

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.queues = {}
        self.carts = {}
        self.producers_no = 0
        self.carts_no = 0
        self.marketplace_lock = Lock()
        self.producer_lock = Lock()
        self.cart_lock = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """

        # Using the lock so not multiple producers get the same id.
        self.producer_lock.acquire()
        try:
            producer_id = self.producers_no
            self.queues[producer_id] = []
            self.producers_no += 1
        finally:
            self.producer_lock.release()

        # print("Registered producer: <{}>".format(producer_id))

        return producer_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        if len(self.queues[producer_id]) >= self.queue_size_per_producer:
            return False

        # print("Published {} to {}".format(product, producer_id))

        self.queues[producer_id].append(product)
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """


        # Using the lock so not multiple consumers get the same cart id.
        self.cart_lock.acquire()
        try:
            cart_id = self.carts_no
            self.carts[cart_id] = []
            self.carts_no += 1
        finally:
            self.cart_lock.release()

        # print("Added new cart with id <{}>".format(cart_id))
        return cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        self.marketplace_lock.acquire()
        for producer, products in self.queues.items():
            for prod in products:
                # # print("p:" + str(p))
                # # print("product:" + str(product))
                # # print("products: " + str(products))
                if prod.name == product.name:
                    self.queues[producer].remove(prod)
                    self.carts[cart_id].append((prod, producer))

                    # print(self.carts[cart_id])
                    self.marketplace_lock.release()
                    return True

        self.marketplace_lock.release()
        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """

        cart = self.carts[cart_id]

        self.marketplace_lock.acquire()
        for i in range(0, len(cart)):
            cart_product = cart[i][0]
            producer = cart[i][1]

            if cart_product.name == product.name:
                self.queues[producer].append(product)
                self.carts[cart_id].pop(i)
                break

        self.marketplace_lock.release()

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        items = []
        for item in self.carts[cart_id]:
            items.append(item)

        return items
