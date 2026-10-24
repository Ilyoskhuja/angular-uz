# Marshrut holatini oʻqish

Angular Router sizga moslashuvchan va kontekstni hisobga oluvchi komponentlar yaratish uchun marshrut (route) bilan bogʻliq maʼlumotlarni oʻqish va ulardan foydalanish imkonini beradi.

## ActivatedRoute yordamida joriy marshrut haqida maʼlumot olish {#get-information-about-the-current-route-with-activatedroute}

`ActivatedRoute` — `@angular/router` paketidagi servis boʻlib, joriy marshrut bilan bogʻliq barcha maʼlumotlarni taqdim etadi.

```angular-ts
import {Component, inject} from '@angular/core';
import {ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-product',
})
export class Product {
  private activatedRoute = inject(ActivatedRoute);

  constructor() {
    console.log(this.activatedRoute);
  }
}
```

`ActivatedRoute` marshrut haqida turli maʼlumotlarni taqdim eta oladi. Keng tarqalgan xususiyatlardan baʼzilari:

| Xususiyat     | Tafsilotlar                                                                                                                                  |
| :------------ | :------------------------------------------------------------------------------------------------------------------------------------------- |
| `url`         | Marshrut yoʻllarining `Observable`'i; marshrut yoʻlining har bir qismi uchun `UrlSegment` obyektlari massivi koʻrinishida ifodalanadi.        |
| `data`        | Marshrut uchun berilgan `data` obyektini oʻz ichiga olgan `Observable`. Shuningdek, resolve guard'dan olingan (resolved) qiymatlarni ham saqlaydi. |
| `params`      | Marshrutga xos majburiy va ixtiyoriy parametrlarni oʻz ichiga olgan `Observable`.                                                             |
| `queryParams` | Barcha marshrutlar uchun mavjud boʻlgan soʻrov parametrlarini (query parameters) oʻz ichiga olgan `Observable`.                               |
| `resources`   | Marshrutda aniqlangan `Resource` nusxalarining ixtiyoriy yozuvi (`withRouterResources` yoqilgan boʻlsa).                                      |

Marshrut ichida nimalarga murojaat qila olishingizning toʻliq roʻyxati uchun [`ActivatedRoute` API hujjatlariga](/api/router/ActivatedRoute) qarang.

## Marshrut snapshot'larini tushunish {#understanding-route-snapshots}

Sahifa navigatsiyalari vaqt davomida yuz beradigan hodisalardir va siz marshrut snapshot'ini olish orqali router holatiga maʼlum bir vaqtda murojaat qilishingiz mumkin.

Marshrut snapshot'lari marshrut haqidagi asosiy maʼlumotlarni, jumladan uning parametrlari, maʼlumotlari va bola marshrutlarini oʻz ichiga oladi. Bundan tashqari, snapshot'lar statik boʻlib, kelajakdagi oʻzgarishlarni aks ettirmaydi.

Marshrut snapshot'iga qanday murojaat qilishingizga misol:

```angular-ts
import {Component, inject} from '@angular/core';
import {ActivatedRoute} from '@angular/router';

@Component(/* ... */)
export class UserProfile {
  readonly userId: string | null;
  private route = inject(ActivatedRoute);

  constructor() {
    // Example URL: https://www.angular.dev/users/123?role=admin&status=active#contact

    // Access route parameters from snapshot
    this.userId = this.route.snapshot.paramMap.get('id');

    // Access multiple route elements
    const snapshot = this.route.snapshot;
    console.log({
      url: snapshot.url, // Array of UrlSegments matched by this route
      // Route parameters object: {id: '123'}
      params: snapshot.params,
      // Query parameters object: {role: 'admin', status: 'active'}
      queryParams: snapshot.queryParams, // Query parameters
    });
  }
}
```

