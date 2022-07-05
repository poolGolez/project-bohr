from domain import Menu
from repository import MenuRepository
from uuid import uuid4
from datetime import datetime


class MenuManagementService:

    def __init__(self) -> None:
        self._repository = MenuRepository()

    def create(self, menu: Menu) -> Menu:
        menu.id = str(uuid4())[-6:]
        menu.status = "INACTIVE"
        menu.date_created = datetime.now()

        self._repository.save(menu)
        return menu

    def find_all_metadata_by_merchant_id(self, merchant_id: str) -> list:
        return self._repository.find_all_by_merchant_id(merchant_id)

    def find_by_merchant_and_menu(self, merchant_id: str, menu_id: str) -> Menu:
        return self._repository.find_by_merchant_and_menu(merchant_id, menu_id)

    def activate(self, active_menu: Menu) -> None:
        active_menu.activate()
        # check if menu is there
        menus = self._repository.find_all_by_merchant_id(
            active_menu.merchant_id)

        other_menus = [menu for menu in menus if menu.id != active_menu.id]
        for menu in other_menus:
            menu.deactivate()

        self._repository.batch_save_metadata(other_menus + [active_menu])
        return active_menu
