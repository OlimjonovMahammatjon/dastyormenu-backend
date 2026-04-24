# 🌐 Public API Endpoints (Autentifikatsiya Kerak Emas)

## 📋 Umumiy Ma'lumot

Quyidagi endpointlar **autentifikatsiya talab qilmaydi** va public access uchun ochiq:

---

## 🏢 Organizations (Tashkilotlar)

### 1. Barcha Tashkilotlar Ro'yxati

**GET** `/api/organizations/`

**Tavsif**: Barcha aktiv tashkilotlar ro'yxatini olish

**Query Parameters**:
- Yo'q

**Response**:
```json
[
  {
    "id": "uuid",
    "name": "Test Restaurant",
    "slug": "test-restaurant",
    "logo": "http://example.com/media/logos/logo.png",
    "is_active": true
  }
]
```

---

### 2. Tashkilot Detallari

**GET** `/api/organizations/{id}/`

**Tavsif**: Bitta tashkilot haqida to'liq ma'lumot

**Response**:
```json
{
  "id": "uuid",
  "name": "Test Restaurant",
  "slug": "test-restaurant",
  "logo": "http://example.com/media/logos/logo.png",
  "address": "Toshkent, Amir Temur ko'chasi",
  "phone": "+998901234567",
  "email": "info@restaurant.uz",
  "is_active": true,
  "subscription_status": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

---

## 📂 Categories (Kategoriyalar)

### 1. Barcha Kategoriyalar

**GET** `/api/categories/`

**Tavsif**: Barcha kategoriyalar ro'yxati

**Query Parameters**:
- `organization_id` (optional): Tashkilot ID si
- `is_active` (optional): `true` yoki `false`

**Misol**:
```
GET /api/categories/?organization_id=uuid&is_active=true
```

**Response**:
```json
[
  {
    "id": "uuid",
    "name": "Salatlar",
    "description": "Yangi salatlar",
    "sort_order": 1,
    "is_active": true
  }
]
```

---

### 2. Kategoriya Detallari

**GET** `/api/categories/{id}/`

**Response**:
```json
{
  "id": "uuid",
  "organization": "uuid",
  "name": "Salatlar",
  "description": "Yangi salatlar",
  "sort_order": 1,
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

---

## 🍽️ Menu (Menyu)

### 1. Barcha Menyu Itemlar

**GET** `/api/menu/`

**Tavsif**: Barcha menyu itemlar ro'yxati

**Query Parameters**:
- `organization_id` (optional): Tashkilot ID si
- `category_id` (optional): Kategoriya ID si
- `is_available` (optional): `true` yoki `false`
- `search` (optional): Qidiruv (name, description, ingredients)

**Misol**:
```
GET /api/menu/?organization_id=uuid&category_id=uuid&is_available=true&search=osh
```

**Response**:
```json
[
  {
    "id": "uuid",
    "name": "Osh",
    "description": "O'zbek milliy taomi",
    "price": "25000.00",
    "image_url": "http://example.com/media/menu/osh.jpg",
    "category": {
      "id": "uuid",
      "name": "Issiq taomlar"
    },
    "is_available": true,
    "sort_order": 1
  }
]
```

---

### 2. Menyu Item Detallari

**GET** `/api/menu/{id}/`

**Response**:
```json
{
  "id": "uuid",
  "organization": "uuid",
  "category": "uuid",
  "name": "Osh",
  "description": "O'zbek milliy taomi",
  "ingredients": "Guruch, go'sht, sabzi, piyoz",
  "price": "25000.00",
  "image_url": "http://example.com/media/menu/osh.jpg",
  "is_available": true,
  "sort_order": 1,
  "created_at": "2024-01-01T00:00:00Z"
}
```

---

## 🪑 Tables (Stollar)

### 1. QR Code orqali Stol Ma'lumotlarini Olish

**GET** `/api/tables/qr-lookup/?qr={qr_code_id}`

**Tavsif**: QR code ID orqali stol va tashkilot ma'lumotlarini olish

**Query Parameters**:
- `qr` (required): QR code ID

**Misol**:
```
GET /api/tables/qr-lookup/?qr=550e8400-e29b-41d4-a716-446655440000
```

**Response**:
```json
{
  "table": {
    "id": "uuid",
    "table_number": "5",
    "capacity": 4,
    "qr_code_id": "uuid",
    "is_active": true
  },
  "organization": {
    "id": "uuid",
    "name": "Test Restaurant",
    "logo": "http://example.com/media/logos/logo.png"
  }
}
```

---

## 🍽️ Public Menu (QR Code orqali)

### 1. QR Code orqali Menyu Olish

**GET** `/api/public/menu/?qr={qr_code_id}`

**Tavsif**: QR code orqali to'liq menyu va tashkilot ma'lumotlarini olish

**Query Parameters**:
- `qr` (required): QR code ID

**Misol**:
```
GET /api/public/menu/?qr=550e8400-e29b-41d4-a716-446655440000
```

**Response**:
```json
{
  "organization": {
    "id": "uuid",
    "name": "Test Restaurant",
    "logo": "http://example.com/media/logos/logo.png"
  },
  "table": {
    "id": "uuid",
    "number": "5",
    "qr_code_id": "uuid"
  },
  "menu": [
    {
      "id": "uuid",
      "name": "Osh",
      "description": "O'zbek milliy taomi",
      "price": "25000.00",
      "image_url": "http://example.com/media/menu/osh.jpg",
      "category": {
        "id": "uuid",
        "name": "Issiq taomlar"
      },
      "is_available": true
    }
  ]
}
```

---

## 🔐 Authentication (Login)

### 1. Login

**POST** `/api/auth/login/`

**Tavsif**: Username/Email va parol bilan login

**Request Body**:
```json
{
  "login": "admin",
  "password": "admin123"
}
```

**Response**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "uuid",
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com"
    },
    "full_name": "Admin User",
    "role": "super_admin",
    "organization": null
  }
}
```

---

### 2. PIN Login

**POST** `/api/auth/pin-login/`

**Tavsif**: PIN kod bilan login (chef va waiter uchun)

**Request Body**:
```json
{
  "organization_id": "uuid",
  "pin_code": "1234"
}
```

**Response**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "uuid",
    "full_name": "Chef User",
    "role": "chef",
    "organization": "uuid"
  }
}
```

