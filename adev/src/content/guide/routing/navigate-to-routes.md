# Marshrutlarga navigatsiya qilish

RouterLink direktivasi — Angular'ning navigatsiyaga deklarativ yondashuvi. U Angular'ning marshrutlash tizimi bilan uzviy integratsiyalashgan standart anchor elementlaridan (`<a>`) foydalanish imkonini beradi.

## RouterLink'dan qanday foydalanish {#how-to-use-routerlink}

Angular marshrutlashidan foydalanish uchun `href` atributli odatiy `<a>` anchor elementlari oʻrniga tegishli yoʻl (path) koʻrsatilgan RouterLink direktivasini qoʻshasiz.

```angular-ts
import {RouterLink} from '@angular/router';

@Component({
  template: `
    <nav>
      <a routerLink="/user-profile">User profile</a>
      <a routerLink="/settings">Settings</a>
    </nav>
  `,
  imports: [RouterLink],
  ...
})
export class App {}
```

### Absolyut yoki nisbiy havolalardan foydalanish {#using-absolute-or-relative-links}

Angular marshrutlashida **nisbiy URL'lar** navigatsiya yoʻllarini joriy marshrutning joylashuviga nisbatan aniqlash imkonini beradi. Bu protokol (masalan, `http://`) va **asosiy domen** (masalan, `google.com`) bilan toʻliq yoʻlni oʻz ichiga olgan **absolyut URL'lar**dan farq qiladi.

```angular-html
<!-- Absolute URL -->
<a href="https://www.angular.dev/essentials">Angular Essentials Guide</a>

<!-- Relative URL -->
<a href="/essentials">Angular Essentials Guide</a>
```

Bu misolda birinchi misol asoslar sahifasi uchun protokol (yaʼni `https://`) va asosiy domen (yaʼni `angular.dev`) aniq koʻrsatilgan toʻliq yoʻlni oʻz ichiga oladi. Ikkinchi misol esa, aksincha, foydalanuvchi `/essentials` uchun toʻgʻri asosiy domenda allaqachon turganini nazarda tutadi.

Umuman olganda, nisbiy URL'larga afzallik beriladi, chunki ular marshrutlash ierarxiyasidagi oʻzining absolyut oʻrnini bilishi shart boʻlmagani uchun ilovalar boʻylab osonroq qoʻllab-quvvatlanadi.

### Nisbiy URL'lar qanday ishlaydi {#how-relative-urls-work}

Angular marshrutlashida nisbiy URL'larni aniqlash uchun ikkita sintaksis mavjud: satrlar va massivlar.

```angular-html
<!-- Navigates user to /dashboard -->
<a routerLink="dashboard">Dashboard</a>
<a [routerLink]="['dashboard']">Dashboard</a>
```

HELPFUL: Satr uzatish — nisbiy URL'larni aniqlashning eng keng tarqalgan usuli.

Nisbiy URL'da dinamik parametrlarni aniqlash kerak boʻlganda massiv sintaksisidan foydalaning:

```angular-html
<a [routerLink]="['user', currentUserId]">Current User</a>
```

Bundan tashqari, Angular marshrutlashi nisbiy yoʻl oldiga qiya chiziq (`/`) qoʻyilgan yoki qoʻyilmaganiga qarab yoʻlning joriy URL'ga yoki asosiy domenga nisbatan boʻlishini koʻrsatish imkonini beradi.

Masalan, foydalanuvchi `example.com/settings` sahifasida boʻlsa, turli holatlar uchun turli nisbiy yoʻllarni quyidagicha aniqlash mumkin:

```angular-html
<!-- Navigates to /settings/notifications -->
<a routerLink="notifications">Notifications</a>
<a routerLink="/settings/notifications">Notifications</a>

<!-- Navigates to /team/:teamId/user/:userId -->
<a routerLink="/team/123/user/456">User 456</a>
<a [routerLink]="['/team', teamId, 'user', userId]">Current User</a>
```

