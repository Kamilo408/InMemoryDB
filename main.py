class InMemoryDB:
    def __init__(self):
        self.main_state = {}
        self.transaction_state = None
        self.in_transaction = False

    def get(self, key):
        value = None
        if self.in_transaction and key in self.transaction_state:
            value = self.transaction_state.get(key)
        else:
            value = self.main_state.get(key)
        print(f"Get('{key}') => {value}")
        return value

    def put(self, key, value):
        if self.in_transaction:
            self.transaction_state[key] = value
            print(f"Put('{key}', {value}) within transaction")
        else:
            print("Error: No transaction in progress for 'put' operation")
           

    def begin_transaction(self):
        if not self.in_transaction:
            self.in_transaction = True
            self.transaction_state = {}
            print("Transaction started")
        else:
            print("Error: Transaction already in progress")
            

    def commit(self):
        if self.in_transaction:
            self.main_state.update(self.transaction_state)
            self.transaction_state = None
            self.in_transaction = False
            print("Transaction committed")
        else:
            print("Error: No transaction in progress to commit")
            

    def rollback(self):
        if self.in_transaction:
            self.transaction_state = None
            self.in_transaction = False
            print("Transaction rolled back")
        else:
            print("Error: No transaction in progress to rollback")
            

def main():
    db = InMemoryDB()

    # should return None, because A doesn’t exist in the DB yet
    db.get("A")

    # should throw an error because a transaction is not in progress
    db.put("A", 5)

    # starts a new transaction
    db.begin_transaction()

    # set’s value of A to 5, but it's not committed yet
    db.put("A", 5)

    # should return None, because updates to A are not committed yet
    db.get("A")

    # update A’s value to 6 within the transaction
    db.put("A", 6)

    # commits the open transaction
    db.commit()

    # should return 6, that was the last value of A to be committed
    db.get("A")

    # should throw an error, because there is no open transaction
    db.commit()

    # should throw an error because there is no ongoing transaction
    db.rollback()

    # should return None because B does not exist in the database
    db.get("B")

    # starts a new transaction
    db.begin_transaction()

    # Set key B’s value to 10 within the transaction
    db.put("B", 10)

    # Rollback the transaction - revert any changes made to B
    db.rollback()

    # Should return None because changes to B were rolled back
    db.get("B")

if __name__ == "__main__":
    main()
