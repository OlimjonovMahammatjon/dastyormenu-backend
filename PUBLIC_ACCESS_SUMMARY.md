# ✅ Public Access - Barcha GET Metodlar

## 🎯 Asosiy O'zgarish

**`config/settings/base.py`** da:

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # ✅ Default: public access
    ],
    # ...
}
```

Bu o'zgarish **barcha endpointlarni default public** qiladi!

---

## ✅ Public Endpoints (Autentifikatsiya Kerak Emas)

### 🏢 Organizations
- `GET /api/organizations/` ✅
- `GET /api/organizations/{id}/` ✅

### 📂 Categories
- `GET /api/categories/` ✅
- `GET /api/categories/{id}/` ✅

### 🍽️ Menu
- `GET /api/menu/` ✅
- `GET /api/menu/{id}/` ✅

### 🪑 Tables
- `GET /api/tables/` ✅
- `GET /api/tables/{id}/` ✅
- `GET /api/tables/qr-lookup/?qr={qr_code_id}` ✅

### 📦 Orders
- `GET /api/orders/` ✅
- `GET /api/orders/{id}/` ✅
- `POST /api/orders/` ✅ (Buyurtma berish)

### 💳 Payments
- `GET /api/payments/` ✅
- `GET /api/payments/{id}/` ✅

### 🔔 Notifications
- `GET /api/notifications/` ✅
- `GET /api/notifications/{id}/` ✅

### 📅 Subscriptions
- `GET /api/subscriptions/` ✅
- `GET /api/subscriptions/{id}/` ✅

### 🔐 Auth
- `POST /api/auth/login/` ✅
- `POST /api/auth/pin-login/` ✅

---

## 🔒 Private Endpoints (Autentifikatsiya Kerak)

Faqat quyidagi actionlar autentifikatsiya talab qiladi:

### Organizations
- `POST /api/organizations/` 🔒 (super_admin)
- `PUT /api/organizations/{id}/` 🔒 (super_admin)
- `DELETE /api/organizations/{id}/` 🔒 (super_admin)
- `POST /api/organizations/{id}/activate_subscription/` 🔒 (super_admin)
- `POST /api/organizations/{id}/deactivate_subscription/` 🔒 (super_admin)

### Categories
- `POST /api/categories/` 🔒 (manager+)
- `PUT /api/categories/{id}/` 🔒 (manager+)
- `DELETE /api/categories/{id}/` 🔒 (manager+)

### Menu
- `POST /api/menu/` 🔒 (manager+)
- `PUT /api/menu/{id}/` 🔒 (manager+)
- `DELETE /api/menu/{id}/` 🔒 (manager+)
- `POST /api/menu/{id}/toggle_availability/` 🔒 (manager+)

### Tables
- `POST /api/tables/` 🔒 (manager+)
- `PUT /api/tables/{id}/` 🔒 (manager+)
- `DELETE /api/tables/{id}/` 🔒 (manager+)
- `GET /api/tables/{id}/qr_code/` 🔒 (manager+)
- `POST /api/tables/{id}/regenerate_qr/` 🔒 (manager+)

### Orders
- `PUT /api/orders/{id}/` 🔒 (waiter+)
- `DELETE /api/orders/{id}/` 🔒 (waiter+)
- `POST /api/orders/{id}/update_status/` 🔒 (chef+)
- `GET /api/orders/active/` 🔒 (chef+)
- `GET /api/orders/my_tables/` 🔒 (waiter+)

### Payments
- `POST /api/payments/` 🔒 (waiter+)
- `PUT /api/payments/{id}/` 🔒 (waiter+)
- `DELETE /api/payments/{id}/` 🔒 (waiter+)
- `POST /api/payments/{id}/confirm/` 🔒 (waiter+)

### Notifications
- `POST /api/notifications/{id}/mark_read/` 🔒 (authenticated)
- `POST /api/notifications/mark_all_read/` 🔒 (authenticated)

### Subscriptions
- `GET /api/subscriptions/current/` 🔒 (manager+)
- `GET /api/subscriptions/history/` 🔒 (manager+)

### Users
- `GET /api/users/` 🔒 (manager+)
- `POST /api/users/` 🔒 (manager+)
- `PUT /api/users/{id}/` 🔒 (manager+)
- `DELETE /api/users/{id}/` 🔒 (manager+)
- `POST /api/users/{id}/set_pin/` 🔒 (manager+)

---

## 🧪 Test Qilish

### Barcha GET Endpointlar

```bash
# Organizations
curl http://localhost:8000/api/organizations/

# Categories
curl http://localhost:8000/api/categories/

# Menu
curl http://localhost:8000/api/menu/

# Tables
curl http://localhost:8000/api/tables/

# Orders
curl http://localhost:8000/api/orders/

# Payments
curl http://localhost:8000/api/payments/

# Notifications
curl http://localhost:8000/api/notifications/

# Subscriptions
curl http://localhost:8000/api/subscriptions/
```

### Buyurtma Berish (POST)

```bash
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "qr_code_id": "YOUR_QR_CODE_ID",
    "customer_note": "Achchiq bo'\''lmasin",
    "tip_percentage": 10,
    "items": [
      {
        "menu": "MENU_ITEM_ID",
        "quantity": 2,
        "modifications": "Achchiq bo'\''lmasin"
      }
    ]
  }'
```

---

## 📊 Xulosa

### ✅ Nima Qilindi?

1. **Global Permission O'zgartirildi**:
   - `DEFAULT_PERMISSION_CLASSES` → `AllowAny`
   - Barcha endpointlar default public

2. **View-Level Permissions**:
   - Har bir ViewSet da `get_permissions()` metodi
   - GET metodlar → `AllowAny()`
   - POST/PUT/DELETE → `IsAuthenticated()` + role permissions

3. **Orders - To'liq Public**:
   - `GET /api/orders/` - Public
   - `POST /api/orders/` - Public (buyurtma berish)
   - `GET /api/orders/{id}/` - Public

### 🎯 Client Flow

1. QR code skanerlash
2. Stol ma'lumotlarini olish (`GET /api/tables/qr-lookup/`)
3. Menyu ko'rish (`GET /api/menu/`)
4. Buyurtma berish (`POST /api/orders/`)
5. Buyurtma statusini tekshirish (`GET /api/orders/{id}/`)

**Hech qanday autentifikatsiya kerak emas!** ✅

---

## 🚀 Railway ga Deploy

```bash
git add .
git commit -m "Made all GET endpoints public by default"
git push origin main
```

Railway avtomatik deploy qiladi!

---

## 📝 Eslatma

- **Barcha GET metodlar** - Public ✅
- **POST /api/orders/** - Public (buyurtma berish) ✅
- **Boshqa POST/PUT/DELETE** - Private (autentifikatsiya kerak) 🔒

Omad! 🎉
