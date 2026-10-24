# Marshrut xatti-harakatini sozlash

Angular Router ilovangizda marshrutlarning qanday ishlashini sozlash imkonini beruvchi kuchli kengaytirish nuqtalarini taqdim etadi. Sukut boʻyicha marshrutlash xatti-harakati koʻpchilik ilovalar uchun yaxshi ishlasa-da, muayyan talablar koʻpincha unumdorlikni optimallashtirish, URL'larni maxsus qayta ishlash yoki murakkab marshrutlash mantiqi uchun maxsus implementatsiyalarni talab qiladi.

Marshrutlarni sozlash ilovangizga quyidagilar kerak boʻlganda foydali boʻlishi mumkin:

- Maʼlumotlarni qayta olishdan qochish uchun navigatsiyalar davomida **komponent holatini saqlash**
- Foydalanuvchi xatti-harakati yoki tarmoq sharoitlariga asoslangan **strategik lazy modul yuklash**
- **Tashqi URL integratsiyasi** yoki Angular marshrutlarini eski (legacy) tizimlar bilan birga qayta ishlash
- Oddiy yoʻl namunalaridan tashqari ish vaqtidagi shartlarga asoslangan **dinamik marshrut
  moslashtirish**

NOTE: Maxsus strategiyalarni implementatsiya qilishdan oldin router'ning sukut boʻyicha xatti-harakati ehtiyojlaringizga javob bermasligiga ishonch hosil qiling. Angular'ning sukut boʻyicha marshrutlashi keng tarqalgan holatlar uchun optimallashtirilgan va unumdorlik bilan soddalik oʻrtasidagi eng yaxshi muvozanatni taʼminlaydi. Marshrut strategiyalarini sozlash, agar ehtiyotkorlik bilan boshqarilmasa, qoʻshimcha kod murakkabligini yuzaga keltirishi va xotira ishlatilishi boʻyicha unumdorlikka taʼsir qilishi mumkin.

## Router konfiguratsiya variantlari {#router-configuration-options}

`withRouterConfig` yoki `RouterModule.forRoot` Router'ning xatti-harakatini moslashtirish uchun qoʻshimcha `RouterConfigOptions` taqdim etish imkonini beradi.

### Bekor qilingan navigatsiyalarni qayta ishlash {#handle-canceled-navigations}

`canceledNavigationResolution` navigatsiya bekor qilinganda Router brauzer tarixini qanday tiklashini boshqaradi. Sukut boʻyicha qiymat — `'replace'`, u `location.replaceState` yordamida navigatsiyadan oldingi URL'ga qaytaradi. Amalda bu shuni anglatadiki, manzil satri navigatsiya uchun allaqachon yangilangan har qanday holatda, masalan brauzerning orqaga yoki oldinga tugmalari bilan, agar navigatsiya muvaffaqiyatsiz boʻlsa yoki marshrut himoyachisi (guard) tomonidan rad etilsa, tarix yozuvi "orqaga qaytarish" (rollback) bilan ustidan yoziladi.
`'computed'` ga oʻtish joriy tarix indeksini Angular navigatsiyasi bilan sinxron saqlaydi, shuning uchun orqaga tugmasi navigatsiyasini bekor qilish asl sahifaga qaytish uchun oldinga navigatsiyani (va aksincha) ishga tushiradi.

Bu sozlama ilovangiz `urlUpdateStrategy: 'eager'` dan foydalanganda yoki himoyachilar brauzer tomonidan boshlangan popstate navigatsiyalarini tez-tez bekor qilganda eng foydali.

```ts
provideRouter(routes, withRouterConfig({canceledNavigationResolution: 'computed'}));
```

### Bir xil URL'ga navigatsiyalarga javob berish {#react-to-same-url-navigations}

