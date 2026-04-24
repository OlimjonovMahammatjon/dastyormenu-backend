# 🌐 Client Public API - Autentifikatsiya Kerak Emas!

## 🎯 Umumiy Konsepsiya

**Client (Mijoz)** - bu restoranda stol yonida o'tirgan va QR code orqali menyu ko'rgan, buyurtma bergan odam.

**Client uchun autentifikatsiya KERAK EMAS!** ✅

---

## 📱 Client Flow (Mijoz Oqimi)

### 1. QR Code Skanerlash

Mijoz stol ustidagi QR code ni skanerlaydi:

```
QR Code: https://yourdomain.com/table?qr=550e8400-e29b-41d4-a716-446655440000
```

---

### 2. Stol Ma'lumotlarini Olish

**GET** `/api/tables/qr-lookup/?qr={qr_code_id}`

**Autentifikatsiya**: ❌ Kerak emas

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

### 3. Menyu Ko'rish

**GET** `/api/menu/?organization_id={organization_id}&is_available=true`

**Autentifikatsiya**: ❌ Kerak emas

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
  },
  {
    "id": "uuid",
    "name": "Lag'mon",
    "description": "Lag'mon",
    "price": "22000.00",
    "image_url": "http://example.com/media/menu/lagmon.jpg",
    "category": {
      "id": "uuid",
      "name": "Issiq taomlar"
    },
    "is_available": true,
    "sort_order": 2
  }
]
```

---

### 4. Kategoriyalar Ko'rish

**GET** `/api/categories/?organization_id={organization_id}&is_active=true`

**Autentifikatsiya**: ❌ Kerak emas

**Response**:
```json
[
  {
    "id": "uuid",
    "name": "Issiq taomlar",
    "description": "Issiq taomlar",
    "sort_order": 1,
    "is_active": true
  },
  {
    "id": "uuid",
    "name": "Salatlar",
    "description": "Yangi salatlar",
    "sort_order": 2,
    "is_active": true
  }
]
```

---

### 5. Buyurtma Berish

**POST** `/api/orders/`

**Autentifikatsiya**: ❌ Kerak emas

**Request Body**:
```json
{
  "qr_code_id": "550e8400-e29b-41d4-a716-446655440000",
  "customer_note": "Achchiq bo'lmasin",
  "tip_percentage": 10,
  "items": [
    {
      "menu": "uuid",
      "quantity": 2,
      "modifications": "Achchiq bo'lmasin"
    },
    {
      "menu": "uuid",
      "quantity": 1,
      "modifications": ""
    }
  ]
}
```

**Response**:
```json
{
  "id": "uuid",
  "status": "pending",
  "items": [
    {
      "id": "uuid",
      "menu_name": "Osh",
      "menu_price": "25000.00",
      "quantity": 2,
      "modifications": "Achchiq bo'lmasin",
      "subtotal": "50000.00"
    },
    {
      "id": "uuid",
      "menu_name": "Lag'mon",
      "menu_price": "22000.00",
      "quantity": 1,
      "modifications": "",
      "subtotal": "22000.00"
    }
  ],
  "total_amount": "72000.00",
  "tip_amount": "7200.00",
  "created_at": "2024-01-01T12:00:00Z"
}
```

---

### 6. Buyurtma Statusini Tekshirish

**GET** `/api/orders/{order_id}/`

**Autentifikatsiya**: ❌ Kerak emas

**Response**:
```json
{
  "id": "uuid",
  "status": "cooking",
  "table_number": 5,
  "total_amount": "72000.00",
  "tip_amount": "7200.00",
  "items": [
    {
      "menu_name": "Osh",
      "quantity": 2,
      "item_status": "cooking"
    },
    {
      "menu_name": "Lag'mon",
      "quantity": 1,
      "item_status": "pending"
    }
  ],
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:05:00Z"
}
```

---

### 7. Barcha Buyurtmalarni Ko'rish (Stol bo'yicha)

**GET** `/api/orders/?table_id={table_id}`

**Autentifikatsiya**: ❌ Kerak emas

**Response**:
```json
[
  {
    "id": "uuid",
    "table_number": 5,
    "status": "cooking",
    "total_amount": "72000.00",
    "items_count": 2,
    "created_at": "2024-01-01T12:00:00Z"
  }
]
```

---

## 📋 Barcha Public Endpoints

### 🏢 Organizations

| Endpoint | Method | Autentifikatsiya | Tavsif |
|----------|--------|------------------|--------|
| `/api/organizations/` | GET | ❌ | Barcha tashkilotlar |
| `/api/organizations/{id}/` | GET | ❌ | Tashkilot detallari |

---

### 📂 Categories

| Endpoint | Method | Autentifikatsiya | Tavsif |
|----------|--------|------------------|--------|
| `/api/categories/` | GET | ❌ | Barcha kategoriyalar |
| `/api/categories/{id}/` | GET | ❌ | Kategoriya detallari |

**Query Parameters**:
- `organization_id` - Tashkilot ID si
- `is_active` - `true` yoki `false`

---

### 🍽️ Menu

| Endpoint | Method | Autentifikatsiya | Tavsif |
|----------|--------|------------------|--------|
| `/api/menu/` | GET | ❌ | Barcha menyu itemlar |
| `/api/menu/{id}/` | GET | ❌ | Menyu item detallari |

**Query Parameters**:
- `organization_id` - Tashkilot ID si
- `category_id` - Kategoriya ID si
- `is_available` - `true` yoki `false`
- `search` - Qidiruv (name, description, ingredients)

---

### 🪑 Tables

| Endpoint | Method | Autentifikatsiya | Tavsif |
|----------|--------|------------------|--------|
| `/api/tables/qr-lookup/?qr={qr_code_id}` | GET | ❌ | QR code orqali stol |

---

### 📦 Orders

| Endpoint | Method | Autentifikatsiya | Tavsif |
|----------|--------|------------------|--------|
| `/api/orders/` | GET | ❌ | Barcha buyurtmalar |
| `/api/orders/` | POST | ❌ | Buyurtma yaratish |
| `/api/orders/{id}/` | GET | ❌ | Buyurtma detallari |

**Query Parameters** (GET):
- `organization_id` - Tashkilot ID si
- `table_id` - Stol ID si
- `status` - Buyurtma statusi

---

### 💳 Payments

| Endpoint | Method | Autentifikatsiya | Tavsif |
|----------|--------|------------------|--------|
| `/api/payments/` | GET | ❌ | Barcha to'lovlar |
| `/api/payments/{id}/` | GET | ❌ | To'lov detallari |

**Query Parameters**:
- `organization_id` - Tashkilot ID si
- `order_id` - Buyurtma ID si

---

### 🔔 Notifications

| Endpoint | Method | Autentifikatsiya | Tavsif |
|----------|--------|------------------|--------|
| `/api/notifications/` | GET | ❌ | Barcha bildirishnomalar |
| `/api/notifications/{id}/` | GET | ❌ | Bildirishnoma detallari |

**Query Parameters**:
- `organization_id` - Tashkilot ID si
- `recipient_id` - Qabul qiluvchi ID si

---

### 📅 Subscriptions

| Endpoint | Method | Autentifikatsiya | Tavsif |
|----------|--------|------------------|--------|
| `/api/subscriptions/` | GET | ❌ | Barcha obunalar |
| `/api/subscriptions/{id}/` | GET | ❌ | Obuna detallari |

**Query Parameters**:
- `organization_id` - Tashkilot ID si

---

## 🔐 Private Endpoints (Autentifikatsiya Kerak)

Quyidagi endpointlar **faqat authenticated userlar** uchun:

### Staff Actions (Manager, Chef, Waiter)

- `POST /api/menu/` - Menyu yaratish (manager+)
- `PUT /api/menu/{id}/` - Menyu yangilash (manager+)
- `DELETE /api/menu/{id}/` - Menyu o'chirish (manager+)
- `POST /api/menu/{id}/toggle-availability/` - Stop-list (manager+)
- `POST /api/orders/{id}/update-status/` - Buyurtma statusini yangilash (chef+)
- `GET /api/orders/active/` - Aktiv buyurtmalar (chef+)
- `GET /api/orders/my-tables/` - Mening stollarim (waiter+)
- `POST /api/payments/{id}/confirm/` - To'lovni tasdiqlash (waiter+)
- `POST /api/notifications/{id}/mark-read/` - Bildirishnomani o'qilgan qilish
- `POST /api/notifications/mark-all-read/` - Barchasini o'qilgan qilish

---

## 🧪 Frontend Integration

### React Example

```javascript
// 1. QR Code dan table ma'lumotlarini olish
const getTableInfo = async (qrCodeId) => {
  const response = await fetch(
    `https://api.dastyormenu.uz/api/tables/qr-lookup/?qr=${qrCodeId}`
  );
  const data = await response.json();
  return data;
};

