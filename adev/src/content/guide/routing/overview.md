<docs-decorative-header title="Angular'da marshrutlash" imgSrc="adev/src/assets/images/routing.svg"> <!-- markdownlint-disable-line -->
Marshrutlash (routing) bir sahifali ilovada foydalanuvchi koʻradigan narsani oʻzgartirishga yordam beradi.
</docs-decorative-header>

Angular Router (`@angular/router`) — Angular ilovalarida navigatsiyani boshqarish uchun rasmiy kutubxona va freymvorkning asosiy qismidir. U Angular CLI yordamida yaratilgan barcha loyihalarga sukut boʻyicha kiritilgan.

## Nega SPA'da marshrutlash zarur? {#why-is-routing-necessary-in-a-spa}

Veb-brauzeringizda biror URL'ga oʻtganingizda, brauzer odatda veb-serverga tarmoq soʻrovi yuboradi va qaytarilgan HTML sahifani koʻrsatadi. Boshqa URL'ga oʻtganingizda, masalan, havolani bosganingizda, brauzer yana bir tarmoq soʻrovi yuboradi va butun sahifani yangisi bilan almashtiradi.

Bir sahifali ilova (single-page application, SPA) bundan shu bilan farq qiladiki, brauzer veb-serverga faqat birinchi sahifa — `index.html` uchun soʻrov yuboradi. Shundan soʻng boshqaruvni klient tomonidagi router oʻz qoʻliga oladi va URL'ga qarab qaysi kontent koʻrsatilishini nazorat qiladi. Foydalanuvchi boshqa URL'ga oʻtganda, router sahifani toʻliq qayta yuklamasdan uning kontentini joyida yangilaydi.

## Angular marshrutlashni qanday boshqaradi {#how-angular-manages-routing}

Angular'da marshrutlash uchta asosiy qismdan iborat:

1. **Marshrutlar (routes)** foydalanuvchi muayyan URL'ga kirganda qaysi komponent koʻrsatilishini belgilaydi.
2. **Outlet'lar** — shablonlaringizdagi toʻldiruvchilar (placeholder) boʻlib, faol marshrutga qarab komponentlarni dinamik yuklaydi va render qiladi.
3. **Havolalar (links)** foydalanuvchilarga sahifani toʻliq qayta yuklamasdan ilovangizdagi turli marshrutlar oʻrtasida harakatlanish imkonini beradi.

Bundan tashqari, Angular marshrutlash kutubxonasi quyidagi kabi qoʻshimcha imkoniyatlarni taqdim etadi:

- Ichma-ich (nested) marshrutlar
- Dasturiy navigatsiya
- Marshrut parametrlari, soʻrovlar (query) va wildcard'lar
- `ActivatedRoute` orqali faol marshrut haqidagi maʼlumot
- Marshrut resurslari va resolver'lar yordamida maʼlumot olish
- View oʻtish effektlari
- Navigatsiya himoyachilari (guards)

## Keyingi qadamlar {#next-steps}

[Angular router yordamida marshrutlarni qanday aniqlash](/guide/routing/define-routes) haqida bilib oling.
