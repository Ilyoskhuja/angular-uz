# Marshrutlarni aniqlash

Marshrutlar (routes) Angular ilovasida navigatsiyaning asosiy qurilish bloklari hisoblanadi.

## Marshrutlar nima? {#what-are-routes}

Angular'da **marshrut** — bu maʼlum bir URL yoʻli yoki namunasi (pattern) uchun qaysi komponent render qilinishini, shuningdek foydalanuvchi oʻsha URL'ga oʻtganda nima sodir boʻlishi haqidagi qoʻshimcha konfiguratsiya variantlarini belgilaydigan obyekt.

Marshrutning oddiy misoli:

```ts
import {AdminPage} from './app-admin';

const adminPage = {
  path: 'admin',
  component: AdminPage,
};
```

Bu marshrut uchun foydalanuvchi `/admin` yoʻliga kirganda ilova `AdminPage` komponentini koʻrsatadi.

### Ilovangizda marshrutlarni boshqarish {#managing-routes-in-your-application}

Koʻpchilik loyihalar marshrutlarni fayl nomida `routes` soʻzi boʻlgan alohida faylda aniqlaydi.

Marshrutlar toʻplami quyidagicha koʻrinadi:

```ts
import {Routes} from '@angular/router';
import {HomePage} from './home-page';
import {AdminPage} from './admin-page';

export const routes: Routes = [
  {
    path: '',
    component: HomePage,
  },
  {
    path: 'admin',
    component: AdminPage,
  },
];
```

TIP: Agar loyihani Angular CLI bilan yaratgan boʻlsangiz, marshrutlaringiz `src/app/app.routes.ts` faylida aniqlangan.

### Ilovangizga router qoʻshish {#adding-the-router-to-your-application}

Angular ilovasini Angular CLI'siz ishga tushirganda (bootstrap) `providers` massivini oʻz ichiga olgan konfiguratsiya obyektini uzatishingiz mumkin.

`providers` massivi ichida marshrutlaringiz bilan `provideRouter` funksiyasi chaqiruvini qoʻshib, ilovangizga Angular router'ini qoʻshishingiz mumkin.

```ts
import {ApplicationConfig} from '@angular/core';
import {provideRouter} from '@angular/router';

import {routes} from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    // ...
  ],
};
```

## Marshrut URL yoʻllari {#route-url-paths}

### Statik URL yoʻllari {#static-url-paths}

Statik URL yoʻllari — dinamik parametrlarga qarab oʻzgarmaydigan, oldindan belgilangan yoʻlli marshrutlar. Bular `path` satriga aynan mos keladigan va qatʼiy natijaga ega marshrutlardir.

Bunga misollar:

- "/admin"
- "/blog"
- "/settings/account"

### URL yoʻllarini marshrut parametrlari bilan aniqlash {#define-url-paths-with-route-parameters}

Parametrlangan URL'lar bir nechta URL'ni bitta komponentga yoʻnaltirib, URL'dagi parametrlarga qarab maʼlumotlarni dinamik koʻrsatish imkonini beruvchi dinamik yoʻllarni aniqlashga imkon beradi.

Bunday namunani marshrutingizning `path` satriga parametrlar qoʻshib va har bir parametr oldiga ikki nuqta (`:`) belgisini qoʻyib aniqlashingiz mumkin.

