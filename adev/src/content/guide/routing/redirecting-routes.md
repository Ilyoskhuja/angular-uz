# Marshrutlarni yoʻnaltirish

Marshrut yoʻnaltirishlari (redirect) foydalanuvchilarni bir marshrutdan boshqasiga avtomatik oʻtkazish imkonini beradi. Buni pochta yoʻnaltirishiga oʻxshatish mumkin: bir manzilga moʻljallangan xat boshqa manzilga yuboriladi. Bu eski URL'lar bilan ishlash, sukut boʻyicha marshrutlarni amalga oshirish yoki kirishni boshqarish uchun foydali.

## Yoʻnaltirishlarni qanday sozlash {#how-to-configure-redirects}

Yoʻnaltirishlarni marshrut konfiguratsiyangizda `redirectTo` xususiyati bilan aniqlashingiz mumkin. Bu xususiyat satr qabul qiladi.

```ts
import {Routes} from '@angular/router';

const routes: Routes = [
  // Simple redirect
  {path: 'marketing', redirectTo: 'newsletter'},

  // Redirect with path parameters
  {path: 'legacy-user/:id', redirectTo: 'users/:id'},

  // Redirect any other URLs that don’t match
  // (also known as a "wildcard" redirect)
  {path: '**', redirectTo: '/login'},
];
```

Bu misolda uchta yoʻnaltirish bor:

1. Foydalanuvchi `/marketing` yoʻliga kirganda, u `/newsletter`'ga yoʻnaltiriladi.
2. Foydalanuvchi istalgan `/legacy-user/:id` yoʻliga kirganda, u tegishli `/users/:id` yoʻliga oʻtkaziladi.
3. Foydalanuvchi router'da aniqlanmagan istalgan yoʻlga kirganda, `**` wildcard yoʻli aniqlanishi sababli u login sahifasiga yoʻnaltiriladi.

## `pathMatch`'ni tushunish {#understanding-pathmatch}

Marshrutlardagi `pathMatch` xususiyati dasturchilarga Angular URL'ni marshrutlarga qanday moslashtirishini boshqarish imkonini beradi.

`pathMatch` ikkita qiymatni qabul qiladi:

| Qiymat     | Tavsif                                              |
| ---------- | --------------------------------------------------- |
| `'full'`   | Butun URL yoʻli aniq mos kelishi kerak              |
| `'prefix'` | Faqat URL'ning boshlanishi mos kelishi kifoya       |

Sukut boʻyicha barcha yoʻnaltirishlar `prefix` strategiyasidan foydalanadi.

### `pathMatch: 'prefix'`

`pathMatch: 'prefix'` — sukut boʻyicha strategiya boʻlib, yoʻnaltirishni ishga tushirishda Angular Router barcha keyingi marshrutlarni moslashtirishini istaganingizda ideal.

```ts
export const routes: Routes = [
  // This redirect route is equivalent to…
  {path: 'news', redirectTo: 'blog'},

  // This explicitly defined route redirect pathMatch
  {path: 'news', redirectTo: 'blog', pathMatch: 'prefix'},
];
```

Bu misolda `news` prefiksiga ega barcha marshrutlar oʻzlarining `/blog` ekvivalentlariga yoʻnaltiriladi. Foydalanuvchilar eski `news` prefiksiga kirganda yoʻnaltirilishiga baʼzi misollar:

- `/news` → `/blog`'ga yoʻnaltiriladi
- `/news/article` → `/blog/article`'ga yoʻnaltiriladi
- `/news/article/:id` → `/blog/article/:id`'ga yoʻnaltiriladi

### `pathMatch: 'full'`

Boshqa tomondan, `pathMatch: 'full'` Angular Router faqat muayyan yoʻlni yoʻnaltirishini istaganingizda foydali.

```ts
export const routes: Routes = [{path: '', redirectTo: '/dashboard', pathMatch: 'full'}];
```

Bu misolda foydalanuvchi ildiz URL'ga (yaʼni `''`) kirganda, router oʻsha foydalanuvchini `'/dashboard'` sahifasiga yoʻnaltiradi.

Keyingi barcha sahifalar (masalan, `/login`, `/about`, `/product/id` va h.k.) eʼtiborga olinmaydi va yoʻnaltirishni ishga tushirmaydi.

TIP: Ildiz sahifada (yaʼni `"/"` yoki `""`) yoʻnaltirishni sozlashda ehtiyot boʻling. Agar `pathMatch: 'full'` ni oʻrnatmasangiz, router barcha URL'larni yoʻnaltiradi.

Buni yanada yaqqolroq koʻrsatish uchun, agar oldingi boʻlimdagi `news` misoli oʻrniga `pathMatch: 'full'` ishlatilsa:

```ts
export const routes: Routes = [{path: 'news', redirectTo: '/blog', pathMatch: 'full'}];
```

Bu quyidagilarni anglatadi:

1. Faqat `/news` yoʻli `/blog`'ga yoʻnaltiriladi.
2. `/news/articles` yoki `/news/articles/1` kabi keyingi segmentlar yangi `/blog` prefiksi bilan yoʻnaltirilmaydi.

## Shartli yoʻnaltirishlar {#conditional-redirects}

Foydalanuvchilar qanday yoʻnaltirilishiga mantiq qoʻshish uchun `redirectTo` xususiyati funksiyani ham qabul qilishi mumkin.

[Funksiya](api/router/RedirectFunction) [`ActivatedRouteSnapshot`](api/router/ActivatedRouteSnapshot) maʼlumotlarining faqat bir qismiga kirish huquqiga ega, chunki baʼzi maʼlumotlar marshrutlarni moslashtirish bosqichida aniq maʼlum boʻlmaydi. Misollar: resolve qilingan sarlavhalar, kechiktirib yuklanadigan komponentlar va h.k.

U odatda satr yoki [`URLTree`](api/router/UrlTree) qaytaradi, lekin observable yoki promise ham qaytarishi mumkin.

Quyida foydalanuvchi kun vaqtiga qarab turli menyuga yoʻnaltiriladigan misol keltirilgan:

```ts
import {Routes} from '@angular/router';
import {Menu} from './menu';

export const routes: Routes = [
  {
    path: 'restaurant/:location/menu',
    pathMatch: 'full',
    redirectTo: (activatedRouteSnapshot) => {
      const location = activatedRouteSnapshot.params['location'];
      const currentHour = new Date().getHours();

      // Check if user requested a specific meal via query parameter
      if (activatedRouteSnapshot.queryParams['meal']) {
        return `/restaurant/${location}/menu/${activatedRouteSnapshot.queryParams['meal']}`;
      }

      // Auto-redirect based on time of day
      if (currentHour >= 5 && currentHour < 11) {
        return `/restaurant/${location}/menu/breakfast`;
      } else if (currentHour >= 11 && currentHour < 17) {
        return `/restaurant/${location}/menu/lunch`;
      } else {
        return `/restaurant/${location}/menu/dinner`;
      }
    },
  },

  // Destination routes
  {path: 'restaurant/:location/menu/breakfast', component: Menu},
  {path: 'restaurant/:location/menu/lunch', component: Menu},
  {path: 'restaurant/:location/menu/dinner', component: Menu},

  // Default redirect
  {path: '', redirectTo: '/restaurant/downtown/menu', pathMatch: 'full'},
];
```

Koʻproq bilish uchun [RedirectFunction API hujjatlariga](api/router/RedirectFunction) qarang.

## Keyingi qadamlar {#next-steps}

`redirectTo` xususiyati haqida koʻproq maʼlumot olish uchun [API hujjatlariga](api/router/Route#redirectTo) qarang.
