# Marshrutlash va navigatsiyani testlash

Marshrutlash va navigatsiyani testlash foydalanuvchilar turli marshrutlar oʻrtasida harakatlanganda ilovangiz toʻgʻri ishlashini taʼminlash uchun zarur. Bu qoʻllanma Angular ilovalarida marshrutlash funksionalligini testlashning turli strategiyalarini qamrab oladi.

## Dastlabki talablar {#prerequisites}

Bu qoʻllanma siz quyidagi vositalar va kutubxonalar bilan tanish ekaningizni nazarda tutadi:

- **[Vitest](https://vitest.dev/)** - test sintaksisini (`describe`, `it`, `expect`) taqdim etuvchi JavaScript testlash freymvorki
- **[Angular testlash vositalari](guide/testing)** - Angular'ning oʻrnatilgan testlash vositalari ([`TestBed`](api/core/testing/TestBed), [`ComponentFixture`](api/core/testing/ComponentFixture))
- **[`RouterTestingHarness`](api/router/testing/RouterTestingHarness)** - oʻrnatilgan navigatsiya va komponent testlash imkoniyatlariga ega, marshrutlangan komponentlarni testlash uchun test harness'i

## Testlash stsenariylari {#testing-scenarios}

### Marshrut parametrlari {#route-parameters}

Komponentlar maʼlumot yuklash uchun koʻpincha URL'dagi marshrut parametrlariga, masalan, profil sahifasi uchun foydalanuvchi ID'siga tayanadi.

Quyidagi misol marshrutdan foydalanuvchi ID'sini koʻrsatadigan `UserProfile` komponentini qanday testlashni koʻrsatadi.

```ts { header: 'user-profile.spec.ts'}
import {TestBed} from '@angular/core/testing';
import {provideRouter, Router} from '@angular/router';
import {RouterTestingHarness} from '@angular/router/testing';
import {UserProfile} from './user-profile';

describe('UserProfile', () => {
  it('should display user ID from route parameters', async () => {
    TestBed.configureTestingModule({
      imports: [UserProfile],
      providers: [provideRouter([{path: 'user/:id', component: UserProfile}])],
    });

    const harness = await RouterTestingHarness.create();
    await harness.navigateByUrl('/user/123', UserProfile);

    expect(harness.routeNativeElement?.textContent).toContain('User Profile: 123');
  });
});
```

```angular-ts {header: 'user-profile.ts'}
import {Component, inject} from '@angular/core';
import {ActivatedRoute} from '@angular/router';

@Component({
  template: '<h1>User Profile: {{userId}}</h1>',
})
export class UserProfile {
  private route = inject(ActivatedRoute);
  userId: string | null = this.route.snapshot.paramMap.get('id');
}
```

### Marshrut himoyachilari (guard) {#route-guards}

Marshrut himoyachilari (guard) autentifikatsiya yoki ruxsatlar kabi shartlarga qarab marshrutlarga kirishni boshqaradi. Guard'larni testlashda bogʻliqliklarni mock qilish va navigatsiya natijalarini tekshirishga eʼtibor qarating.

Quyidagi misol autentifikatsiyadan oʻtgan foydalanuvchilar uchun navigatsiyaga ruxsat beradigan va autentifikatsiyadan oʻtmagan foydalanuvchilarni login sahifasiga yoʻnaltiradigan `authGuard`'ni testlaydi.

```ts {header: 'auth.guard.spec.ts'}
import {describe, expect, it, vi, type Mocked} from 'vitest';
import {RouterTestingHarness} from '@angular/router/testing';
import {provideRouter, Router} from '@angular/router';
import {authGuard} from './auth.guard';
import {AuthStore} from './auth-store';
import {Component} from '@angular/core';
import {TestBed} from '@angular/core/testing';

@Component({template: '<h1>Protected Page</h1>'})
class Protected {}

@Component({template: '<h1>Login Page</h1>'})
class Login {}

describe('authGuard', () => {
  let authStore: Mocked<AuthStore>;
  let harness: RouterTestingHarness;

  async function setup(isAuthenticated: boolean) {
    authStore = {isAuthenticated: vi.fn().mockReturnValue(isAuthenticated)} as Mocked<AuthStore>;

    TestBed.configureTestingModule({
      providers: [
        {provide: AuthStore, useValue: authStore},
        provideRouter([
          {path: 'protected', component: Protected, canActivate: [authGuard]},
          {path: 'login', component: Login},
        ]),
      ],
    });

    harness = await RouterTestingHarness.create();
  }

  it('allows navigation when user is authenticated', async () => {
    await setup(true);
    await harness.navigateByUrl('/protected', Protected);
    // The protected component should render when authenticated
    expect(harness.routeNativeElement?.textContent).toContain('Protected Page');
  });

  it('redirects to login when user is not authenticated', async () => {
    await setup(false);
    await harness.navigateByUrl('/protected', Login);
    // The login component should render after redirect
    expect(harness.routeNativeElement?.textContent).toContain('Login Page');
  });
});
```

```ts {header: 'auth.guard.ts'}
import {inject} from '@angular/core';
import {CanActivateFn, Router} from '@angular/router';
import {AuthStore} from './auth-store';

export const authGuard: CanActivateFn = () => {
  const authStore = inject(AuthStore);
  const router = inject(Router);
  return authStore.isAuthenticated() ? true : router.parseUrl('/login');
};
```

### Router outlet'lar {#router-outlets}

Router outlet testlari koʻproq integratsiya testiga oʻxshaydi, chunki siz aslida [`Router`](api/router/Router), outlet va koʻrsatilayotgan komponentlar oʻrtasidagi integratsiyani testlaysiz.

Quyida turli marshrutlar uchun turli komponentlar koʻrsatilishini tekshiradigan testni qanday sozlashga misol keltirilgan:

```ts {header: 'app.spec.ts'}
import {TestBed} from '@angular/core/testing';
import {RouterTestingHarness} from '@angular/router/testing';
import {provideRouter} from '@angular/router';
import {Component} from '@angular/core';
import {App} from './app';

@Component({
  template: '<h1>Home Page</h1>',
})
class MockHome {}

@Component({
  template: '<h1>About Page</h1>',
})
class MockAbout {}

describe('App Router Outlet', () => {
  let harness: RouterTestingHarness;

  beforeEach(async () => {
    TestBed.configureTestingModule({
      imports: [App],
      providers: [
        provideRouter([
          {path: '', component: MockHome},
          {path: 'about', component: MockAbout},
        ]),
      ],
    });

    harness = await RouterTestingHarness.create();
  });

  it('should display home component for default route', async () => {
    await harness.navigateByUrl('');

    expect(harness.routeNativeElement?.textContent).toContain('Home Page');
  });

  it('should display about component for about route', async () => {
    await harness.navigateByUrl('/about');

    expect(harness.routeNativeElement?.textContent).toContain('About Page');
  });
});
```

```angular-ts {header: 'app.ts'}
import {Component} from '@angular/core';
import {RouterOutlet, RouterLink} from '@angular/router';

@Component({
  imports: [RouterOutlet, RouterLink],
  template: `
    <nav>
      <a routerLink="/">Home</a>
      <a routerLink="/about">About</a>
    </nav>
    <router-outlet />
  `,
})
export class App {}
```

### Ichki marshrutlar {#nested-routes}

Ichki (nested) marshrutlarni testlash ichki URL'larga oʻtishda ota va bola komponentlarning ikkalasi ham toʻgʻri render qilinishini taʼminlaydi. Bu muhim, chunki ichki marshrutlar bir nechta qatlamni oʻz ichiga oladi.

Siz quyidagilarni tekshirishingiz kerak:

1. Ota komponent toʻgʻri render qilinadi.
2. Bola komponent uning ichida render qilinadi.
3. Ikkala komponent ham oʻzlariga tegishli marshrut maʼlumotlariga murojaat qila olishiga ishonch hosil qiling.

Quyida ota-bola marshrut tuzilmasini testlashga misol keltirilgan:

```ts {header: 'nested-routes.spec.ts'}
import {TestBed} from '@angular/core/testing';
import {RouterTestingHarness} from '@angular/router/testing';
import {provideRouter} from '@angular/router';
import {Parent, Child} from './nested-components';

describe('Nested Routes', () => {
  let harness: RouterTestingHarness;

  beforeEach(async () => {
    TestBed.configureTestingModule({
      imports: [Parent, Child],
      providers: [
        provideRouter([
          {
            path: 'parent',
            component: Parent,
            children: [{path: 'child', component: Child}],
          },
        ]),
      ],
    });

    harness = await RouterTestingHarness.create();
  });

  it('should render parent and child components for nested route', async () => {
    await harness.navigateByUrl('/parent/child');

    expect(harness.routeNativeElement?.textContent).toContain('Parent Component');
    expect(harness.routeNativeElement?.textContent).toContain('Child Component');
  });
});
```

```angular-ts {header: 'nested.ts'}
import {Component} from '@angular/core';
import {RouterOutlet} from '@angular/router';

@Component({
  imports: [RouterOutlet],
  template: `
    <h1>Parent Component</h1>
    <router-outlet />
  `,
})
export class Parent {}

@Component({
  template: '<h2>Child Component</h2>',
})
export class Child {}
```

### Soʻrov parametrlari va fragmentlar {#query-parameters-and-fragments}

Soʻrov parametrlari (masalan, `?search=angular&category=web`) va URL fragmentlari (masalan, `#section1`) URL orqali qaysi komponent yuklanishiga taʼsir qilmaydigan, lekin komponentning qanday ishlashiga taʼsir qiladigan qoʻshimcha maʼlumotlarni taqdim etadi. Soʻrov parametrlarini [`ActivatedRoute.queryParams`](api/router/ActivatedRoute#queryParams) orqali oʻqiydigan komponentlar turli parametr stsenariylariga toʻgʻri ishlov berishini taʼminlash uchun testlanishi kerak.

Marshrut taʼrifining bir qismi boʻlgan marshrut parametrlaridan farqli oʻlaroq, soʻrov parametrlari ixtiyoriy boʻlib, marshrut navigatsiyasini ishga tushirmasdan oʻzgarishi mumkin. Bu dastlabki yuklanishni ham, soʻrov parametrlari oʻzgarganda reaktiv yangilanishlarni ham testlashingiz kerakligini anglatadi.

Quyida soʻrov parametrlari va fragmentlarni qanday testlashga misol keltirilgan:

```ts {header: 'search.spec.ts'}
import {TestBed} from '@angular/core/testing';
import {Router, provideRouter} from '@angular/router';
import {RouterTestingHarness} from '@angular/router/testing';
import {Search} from './search';

describe('Search', () => {
  let component: Search;
  let harness: RouterTestingHarness;

  beforeEach(async () => {
    TestBed.configureTestingModule({
      imports: [Search],
      providers: [provideRouter([{path: 'search', component: Search}])],
    });

    harness = await RouterTestingHarness.create();
  });

  it('should read search term from query parameters', async () => {
    component = await harness.navigateByUrl('/search?q=angular', Search);

    expect(component.searchTerm()).toBe('angular');
  });
});
```

```angular-ts {header: 'search.ts'}
import {Component, inject, computed} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {toSignal} from '@angular/core/rxjs-interop';

@Component({
  template: '<div>Search term: {{searchTerm()}}</div>',
})
export class Search {
  private route = inject(ActivatedRoute);
  private queryParams = toSignal(this.route.queryParams, {initialValue: {}});

  searchTerm = computed(() => this.queryParams()['q'] || null);
}
```

## Router testlash uchun eng yaxshi amaliyotlar {#best-practices-for-router-testing}

1. **RouterTestingHarness'dan foydalaning** - Marshrutlangan komponentlarni testlash uchun toza API taqdim etuvchi va test host komponentlariga ehtiyojni bartaraf etuvchi [`RouterTestingHarness`](api/router/testing/RouterTestingHarness)'dan foydalaning. U komponentga toʻgʻridan-toʻgʻri murojaat, oʻrnatilgan navigatsiya va yaxshiroq tur xavfsizligini taklif qiladi. Biroq u baʼzi stsenariylar, masalan, nomlangan outlet'larni testlash uchun unchalik mos emas — bunday hollarda maxsus host komponentlar yaratishingiz kerak boʻlishi mumkin.
2. **Tashqi bogʻliqliklarga oʻylab yondashing** - Yanada realistik testlar uchun imkon qadar haqiqiy implementatsiyalardan foydalaning. Haqiqiy implementatsiyalar imkonsiz boʻlsa (masalan, tashqi API'lar), haqiqiy xatti-harakatga yaqin fake'lardan foydalaning. Mock yoki stub'lardan faqat oxirgi chora sifatida foydalaning, chunki ular testlarni moʻrt va kamroq ishonchli qilishi mumkin.
3. **Navigatsiya holatini testlang** - Navigatsiya harakatini ham, natijada hosil boʻlgan ilova holatini ham, jumladan URL oʻzgarishlari va komponent render qilinishini tekshiring.
4. **Asinxron operatsiyalarga ishlov bering** - Router navigatsiyasi asinxron. Testlaringizda vaqtni toʻgʻri boshqarish uchun `async/await`'dan foydalaning.
5. **Xato stsenariylarini testlang** - Ilovangiz chekka holatlarga toʻgʻri ishlov berishini taʼminlash uchun notoʻgʻri marshrutlar, muvaffaqiyatsiz navigatsiya va guard rad etishlari uchun testlar qoʻshing.
6. **Angular Router'ni mock qilmang** - Buning oʻrniga haqiqiy marshrut konfiguratsiyalarini taqdim eting va navigatsiya uchun harness'dan foydalaning. Bu testlaringizni yanada mustahkam qiladi va Angular'ning ichki yangilanishlarida buzilish ehtimolini kamaytiradi, shu bilan birga router yangilanganda haqiqiy muammolarni aniqlashingizni taʼminlaydi, chunki mock'lar buzuvchi oʻzgarishlarni yashirishi mumkin.