// 2. Menyu olish
const getMenu = async (organizationId) => {
  const response = await fetch(
    `https://api.dastyormenu.uz/api/menu/?organization_id=${organizationId}&is_available=true`
  );
  const data = await response.json();
  return data;
};

// 3. Buyurtma berish
const createOrder = async (qrCodeId, items) => {
  const response = await fetch(
    'https://api.dastyormenu.uz/api/orders/',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        qr_code_id: qrCodeId,
        customer_note: 'Achchiq bo'lmasin',
        tip_percentage: 10,
        items: items
      })
    }
  );
  const data = await response.json();
  return data;
};

// 4. Buyurtma statusini tekshirish
const getOrderStatus = async (orderId) => {
  const response = await fetch(
    `https://api.dastyormenu.uz/api/orders/${orderId}/`
  );
  const data = await response.json();
  return data;
};
```

---

### Vue Example

```javascript
// composables/useMenu.js
export const useMenu = () => {
  const getTableInfo = async (qrCodeId) => {
    const { data } = await useFetch(
      `/api/tables/qr-lookup/?qr=${qrCodeId}`
    );
    return data.value;
  };

  const getMenu = async (organizationId) => {
    const { data } = await useFetch(
      `/api/menu/?organization_id=${organizationId}&is_available=true`
    );
    return data.value;
  };

  const createOrder = async (orderData) => {
    const { data } = await useFetch('/api/orders/', {
      method: 'POST',
      body: orderData
    });
    return data.value;
  };

  return {
    getTableInfo,
    getMenu,
    createOrder
  };
};
```

---

## 📊 Order Status Flow

```
pending → cooking → ready → completed
   ↓         ↓        ↓         ↓
Client   Kitchen   Waiter   Finished
```

**Status Tavsifi**:
- `pending` - Yangi buyurtma, kutilmoqda
- `cooking` - Oshxonada tayyorlanmoqda
- `ready` - Tayyor, waiter olib kelishi kerak
- `completed` - Buyurtma tugallandi
- `cancelled` - Bekor qilindi

---

## 🎯 Xulosa

### ✅ Client uchun (Autentifikatsiya Kerak Emas)

1. QR code skanerlash
2. Stol ma'lumotlarini olish
3. Menyu ko'rish
4. Kategoriyalar ko'rish
5. Buyurtma berish
6. Buyurtma statusini tekshirish
7. To'lovlarni ko'rish

### 🔒 Staff uchun (Autentifikatsiya Kerak)

1. Menyu boshqarish (CRUD)
2. Buyurtma statusini yangilash
3. Aktiv buyurtmalarni ko'rish
4. To'lovni tasdiqlash
5. Bildirishnomalarni boshqarish

---

Omad! 🚀
