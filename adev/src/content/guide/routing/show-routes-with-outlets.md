# Marshrutlarni outlet'lar bilan koʻrsatish

`RouterOutlet` direktivasi — router joriy URL uchun komponentni qayerda render qilishi kerakligini belgilovchi toʻldiruvchi (placeholder).

```html
<app-header />
<!-- Angular inserts your route content here -->
<router-outlet />
<app-footer />
```

```ts
import {Component} from '@angular/core';
import {RouterOutlet} from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {}
```

Bu misolda, agar ilovada quyidagi marshrutlar aniqlangan boʻlsa:

```ts
import {Routes} from '@angular/router';
import {Home} from './home';
import {Products} from './products';

const routes: Routes = [
  {
    path: '',
    component: Home,
    title: 'Home Page',
  },
  {
    path: 'products',
    component: Products,
    title: 'Our Products',
  },
];
```

Foydalanuvchi `/products`'ga kirganda Angular quyidagini render qiladi:

```angular-html
<app-header />
<app-products />
<app-footer />
```

Agar foydalanuvchi bosh sahifaga qaytsa, Angular quyidagini render qiladi:

```angular-html
<app-header />
<app-home />
<app-footer />
```

Marshrut koʻrsatilayotganda `<router-outlet>` elementi kelajakdagi navigatsiyalar uchun moʻljal nuqtasi sifatida DOM'da qoladi. Angular marshrutlangan kontentni outlet elementidan keyin darhol, uning qoʻshni (sibling) elementi sifatida joylashtiradi.

```angular-html
<!-- Contents of the component's template -->
<app-header />
<router-outlet />
<app-footer />
```

```angular-html
<!-- Content rendered on the page when the user visits /admin -->
<app-header />
<router-outlet />
<app-admin-page />
<app-footer />
```

## Bola marshrutlar bilan ichma-ich marshrutlar yaratish {#nesting-routes-with-child-routes}

Ilovangiz murakkablashgani sari ildiz komponentingizdan boshqa komponentga nisbatan boʻlgan marshrutlar yaratishni istashingiz mumkin. Bu URL oʻzgarganda foydalanuvchi butun sahifa yangilanganday his qilish oʻrniga ilovaning faqat bir qismi oʻzgaradigan tajribalar yaratish imkonini beradi.

Bunday ichma-ich marshrutlar bola marshrutlar (child routes) deb ataladi. Bu ilovangizga ikkinchi `<router-outlet>` qoʻshishingizni anglatadi, chunki u AppComponent'dagi `<router-outlet>`'ga qoʻshimcha boʻladi.

Bu misolda `Settings` komponenti foydalanuvchi tanloviga qarab kerakli panelni koʻrsatadi. Bola marshrutlarning oʻziga xos jihatlaridan biri shundaki, komponent koʻpincha oʻzining `<nav>` va `<router-outlet>`'iga ega boʻladi.

```angular-html
<h1>Settings</h1>
<nav>
  <ul>
    <li><a routerLink="profile">Profile</a></li>
    <li><a routerLink="security">Security</a></li>
  </ul>
</nav>
<router-outlet />
```

Bola marshrut har qanday boshqa marshrut kabi `path` va `component`'ga muhtoj. Yagona farq shundaki, bola marshrutlarni ota marshrut ichidagi children massiviga joylashtirasiz.

```ts
const routes: Routes = [
  {
    path: 'settings',
    component: Settings, // this is the component with the <router-outlet> in the template
    children: [
      {
        path: 'profile', // child route path
        component: Profile, // child route component that the router renders
      },
      {
        path: 'security',
        component: Security, // another child route component that the router renders
      },
    ],
  },
];
```

`routes` ham, `<router-outlet>` ham toʻgʻri sozlangach, ilovangiz endi ichma-ich marshrutlardan foydalanadi!

## Nomlangan outlet'lar bilan ikkilamchi marshrutlar {#secondary-routes-with-named-outlets}

Sahifalarda bir nechta outlet boʻlishi mumkin — qaysi kontent qaysi outlet'ga tegishli ekanini koʻrsatish uchun har bir outlet'ga nom berishingiz mumkin.