IMPORTANT: Parametrlar URL'ning [soʻrov satridagi (query string)](https://en.wikipedia.org/wiki/Query_string) maʼlumotlardan farq qiladi.
[Angular'dagi soʻrov parametrlari haqida ushbu qoʻllanmada](/guide/routing/read-route-state#query-parameters) koʻproq bilib oling.

Quyidagi misol URL orqali uzatilgan foydalanuvchi id'siga asoslanib foydalanuvchi profili komponentini koʻrsatadi.

```ts
import {Routes} from '@angular/router';
import {UserProfile} from './user-profile/user-profile';

const routes: Routes = [{path: 'user/:id', component: UserProfile}];
```

Bu misolda `/user/leeroy` va `/user/jenkins` kabi URL'lar `UserProfile` komponentini render qiladi. Keyin bu komponent `id` parametrini oʻqib, undan maʼlumotlarni olish kabi qoʻshimcha ishlarni bajarish uchun foydalanishi mumkin. Marshrut parametrlarini oʻqish tafsilotlari uchun [marshrut holatini oʻqish qoʻllanmasiga](/guide/routing/read-route-state) qarang.

Toʻgʻri marshrut parametri nomlari harf (a-z, A-Z) bilan boshlanishi va faqat quyidagilarni oʻz ichiga olishi mumkin:

- Harflar (a-z, A-Z)
- Raqamlar (0-9)
- Pastki chiziq (\_)
- Defis (-)

Shuningdek, bir nechta parametrli yoʻllarni ham aniqlashingiz mumkin:

```ts
import {Routes} from '@angular/router';
import {UserProfile} from './user-profile';
import {SocialMediaFeed} from './social-media-feed';

const routes: Routes = [
  {path: 'user/:id/:social-media', component: SocialMediaFeed},
  {path: 'user/:id', component: UserProfile},
];
```

Bu yangi yoʻl bilan foydalanuvchilar `/user/leeroy/youtube` va `/user/leeroy/bluesky` manzillariga kirib, leeroy foydalanuvchisi uchun parametrga mos ijtimoiy tarmoq lentalarini koʻrishi mumkin.

Marshrut parametrlarini oʻqish tafsilotlari uchun [Marshrut holatini oʻqish](/guide/routing/read-route-state) boʻlimiga qarang.

### Wildcard'lar {#wildcards}

Maʼlum bir yoʻl uchun barcha marshrutlarni ushlab olish kerak boʻlganda, yechim — ikki yulduzcha (`**`) bilan aniqlanadigan wildcard marshrut.

Keng tarqalgan misol — "Sahifa topilmadi" (Page Not Found) komponentini aniqlash.

```ts
import {Home} from './home/home';
import {UserProfile} from './user-profile';
import {NotFound} from './not-found';

const routes: Routes = [
  {path: 'home', component: Home},
  {path: 'user/:id', component: UserProfile},
  {path: '**', component: NotFound},
];
```

Bu marshrutlar massivida foydalanuvchi `home` va `user/:id` dan tashqari istalgan yoʻlga kirganda ilova `NotFound` komponentini koʻrsatadi.

TIP: Wildcard marshrutlar odatda marshrutlar massivining oxiriga joylashtiriladi.

## Angular URL'larni qanday moslashtiradi {#how-angular-matches-urls}

Marshrutlarni aniqlashda tartib muhim, chunki Angular "birinchi moslik gʻolib" strategiyasidan foydalanadi. Bu Angular URL'ni marshrut `path`'iga moslashtirgach, keyingi marshrutlarni tekshirishni toʻxtatishini anglatadi. Shu sababli aniqroq marshrutlarni doimo kamroq aniq marshrutlardan oldin joylashtiring.

Quyidagi misolda marshrutlar eng aniqdan eng kam aniqgacha tartibda aniqlangan:

```ts
const routes: Routes = [
  {path: '', component: Home}, // Empty path
  {path: 'users/new', component: NewUser}, // Static, most specific
  {path: 'users/:id', component: UserDetail}, // Dynamic
  {path: 'users', component: Users}, // Static, less specific
  {path: '**', component: NotFound}, // Wildcard - always last
];
```

Agar foydalanuvchi `/users/new` manziliga kirsa, Angular router quyidagi qadamlarni bosib oʻtadi:

1. `''` ni tekshiradi — mos kelmaydi
1. `users/new` ni tekshiradi — mos keldi! Shu yerda toʻxtaydi
1. `users/:id` mos kelishi mumkin boʻlsa ham, unga hech qachon yetib bormaydi
1. `users` ga hech qachon yetib bormaydi
1. `**` ga hech qachon yetib bormaydi

## Qayta yoʻnaltirishlar {#redirects}

Komponentni render qilish oʻrniga boshqa marshrutga qayta yoʻnaltiradigan (redirect) marshrutni aniqlashingiz mumkin:

```ts
import {Blog} from './home/blog';

const routes: Routes = [
  {
    path: 'articles',
    redirectTo: '/blog',
  },
  {
    path: 'blog',
    component: Blog,
  },
];
```

Agar marshrutni oʻzgartirsangiz yoki olib tashlasangiz, baʼzi foydalanuvchilar hali ham oʻsha marshrutga eskirgan havolalar yoki xatchoʻplar orqali kirishi mumkin. Bunday foydalanuvchilarni "topilmadi" sahifasi oʻrniga mos muqobil marshrutga yoʻnaltirish uchun qayta yoʻnaltirish qoʻshishingiz mumkin.

## Sahifa sarlavhalari {#page-titles}

Har bir marshrutga **sarlavha** (title) biriktirishingiz mumkin. Marshrut faollashganda Angular [sahifa sarlavhasini](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/title) avtomatik yangilaydi. Ilovangiz uchun doimo mos sahifa sarlavhalarini aniqlang, chunki bu sarlavhalar qulay (accessible) tajriba yaratish uchun zarur.

```ts
import {Routes} from '@angular/router';
import {Home} from './home';
import {About} from './about';
import {Products} from './products';

const routes: Routes = [
  {
    path: '',
    component: Home,
    title: 'Home Page',
  },
  {
    path: 'about',
    component: About,
    title: 'About Us',
  },
];
```

Sahifaning `title` xususiyatini [`ResolveFn`](/api/router/ResolveFn) yordamida resolver funksiyasiga dinamik ravishda oʻrnatish mumkin.

```ts
const titleResolver: ResolveFn<string> = (route) => route.queryParams['id'];
const routes: Routes = [
  // ...
  {
    path: 'products',
    component: Products,
    title: titleResolver,
  },
];
```

Marshrut sarlavhalarini [`TitleStrategy`](/api/router/TitleStrategy) abstrakt klassini kengaytiruvchi servis orqali ham oʻrnatish mumkin. Sukut boʻyicha Angular [`DefaultTitleStrategy`](/api/router/DefaultTitleStrategy)'dan foydalanadi.

### Sahifa sarlavhalari uchun TitleStrategy'dan foydalanish {#using-titlestrategy-for-page-titles}

Hujjat sarlavhasi qanday tuzilishini markazlashgan holda boshqarish kerak boʻlgan murakkab holatlar uchun `TitleStrategy`'ni implementatsiya qiling.

`TitleStrategy` — Angular ishlatadigan sukut boʻyicha sarlavha strategiyasini qayta belgilash uchun taqdim etishingiz (provide) mumkin boʻlgan token. Ilova suffiksini qoʻshish, sarlavhalarni breadcrumb'lardan shakllantirish yoki marshrut maʼlumotlaridan dinamik ravishda sarlavha yaratish kabi qoidalarni amalga oshirish uchun maxsus `TitleStrategy` taqdim etishingiz mumkin.

```ts
import {inject, Injectable} from '@angular/core';
import {Title} from '@angular/platform-browser';
import {TitleStrategy, RouterStateSnapshot} from '@angular/router';

@Injectable()
export class AppTitleStrategy extends TitleStrategy {
  private readonly title = inject(Title);

  updateTitle(snapshot: RouterStateSnapshot): void {
    // PageTitle is equal to the "Title" of a route if it's set
    // If its not set it will use the "title" given in index.html
    const pageTitle = this.buildTitle(snapshot) || this.title.getTitle();
    this.title.setTitle(`MyAwesomeApp - ${pageTitle}`);
  }
}
```

Maxsus strategiyadan foydalanish uchun uni ilova darajasida `TitleStrategy` tokeni bilan taqdim eting:

```ts
import {provideRouter, TitleStrategy} from '@angular/router';
import {AppTitleStrategy} from './app-title.strategy';

export const appConfig = {
  providers: [provideRouter(routes), {provide: TitleStrategy, useClass: AppTitleStrategy}],
};
```

## Bogʻliqliklarni inyeksiya qilish uchun marshrut darajasidagi provider'lar {#route-level-providers-for-dependency-injection}

Har bir marshrut [bogʻliqliklarni inyeksiya qilish](/guide/di) orqali oʻsha marshrut kontentiga bogʻliqliklarni taqdim etish imkonini beruvchi `providers` xususiyatiga ega.

Bu foydali boʻladigan keng tarqalgan holatlarga foydalanuvchi administrator yoki yoʻqligiga qarab turli servislarga ega ilovalar kiradi.

```ts
export const ROUTES: Route[] = [
  {
    path: 'admin',
    providers: [AdminService, {provide: ADMIN_API_KEY, useValue: '12345'}],
    children: [
      {path: 'users', component: AdminUsers},
      {path: 'teams', component: AdminTeams},
    ],
  },
  // ... other application routes that don't
  //     have access to ADMIN_API_KEY or AdminService.
];
```

Bu kod namunasida `admin` yoʻli faqat oʻz boʻlimidagi bolalarga mavjud boʻlgan `ADMIN_API_KEY` himoyalangan maʼlumot xususiyatini oʻz ichiga oladi. Natijada boshqa hech bir yoʻl `ADMIN_API_KEY` orqali taqdim etilgan maʼlumotlarga kira olmaydi.

Angular'da provider'lar va inyeksiya haqida koʻproq maʼlumot olish uchun [Bogʻliqliklarni inyeksiya qilish qoʻllanmasiga](/guide/di) qarang.

## Marshrutlarga maʼlumot biriktirish {#associating-data-with-routes}

Marshrut maʼlumotlari (route data) marshrutlarga qoʻshimcha axborot biriktirish imkonini beradi. Komponentlarning bu maʼlumotlarga qarab qanday ishlashini sozlashingiz mumkin.

Marshrut maʼlumotlari bilan ishlashning ikki usuli bor: oʻzgarmas qoladigan statik maʼlumotlar va ish vaqtidagi shartlarga qarab oʻzgarishi mumkin boʻlgan dinamik maʼlumotlar.

### Statik maʼlumotlar {#static-data}

Marshrutga xos metamaʼlumotlarni (masalan, analitika kuzatuvi, ruxsatlar va h.k.) markazlashtirish uchun `data` xususiyati orqali marshrutga istalgan statik maʼlumotlarni biriktirishingiz mumkin:

```ts
import {Routes} from '@angular/router';
import {Home} from './home';
import {About} from './about';
import {Products} from './products';

const routes: Routes = [
  {
    path: 'about',
    component: About,
    data: {analyticsId: '456'},
  },
  {
    path: '',
    component: Home,
    data: {analyticsId: '123'},
  },
];
```

Bu kod namunasida bosh sahifa va "about" sahifasi maʼlum `analyticsId` bilan sozlangan boʻlib, u keyinchalik tegishli komponentlarda sahifa kuzatuvi analitikasi uchun ishlatiladi.

Bu statik maʼlumotlarni `ActivatedRoute`'ni inyeksiya qilib oʻqishingiz mumkin. Tafsilotlar uchun [Marshrut holatini oʻqish](/guide/routing/read-route-state) boʻlimiga qarang.

### Resurslar va resolver'lar bilan dinamik maʼlumotlar {#dynamic-data-with-resources-and-resolvers}

Marshrut uchun maʼlumot olish kerak boʻlganda Angular Router reaktiv marshrut resurslarini ham, maʼlumot resolver'larini ham qoʻllab-quvvatlaydi:

- [Resurslar bilan maʼlumot olish](/guide/routing/data-fetching-with-resources): Angular Signals `Resource` API'lari yordamida maʼlumotlarni reaktiv tarzda oling.
- [Marshrut maʼlumot resolver'lari](/guide/routing/data-resolvers): Resolver funksiyalari yordamida marshrut faollashishidan oldin maʼlumotlarni oling.

## Ichki marshrutlar {#nested-routes}

Ichki (nested) marshrutlar, bola marshrutlar deb ham ataladi, komponentning URL'ga qarab oʻzgaradigan ichki koʻrinishi (sub-view) boʻlgan murakkabroq navigatsiya marshrutlarini boshqarishning keng tarqalgan usulidir.

<img alt="Ichki marshrutlarni tushuntiruvchi diagramma" src="assets/images/guide/router/nested-routing-diagram.svg">

Istalgan marshrut taʼrifiga `children` xususiyati bilan bola marshrutlar qoʻshishingiz mumkin:

```ts
const routes: Routes = [
  {
    path: 'product/:id',
    component: Product,
    children: [
      {
        path: 'info',
        component: ProductInfo,
      },
      {
        path: 'reviews',
        component: ProductReviews,
      },
    ],
  },
];
```

Yuqoridagi misol mahsulot sahifasi uchun marshrutni aniqlaydi, bu foydalanuvchiga URL'ga qarab mahsulot haqidagi maʼlumot yoki sharhlar koʻrsatilishini oʻzgartirish imkonini beradi.

`children` xususiyati `Route` obyektlari massivini qabul qiladi.

Bola marshrutlarni koʻrsatish uchun ota komponent (yuqoridagi misolda `Product`) oʻzining `<router-outlet>`'ini oʻz ichiga oladi.

```angular-html
<!-- Product -->
<article>
  <h1>Product {{ id }}</h1>
  <router-outlet />
</article>
```

Konfiguratsiyaga bola marshrutlarni qoʻshib va komponentga `<router-outlet>` qoʻshgandan soʻng, bola marshrutlarga mos URL'lar oʻrtasidagi navigatsiya faqat ichki outlet'ni yangilaydi.

## Keyingi qadamlar {#next-steps}

<docs-pill-row>
  <docs-pill href="/guide/routing/loading-strategies" title="Marshrutlarni yuklash strategiyalari"/>
  <docs-pill href="/guide/routing/show-routes-with-outlets" title="Marshrutlaringiz kontentini Outlet'lar bilan koʻrsatish"/>
</docs-pill-row>