---

## 📝 Public Orders (Buyurtmalar)

### 1. Buyurtma Yaratish (Public)

**POST** `/api/public/orders/`

**Tavsif**: QR code orqali buyurtma yaratish (autentifikatsiya kerak emas)

**Request Body**:
```json
{
  "table_qr_code": "uuid",
  "customer_name": "Sardor",
  "items": [
    {
      "menu_item_id": "uuid",
      "quantity": 2,
      "notes": "Achchiq bo'lmasin"
    }
  ]
}
```

**Response**:
```json
{
  "id": "uuid",
  "order_number": "ORD-001",
  "table": {
    "id": "uuid",
    "table_number": "5"
  },
  "customer_name": "Sardor",
  "items": [
    {
      "menu_item": {
        "id": "uuid",
        "name": "Osh",
        "price": "25000.00"
      },
      "quantity": 2,
      "price": "25000.00",
      "subtotal": "50000.00",
      "notes": "Achchiq bo'lmasin"
    }
  ],
  "total_amount": "50000.00",
  "status": "pending",
  "created_at": "2024-01-01T12:00:00Z"
}
```

---

### 2. Buyurtma Statusini Tekshirish

**GET** `/api/public/orders/{id}/status/`

**Tavsif**: Buyurtma statusini tekshirish

**Response**:
```json
{
  "id": "uuid",
  "order_number": "ORD-001",
  "status": "preparing",
  "estimated_time": 15,
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:05:00Z"
}
```

---

## 🔒 Private Endpoints (Autentifikatsiya Kerak)

Quyidagi endpointlar **autentifikatsiya talab qiladi**:

### Organizations
- `POST /api/organizations/` - Yangi tashkilot yaratish (super_admin)
- `PUT /api/organizations/{id}/` - Tashkilotni yangilash (super_admin)
- `DELETE /api/organizations/{id}/` - Tashkilotni o'chirish (super_admin)