## Marshrutlarga dasturiy navigatsiya {#programmatic-navigation-to-routes}

`RouterLink` shablonlarda deklarativ navigatsiyani taʼminlasa, Angular mantiq, foydalanuvchi harakatlari yoki ilova holatiga asoslanib navigatsiya qilish kerak boʻlgan holatlar uchun dasturiy navigatsiyani ham taqdim etadi. `Router`'ni inyeksiya qilib, TypeScript kodingizda marshrutlarga dinamik navigatsiya qilishingiz, parametrlar uzatishingiz va navigatsiya xatti-harakatini boshqarishingiz mumkin.

### `router.navigate()`

URL yoʻli massivini koʻrsatib, marshrutlar oʻrtasida dasturiy navigatsiya qilish uchun `router.navigate()` metodidan foydalanishingiz mumkin.

```angular-ts
import {Router} from '@angular/router';

@Component({
  selector: 'app-dashboard',
  template: ` <button (click)="navigateToProfile()">View Profile</button> `,
})
export class AppDashboard {
  private router = inject(Router);

  navigateToProfile() {
    // Standard navigation
    this.router.navigate(['/profile']);

    // With route parameters
    this.router.navigate(['/users', userId]);

    // With query parameters
    this.router.navigate(['/search'], {
      queryParams: {category: 'books', sort: 'price'},
    });

    // With matrix parameters
    this.router.navigate(['/products', {featured: true, onSale: true}]);
  }
}
```

