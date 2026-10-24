# Marshrutga kirishni himoyachilar bilan boshqarish

CRITICAL: Hech qachon klient tomonidagi himoyachilarga kirishni boshqarishning yagona manbai sifatida tayanmang. Veb-brauzerda ishlaydigan har qanday JavaScript'ni brauzerni ishlatayotgan foydalanuvchi oʻzgartirishi mumkin. Klient tomonidagi har qanday himoyachilarga qoʻshimcha ravishda foydalanuvchi avtorizatsiyasini doimo server tomonida ham taʼminlang.

Marshrut himoyachilari (route guards) — foydalanuvchi muayyan marshrutga oʻta olishi yoki undan chiqa olishini boshqaruvchi funksiyalar. Ular foydalanuvchining muayyan marshrutlarga kirishini boshqaruvchi nazorat punktlariga oʻxshaydi. Marshrut himoyachilaridan foydalanishning keng tarqalgan misollariga autentifikatsiya va kirishni boshqarish kiradi.

## Marshrut himoyachisini yaratish {#creating-a-route-guard}

Marshrut himoyachisini Angular CLI yordamida generatsiya qilishingiz mumkin:

```bash
ng generate guard CUSTOM_NAME
```

Bu sizdan qaysi [marshrut himoyachisi turini](#types-of-route-guards) ishlatishni tanlashni soʻraydi va soʻngra tegishli `CUSTOM_NAME-guard.ts` faylini yaratadi.

TIP: Marshrut himoyachisini Angular loyihangizda alohida TypeScript fayli yaratib, qoʻlda ham yaratishingiz mumkin. Dasturchilar odatda uni boshqa fayllardan ajratish uchun fayl nomiga `-guard.ts` suffiksini qoʻshadi.

## Marshrut himoyachisining qaytarish turlari {#route-guard-return-types}

Barcha marshrut himoyachilari bir xil mumkin boʻlgan qaytarish turlariga ega. Bu sizga navigatsiyani boshqarishda moslashuvchanlik beradi:

| Qaytarish turlari               | Tavsif                                                                                          |
| ------------------------------- | ----------------------------------------------------------------------------------------------- |
| `boolean`                       | `true` navigatsiyaga ruxsat beradi, `false` uni bloklaydi (`CanMatch` marshrut himoyachisi uchun izohga qarang) |
| `UrlTree` yoki `RedirectCommand` | Bloklash oʻrniga boshqa marshrutga yoʻnaltiradi                                                |
| `Promise<T>` yoki `Observable<T>` | Router birinchi yuborilgan qiymatdan foydalanadi va soʻngra obunani bekor qiladi             |

NOTE: `CanMatch` boshqacha ishlaydi — u `false` qaytarganda Angular navigatsiyani butunlay bloklash oʻrniga boshqa mos marshrutlarni sinab koʻradi.

## Marshrut himoyachilarining turlari {#types-of-route-guards}

Angular har biri turli maqsadlarga xizmat qiluvchi toʻrt turdagi marshrut himoyachisini taqdim etadi:

<docs-pill-row>
  <docs-pill href="#canactivate" title="CanActivate"/>
  <docs-pill href="#canactivatechild" title="CanActivateChild"/>
  <docs-pill href="#candeactivate" title="CanDeactivate"/>
  <docs-pill href="#canmatch" title="CanMatch"/>
</docs-pill-row>

Barcha himoyachilar [marshrut darajasida taqdim etilgan servislarga](guide/di/defining-dependency-providers#route-providers), shuningdek `route` argumenti orqali marshrutga xos maʼlumotlarga kirish huquqiga ega.

### CanActivate

`CanActivate` himoyachisi foydalanuvchi marshrutga kira olishini aniqlaydi. U koʻpincha autentifikatsiya va avtorizatsiya uchun ishlatiladi.

U quyidagi standart argumentlarga kirish huquqiga ega:

- `route`: `ActivatedRouteSnapshot` — faollashtirilayotgan marshrut haqidagi maʼlumotni oʻz ichiga oladi
- `state`: `RouterStateSnapshot` — router'ning joriy holatini oʻz ichiga oladi

U [standart himoyachi qaytarish turlarini](#route-guard-return-types) qaytarishi mumkin.

```ts
export const authGuard: CanActivateFn = (
  route: ActivatedRouteSnapshot,
  state: RouterStateSnapshot,
) => {
  const authService = inject(AuthService);
  return authService.isAuthenticated();
};
```

TIP: Agar foydalanuvchini yoʻnaltirishingiz kerak boʻlsa, [`URLTree`](api/router/UrlTree) yoki [`RedirectCommand`](api/router/RedirectCommand) qaytaring. `false` qaytarib, soʻngra foydalanuvchini dasturiy ravishda `navigate` qilish **kerak emas**.

Koʻproq maʼlumot uchun [CanActivateFn API hujjatlariga](api/router/CanActivateFn) qarang.

### CanActivateChild

`CanActivateChild` himoyachisi foydalanuvchi muayyan ota marshrutning bola marshrutlariga kira olishini aniqlaydi. Bu ichma-ich marshrutlarning butun boʻlimini himoya qilmoqchi boʻlganingizda foydali. Boshqacha aytganda, `canActivateChild` _barcha_ bolalar uchun ishga tushadi. Agar bola komponent ostida yana bir bola komponent boʻlsa, `canActivateChild` ularning har biri uchun bir martadan ishga tushadi.

U quyidagi standart argumentlarga kirish huquqiga ega:

- `childRoute`: `ActivatedRouteSnapshot` — faollashtirilayotgan bola marshrutning "kelajakdagi" surati (yaʼni router oʻtmoqchi boʻlgan holat) haqidagi maʼlumotni oʻz ichiga oladi
- `state`: `RouterStateSnapshot` — router'ning joriy holatini oʻz ichiga oladi

U [standart himoyachi qaytarish turlarini](#route-guard-return-types) qaytarishi mumkin.

```ts
export const adminChildGuard: CanActivateChildFn = (
  childRoute: ActivatedRouteSnapshot,
  state: RouterStateSnapshot,
) => {
  const authService = inject(AuthService);
  return authService.hasRole('admin');
};
```

Koʻproq maʼlumot uchun [CanActivateChildFn API hujjatlariga](api/router/CanActivateChildFn) qarang.

### CanDeactivate

`CanDeactivate` himoyachisi foydalanuvchi marshrutdan chiqa olishini aniqlaydi. Keng tarqalgan holat — saqlanmagan formalardan chiqib ketishning oldini olish.

U quyidagi standart argumentlarga kirish huquqiga ega:

- `component`: `T` — oʻchirilayotgan (deactivate) komponent nusxasi
- `currentRoute`: `ActivatedRouteSnapshot` — joriy marshrut haqidagi maʼlumotni oʻz ichiga oladi
- `currentState`: `RouterStateSnapshot` — router'ning joriy holatini oʻz ichiga oladi
- `nextState`: `RouterStateSnapshot` — oʻtilayotgan keyingi router holatini oʻz ichiga oladi

U [standart himoyachi qaytarish turlarini](#route-guard-return-types) qaytarishi mumkin.

```ts
export const unsavedChangesGuard: CanDeactivateFn<Form> = (
  component: Form,
  currentRoute: ActivatedRouteSnapshot,
  currentState: RouterStateSnapshot,
  nextState: RouterStateSnapshot,
) => {
  return component.hasUnsavedChanges()
    ? confirm('You have unsaved changes. Are you sure you want to leave?')
    : true;
};
```

Koʻproq maʼlumot uchun [CanDeactivateFn API hujjatlariga](api/router/CanDeactivateFn) qarang.

### CanMatch

`CanMatch` himoyachisi yoʻlni moslashtirish davomida marshrut mos kelishi mumkinligini aniqlaydi. Boshqa himoyachilardan farqli oʻlaroq, rad etish navigatsiyani butunlay bloklash oʻrniga boshqa mos marshrutlarni sinab koʻrishga oʻtadi. Bu feature flag'lar, A/B testlash yoki shartli marshrut yuklash uchun foydali boʻlishi mumkin.

U quyidagi standart argumentlarga kirish huquqiga ega:

- `route`: `Route` — baholanayotgan marshrut konfiguratsiyasi
- `segments`: `UrlSegment[]` — oldingi ota marshrutlarni baholashda isteʼmol qilinmagan URL segmentlari
- `currentSnapshot: PartialMatchRouteSnapshot` — moslashtirish jarayonining shu nuqtasigacha boʻlgan joriy marshrut surati

U [standart himoyachi qaytarish turlarini](#route-guard-return-types) qaytarishi mumkin, lekin `false` qaytarganda Angular navigatsiyani butunlay bloklash oʻrniga boshqa mos marshrutlarni sinab koʻradi.

```ts
export const featureToggleGuard: CanMatchFn = (
  route: Route,
  segments: UrlSegment[],
  currentSnapshot: PartialMatchRouteSnapshot,
) => {
  const featureService = inject(FeatureService);
  return featureService.isFeatureEnabled('newDashboard');
};
```

Shuningdek, u bir xil yoʻl uchun turli komponentlardan foydalanish imkonini ham beradi.

```ts {header: "routes.ts"}
const routes: Routes = [
  {
    path: 'dashboard',
    component: AdminDashboard,
    canMatch: [adminGuard],
  },
  {
    path: 'dashboard',
    component: UserDashboard,
    canMatch: [userGuard],
  },
];
```

Bu misolda foydalanuvchi `/dashboard`'ga kirganda, toʻgʻri himoyachiga mos kelgan birinchisi ishlatiladi.

Koʻproq maʼlumot uchun [CanMatchFn API hujjatlariga](api/router/CanMatchFn) qarang.

## Himoyachilarni marshrutlarga qoʻllash {#applying-guards-to-routes}

Marshrut himoyachilarini yaratgach, ularni marshrut aniqlanishlaringizda sozlashingiz kerak.

Bitta marshrutga bir nechta himoyachi qoʻllash imkonini berish uchun himoyachilar marshrut konfiguratsiyasida massiv sifatida koʻrsatiladi. Router himoyachilarni massivda koʻrsatilgan tartibda ishga tushiradi, lekin keyingisini boshlashdan oldin bitta himoyachining tugashini kutmaydi. Shu sababli `Promise` yoki `Observable` qaytaruvchi himoyachilar parallel ishlaydi.

Massiv tartibi qaysi natija ustuvor boʻlishini belgilaydi. Navigatsiya faqat har bir himoyachi `true` qaytarsa davom etadi. Aks holda router massivdagi `true` qaytarmagan birinchi himoyachining natijasidan foydalanadi, hatto keyingi himoyachi ertaroq tugagan boʻlsa ham.

NOTE: Asinxron himoyachilar parallel ishlagani sababli, himoyachi bir xil massivdagi oldingi himoyachi bajargan ishga, masalan, joriy foydalanuvchini yuklashga tayanmasligi kerak. Bu ishni ikkala himoyachi ham foydalanadigan servisga joylashtiring yoki tekshiruvlarni bitta himoyachiga birlashtiring.

```ts
import {Routes} from '@angular/router';
import {authGuard} from './guards/auth.guard';
import {adminGuard} from './guards/admin.guard';
import {canDeactivateGuard} from './guards/can-deactivate.guard';
import {featureToggleGuard} from './guards/feature-toggle.guard';

const routes: Routes = [
  // Basic CanActivate - requires authentication
  {
    path: 'dashboard',
    component: Dashboard,
    canActivate: [authGuard],
  },

  // Multiple CanActivate guards - requires authentication AND admin role
  {
    path: 'admin',
    component: Admin,
    canActivate: [authGuard, adminGuard],
  },

  // CanActivate + CanDeactivate - protected route with unsaved changes check
  {
    path: 'profile',
    component: Profile,
    canActivate: [authGuard],
    canDeactivate: [canDeactivateGuard],
  },

  // CanActivateChild - protects all child routes
  {
    path: 'users', // /user - NOT protected
    canActivateChild: [authGuard],
    children: [
      // /users/list - PROTECTED
      {path: 'list', component: UserList},
      // /users/detail/:id - PROTECTED
      {path: 'detail/:id', component: UserDetail},
    ],
  },

  // CanMatch - conditionally matches route based on feature flag
  {
    path: 'beta-feature',
    component: BetaFeature,
    canMatch: [featureToggleGuard],
  },

  // Fallback route if beta feature is disabled
  {
    path: 'beta-feature',
    component: ComingSoon,
  },
];
```