Murojaat qilishingiz mumkin boʻlgan barcha xususiyatlarning toʻliq roʻyxati uchun [`ActivatedRoute` API hujjatlari](/api/router/ActivatedRoute) va [`ActivatedRouteSnapshot` API hujjatlariga](/api/router/ActivatedRouteSnapshot) qarang.

## Marshrutdagi parametrlarni oʻqish {#reading-parameters-on-a-route}

Dasturchilar marshrutdan foydalanishi mumkin boʻlgan parametrlarning ikki turi mavjud: marshrut parametrlari va soʻrov parametrlari.

### Marshrut parametrlari {#route-parameters}

Marshrut parametrlari komponentga URL orqali maʼlumot uzatish imkonini beradi. Bu URL'dagi identifikator, masalan, foydalanuvchi ID'si yoki mahsulot ID'si asosida muayyan kontentni koʻrsatmoqchi boʻlganingizda foydalidir.

Parametr nomi oldiga ikki nuqta (`:`) qoʻyish orqali [marshrut parametrlarini aniqlashingiz](/guide/routing/define-routes#define-url-paths-with-route-parameters) mumkin.

```angular-ts
import {Routes} from '@angular/router';
import {Product} from './product';

const routes: Routes = [{path: 'product/:id', component: Product}];
```

Parametrlarga `route.params`'ga obuna boʻlish orqali murojaat qilishingiz mumkin.

```angular-ts
import {Component, inject, signal} from '@angular/core';
import {ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-product-detail',
  template: `<h1>Product Details: {{ productId() }}</h1>`,
})
export class ProductDetail {
  productId = signal('');
  private activatedRoute = inject(ActivatedRoute);

  constructor() {
    // Access route parameters
    this.activatedRoute.params.subscribe((params) => {
      this.productId.set(params['id']);
    });
  }
}
```

### Soʻrov parametrlari {#query-parameters}

[Soʻrov parametrlari](https://developer.mozilla.org/en-US/docs/Web/API/URLSearchParams) marshrut tuzilmasiga taʼsir qilmasdan URL orqali ixtiyoriy maʼlumotlarni uzatishning moslashuvchan usulini taqdim etadi. Marshrut parametrlaridan farqli oʻlaroq, soʻrov parametrlari navigatsiya hodisalari davomida saqlanib qolishi mumkin va filtrlash, saralash, sahifalash (pagination) va boshqa holatga ega UI elementlarini boshqarish uchun juda mos keladi.

```angular-ts
// Single parameter structure
// /products?category=electronics
router.navigate(['/products'], {
  queryParams: {category: 'electronics'},
});

// Multiple parameters
// /products?category=electronics&sort=price&page=1
router.navigate(['/products'], {
  queryParams: {
    category: 'electronics',
    sort: 'price',
    page: 1,
  },
});
```

Soʻrov parametrlariga `route.queryParams` orqali murojaat qilishingiz mumkin.

Quyida mahsulotlar roʻyxatini qanday koʻrsatishiga taʼsir qiluvchi soʻrov parametrlarini yangilaydigan `ProductList` misoli keltirilgan:

```angular-ts
import {Component, inject} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';

@Component({
  selector: 'app-product-list',
  template: `
    <div>
      <select (change)="updateSort($event)">
        <option value="price">Price</option>
        <option value="name">Name</option>
      </select>
      <!-- Products list -->
    </div>
  `,
})
export class ProductList {
  private route = inject(ActivatedRoute);
  private router = inject(Router);

  constructor() {
    // Access query parameters reactively
    this.route.queryParams.subscribe((params) => {
      const sort = params['sort'] || 'price';
      const page = Number(params['page']) || 1;
      this.loadProducts(sort, page);
    });
  }

  updateSort(event: Event) {
    const sort = (event.target as HTMLSelectElement).value;
    // Update URL with new query parameter
    this.router.navigate([], {
      queryParams: {sort},
      queryParamsHandling: 'merge', // Preserve other query parameters
    });
  }
}
```

Bu misolda foydalanuvchilar mahsulotlar roʻyxatini nomi yoki narxi boʻyicha saralash uchun select elementidan foydalanishi mumkin. Tegishli change ishlov beruvchisi URL'ning soʻrov parametrlarini yangilaydi, bu esa oʻz navbatida yangilangan soʻrov parametrlarini oʻqib, mahsulotlar roʻyxatini yangilay oladigan oʻzgarish hodisasini ishga tushiradi.

Koʻproq maʼlumot uchun [QueryParamsHandling boʻyicha rasmiy hujjatlarga](/api/router/QueryParamsHandling) qarang.

### Matritsa parametrlari {#matrix-parameters}

Matritsa parametrlari (matrix parameters) — butun marshrutga emas, balki URL'ning muayyan segmentiga tegishli boʻlgan ixtiyoriy parametrlar. `?` belgisidan keyin keladigan va global qoʻllaniladigan soʻrov parametrlaridan farqli oʻlaroq, matritsa parametrlari nuqtali vergul (`;`) ishlatadi va alohida yoʻl segmentlari doirasida amal qiladi.

Matritsa parametrlari marshrut taʼrifiga yoki moslashtirish xatti-harakatiga taʼsir qilmasdan muayyan marshrut segmentiga yordamchi maʼlumot uzatish kerak boʻlganda foydalidir. Soʻrov parametrlari kabi, ularni marshrut konfiguratsiyasida aniqlash shart emas.

```ts
// URL format: /path;key=value
// Multiple parameters: /path;key1=value1;key2=value2

// Navigate with matrix parameters
this.router.navigate(['/awesome-products', {view: 'grid', filter: 'new'}]);
// Results in URL: /awesome-products;view=grid;filter=new
```

**ActivatedRoute'dan foydalanish**

```ts
import {Component, inject} from '@angular/core';
import {ActivatedRoute} from '@angular/router';

@Component(/* ... */)
export class AwesomeProducts {
  private route = inject(ActivatedRoute);

  constructor() {
    // Access matrix parameters via params
    this.route.params.subscribe((params) => {
      const view = params['view']; // e.g., 'grid'
      const filter = params['filter']; // e.g., 'new'
    });
  }
}
```

NOTE: `ActivatedRoute`'dan foydalanishga muqobil sifatida, `withComponentInputBinding` ishlatilganda matritsa parametrlari komponent input'lariga ham bogʻlanadi.

## RouterLinkActive yordamida faol joriy marshrutni aniqlash {#detect-active-current-route-with-routerlinkactive}

Joriy faol marshrutga qarab navigatsiya elementlariga dinamik stil berish uchun `RouterLinkActive` direktivasidan foydalanishingiz mumkin. Bu navigatsiya elementlarida foydalanuvchilarga qaysi marshrut faol ekanini bildirish uchun keng qoʻllaniladi.

```angular-html
<nav>
  <a
    class="button"
    routerLink="/about"
    routerLinkActive="active-button"
    ariaCurrentWhenActive="page"
  >
    About
  </a>
  |
  <a
    class="button"
    routerLink="/settings"
    routerLinkActive="active-button"
    ariaCurrentWhenActive="page"
  >
    Settings
  </a>
</nav>
```

Bu misolda URL tegishli `routerLink`'ga mos kelganda Angular Router toʻgʻri anchor havolasiga `active-button` klassini qoʻllaydi va `ariaCurrentWhenActive`'ni `page` qiymatiga oʻrnatadi.

Elementga bir nechta klass qoʻshishingiz kerak boʻlsa, boʻshliq bilan ajratilgan satrdan yoki massivdan foydalanishingiz mumkin:

```angular-html
<!-- Space-separated string syntax -->
<a routerLink="/user/bob" routerLinkActive="class1 class2">Bob</a>

<!-- Array syntax -->
<a routerLink="/user/bob" [routerLinkActive]="['class1', 'class2']">Bob</a>
```

Faqat `routerLinkActive`'ni oʻrnatish `aria-current`'ni oʻrnatmaydi. Yuqoridagi misoldagi kabi `ariaCurrentWhenActive` input'ini oʻrnating, shunda koʻrish qobiliyati cheklangan foydalanuvchilar (qoʻllanilayotgan stil farqini sezmasligi mumkin) ham faol havolani aniqlay oladi.

### Marshrutni moslashtirish strategiyasi {#route-matching-strategy}

Sukut boʻyicha `RouterLinkActive` marshrutdagi har qanday ajdod (ancestor) marshrutni mos deb hisoblaydi.

```angular-html
<a [routerLink]="['/user/jane']" routerLinkActive="active-link"> User </a>
<a [routerLink]="['/user/jane/role/admin']" routerLinkActive="active-link"> Role </a>
```

Foydalanuvchi `/user/jane/role/admin` manziliga kirganda ikkala havola ham `active-link` klassiga ega boʻladi.

### RouterLinkActive'ni faqat aniq mos kelgan marshrutlarga qoʻllash {#only-apply-routerlinkactive-on-exact-route-matches}

Klassni faqat aniq moslikda qoʻllamoqchi boʻlsangiz, `routerLinkActiveOptions` direktivasiga `exact: true` qiymatini oʻz ichiga olgan konfiguratsiya obyektini berishingiz kerak.

```angular-html
<a
  [routerLink]="['/user/jane']"
  routerLinkActive="active-link"
  [routerLinkActiveOptions]="{exact: true}"
>
  User
</a>
<a
  [routerLink]="['/user/jane/role/admin']"
  routerLinkActive="active-link"
  [routerLinkActiveOptions]="{exact: true}"
>
  Role
</a>
```

Marshrutning qanday moslashtirilishini yanada aniqroq boshqarmoqchi boʻlsangiz, shuni taʼkidlash joizki, `exact: true` aslida moslashtirish variantlarining toʻliq toʻplami uchun sintaktik qisqartma (syntactic sugar) hisoblanadi:

```angular-ts
// `exact: true` is equivalent to
{
  paths: 'exact',
  fragment: 'ignored',
  matrixParams: 'ignored',
  queryParams: 'exact',
}

// `exact: false` is equivalent
{
  paths: 'subset',
  fragment: 'ignored',
  matrixParams: 'ignored',
  queryParams: 'subset',
}
```

Koʻproq maʼlumot uchun [isActiveMatchOptions](/api/router/IsActiveMatchOptions) boʻyicha rasmiy hujjatlarga qarang.

### RouterLinkActive'ni ajdod elementga qoʻllash {#apply-routerlinkactive-to-an-ancestor}

RouterLinkActive direktivasini dasturchilar elementlarga oʻzlari istagandek stil bera olishi uchun ajdod elementga ham qoʻllash mumkin.

```angular-html
<div routerLinkActive="active-link" [routerLinkActiveOptions]="{exact: true}">
  <a routerLink="/user/jim">Jim</a>
  <a routerLink="/user/bob">Bob</a>
</div>
```

Koʻproq maʼlumot uchun [RouterLinkActive API hujjatlariga](/api/router/RouterLinkActive) qarang.

## URL faol ekanini tekshirish {#check-if-a-url-is-active}

`isActive` funksiyasi berilgan URL hozirda router'da faol ekanini kuzatuvchi computed signal qaytaradi. Router holati oʻzgarganda signal avtomatik yangilanadi.

```angular-ts
import {Component, inject} from '@angular/core';
import {isActive, Router} from '@angular/router';

@Component({
  template: `
    <div [class.active]="isSettingsActive()">
      <h2>Settings</h2>
    </div>
  `,
})
export class Panel {
  private router = inject(Router);

  isSettingsActive = isActive('/settings', this.router, {
    paths: 'subset',
    queryParams: 'ignored',
    fragment: 'ignored',
    matrixParams: 'ignored',
  });
}
```
