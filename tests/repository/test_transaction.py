import time


class TestTransactions:
    def test_transaction_rollback_as_default_behavior(self, transaction, package):
        with transaction as change:
            change.packages.insert(package)
            assert package in change.packages

        with transaction as change:
            assert package not in change.packages

    def test_transaction_commit_persists_changes(self, transaction, package):
        with transaction:
            transaction.packages.insert(package)
            assert package in transaction.packages
            transaction.commit()

        with transaction:
            assert package in transaction.packages

    def test_transaction_rollback_reverts_changes(self, transaction, package):
        with transaction:
            transaction.packages.insert(package)
            assert package in transaction.packages
            transaction.rollback()
            assert package not in transaction.packages

    def test_accessing_repository_on_transaction(self, transaction):
        assert transaction.packages is None
        with transaction:
            assert transaction.packages is not None
        assert transaction.packages is None

    def test_transaction_delete_rollback(self, transaction, package):
        uuid = package.uuid
        with transaction:
            transaction.packages.insert(package)
            transaction.commit()

        with transaction:
            assert package in transaction.packages
            transaction.packages.delete(package.uuid)
            # Unless we commit, the package should still be there - we're in a transaction
            assert package in transaction.packages

        with transaction:
            assert package in transaction.packages

    def test_transaction_delete_commit(self, transaction, package):
        with transaction:
            transaction.packages.insert(package)
            transaction.commit()

        with transaction:
            assert package in transaction.packages
            transaction.packages.delete(package.uuid)
            transaction.commit()

        with transaction:
            assert package not in transaction.packages