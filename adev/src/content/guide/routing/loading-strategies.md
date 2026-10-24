# Marshrutlarni yuklash strategiyalari

Angular marshrutlashida marshrutlar va komponentlar qanday va qachon yuklanishini tushunish tez javob beradigan veb-ilovalar yaratish uchun juda muhim. Angular yuklash xatti-harakatini boshqarish uchun ikkita asosiy strategiyani taklif qiladi:

1. **Darhol yuklanadigan (eagerly loaded)**: darhol yuklanadigan marshrutlar va komponentlar
2. **Kechiktirib yuklanadigan (lazily loaded)**: faqat kerak boʻlganda yuklanadigan marshrutlar va komponentlar

Har bir yondashuv turli holatlar uchun oʻziga xos afzalliklarga ega.

## Darhol yuklanadigan komponentlar {#eagerly-loaded-components}

Marshrutni [`component`](api/router/Route#component) xususiyati bilan aniqlaganingizda, koʻrsatilgan komponent marshrut konfiguratsiyasi bilan bir xil JavaScript bundle'ning qismi sifatida darhol yuklanadi.

```ts
import {Routes} from '@angular/router';
import {HomePage} from './components/home/home-page';
import {LoginPage} from './components/auth/login-page';

export const routes: Routes = [
  // HomePage and LoginPage are both directly referenced in this config,
  // so their code is eagerly included in the same JavaScript bundle as this file.
  {
    path: '',
    component: HomePage,
  },
  {
    path: 'login',
    component: LoginPage,
  },
];
```

Marshrut komponentlarini shu tarzda darhol yuklash brauzer bu komponentlarning barcha JavaScript kodini sahifaning dastlabki yuklanishi doirasida yuklab olishi va tahlil qilishi kerakligini anglatadi, lekin bunda komponentlar Angular uchun darhol tayyor boʻladi.

Dastlabki sahifa yuklanishiga koʻproq JavaScript kiritish dastlabki yuklanish vaqtini sekinlashtirsa-da, bu foydalanuvchi ilova boʻylab harakatlanganda yanada uzluksiz oʻtishlarga olib kelishi mumkin.

## Kechiktirib yuklanadigan komponentlar va marshrutlar {#lazily-loaded-components-and-routes}

Komponentning JavaScript kodini oʻsha marshrut faol boʻladigan paytda kechiktirib yuklash uchun [`loadComponent`](api/router/Route#loadComponent) xususiyatidan foydalanishingiz mumkin. [`loadChildren`](api/router/Route#loadChildren) xususiyati marshrutlarni moslashtirish vaqtida bola marshrutlarni kechiktirib yuklaydi.

```ts
import {Routes} from '@angular/router';

export const routes: Routes = [
  {
    path: 'login',
    loadComponent: () => import('./components/auth/login-page'),
  },
  {
    path: 'admin',
    loadComponent: () => import('./admin/admin.component'),
    loadChildren: () => import('./admin/admin.routes'),
  },
];
```

[`loadComponent`](/api/router/Route#loadComponent) va [`loadChildren`](/api/router/Route#loadChildren) xususiyatlari mos ravishda Angular komponentiga yoki marshrutlar toʻplamiga yechiladigan (resolve) Promise qaytaruvchi yuklovchi funksiyani qabul qiladi. Koʻp hollarda bu funksiya standart [JavaScript dinamik import API](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/import)'sidan foydalanadi. Biroq siz istalgan asinxron yuklovchi funksiyadan foydalanishingiz mumkin.

Agar kechiktirib yuklanadigan fayl `default` eksportdan foydalansa, eksport qilingan klassni tanlash uchun qoʻshimcha `.then` chaqiruvisiz `import()` promise'ini toʻgʻridan-toʻgʻri qaytarishingiz mumkin.

Marshrutlarni kechiktirib yuklash dastlabki bundle'dan JavaScript'ning katta qismlarini olib tashlash orqali Angular ilovangizning yuklanish tezligini sezilarli darajada yaxshilashi mumkin. Kodingizning bu qismlari alohida JavaScript "chunk"lariga kompilyatsiya qilinadi va router ularni faqat foydalanuvchi tegishli marshrutga kirganda soʻraydi.

## Inyeksiya kontekstida kechiktirib yuklash {#injection-context-lazy-loading}

Router [`loadComponent`](/api/router/Route#loadComponent) va [`loadChildren`](/api/router/Route#loadChildren)'ni **joriy marshrutning inyeksiya kontekstida** bajaradi. Bu sizga ushbu yuklovchi funksiyalar ichida [`inject`](/api/core/inject)'ni chaqirib, oʻsha marshrutda eʼlon qilingan, ierarxik bogʻliqliklarni inyeksiya qilish orqali ota marshrutlardan meros olingan yoki global mavjud provider'larga murojaat qilish imkonini beradi. Bu kontekstga bogʻliq kechiktirib yuklashni taʼminlaydi.

```ts
import {Routes} from '@angular/router';
import {inject} from '@angular/core';
import {FeatureFlags} from './feature-flags';

export const routes: Routes = [
  {
    path: 'dashboard',
    // Runs inside the route's injection context
    loadComponent: () => {
      const flags = inject(FeatureFlags);
      return flags.isPremium
        ? import('./dashboard/premium-dashboard')
        : import('./dashboard/basic-dashboard');
    },
  },
];
```

## Darhol yuklanadigan yoki kechiktirib yuklanadigan marshrutdan foydalanishim kerakmi? {#should-i-use-an-eager-or-a-lazy-route}

Marshrut darhol yoki kechiktirib yuklanishi kerakligini hal qilishda eʼtiborga olish kerak boʻlgan koʻplab omillar bor.

Umuman olganda, asosiy kirish sahifa(lar)i uchun darhol yuklash tavsiya etiladi, boshqa sahifalar esa kechiktirib yuklanadi.

NOTE: Kechiktirib yuklanadigan marshrutlar foydalanuvchi soʻraydigan dastlabki maʼlumotlar hajmini kamaytirish orqali boshlangʻich unumdorlik afzalligini bersa-da, bu kelajakda nomaqbul boʻlishi mumkin boʻlgan qoʻshimcha maʼlumot soʻrovlarini qoʻshadi. Bu, ayniqsa, bir necha darajadagi ichma-ich kechiktirib yuklash bilan ishlashda yaqqol namoyon boʻladi va unumdorlikka sezilarli taʼsir qilishi mumkin.

## Keyingi qadamlar {#next-steps}

[Marshrutlaringiz kontentini Outlet'lar yordamida koʻrsatish](/guide/routing/show-routes-with-outlets)ni qanday amalga oshirishni bilib oling.