`router.navigate()` oddiy va murakkab marshrutlash holatlarining ikkalasini ham qoʻllab-quvvatlaydi va marshrut parametrlarini, [soʻrov parametrlarini (query parameters)](/guide/routing/read-route-state#query-parameters) uzatish va navigatsiya xatti-harakatini boshqarish imkonini beradi.

Shuningdek, `relativeTo` opsiyasidan foydalanib, marshrutlash daraxtidagi komponentingizning joylashuviga nisbatan dinamik navigatsiya yoʻllarini ham tuzishingiz mumkin.

```angular-ts
import {Router, ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-user-detail',
  template: `
    <button (click)="navigateToEdit()">Edit User</button>
    <button (click)="navigateToParent()">Back to List</button>
  `,
})
export class UserDetail {
  private route = inject(ActivatedRoute);
  private router = inject(Router);

  // Navigate to a sibling route
  navigateToEdit() {
    // From: /users/123
    // To:   /users/123/edit
    this.router.navigate(['edit'], {relativeTo: this.route});
  }

  // Navigate to parent
  navigateToParent() {
    // From: /users/123
    // To:   /users
    this.router.navigate(['..'], {relativeTo: this.route});
  }

  navigateToList() {
    // Angular resolves the commands array as a single navigation path relative to the current route.
    // From: /users/123
    // Result: /users/list
    this.router.navigate(['..', 'list'], {relativeTo: this.route});
  }
}
```

Bir necha daraja yuqoriga navigatsiya qilganda barcha `..` segmentlari buyruqlar massivining **birinchi elementida** boʻlishi shart. Router `..` ni faqat birinchi buyruq satridan tahlil qiladi — keyingi massiv elementlari oddiy yoʻl segmentlari sifatida qabul qilinadi.

```angular-ts {prefer}
// From: /team/123/users/456
// Result: /team/123/settings
this.router.navigate(['../../settings'], {relativeTo: this.route});
```

`relativeTo` ishlatilganda birinchi buyruq oldiga hech qachon `/` qoʻymang. Boshidagi `/` navigatsiyani absolyut qiladi va `relativeTo` ni butunlay eʼtiborsiz qoldiradi.

```angular-ts {prefer}
// From: /team/123/users/456
// Result: /team/123/users/456/edit
this.router.navigate(['edit'], {relativeTo: this.route});
```

```angular-ts {avoid}
// From: /team/123/users/456
// Leading '/' causes absolute navigation — relativeTo is ignored
// Result: /edit
this.router.navigate(['/edit'], {relativeTo: this.route});
```

### `router.navigateByUrl()`

`router.navigateByUrl()` metodi massiv segmentlari oʻrniga URL yoʻli satrlaridan foydalanib dasturiy navigatsiya qilishning bevosita usulini taqdim etadi. Bu metod toʻliq URL yoʻlingiz boʻlib, absolyut navigatsiya qilish kerak boʻlganda, xususan, tashqaridan berilgan URL'lar yoki deep linking holatlari bilan ishlashda juda mos keladi.

```ts
// Standard route navigation
router.navigateByUrl('/products');

// Navigate to nested route
router.navigateByUrl('/products/featured');

// Complete URL with parameters and fragment
router.navigateByUrl('/products/123?view=details#reviews');

// Navigate with query parameters
router.navigateByUrl('/search?category=books&sortBy=price');

// With matrix parameters
router.navigateByUrl('/sales-awesome;isOffer=true;showModal=false');
```

Tarixdagi (history) joriy URL'ni almashtirish kerak boʻlsa, `navigateByUrl` `replaceUrl` opsiyasiga ega konfiguratsiya obyektini ham qabul qiladi.

```ts
// Replace current URL in history
router.navigateByUrl('/checkout', {
  replaceUrl: true,
});
```

### Manzil satrida boshqa URL'ni koʻrsatish {#display-a-different-url-in-the-address-bar}

Brauzerning manzil satrida marshrutni moslashtirish uchun ishlatilgan URL'dan boshqa URL'ni koʻrsatish uchun navigateByUrl'ga browserUrl opsiyasini uzatishingiz mumkin.

Bu foydalanuvchini dastlab tashrif buyurmoqchi boʻlgan URL'ni oʻzgartirmasdan boshqa marshrutga — masalan, xato sahifasiga — yoʻnaltirmoqchi boʻlganingizda foydali.

```ts
router.navigateByUrl('/not-found', {browserUrl: '/products/missing-item'});
```

Angular `/not-found` marshrutiga navigatsiya qiladi va uni render qiladi, lekin brauzer manzil satrida `/products/missing-item` koʻrsatiladi.

NOTE: `browserUrl` faqat brauzer manzil satrida nima koʻrinishiga taʼsir qiladi.

## RouterLink bilan brauzer URL'ini sozlash {#customizing-the-browser-url-with-routerlink}

`RouterLink` direktivasi `browserUrl` input'ini ham qoʻllab-quvvatlaydi; u havola bosilganda Angular navigatsiya qiladigan marshrutdan mustaqil ravishda brauzer manzil satrida koʻrsatiladigan URL'ni boshqarish imkonini beradi.

```angular-html
<!-- Navigates to /dashboard, but the address bar shows /home -->
<a [routerLink]="['/dashboard']" [browserUrl]="'/home'">Go to Dashboard</a>
```

Yanada dinamik holatlar uchun `UrlTree` ni ham bogʻlashingiz mumkin:

```angular-ts
import {Component, inject} from '@angular/core';
import {Router, RouterLink, UrlTree} from '@angular/router';

@Component({
  template: `
    <a [routerLink]="['/products', product.id]" [browserUrl]="displayUrl">
      {{ product.name }}
    </a>
  `,
  imports: [RouterLink],
})
export class ProductList {
  private router = inject(Router);

  product = {id: 42, name: 'Widget'};

  // Create a UrlTree to display in the address bar
  displayUrl: UrlTree = this.router.createUrlTree(['/products', 'widget']);
}
```

## Keyingi qadamlar {#next-steps}

Moslashuvchan va kontekstni hisobga oladigan komponentlar yaratish uchun [marshrut holatini oʻqishni](/guide/routing/read-route-state) oʻrganing.