### Categories
- `POST /api/categories/` - Yangi kategoriya yaratish (manager+)
- `PUT /api/categories/{id}/` - Kategoriyani yangilash (manager+)
- `DELETE /api/categories/{id}/` - Kategoriyani o'chirish (manager+)

### Menu
- `POST /api/menu/` - Yangi menyu item yaratish (manager+)
- `PUT /api/menu/{id}/` - Menyu itemni yangilash (manager+)
- `DELETE /api/menu/{id}/` - Menyu itemni o'chirish (manager+)
- `POST /api/menu/{id}/toggle-availability/` - Stop-list (manager+)

### Tables
- `GET /api/tables/` - Barcha stollar (manager+)
- `POST /api/tables/` - Yangi stol yaratish (manager+)
- `PUT /api/tables/{id}/` - Stolni yangilash (manager+)
- `DELETE /api/tables/{id}/` - Stolni o'chirish (manager+)
- `GET /api/tables/{id}/qr-code/` - QR code yuklab olish (manager+)
- `POST /api/tables/{id}/regenerate-qr/` - QR code qayta yaratish (manager+)

### Orders
- `GET /api/orders/` - Barcha buyurtmalar (authenticated)
- `PUT /api/orders/{id}/` - Buyurtmani yangilash (authenticated)
- `POST /api/orders/{id}/update-status/` - Status yangilash (chef+)
- `GET /api/orders/active/` - Aktiv buyurtmalar (chef+)
- `GET /api/orders/my-tables/` - Mening stollarim (waiter+)

### Users
- `GET /api/users/` - Barcha userlar (manager+)
- `POST /api/users/` - Yangi user yaratish (manager+)
- `PUT /api/users/{id}/` - Userni yangilash (manager+)
- `POST /api/users/{id}/set-pin/` - PIN o'rnatish (manager+)

---

## 🧪 Test Qilish

### cURL bilan

```bash
# Organizations
curl https://dastyormenu-backend-production.up.railway.app/api/organizations/

# Categories
curl https://dastyormenu-backend-production.up.railway.app/api/categories/?organization_id=uuid

# Menu
curl https://dastyormenu-backend-production.up.railway.app/api/menu/?organization_id=uuid

# Table lookup
curl https://dastyormenu-backend-production.up.railway.app/api/tables/qr-lookup/?qr=uuid

# Public menu
curl https://dastyormenu-backend-production.up.railway.app/api/public/menu/?qr=uuid
```

### JavaScript bilan

```javascript
// Organizations
fetch('https://dastyormenu-backend-production.up.railway.app/api/organizations/')
  .then(res => res.json())
  .then(data => console.log(data));

// Menu with filters
fetch('https://dastyormenu-backend-production.up.railway.app/api/menu/?organization_id=uuid&is_available=true')
  .then(res => res.json())
  .then(data => console.log(data));

// Public menu via QR
fetch('https://dastyormenu-backend-production.up.railway.app/api/public/menu/?qr=uuid')
  .then(res => res.json())
  .then(data => console.log(data));
```

---

## 📊 Xulosa

### Public Endpoints (Autentifikatsiya Kerak Emas)

| Endpoint | Method | Tavsif |
|----------|--------|--------|
| `/api/organizations/` | GET | Tashkilotlar ro'yxati |
| `/api/organizations/{id}/` | GET | Tashkilot detallari |
| `/api/categories/` | GET | Kategoriyalar ro'yxati |
| `/api/categories/{id}/` | GET | Kategoriya detallari |
| `/api/menu/` | GET | Menyu ro'yxati |
| `/api/menu/{id}/` | GET | Menyu item detallari |
| `/api/tables/qr-lookup/` | GET | QR code orqali stol |
| `/api/public/menu/` | GET | QR code orqali menyu |
| `/api/public/orders/` | POST | Buyurtma yaratish |
| `/api/public/orders/{id}/status/` | GET | Buyurtma statusi |
| `/api/auth/login/` | POST | Login |
| `/api/auth/pin-login/` | POST | PIN login |

### Private Endpoints (Autentifikatsiya Kerak)

- Barcha `POST`, `PUT`, `DELETE` metodlar (faqat public orders bundan mustasno)
- User management
- Order management (chef, waiter)
- Table management
- Organization management (super_admin)

---

Omad! 🚀
