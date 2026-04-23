# ✅ Login Field Yangilandi!

## 🔧 O'zgarishlar

Login endpoint da `email` maydoni o'rniga `login` maydoni qo'shildi. Endi foydalanuvchilar username yoki email bilan login qilishlari mumkin.

## 📝 Yangilangan Fayllar

### 1. apps/users/serializers.py
```python
class LoginSerializer(serializers.Serializer):
    """Serializer for login/password authentication."""
    
    login = serializers.CharField(help_text="Username or email")
    password = serializers.CharField(write_only=True)
```

**O'zgarish:**
- ❌ `email = serializers.EmailField()`
- ✅ `login = serializers.CharField(help_text="Username or email")`

### 2. apps/users/views.py
```python
def login_view(request):
    """Login with username/email and password."""
    login_input = serializer.validated_data['login']
    password = serializer.validated_data['password']
    
    # Try to authenticate with username first
    user = authenticate(username=login_input, password=password)
    
    # If failed, try with email
    if not user:
        try:
            user_obj = User.objects.get(email=login_input)
            user = authenticate(username=user_obj.username, password=password)
        except User.DoesNotExist:
            pass
```

**Logika:**
1. Avval `login` ni username sifatida sinab ko'radi
2. Agar muvaffaqiyatsiz bo'lsa, email sifatida qidiradi
3. Email topilsa, username orqali authenticate qiladi

## 🧪 Test Natijalari

### ✅ Email bilan Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"login": "manager@test.com", "password": "password123"}'
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "user": {
    "id": "...",
    "full_name": "Test Manager",
    "role": "manager"
  }
}
```

### ✅ Username bilan Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"login": "manager", "password": "password123"}'
```

**Response:** Xuddi yuqoridagidek

### ❌ Noto'g'ri Credentials
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"login": "wronguser", "password": "wrongpass"}'
```

**Response:**
```json
{
  "error": "Invalid credentials",
  "code": "INVALID_CREDENTIALS"
}
```

## 📊 Swagger Schema

### Login Request Body:
```yaml
LoginRequest:
  type: object
  description: Serializer for login/password authentication.
  properties:
    login:
      type: string
      minLength: 1
      description: Username or email
    password:
      type: string
      writeOnly: true
      minLength: 1
  required:
    - login
    - password
```

## 🎯 Swagger UI da Ko'rinishi

### Endpoint: POST /api/auth/login/

**Request Body:**
```json
{
  "login": "string",
  "password": "string"
}
```

**Field Descriptions:**
- `login` - Username yoki email (required)
- `password` - Parol (required, write-only)

## 📋 Misol: Swagger UI da Test

1. **Swagger UI ga kiring**: http://localhost:8000/api/docs/
2. **`/api/auth/login/` ni toping**
3. **"Try it out" tugmasini bosing**
4. **Request body ga kiriting:**
   ```json
   {
     "login": "manager@test.com",
     "password": "password123"
   }
   ```
5. **"Execute" tugmasini bosing**
6. **Response ko'ring:**
   - 200 OK - Token va user ma'lumotlari
   - 401 Unauthorized - Noto'g'ri credentials

## ✅ Afzalliklar

### Moslashuvchanlik
- ✅ Username bilan login
- ✅ Email bilan login
- ✅ Ikkalasi ham ishlaydi

### Foydalanuvchi Tajribasi
- ✅ Foydalanuvchi o'zi xohlagan formatda kirishi mumkin
- ✅ Email esdan chiqsa, username ishlatish mumkin
- ✅ Username esdan chiqsa, email ishlatish mumkin

### Xavfsizlik
- ✅ Password hali ham write-only
- ✅ Authentication logikasi o'zgarmagan
- ✅ Token generation xavfsiz

## 🔐 Test Foydalanuvchilar

### Manager
- **Login**: `manager@test.com` yoki `manager` (agar username o'rnatilgan bo'lsa)
- **Password**: `password123`

### Chef
- **Login**: `chef@test.com` yoki `chef`
- **Password**: `password123`
- **PIN**: `1234` (PIN login uchun)

## 📚 Qo'shimcha Ma'lumot

### PIN Login
PIN login o'zgarmagan, hali ham organization_id va pin_code kerak:
```json
{
  "organization_id": "uuid",
  "pin_code": "1234"
}
```

### Token Refresh
Token refresh ham o'zgarmagan:
```json
{
  "refresh": "refresh_token"
}
```

## 🌐 API Endpoints

- **Login**: `POST /api/auth/login/`
- **PIN Login**: `POST /api/auth/pin-login/`
- **Refresh**: `POST /api/auth/refresh/`
- **Logout**: `POST /api/auth/logout/`

Omad! 🚀