```angular-html
<app-header />
<router-outlet />
<router-outlet name="read-more" />
<router-outlet name="additional-actions" />
<app-footer />
```

Har bir outlet noyob nomga ega boʻlishi kerak. Nomni dinamik tarzda oʻrnatish yoki oʻzgartirish mumkin emas. Sukut boʻyicha nom `'primary'` boʻladi.

Angular outlet nomini har bir marshrutda aniqlangan `outlet` xususiyatiga moslashtiradi:

```ts
{
  path: 'user/:id',
  component: UserDetails,
  outlet: 'additional-actions'
}
```

## Outlet hayot sikli hodisalari {#outlet-lifecycle-events}

Router outlet yuborishi mumkin boʻlgan toʻrtta hayot sikli hodisasi bor:

| Hodisa       | Tavsif                                                                   |
| ------------ | ------------------------------------------------------------------------ |
| `activate`   | Yangi komponent nusxasi yaratilganda                                     |
| `deactivate` | Komponent yoʻq qilinganda                                                |
| `attach`     | `RouteReuseStrategy` outlet'ga pastki daraxtni biriktirishni buyurganda  |
| `detach`     | `RouteReuseStrategy` outlet'ga pastki daraxtni ajratishni buyurganda     |

Hodisa tinglovchilarini standart hodisa bogʻlash sintaksisi bilan qoʻshishingiz mumkin:

```angular-html
<router-outlet
  (activate)="onActivate($event)"
  (deactivate)="onDeactivate($event)"
  (attach)="onAttach($event)"
  (detach)="onDetach($event)"
/>
```

Koʻproq bilishni istasangiz, [RouterOutlet API hujjatlariga](/api/router/RouterOutlet?tab=api) qarang.

## Marshrutlangan komponentlarga kontekst maʼlumotlarini uzatish {#passing-contextual-data-to-routed-components}

Marshrutlangan komponentlarga kontekst maʼlumotlarini uzatish koʻpincha global holat yoki murakkab marshrut konfiguratsiyalarini talab qiladi. Buni osonlashtirish uchun har bir `RouterOutlet` `routerOutletData` input'ini qoʻllab-quvvatlaydi. Marshrutlangan komponentlar va ularning bolalari bu maʼlumotlarni `ROUTER_OUTLET_DATA` inyeksiya tokeni orqali signal sifatida oʻqishi mumkin, bu marshrut aniqlanishlarini oʻzgartirmasdan outlet'ga xos konfiguratsiya qilish imkonini beradi.

```angular-ts
import {Component} from '@angular/core';
import {RouterOutlet} from '@angular/router';

@Component({
  selector: 'app-dashboard',
  imports: [RouterOutlet],
  template: `
    <h2>Dashboard</h2>
    <router-outlet [routerOutletData]="{layout: 'sidebar'}" />
  `,
})
export class Dashboard {}
```

Marshrutlangan komponent taqdim etilgan outlet maʼlumotlarini `ROUTER_OUTLET_DATA` yordamida inyeksiya qilishi mumkin:

```angular-ts
import {Component, inject, Signal} from '@angular/core';
import {ROUTER_OUTLET_DATA} from '@angular/router';

@Component({
  selector: 'app-stats',
  template: `<p>Stats view (layout: {{ outletData().layout }})</p>`,
})
export class Stats {
  outletData = inject(ROUTER_OUTLET_DATA) as Signal<{layout: string}>;
}
```

Angular oʻsha outlet'da `Stats`'ni faollashtirganda, u inyeksiya qilingan maʼlumot sifatida `{ layout: 'sidebar' }` ni oladi.

NOTE: `routerOutletData` input'i oʻrnatilmagan boʻlsa, inyeksiya qilingan signalning qiymati sukut boʻyicha `undefined` boʻladi.

---

## Keyingi qadamlar {#next-steps}

Angular Router bilan [marshrutlarga oʻtish](/guide/routing/navigate-to-routes)ni qanday amalga oshirishni bilib oling.
