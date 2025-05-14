"""
Tests for the Sui Embedded Wallet Library.

These tests verify key functionality:
- Deriving keys from a known mnemonic
- Matching expected addresses and private keys
"""

import unittest
from main import Suiwallet


class TestSuiWallet(unittest.TestCase):
    """Test suite for the Suiwallet class."""

    # Known test values
    TEST_MNEMONIC = "border tiger theory iron early girl solid balance host pitch yard naive"
    EXPECTED_ADDRESS = "0x0c0672024dabb73c864939acb971ac159fa14699cf4f12f9cd938f3c634d59df"
    EXPECTED_PK = "suiprivkey1qyavhj8evj29wqhjlfdz2uyf05vu4x5gnclkch35rm0j7hpkqjaqv0tlqrk"

    def setUp(self):
        """Set up test fixtures before each test."""
        self.wallet = Suiwallet(mnemonic=self.TEST_MNEMONIC)

    def test_derive_from_mnemonic(self):
        """Test deriving keys from a known mnemonic produces expected results."""
        # Test deriving both address and pk
        derived_address, derived_pk = self.wallet.derive_keys_from_mnemonic()
        
        self.assertEqual(
            derived_address, 
            self.EXPECTED_ADDRESS, 
            "Derived address should match expected"
        )
        self.assertEqual(
            derived_pk, 
            self.EXPECTED_PK, 
            "Derived private key should match expected"
        )

        # Test deriving address only
        derived_address_only = self.wallet.derive_address_from_mnemonic()
        self.assertEqual(
            derived_address_only, 
            self.EXPECTED_ADDRESS, 
            "Derived address (only) should match expected"
        )

        # Test deriving pk only
        derived_pk_only = self.wallet.derive_pk_from_mnemonic()
        self.assertEqual(
            derived_pk_only, 
            self.EXPECTED_PK, 
            "Derived private key (only) should match expected"
        )

    def test_derive_pk_from_mnemonic(self):
        """Test deriving pk from mnemonic produces expected results."""
        derived_pk_only = self.wallet.derive_pk_from_mnemonic()
        self.assertEqual(
            derived_pk_only, 
            self.EXPECTED_PK, 
            "Derived private key (only) should match expected"
        )

    def test_generate_new_wallet(self):
        """Test generating a new wallet creates a valid wallet instance."""
        # Note: generate_new_wallet is a classmethod, so it's called on the class, not instance
        new_wallet = Suiwallet.generate_new_wallet()
        self.assertIsNotNone(new_wallet.mnemonic, "New wallet should have a mnemonic")
        self.assertTrue(len(new_wallet.mnemonic.split()) >= 12, "Mnemonic should have at least 12 words")
        
        # Check if address and pk can be derived (basic sanity check)
        # This also implicitly checks if the SuiConfig was initialized correctly within generate_new_wallet
        try:
            address, pk = new_wallet.derive_keys_from_mnemonic()
            self.assertIsNotNone(address, "Derived address from new wallet should not be None")
            self.assertTrue(address.startswith("0x"), "Derived address should start with 0x")
            self.assertIsNotNone(pk, "Derived PK from new wallet should not be None")
            self.assertTrue(pk.startswith("suiprivkey"), "Derived PK should start with suiprivkey")
        except Exception as e:
            self.fail(f"Key derivation from generated wallet failed: {e}")


if __name__ == '__main__':
    unittest.main() 