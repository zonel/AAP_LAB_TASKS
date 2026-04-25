# -*- coding: utf-8 -*-
"""Testy pytest dla klasy Product -- uzupelnij!

Uruchomienie: pytest test_product_pytest.py -v
"""

import pytest
from product import Product


# --- Fixture ---

@pytest.fixture
def product():
    """Tworzy instancje Product do testow (odpowiednik setUp)."""
    return Product("Laptop", 2999.99, 10)


# --- Testy z fixture ---

def test_is_available(product):
    """Sprawdz dostepnosc produktu."""
    assert product.is_available() == True


def test_is_not_available_when_empty():
    """Sprawdz, ze produkt z quantity=0 jest niedostepny."""
    empty = Product("Brak", 10.0, 0)
    assert empty.is_available() == False


def test_total_value(product):
    """Sprawdz wartosc calkowita."""
    assert product.total_value() == pytest.approx(2999.99 * 10)


# --- Testy z parametryzacja ---

@pytest.mark.parametrize("amount, expected_quantity", [
    (5, 15),    # dodanie 5 do poczatkowych 10 = 15
    (0, 10),    # dodanie 0 = bez zmian
    (100, 110), # dodanie 100
])
def test_add_stock_parametrized(product, amount, expected_quantity):
    """Testuje add_stock z roznymi wartosciami."""
    product.add_stock(amount)
    assert product.quantity == expected_quantity


# --- Testy bledow ---

def test_remove_stock_too_much_raises(product):
    """Sprawdz, czy proba usuniecia za duzej ilosci rzuca ValueError."""
    with pytest.raises(ValueError):
        product.remove_stock(999)


def test_add_stock_negative_raises(product):
    """Sprawdz, czy ujemna wartosc w add_stock rzuca ValueError."""
    with pytest.raises(ValueError):
        product.add_stock(-1)


def test_remove_stock_negative_raises(product):
    """Sprawdz, czy ujemna wartosc w remove_stock rzuca ValueError."""
    with pytest.raises(ValueError):
        product.remove_stock(-3)


# --- Zadanie dodatkowe: apply_discount ---

@pytest.fixture
def expensive_product():
    """Produkt z cena 100.0 do testow rabatow."""
    return Product("Telewizor", 100.0, 5)


@pytest.mark.parametrize("percent, expected_price", [
    (0, 100.0),   # brak rabatu
    (50, 50.0),   # polowa ceny
    (100, 0.0),   # cena = 0
    (25, 75.0),   # 25% znizki
])
def test_apply_discount(expensive_product, percent, expected_price):
    """Testuje apply_discount z roznymi procentami."""
    expensive_product.apply_discount(percent)
    assert expensive_product.price == pytest.approx(expected_price)


@pytest.mark.parametrize("invalid_percent", [-1, -10, 101, 200])
def test_apply_discount_invalid_raises(expensive_product, invalid_percent):
    """Sprawdz, ze nieprawidlowy procent rzuca ValueError."""
    with pytest.raises(ValueError):
        expensive_product.apply_discount(invalid_percent)
