# English version README.md
# Online Store - Django Backend Project

A comprehensive e-commerce project focusing on backend development using the Django framework.  
This project includes advanced modules for product management, users, payments, and customer interactions.

## 🌟 Key Features
- **Advanced Authentication**  
  Login/Logout with one-time password (OTP) via SMS (using Kavenegar service).
- **Product Management**  
  Categorization, advanced search, filtering, and sorting + Discount and coupon system.
- **Smart Cart**  
  Add/Remove products, real-time updates with AJAX, and payment gateway integration.
- **User Panel**  
  Profile editing, order tracking, and wishlist management.
- **Comment System**  
  Admin-approved commenting + product rating system.
- **Product Comparison**  
  Create comparison tables for related products.
- **Simple API**  
  Get product list in JSON format (`/test_api/products/`).

## 🛠 Project Applications
| Application       | Description                          |
|-------------------|--------------------------------------|
| `accounts`        | User management & authentication    |
| `products`        | Product catalog & categorization    |
| `orders`          | Shopping cart & orders               |
| `payments`        | Payment gateways & transactions      |
| `discounts`       | Smart coupon & discount system       |
| `comment_scoring_favorit...` | Comments, ratings & wishlists        |
| `warehouses`      | Inventory management                 |
| `search`          | Advanced search with dynamic filters |

## 🚀 Project Setup
1. **Clone Repository**:
   ```bash
   git clone https://github.com/yourusername/shop.git
   cd shop
   ```

2. **Install Dependencies**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate    # For Windows
   pip install -r requirements.txt
   ```

3. **Database Configuration** (in `settings.py`):  
   Configure `DATABASES` for MySQL connection.

4. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create Admin User**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run Server**:
   ```bash
   python manage.py runserver
   ```

## 🔧 Used Technologies
- **Core Platform**: Django 5.1
- **Database**: MySQL
- **Authentication**: SMS OTP (Kavenegar API)
- **Content Editor**: Django-CKEditor
- **Payment**: Iranian Gateways (Extendable)


## 📌 Technical Notes
- Using **Class-Based Views** & **Django REST Framework** for clean logic
- **AJAX Integration** in: Cart, Wishlist, and Comments
- **Custom Middlewares** for access control and logging
- **Unit Tests** for critical modules (Under development)

## 📥 Contribution
Project is actively developed! To contribute:
1. Fork the repository
2. Create your feature branch
3. Submit a Pull Request

## 📅 Roadmap
- Add blog section with commenting capability
- Integrate product recommendation system
- More details to be implemented on site

---
## License
This project is licensed under the [MIT](LICENSE) License.

## Contact Developer  
    Email: masudpythongit@gmail.com 
    Telegram: https://t.me/Masoud_GhasemiI_sorna_fast
🔗 GitHub Account: [sorna-fast](https://github.com/sorna-fast)

---

# نسخه فارسی README.md


# فروشگاه آنلاین - پروژه بک‌اند جنگو

یک پروژه جامع فروشگاه اینترنتی با تمرکز بر برنامه‌نویسی بک‌اند به کمک فریمورک Django.  
این پروژه شامل ماژول‌های پیشرفته برای مدیریت محصولات، کاربران، پرداخت‌ها و تعاملات مشتریان است.

## 🌟 ویژگی‌های کلیدی
- **احراز هویت پیشرفته**  
  ورود/خروج با کد یکبار مصرف از طریق پیامک (با استفاده از سرویس کاوه‌نگار).
- **مدیریت محصولات**  
  دسته‌بندی، جستجو، فیلتر و مرتب‌سازی پیشرفته + سیستم تخفیف و کوپن.
- **سبد خرید هوشمند**  
  افزودن/حذف محصولات، بروزرسانی لحظه‌ای با AJAX و اتصال به درگاه پرداخت.
- **پنل کاربری**  
  ویرایش پروفایل، پیگیری سفارشات و مدیریت علاقه‌مندی‌ها.
- **سیستم نظرات**  
  کامنت‌گذاری با تایید ادمین + امتیازدهی به محصولات.
- **مقایسه محصولات**  
  ایجاد جدول مقایسه برای کالاهای مرتبط.
- **API ساده**  
  دریافت لیست محصولات به صورت JSON (`/test_api/products/`).

## 🛠 اپلیکیشن‌های پروژه
| اپلیکیشن       | توضیحات                          |
|----------------|----------------------------------|
| `accounts`     | مدیریت کاربران و احراز هویت     |
| `products`     | کاتالوگ محصولات و دسته‌بندی‌ها  |
| `orders`       | سبد خرید و سفارشات               |
| `payments`     | درگاه‌های پرداخت و تراکنش‌ها     |
| `discounts`    | سیستم کوپن و تخفیف‌های هوشمند   |
| `comment_scoring_favorit...` | نظرات، امتیازها و لیست علاقه‌مندی‌ها |
| `warehouses`   | مدیریت انبار و موجودی کالا      |
| `search`       | جستجوی پیشرفته با فیلترهای داینامیک |

## 🚀 راه‌اندازی پروژه
1. **کلون کردن ریپازیتوری**:
   ```bash
   git clone https://github.com/yourusername/shop.git
   cd shop
   ```

2. **نصب وابستگی‌ها**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # برای Linux/Mac
   venv\Scripts\activate    # برای Windows
   pip install -r requirements.txt
   ```

3. **تنظیمات پایگاه داده** (در `settings.py`):  
   تنظیم `DATABASES` برای اتصال به MySQL.

4. **اجرای میگریشن‌ها**:
   ```bash
   python manage.py migrate
   ```

5. **ایجاد کاربر ادمین**:
   ```bash
   python manage.py createsuperuser
   ```

6. **اجرای سرور**:
   ```bash
   python manage.py runserver
   ```

## 🔧 فناوری‌های استفاده شده
- **پلتفرم اصلی**: Django 5.1
- **پایگاه داده**: MySQL
- **احراز هویت**: کد یکبار مصرف پیامکی (Kavenegar API)
- **ویرایشگر محتوا**: Django-CKEditor
- **پرداخت**: درگاه‌های ایرانی (قابل توسعه)


## 📌 نکات فنی
- استفاده از **Class-Based Views** و **Django REST Framework** برای منطق تمیز.
- **AJAX Integration** در بخش‌های: سبد خرید، علاقه‌مندی‌ها و نظرات.
- **Custom Middlewares** برای مدیریت دسترسی‌ها و لاگینگ.
- **Unit Tests** برای ماژول‌های حیاتی (در حال توسعه).

## 📥 مشارکت در پروژه
پروژه به صورت فعال در حال توسعه است! برای مشارکت:
1. ریپازیتوری را Fork کنید.
2. تغییرات خود را در یک Branch جدید اعمال کنید.
3. Pull Request ارسال کنید.

## 📅 برنامه آینده
-  افزودن بخش بلاگ با قابلیت کامنت‌گذاری برای بلاگ
- یکپارچه‌سازی سیستم توصیه‌گر محصولات
- و جزییات بیشتر در سایت که قراره پیاده سازی شود

---
## مجوز
این پروژه تحت مجوز [MIT](LICENSE) منتشر شده است.

## ارتباط با توسعه‌دهنده  
    ایمیل: masudpythongit@gmail.com 
    تلگرام: https://t.me/Fast_programmer
🔗 حساب گیتهاب: [sorna-fast](https://github.com/sorna-fast)
```
