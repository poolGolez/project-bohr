# Overview

* Each merchant will only have one menu.

## Use Cases

### Merchant-side

#### Menu Management

* **UC-M001**: Merchant creates a menu (metadata + content)

* **UC-M002**: Merchant lists all their menus (metadata only)

* **UC-M003**: Merchant gets a specific menu (metadata only)

* **UC-M003**: Merchant creates a PDF file

### Customer-side

* **UC-M005**: Customer gets specific menu


1. Allow merchants to manage their menu

    a. List all menus (metadata only)
    * **GET** /api/v1/merchants/1/menu/

    b. Create menu (metadata + content)
    * **POST** /api/v1/merchants/1/menu/

    c. Get menu (metadata)
    * **GET** /api/v1/merchants/1/menu/1

2. Allow customers to see the merchant's specific menu

    a. Get menu (content)
    * **GET** /api/v1/merchants/1/menu/1/

---
# DB Design

|PK                    |Name|                       |
|----------------------|----------------|-----------|
| MERCHANT#1\|MENU#1   | Breakfast menu | {dasfas...}