`onSameUrlNavigation` foydalanuvchi joriy URL'ga oʻtishni soʻraganda nima sodir boʻlishini sozlaydi. Sukut boʻyicha `'ignore'` ishni oʻtkazib yuboradi, `'reload'` esa Router'ga URL'ni oʻtkazib yubormasdan, navigatsiya konveyerida (pipeline) qayta ishlashni buyuradi. Himoyachi va resolver'larning qayta ishga tushishi [`runGuardsAndResolvers`](api/router/RunGuardsAndResolvers) tomonidan, komponentni qayta ishlatish esa [marshrutni qayta ishlatish strategiyasi](#route-reuse-strategy) tomonidan belgilanadi.

Bu roʻyxat filtri, chap navigatsiya elementi yoki yangilash tugmasini takroran bosish URL oʻzgarmasa ham yangi maʼlumotlarni olishni ishga tushirishini istaganingizda foydali.

```ts
provideRouter(routes, withRouterConfig({onSameUrlNavigation: 'reload'}));
```

Bu xatti-harakatni global emas, balki alohida navigatsiyalarda ham boshqarishingiz mumkin. Bu sukut boʻyicha `'ignore'` ni saqlab, muayyan holatlar uchun qayta yuklash xatti-harakatini tanlab yoqish imkonini beradi:

```ts
router.navigate(['/some-path'], {onSameUrlNavigation: 'reload'});
```

TIP: Agar [marshrut resurslaridan](/guide/routing/data-fetching-with-resources#reloading-resources-without-renavigation) foydalansangiz, `onSameUrlNavigation`'ni sozlash yoki router navigatsiyasini ishga tushirishga hojat qolmasdan, resursda `.reload()` ni chaqirib yoki `params` ichida oʻqiladigan signallarni yangilab, maʼlumotlarni talab boʻyicha yangilashingiz mumkin.

### Parametrlar merosini boshqarish {#control-parameter-inheritance}

`paramsInheritanceStrategy` marshrut parametrlari va maʼlumotlarining ota marshrutlardan qanday oʻtishini belgilaydi.

Sukut boʻyicha (`'always'`) bola marshrutlar ota marshrutlardan parametrlarni, marshrut maʼlumotlarini va resolve qilingan qiymatlarni avtomatik meros qilib oladi. Bu matritsa parametrlari, marshrut maʼlumotlari va resolve qilingan qiymatlar marshrut daraxtining quyi qismlarida ham mavjud boʻlishini taʼminlaydi — bu kontekstual identifikatorlarni quyidagi kabi funksional sohalar boʻylab ulashganda qoʻl keladi:

```text {hideCopy}
/org/:orgId/projects/:projectId/customers/:customerId
```

```ts
export const routes: Routes = [
  {
    path: 'org/:orgId',
    component: Organization,
    children: [
      {
        path: 'projects/:projectId',
        component: Project,
        children: [
          {
            path: 'customers/:customerId',
            component: Customer,
          },
        ],
      },
    ],
  },
];
```

```ts
@Component({/* ... */})
export class Customer {
  private route = inject(ActivatedRoute);

  // All parent parameters are available directly
  orgId = this.route.snapshot.params['orgId'];
  projectId = this.route.snapshot.params['projectId'];
  customerId = this.route.snapshot.params['customerId'];
}
```

Eski xatti-harakatni tiklash uchun `paramsInheritanceStrategy`'ni `'emptyOnly'` ga oʻrnating. `'emptyOnly'` bilan bola marshrutlar parametrlarni faqat yoʻli boʻsh boʻlganda yoki ota komponent eʼlon qilmaganda meros qilib oladi:

```ts
provideRouter(routes, withRouterConfig({paramsInheritanceStrategy: 'emptyOnly'}));
```

Bu holda `Customer` komponenti ota parametrlarni oʻzining ajdod marshrutlaridan oʻqishi kerak:

```ts
@Component({/* ... */})
export class Customer {
  private route = inject(ActivatedRoute);

  orgId = this.route.parent?.parent?.snapshot.params['orgId'];
  projectId = this.route.parent?.snapshot.params['projectId'];
  customerId = this.route.snapshot.params['customerId'];
}
```

### URL qachon yangilanishini hal qilish {#decide-when-the-url-updates}

`urlUpdateStrategy` Angular brauzer manzil satriga qachon yozishini belgilaydi. Sukut boʻyicha `'deferred'` URL'ni oʻzgartirishdan oldin muvaffaqiyatli navigatsiyani kutadi. Navigatsiya boshlanishi bilan darhol yangilash uchun `'eager'` dan foydalaning. Eager yangilashlar himoyachilar yoki xatolar sababli navigatsiya muvaffaqiyatsiz boʻlganda urinilgan URL'ni koʻrsatishni osonlashtiradi, lekin uzoq ishlaydigan himoyachilaringiz boʻlsa, jarayondagi URL'ni qisqa vaqt koʻrsatib qoʻyishi mumkin.

Analitika konveyeringiz himoyachilar bloklasa ham urinilgan marshrutni koʻrishi kerak boʻlganda buni koʻrib chiqing.

```ts
provideRouter(routes, withRouterConfig({urlUpdateStrategy: 'eager'}));
```

### Soʻrov parametrlarini sukut boʻyicha qayta ishlashni tanlash {#choose-default-query-parameter-handling}

`defaultQueryParamsHandling` chaqiruvda `queryParamsHandling` koʻrsatilmaganda `Router.createUrlTree` uchun zaxira xatti-harakatni oʻrnatadi. `'replace'` — sukut boʻyicha qiymat boʻlib, mavjud soʻrov satrini almashtiradi. `'merge'` berilgan qiymatlarni joriylari bilan birlashtiradi, `'preserve'` esa siz aniq yangilarini bermaguningizcha mavjud soʻrov parametrlarini saqlab qoladi.

```ts
provideRouter(routes, withRouterConfig({defaultQueryParamsHandling: 'merge'}));
```

Bu, ayniqsa, qoʻshimcha parametrlar berilganda mavjud filtrlarni avtomatik saqlab qolish uchun qidiruv va filtr sahifalarida foydali.

### Oxirgi slash'ni qayta ishlashni sozlash {#configure-trailing-slash-handling}

Sukut boʻyicha `Location` servisi oʻqishda URL'lardan oxirgi slash'larni (trailing slash) olib tashlaydi.

Ilovangizda `TrailingSlashPathLocationStrategy`'ni taqdim etib, `Location` servisini brauzerga yoziladigan barcha URL'larda oxirgi slash'ni majburiy qoʻyishga sozlashingiz mumkin.

```ts
import {LocationStrategy, TrailingSlashPathLocationStrategy} from '@angular/common';

bootstrapApplication(App, {
  providers: [{provide: LocationStrategy, useClass: TrailingSlashPathLocationStrategy}],
});
```

Shuningdek, ilovangizda `NoTrailingSlashPathLocationStrategy`'ni taqdim etib, `Location` servisini brauzerga yoziladigan barcha URL'larda hech qachon oxirgi slash boʻlmasligiga majburlashingiz mumkin.

```ts
import {LocationStrategy, NoTrailingSlashPathLocationStrategy} from '@angular/common';

bootstrapApplication(App, {
  providers: [{provide: LocationStrategy, useClass: NoTrailingSlashPathLocationStrategy}],
});
```

Bu strategiyalar faqat brauzerga yoziladigan URL'ga taʼsir qiladi.
`Location.path()` va `Location.normalize()` URL'ni oʻqishda oxirgi slash'larni olib tashlashda davom etadi.

Angular Router sozlash uchun toʻrtta asosiy sohani taqdim etadi:

  <docs-pill-row>
    <docs-pill href="#route-reuse-strategy" title="Marshrutni qayta ishlatish strategiyasi"/>
    <docs-pill href="#preloading-strategy" title="Oldindan yuklash strategiyasi"/>
    <docs-pill href="#url-handling-strategy" title="URL'ni qayta ishlash strategiyasi"/>
    <docs-pill href="#custom-route-matchers" title="Maxsus marshrut moslashtiruvchilari"/>
  </docs-pill-row>

## Marshrutni qayta ishlatish strategiyasi {#route-reuse-strategy}

Marshrutni qayta ishlatish strategiyasi (route reuse strategy) Angular navigatsiya davomida komponentlarni yoʻq qilib qayta yaratishini yoki ularni qayta ishlatish uchun saqlab qolishini boshqaradi. Sukut boʻyicha Angular marshrutdan chiqib ketganda komponent nusxalarini yoʻq qiladi va qaytib kelganda yangi nusxalar yaratadi.

### Marshrutni qayta ishlatishni qachon implementatsiya qilish kerak {#when-to-implement-route-reuse}

Maxsus marshrutni qayta ishlatish strategiyalari quyidagilarga muhtoj ilovalar uchun foydali:

- **Forma holatini saqlash** — foydalanuvchilar chiqib ketib qaytganda qisman toʻldirilgan formalarni saqlab qolish
- **Qimmat maʼlumotlarni ushlab turish** — katta maʼlumotlar toʻplamlari yoki murakkab hisob-kitoblarni qayta olishdan qochish
- **Scroll holatini saqlash** — uzun roʻyxatlar yoki cheksiz scroll implementatsiyalarida scroll holatini saqlab qolish
- **Tab'ga oʻxshash interfeyslar** — tab'lar oʻrtasida almashganda komponent holatini saqlab turish

### Maxsus marshrutni qayta ishlatish strategiyasini yaratish {#creating-a-custom-route-reuse-strategy}

Angular'ning `RouteReuseStrategy` klassi "ajratilgan marshrut dastaklari" (detached route handles) tushunchasi orqali navigatsiya xatti-harakatini sozlash imkonini beradi.

"Ajratilgan marshrut dastaklari" — Angular'ning komponent nusxalari va ularning butun view iyerarxiyasini saqlash usuli. Marshrut ajratilganda Angular komponent nusxasini, uning bola komponentlarini va barcha bogʻliq holatni xotirada saqlab qoladi. Bu saqlangan holat keyinchalik marshrutga qaytib kelganda qayta biriktirilishi mumkin.

`RouteReuseStrategy` klassi marshrut komponentlarining hayot siklini boshqaruvchi quyidagi metodlarni taqdim etadi:

| Metod                                                                          | Tavsif                                                                                                      |
| ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| [`shouldDetach`](api/router/RouteReuseStrategy#shouldDetach)                   | Marshrutdan chiqib ketganda uni keyinchalik qayta ishlatish uchun saqlash kerakligini aniqlaydi             |
| [`store`](api/router/RouteReuseStrategy#store)                                 | `shouldDetach` true qaytarganda ajratilgan marshrut dastagini saqlaydi                                      |
| [`shouldAttach`](api/router/RouteReuseStrategy#shouldAttach)                   | Saqlangan marshrutga oʻtganda uni qayta biriktirish kerakligini aniqlaydi                                   |
| [`retrieve`](api/router/RouteReuseStrategy#retrieve)                           | Qayta biriktirish uchun oldin saqlangan marshrut dastagini qaytaradi                                        |
| [`shouldReuseRoute`](api/router/RouteReuseStrategy#shouldReuseRoute)           | Router navigatsiya davomida joriy marshrut nusxasini yoʻq qilish oʻrniga qayta ishlatishi kerakligini aniqlaydi |
| [`shouldDestroyInjector`](api/router/RouteReuseStrategy#shouldDestroyInjector) | Ajratilgan marshrut endi saqlanmayotganda router uning injector'ini yoʻq qilishi kerakligini aniqlaydi      |

Quyidagi misol marshrut metamaʼlumotlariga asoslanib komponent holatini tanlab saqlaydigan maxsus marshrutni qayta ishlatish strategiyasini koʻrsatadi:

```ts
import {
  RouteReuseStrategy,
  Route,
  ActivatedRouteSnapshot,
  DetachedRouteHandle,
} from '@angular/router';
import {Injectable} from '@angular/core';

@Injectable()
export class CustomRouteReuseStrategy implements RouteReuseStrategy {
  private handlers = new Map<Route | null, DetachedRouteHandle>();

  shouldDetach(route: ActivatedRouteSnapshot): boolean {
    // Determines if a route should be stored for later reuse
    return route.data['reuse'] === true;
  }

  store(route: ActivatedRouteSnapshot, handle: DetachedRouteHandle | null): void {
    // Stores the detached route handle when shouldDetach returns true
    if (handle && route.data['reuse'] === true) {
      const key = this.getRouteKey(route);
      this.handlers.set(key, handle);
    }
  }

  shouldAttach(route: ActivatedRouteSnapshot): boolean {
    // Checks if a stored route should be reattached
    const key = this.getRouteKey(route);
    return route.data['reuse'] === true && this.handlers.has(key);
  }

  retrieve(route: ActivatedRouteSnapshot): DetachedRouteHandle | null {
    // Returns the stored route handle for reattachment
    const key = this.getRouteKey(route);
    return route.data['reuse'] === true ? (this.handlers.get(key) ?? null) : null;
  }

  shouldReuseRoute(future: ActivatedRouteSnapshot, curr: ActivatedRouteSnapshot): boolean {
    // Determines if the router should reuse the current route instance
    return future.routeConfig === curr.routeConfig;
  }

  private getRouteKey(route: ActivatedRouteSnapshot): Route | null {
    return route.routeConfig;
  }
}
```

### Ajratilgan marshrut dastaklarini qoʻlda yoʻq qilish {#manually-destroying-detached-route-handles}

Maxsus `RouteReuseStrategy`'ni implementatsiya qilganda, agar `DetachedRouteHandle`'ni qayta biriktirmasdan tashlab yuborishga qaror qilsangiz, uni qoʻlda yoʻq qilishingiz kerak boʻlishi mumkin. Masalan, agar strategiyangizda kesh hajmi cheklovi boʻlsa yoki dastaklar maʼlum vaqtdan keyin eskirsa, xotira oqishlaridan (memory leak) qochish uchun komponent va uning holati toʻgʻri yoʻq qilinishini taʼminlashingiz shart.

`DetachedRouteHandle` shaffof boʻlmagan (opaque) tur boʻlgani uchun unda bevosita yoʻq qilish metodini chaqira olmaysiz. Buning oʻrniga Router taqdim etgan `destroyDetachedRouteHandle` funksiyasidan foydalaning.

```ts
import {destroyDetachedRouteHandle} from '@angular/router';

// ... inside your strategy
if (this.handles.size > MAX_CACHE_SIZE) {
  const handle = this.handles.get(oldestKey);
  if (handle) {
    destroyDetachedRouteHandle(handle);
    this.handles.delete(oldestKey);
  }
}
```

NOTE: `canMatch` himoyachilari ishtirok etganda marshrut yoʻlini kalit sifatida ishlatishdan qoching, chunki bu takroriy yozuvlarga olib kelishi mumkin.

### Ishlatilmayotgan marshrut injector'larini avtomatik tozalash {#automatic-cleanup-of-unused-route-injectors}

Sukut boʻyicha Angular ajratilgan marshrutlarning injector'larini, ular endi `RouteReuseStrategy` tomonidan saqlanmasa ham, yoʻq qilmaydi. Bu asosan koʻpchilik ilovalar uchun xotirani bu darajada boshqarish odatda talab qilinmagani bilan bogʻliq.

Ishlatilmayotgan marshrut injector'larini avtomatik tozalashni yoqish uchun router konfiguratsiyangizda `withAutoCleanupInjectors` imkoniyatidan foydalanishingiz mumkin. Bu imkoniyat navigatsiyalardan soʻng qaysi marshrutlar hozir strategiya tomonidan saqlanayotganini tekshiradi va qayta ishlatish strategiyasi tomonidan hozir saqlanmayotgan har qanday ajratilgan marshrutlarning injector'larini yoʻq qiladi.

```ts
import {provideRouter, withAutoCleanupInjectors} from '@angular/router';

export const appConfig: ApplicationConfig = {
  providers: [provideRouter(routes, withAutoCleanupInjectors())],
};
```

Agar maxsus `RouteReuseStrategy` taqdim etmasangiz yoki maxsus strategiyangiz `BaseRouteReuseStrategy`'ni kengaytirsa, injector'lar endi marshrut nofaol boʻlganda yoʻq qilinadi.

#### Maxsus `RouteReuseStrategy` bilan tozalash {#cleanup-with-a-custom-routereusestrategy}

Agar ilovangiz maxsus `RouteReuseStrategy`'dan foydalansa _va_ strategiya `BaseRouteReuseStrategy`'ni kengaytirmasa, router'ga qaysi marshrutlarning injector'lari yoʻq qilinishi kerakligini aytish uchun `shouldDestroyInjector`'ni implementatsiya qilishingiz shart:

```ts
@Injectable()
export class CustomRouteReuseStrategy implements RouteReuseStrategy {
  // ... other methods

  shouldDestroyInjector(route: Route): boolean {
    return !route.data['retainInjector'];
  }
}
```

Agar strategiyangiz qachondir `DetachedRouteHandle` saqlasa, Router oʻsha ajratilgan dastakka kerak boʻlgan injector'larni yoʻq qilmasligi uchun ular haqida Router'ga ham xabar berishingiz kerak boʻladi:

```ts
@Injectable()
export class CustomRouteReuseStrategy implements RouteReuseStrategy {
  private readonly handles = new Map<Route, DetachedRouteHandle>();

  store(route: ActivatedRouteSnapshot, handle: DetachedRouteHandle | null) {
    if (handle) {
      this.handles.set(route.routeConfig!, handle);
    }
  }

  retrieveStoredRouteHandles(): DetachedRouteHandle[] {
    return Array.from(this.handles.values());
  }

  // ... other methods
}
```

### Marshrutni maxsus qayta ishlatish strategiyasidan foydalanishga sozlash {#configuring-a-route-to-use-a-custom-route-reuse-strategy}

Marshrutlar marshrut konfiguratsiyasi metamaʼlumotlari orqali qayta ishlatish xatti-harakatini tanlashi mumkin. Bu yondashuv qayta ishlatish mantiqini komponent kodidan ajratib saqlaydi va komponentlarni oʻzgartirmasdan xatti-harakatni osongina moslashtirish imkonini beradi:

```ts
export const routes: Routes = [
  {
    path: 'products',
    component: ProductList,
    data: {reuse: true}, // Component state persists across navigations
  },
  {
    path: 'products/:id',
    component: ProductDetail,
    // No reuse flag - component recreates on each navigation
  },
  {
    path: 'search',
    component: Search,
    data: {reuse: true}, // Preserves search results and filter state
  },
];
```

Shuningdek, maxsus marshrutni qayta ishlatish strategiyasini Angular'ning bogʻliqliklarni inyeksiya qilish tizimi orqali ilova darajasida sozlashingiz mumkin. Bu holda Angular butun ilova boʻylab marshrutni qayta ishlatish bilan bogʻliq barcha qarorlarni boshqaradigan strategiyaning yagona nusxasini yaratadi:

```ts
export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    {provide: RouteReuseStrategy, useClass: CustomRouteReuseStrategy},
  ],
};
```

## Oldindan yuklash strategiyasi {#preloading-strategy}

Oldindan yuklash (preloading) strategiyalari Angular kechiktirilgan yuklanadigan (lazy-loaded) marshrut modullarini fonda qachon yuklashini belgilaydi. Lazy loading modullarni yuklab olishni kechiktirib dastlabki yuklanish vaqtini yaxshilasa-da, foydalanuvchilar lazy marshrutga birinchi marta oʻtganda baribir kechikishni sezadi. Oldindan yuklash strategiyalari modullarni foydalanuvchilar soʻrashidan oldin yuklab, bu kechikishni bartaraf etadi.

### Oʻrnatilgan oldindan yuklash strategiyalari {#built-in-preloading-strategies}

Angular tayyor holda ikkita oldindan yuklash strategiyasini taqdim etadi:

| Strategiya                                          | Tavsif                                                                                                           |
| --------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| [`NoPreloading`](api/router/NoPreloading)           | Barcha oldindan yuklashni oʻchirib qoʻyadigan sukut boʻyicha strategiya. Boshqacha aytganda, modullar faqat foydalanuvchilar ularga oʻtganda yuklanadi |
| [`PreloadAllModules`](api/router/PreloadAllModules) | Dastlabki navigatsiyadan soʻng darhol barcha kechiktirilgan yuklanadigan modullarni yuklaydi                   |

`PreloadAllModules` strategiyasini quyidagicha sozlash mumkin:

```ts
import {ApplicationConfig} from '@angular/core';
import {provideRouter, withPreloading, PreloadAllModules} from '@angular/router';
import {routes} from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [provideRouter(routes, withPreloading(PreloadAllModules))],
};
```

`PreloadAllModules` strategiyasi barcha modullarni yuklab olish unumdorlikka sezilarli taʼsir qilmaydigan kichik va oʻrta ilovalar uchun yaxshi ishlaydi. Biroq koʻplab funksional modullarga ega kattaroq ilovalar tanlab oldindan yuklashdan koʻproq foyda koʻrishi mumkin.

### Maxsus oldindan yuklash strategiyasini yaratish {#creating-a-custom-preloading-strategy}

Maxsus oldindan yuklash strategiyalari yagona `preload` metodini talab qiluvchi `PreloadingStrategy` interfeysini implementatsiya qiladi. Bu metod marshrut konfiguratsiyasini va haqiqiy modul yuklashni ishga tushiradigan funksiyani qabul qiladi. Strategiya oldindan yuklash tugaganda emit qiladigan Observable yoki oldindan yuklashni oʻtkazib yuborish uchun boʻsh Observable qaytaradi:

```ts
import {Injectable} from '@angular/core';
import {PreloadingStrategy, Route} from '@angular/router';
import {Observable, of, timer} from 'rxjs';
import {mergeMap} from 'rxjs/operators';

@Injectable()
export class SelectivePreloadingStrategy implements PreloadingStrategy {
  preload(route: Route, load: () => Observable<any>): Observable<any> {
    // Only preload routes marked with data: { preload: true }
    if (route.data?.['preload']) {
      return load();
    }
    return of(null);
  }
}
```

Bu tanlab yuklash strategiyasi oldindan yuklash xatti-harakatini aniqlash uchun marshrut metamaʼlumotlarini tekshiradi. Marshrutlar oʻz konfiguratsiyasi orqali oldindan yuklashni tanlashi mumkin:

```ts
import {Routes} from '@angular/router';

export const routes: Routes = [
  {
    path: 'dashboard',
    loadChildren: () => import('./dashboard/dashboard.routes'),
    data: {preload: true}, // Preload immediately after initial navigation
  },
  {
    path: 'reports',
    loadChildren: () => import('./reports/reports.routes'),
    data: {preload: false}, // Only load when user navigates to reports
  },
  {
    path: 'admin',
    loadChildren: () => import('./admin/admin.routes'),
    // No preload flag - won't be preloaded
  },
];
```

### Oldindan yuklashda unumdorlik masalalari {#performance-considerations-for-preloading}

Oldindan yuklash tarmoqdan foydalanishga ham, xotira sarfiga ham taʼsir qiladi. Har bir oldindan yuklangan modul tarmoq oʻtkazuvchanligini sarflaydi va ilovaning xotira hajmini oshiradi. Cheklangan trafikli ulanishdagi mobil foydalanuvchilar minimal oldindan yuklashni afzal koʻrishi mumkin, tez tarmoqdagi desktop foydalanuvchilari esa agressiv oldindan yuklash strategiyalarini koʻtara oladi.

Oldindan yuklash vaqti ham muhim. Dastlabki yuklanishdan keyin darhol oldindan yuklash rasmlar yoki API chaqiruvlari kabi boshqa muhim resurslar bilan raqobatlashishi mumkin. Strategiyalar unumdorlik pasayishidan qochish uchun ilovaning yuklanishdan keyingi xatti-harakatini hisobga olishi va boshqa fon vazifalari bilan muvofiqlashishi kerak.

Brauzer resurs cheklovlari ham oldindan yuklash xatti-harakatiga taʼsir qiladi. Brauzerlar bir vaqtdagi HTTP ulanishlarini cheklaydi, shuning uchun agressiv oldindan yuklash boshqa soʻrovlar orqasida navbatda qolishi mumkin. Service worker'lar keshlash va tarmoq soʻrovlarini nozik boshqarish imkonini berib, oldindan yuklash strategiyasini toʻldirishga yordam beradi.

## URL'ni qayta ishlash strategiyasi {#url-handling-strategy}

URL'ni qayta ishlash strategiyalari Angular router qaysi URL'larni qayta ishlashini va qaysilarini eʼtiborsiz qoldirishini belgilaydi. Sukut boʻyicha Angular ilova ichidagi barcha navigatsiya hodisalarini qayta ishlashga urinadi, lekin haqiqiy ilovalar koʻpincha boshqa tizimlar bilan birga yashashi, tashqi havolalarni qayta ishlashi yoki oʻz marshrutlarini oʻzi boshqaradigan eski ilovalar bilan integratsiya qilishi kerak boʻladi.

`UrlHandlingStrategy` klassi Angular boshqaradigan marshrutlar va tashqi URL'lar oʻrtasidagi bu chegarani boshqarish imkonini beradi. Bu ilovalarni Angular'ga bosqichma-bosqich koʻchirishda yoki Angular ilovalari URL maydonini boshqa freymvorklar bilan ulashishi kerak boʻlganda zarur boʻladi.

### Maxsus URL'ni qayta ishlash strategiyasini implementatsiya qilish {#implementing-a-custom-url-handling-strategy}

Maxsus URL'ni qayta ishlash strategiyalari `UrlHandlingStrategy` klassini kengaytiradi va uchta metodni implementatsiya qiladi. `shouldProcessUrl` metodi Angular berilgan URL'ni qayta ishlashi kerakligini aniqlaydi, `extract` URL'ning Angular qayta ishlashi kerak boʻlgan qismini qaytaradi, `merge` esa URL fragmentini URL'ning qolgan qismi bilan birlashtiradi:

```ts
import {Injectable} from '@angular/core';
import {UrlHandlingStrategy, UrlTree} from '@angular/router';

@Injectable()
export class CustomUrlHandlingStrategy implements UrlHandlingStrategy {
  shouldProcessUrl(url: UrlTree): boolean {
    // Only handle URLs that start with /app or /admin
    return url.toString().startsWith('/app') || url.toString().startsWith('/admin');
  }

  extract(url: UrlTree): UrlTree {
    // Return the URL unchanged if we should process it
    return url;
  }

  merge(newUrlPart: UrlTree, rawUrl: UrlTree): UrlTree {
    // Combine the URL fragment with the rest of the URL
    return newUrlPart;
  }
}
```

Bu strategiya URL maydonida aniq chegaralar yaratadi. Angular `/app` va `/admin` yoʻllarini qayta ishlaydi, qolgan hamma narsani eʼtiborsiz qoldiradi. Bu namuna Angular muayyan boʻlimlarni boshqarib, eski tizim boshqalarini saqlab turadigan eski ilovalarni koʻchirishda yaxshi ishlaydi.

### Maxsus URL'ni qayta ishlash strategiyasini sozlash {#configuring-a-custom-url-handling-strategy}

Maxsus strategiyani Angular'ning bogʻliqliklarni inyeksiya qilish tizimi orqali roʻyxatdan oʻtkazishingiz mumkin:

```ts
import {ApplicationConfig} from '@angular/core';
import {provideRouter, UrlHandlingStrategy} from '@angular/router';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    {provide: UrlHandlingStrategy, useClass: CustomUrlHandlingStrategy},
  ],
};
```

## Maxsus marshrut moslashtiruvchilari {#custom-route-matchers}

Sukut boʻyicha Angular router'i marshrutlarni aniqlangan tartibda koʻrib chiqib, URL yoʻlini har bir marshrutning yoʻl namunasiga moslashtirishga urinadi. U statik segmentlarni, parametrlangan segmentlarni (`:id`) va wildcard'larni (`**`) qoʻllab-quvvatlaydi. Mos kelgan birinchi marshrut gʻolib boʻladi va router qidirishni toʻxtatadi.

Ilovalar ish vaqtidagi shartlar, murakkab URL namunalari yoki boshqa maxsus qoidalarga asoslangan murakkabroq moslashtirish mantiqini talab qilganda, maxsus moslashtiruvchilar (custom matchers) standart marshrutlarning soddaligiga putur yetkazmasdan bu moslashuvchanlikni taqdim etadi.

Router maxsus moslashtiruvchilarni marshrutni moslashtirish bosqichida, yoʻl moslashtirilishidan oldin baholaydi. Moslashtiruvchi muvaffaqiyatli moslikni qaytarganda, u URL'dan parametrlarni ham ajratib olishi mumkin va ular standart marshrut parametrlari kabi faollashgan komponentga taqdim etiladi.

### Maxsus moslashtiruvchi yaratish {#creating-a-custom-matcher}

Maxsus moslashtiruvchi — URL segmentlarini qabul qilib, yo isteʼmol qilingan segmentlar va parametrlarga ega moslik natijasini, yo moslik yoʻqligini bildirish uchun null qaytaradigan funksiya. Moslashtiruvchi funksiya Angular marshrutning path xususiyatini baholashidan oldin ishga tushadi:

```ts
import {Route, UrlSegment, UrlSegmentGroup, UrlMatchResult} from '@angular/router';

export function customMatcher(
  segments: UrlSegment[],
  group: UrlSegmentGroup,
  route: Route,
): UrlMatchResult | null {
  // Matching logic here
  if (matchSuccessful) {
    return {
      consumed: segments,
      posParams: {
        paramName: new UrlSegment('paramValue', {}),
      },
    };
  }
  return null;
}
```

### Versiyaga asoslangan marshrutlashni implementatsiya qilish {#implementing-version-based-routing}

URL'dagi versiya raqamlariga qarab marshrutlashi kerak boʻlgan API hujjatlari saytini koʻrib chiqaylik. Turli versiyalar turli komponent tuzilmalari yoki imkoniyatlar toʻplamiga ega boʻlishi mumkin:

```ts
import {Routes, UrlSegment, UrlMatchResult} from '@angular/router';

export function versionMatcher(segments: UrlSegment[]): UrlMatchResult | null {
  // Match patterns like /v1/docs, /v2.1/docs, /v3.0.1/docs
  if (segments.length >= 2 && segments[0].path.match(/^v\d+(\.\d+)*$/)) {
    return {
      consumed: segments.slice(0, 2), // Consume version and 'docs'
      posParams: {
        version: segments[0], // Make version available as a parameter
        section: segments[1], // Make section available too
      },
    };
  }
  return null;
}

// Route configuration
export const routes: Routes = [
  {
    matcher: versionMatcher,
    component: Documentation,
  },
  {
    path: 'latest/docs',
    redirectTo: 'v3/docs',
  },
];
```

Komponent ajratib olingan parametrlarni marshrut input'lari orqali qabul qiladi:

```angular-ts
import {Component, input, inject, resource} from '@angular/core';

@Component({
  selector: 'app-documentation',
  template: `
    @if (documentation.isLoading()) {
      <div>Loading documentation...</div>
    } @else if (documentation.error()) {
      <div>Error loading documentation</div>
    } @else if (documentation.value(); as docs) {
      <article>{{ docs.content }}</article>
    }
  `,
})
export class Documentation {
  // Route parameters are automatically bound to signal inputs
  version = input.required<string>(); // Receives the version parameter
  section = input.required<string>(); // Receives the section parameter

  private docsService = inject(DocumentationService);

  // Resource automatically loads documentation when version or section changes
  documentation = resource({
    params: () => {
      if (!this.version() || !this.section()) return;

      return {
        version: this.version(),
        section: this.section(),
      };
    },
    loader: ({params}) => {
      return this.docsService.loadDocumentation(params.version, params.section);
    },
  });
}
```

### Lokalni hisobga oluvchi marshrutlash {#locale-aware-routing}

Xalqaro ilovalar koʻpincha lokal (locale) maʼlumotlarini URL'larda kodlaydi. Maxsus moslashtiruvchi lokal kodlarini ajratib olib, lokalni parametr sifatida taqdim etgan holda mos komponentlarga marshrutlashi mumkin:

```ts
// Supported locales
const locales = ['en', 'es', 'fr', 'de', 'ja', 'zh'];

export function localeMatcher(segments: UrlSegment[]): UrlMatchResult | null {
  if (segments.length > 0) {
    const potentialLocale = segments[0].path;

    if (locales.includes(potentialLocale)) {
      // This is a locale prefix, consume it and continue matching
      return {
        consumed: [segments[0]],
        posParams: {
          locale: segments[0],
        },
      };
    } else {
      // No locale prefix, use default locale
      return {
        consumed: [], // Don't consume any segments
        posParams: {
          locale: new UrlSegment('en', {}),
        },
      };
    }
  }

  return null;
}
```

### Murakkab biznes mantiqi boʻyicha moslashtirish {#complex-business-logic-matching}

Maxsus moslashtiruvchilar yoʻl namunalarida ifodalash noqulay boʻlgan biznes qoidalarini implementatsiya qilishda juda samarali. Mahsulot URL'lari mahsulot turiga qarab turli namunalarga amal qiladigan elektron tijorat saytini koʻrib chiqaylik:

```ts
export function productMatcher(segments: UrlSegment[]): UrlMatchResult | null {
  if (segments.length === 0) return null;

  const firstSegment = segments[0].path;

  // Books: /isbn-1234567890
  if (firstSegment.startsWith('isbn-')) {
    return {
      consumed: [segments[0]],
      posParams: {
        productType: new UrlSegment('book', {}),
        identifier: new UrlSegment(firstSegment.substring(5), {}),
      },
    };
  }

  // Electronics: /sku/ABC123
  if (firstSegment === 'sku' && segments.length > 1) {
    return {
      consumed: segments.slice(0, 2),
      posParams: {
        productType: new UrlSegment('electronics', {}),
        identifier: segments[1],
      },
    };
  }

  // Clothing: /style/BRAND/ITEM
  if (firstSegment === 'style' && segments.length > 2) {
    return {
      consumed: segments.slice(0, 3),
      posParams: {
        productType: new UrlSegment('clothing', {}),
        brand: segments[1],
        identifier: segments[2],
      },
    };
  }

  return null;
}
```

### Maxsus moslashtiruvchilarda unumdorlik masalalari {#performance-considerations-for-custom-matchers}

Maxsus moslashtiruvchilar moslik topilgunga qadar har bir navigatsiya urinishida ishga tushadi. Natijada murakkab moslashtirish mantiqi, ayniqsa koʻp marshrutli ilovalarda, navigatsiya unumdorligiga taʼsir qilishi mumkin. Moslashtiruvchilarni aniq maqsadli va samarali saqlang:

- Moslik imkonsiz boʻlganda erta qaytaring
- API chaqiruvlari yoki murakkab regulyar ifodalar kabi qimmat operatsiyalardan qoching
- Takrorlanuvchi URL namunalari uchun natijalarni keshlashni koʻrib chiqing

Maxsus moslashtiruvchilar murakkab marshrutlash talablarini nafis hal qilsa-da, ulardan haddan ortiq foydalanish marshrut konfiguratsiyasini tushunish va qoʻllab-quvvatlashni qiyinlashtirishi mumkin. Maxsus moslashtiruvchilarni standart yoʻl moslashtirish haqiqatan ham yetarli boʻlmagan holatlar uchun saqlang.
