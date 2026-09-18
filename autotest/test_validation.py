import sys
from pathlib import Path
from unittest.mock import Mock
import pytest

CLIENT_DIR = Path(__file__).resolve().parent.parent / "client"
if str(CLIENT_DIR) not in sys.path:
    sys.path.insert(0, str(CLIENT_DIR))

from client import *


@pytest.fixture
def client():
    return Mock()

class TestCmdCreateUser:
    def test_returns_true_on_success(self, client, capsys):
        client.create_user.return_value = {
            "id": 1,
            "name": "user resu",
            "email": "user@mail.dom",
            "age": 22,
        }

        result = cmd_create_user(client, ["user resu", "user@mail.dom", "22"])

        assert result is True
        assert client.create_user.called
        assert "User created" in capsys.readouterr().out

    @pytest.mark.parametrize(
        "args",
        [
            ["user resu"],
            ["user resu", "mainmail", "22"],
            ["user resu", "user@mail.dom", "0"],
            ["user resu", "user@mail.dom", "222"],
        ],
    )
    def test_returns_false_on_validation_error(self, client, capsys, args):
        result = cmd_create_user(client, args)

        assert result is False
        client.create_user.assert_not_called()


class TestCmdCreateProduct:
    def test_returns_true_on_success(self, client, capsys):
        client.create_product.return_value = {
            "id": 1,
            "name": "prod prod",
            "price": 222.22,
            "stock": 23,
            "number_of_purchases": 11,
        }

        result = cmd_create_product(client, ["prod prod", "222.22", "23", "11"])

        assert result is True
        assert client.create_product.called
        assert "Product created" in capsys.readouterr().out

    @pytest.mark.parametrize(
        "args",
        [
            ["prod prod"],
            ["prod prod", "price"],
            ["prod prod", "-10", "3", "1"],
            ["prod prod", "222", "2.2", "1"],
            ["prod prod", "222.4", "-1", "1"],
            ["prod prod", "-10", "3", "-1"],
            ["prod prod", "222", "2", "abc"],
            ["prod prod", "222", "2.2", "-333"],
        ],
    )
    def test_returns_false_on_validation_error(self, client, capsys, args):
        result = cmd_create_product(client, args)

        assert result is False
        client.create_product.assert_not_called()


class TestCmdUpdateUserById:
    def test_returns_true_on_success(self, client, capsys):
        client.update_user_by_id.return_value = {
            "id": 1,
            "name": "user resu",
            "email": "user@mail.dom",
            "age": 22,
        }

        result = cmd_update_user_by_id(client, ["1", "email=user@mail.dom", "age=22"])

        assert result is True
        assert client.update_user_by_id.called
        assert "Updated user" in capsys.readouterr().out

    def test_returns_true_when_user_not_found(self, client, capsys):
        client.update_user_by_id.return_value = None

        result = cmd_update_user_by_id(client, ["999", "age=22"])

        assert result is True
        assert client.update_user_by_id.called
        assert "not found" in capsys.readouterr().out.lower()

    @pytest.mark.parametrize(
        "args",
        [
            ["1", "email=wrong"],
            ["qwe", "age=22"],
            ["1", "age=0"],
            ["1", "age=222"],
            ["1", "age=22.2"],
            ["1", "age"],
        ],
    )
    def test_returns_false_on_validation_error(self, client, capsys, args):
        result = cmd_update_user_by_id(client, args)

        assert result is False
        client.update_user.assert_not_called()


class TestCmdUpdateProductById:
    def test_returns_true_on_success(self, client, capsys):
        client.update_product_by_id.return_value = {
            "id": 1,
            "name": "prod prod",
            "price": 222.22,
            "stock": 11,
        }

        result = cmd_update_product_by_id(client, ["1", "price=222.22", "stock=11"])

        assert result is True
        assert client.update_product_by_id.called
        assert "Updated product" in capsys.readouterr().out

    def test_returns_true_when_product_not_found(self, client, capsys):
        client.update_product_by_id.return_value = None

        result = cmd_update_product_by_id(client, ["999", "price=100"])

        assert result is True
        assert client.update_product_by_id.called
        assert "not found" in capsys.readouterr().out.lower()

    @pytest.mark.parametrize(
        "args",
        [
            ["1", "price=qqq"],
            ["1", "price=-111"],
            ["1", "stock=22.22"],
            ["1", "stock=-1"],
            ["abc", "price=111"],
            ["1", "stock"],
        ],
    )
    def test_returns_false_on_validation_error(self, client, capsys, args):
        result = cmd_update_product_by_id(client, args)

        assert result is False
        client.update_product.assert_not_called()