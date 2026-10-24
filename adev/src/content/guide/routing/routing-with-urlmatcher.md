# Maxsus marshrut mosliklarini yaratish

Angular Router foydalanuvchilarga ilovangiz boʻylab harakatlanishda yordam berish uchun ishlatishingiz mumkin boʻlgan kuchli moslashtirish (matching) strategiyasini qoʻllab-quvvatlaydi.
Bu moslashtirish strategiyasi statik marshrutlar, parametrli oʻzgaruvchan marshrutlar, wildcard marshrutlar va shu kabilarni qoʻllab-quvvatlaydi.
Shuningdek, URL'lar murakkabroq boʻlgan holatlar uchun oʻzingizning maxsus shablon moslashtirishingizni yaratishingiz mumkin.

Bu darslikda siz Angular'ning `UrlMatcher`'idan foydalanib maxsus marshrut moslashtiruvchisini (matcher) yaratasiz.
Bu moslashtiruvchi URL'da X (avvalgi Twitter) foydalanuvchi nomini (handle) qidiradi.

## Maqsadlar {#objectives}

Maxsus marshrut moslashtiruvchisini yaratish uchun Angular'ning `UrlMatcher`'ini amalga oshirish.

## Namuna ilova yaratish {#create-a-sample-application}

Angular CLI yordamida _angular-custom-route-match_ nomli yangi ilova yarating.
Angular ilovasining standart tuzilmasiga qoʻshimcha ravishda siz _profile_ komponentini ham yaratasiz.

1. _angular-custom-route-match_ nomli yangi Angular loyihasini yarating.

   ```shell
   ng new angular-custom-route-match
   ```

   `Would you like to add Angular routing?` soʻrovi chiqqanda `Y` ni tanlang.

   `Which stylesheet format would you like to use?` soʻrovi chiqqanda `CSS` ni tanlang.

   Bir necha lahzadan soʻng yangi `angular-custom-route-match` loyihasi tayyor boʻladi.

1. Terminalingizdan `angular-custom-route-match` katalogiga oʻting.
1. _profile_ komponentini yarating.

   ```shell
   ng generate component profile
   ```

1. Kod muharriringizda `profile.html` faylini topib, undagi toʻldiruvchi kontentni quyidagi HTML bilan almashtiring.

   <docs-code header="profile.html" path="adev/src/content/examples/routing-with-urlmatcher/src/app/profile/profile.html"/>

1. Kod muharriringizda `app.html` faylini topib, undagi toʻldiruvchi kontentni quyidagi HTML bilan almashtiring.

   <docs-code header="app.html" path="adev/src/content/examples/routing-with-urlmatcher/src/app/app.html"/>

## Ilovangiz uchun marshrutlarni sozlash {#configure-your-routes-for-your-application}

Ilova tuzilmasi tayyor boʻlgach, keyingi qadamda `app.config.ts` fayliga marshrutlash imkoniyatlarini qoʻshishingiz kerak.
Bu jarayon davomida siz URL'da X foydalanuvchi nomini qidiradigan maxsus URL moslashtiruvchisini yaratasiz.
Bu foydalanuvchi nomi oldidan keladigan `@` belgisi orqali aniqlanadi.

1. Kod muharriringizda `app.config.ts` faylini oching.
1. Angular'ning `provideRouter` va `withComponentInputBinding`'i, shuningdek ilova marshrutlari uchun `import` koʻrsatmasini qoʻshing.

   ```ts
   import {provideRouter, withComponentInputBinding} from '@angular/router';

   import {routes} from './app.routes';
   ```

1. Providers massiviga `provideRouter(routes, withComponentInputBinding())` koʻrsatmasini qoʻshing.

1. Ilova marshrutlariga quyidagi kodni qoʻshib, maxsus marshrut moslashtiruvchisini aniqlang.

   <docs-code header="app.routes.ts" path="adev/src/content/examples/routing-with-urlmatcher/src/app/app.routes.ts" region="matcher"/>

Bu maxsus moslashtiruvchi quyidagi vazifalarni bajaruvchi funksiyadir:

- Moslashtiruvchi massiv faqat bitta segmentdan iboratligini tekshiradi
- Moslashtiruvchi foydalanuvchi nomi formati mos kelishini taʼminlash uchun regulyar ifodadan foydalanadi
- Agar moslik boʻlsa, funksiya butun URL'ni qaytaradi va `username` marshrut parametrini yoʻlning qism satri (substring) sifatida aniqlaydi
- Agar moslik boʻlmasa, funksiya null qaytaradi va router URL'ga mos keladigan boshqa marshrutlarni qidirishda davom etadi

HELPFUL: Maxsus URL moslashtiruvchisi har qanday boshqa marshrut aniqlanishi kabi ishlaydi. Bola marshrutlarni yoki kechiktirib yuklanadigan marshrutlarni boshqa har qanday marshrutdagi kabi aniqlang.

## Marshrut parametrlarini oʻqish {#reading-the-route-parameters}

Maxsus moslashtiruvchi tayyor boʻlgach, endi `profile` komponentida marshrut parametrini bogʻlashingiz mumkin.

Kod muharriringizda `profile.ts` faylini oching va `username` parametriga mos keladigan `input` yarating.
Biz avvalroq `provideRouter`'ga `withComponentInputBinding` imkoniyatini qoʻshgan edik.
Bu `Router`'ga maʼlumotni toʻgʻridan-toʻgʻri marshrut komponentlariga bogʻlash imkonini beradi.

```ts
username = input.required<string>();
```

## Maxsus URL moslashtiruvchingizni sinab koʻrish {#test-your-custom-url-matcher}

Kodingiz tayyor boʻlgach, endi maxsus URL moslashtiruvchingizni sinab koʻrishingiz mumkin.

1. Terminal oynasidan `ng serve` buyrugʻini ishga tushiring.

   ```shell
   ng serve
   ```

1. Brauzerda `http://localhost:4200` manzilini oching.

   Siz `Navigate to my profile` degan jumladan iborat bitta veb-sahifani koʻrishingiz kerak.

1. **my profile** havolasini bosing.

   Sahifada `Hello, Angular!` degan yangi jumla paydo boʻladi.

## Keyingi qadamlar {#next-steps}

Angular Router bilan shablon moslashtirish ilovangizda dinamik URL'lar boʻlganda sizga katta moslashuvchanlik beradi.
Angular Router haqida koʻproq bilish uchun quyidagi mavzularga qarang:

<docs-pill-row>
  <docs-pill href="guide/routing/common-router-tasks" title="Ilova ichida marshrutlash va navigatsiya"/>
  <docs-pill href="api/router/Router" title="Router API"/>
</docs-pill-row>

HELPFUL: Bu kontent [Brandon Roberts](https://x.com/brandontroberts) tomonidan yozilgan [Custom Route Matching with the Angular Router](https://medium.com/@brandontroberts/custom-route-matching-with-the-angular-router-fbdd48665483) maqolasiga asoslangan.
