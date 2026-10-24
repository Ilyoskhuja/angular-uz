# Resource'lar bilan maʼlumot olish

Angular Router `resources` marshrut konfiguratsiyasi orqali Angular signallari bilan integratsiyalashadi. Bu `Resource` API'lari yordamida maʼlumotlarni reaktiv tarzda olish (data fetching) imkonini beradi.

## Nega marshrut resource'laridan foydalanish kerak? {#why-use-route-resources}

Marshrut resource'lari anʼanaviy [maʼlumot resolver'lariga](/guide/routing/data-resolvers) nisbatan bir qancha afzalliklarga ega:

- **Parallel bajarilish**: Barcha mos kelgan marshrutlardagi marshrut resource'lari bir vaqtning oʻzida bitta marshrut oʻrniga parallel yuklanadi.
- **Bloklamaydigan maʼlumot yuklash**: Marshrutni darhol faollashtirish va maʼlumot fonda yuklanayotganda yuklanish skeletlari yoki UI holatlarini render qilish uchun `nonBlocking()` dan foydalaning.
- **Qayta navigatsiyasiz qayta yuklash**: Guard'larni qayta ishga tushirmasdan yoki marshrutlarni qayta moslashtirmasdan maʼlumotni yangilash uchun alohida resource'larda `.reload()` ni chaqiring yoki signal parametrlarini yangilang.
- **Reaktiv maʼlumot olish**: Resource'lar Angular signallari bilan bevosita integratsiyalashadi, signal bogʻliqliklari oʻzgarganda avtomatik qayta hisoblanadi va `isLoading()` va `error()` kabi reaktiv holat signallarini taqdim etadi.

## Marshrut resource'larini yoqish {#enabling-route-resources}

Marshrut resource'larini yoqish uchun router konfiguratsiyangizga `withRouterResources()` ni taqdim eting:

```ts
import {provideRouter, withComponentInputBinding, withRouterResources} from '@angular/router';

bootstrapApplication(App, {
  providers: [provideRouter(routes, withComponentInputBinding(), withRouterResources())],
});
```

TIP: Router hal qilingan resource'larni bevosita komponent input'lariga bogʻlay olishi uchun `withComponentInputBinding()` ni yoqing.

## Marshrut resource'larini aniqlash {#defining-route-resources}

Marshrutdagi resource'larni `resources` funksiyasi bilan aniqlaysiz. Funksiya inyeksiya kontekstida ishlaydi, shuning uchun servislar, API klientlari yoki store'larga bevosita marshrut taʼrifi ichida `inject()` orqali murojaat qilishingiz mumkin.

```angular-ts
import {Component, inject, input, resource} from '@angular/core';
import {Routes} from '@angular/router';
import {UserService} from './user.service';

const routes: Routes = [
  {
    path: 'user/:id',
    component: UserProfile,
    resources: (ctx) => {
      const userService = inject(UserService);
      return {
        user: resource({
          params: () => ctx.params()['id'],
          loader: ({params: id}) => userService.getUser(id),
        }),
      };
    },
  },
];

@Component({
  template: `<p>User: {{ user().name }}</p>`,
})
export class UserProfile {
  // The router binds only the value for blocking resources.
  user = input.required<User>();
}
```

### `ResourceContext` obyekti {#the-resourcecontext-object}

`resources` funksiyasi reaktiv marshrut signallariga — `params`, `queryParams`, `fragment` va `data` — kirish imkonini beruvchi `ResourceContext` ni qabul qiladi.

### Qoʻllab-quvvatlanadigan resource implementatsiyalari {#supported-resource-implementations}

`resources` funksiyasi `resource()`, `rxResource()` yoki maxsus resource kabi har qanday Angular `Resource` implementatsiyasini qaytarishi mumkin.

```ts
import {Routes} from '@angular/router';
import {rxResource} from '@angular/core/rxjs-interop';

const routes: Routes = [
  {
    path: 'user/:id',
    component: UserProfile,
    resources: (ctx) => ({
      user: rxResource({
        params: () => ctx.params()['id'],
        stream: ({params: id}) => fetchUserObservable(id),
      }),
    }),
  },
];
```

NOTE: `rxResource` Observable qaytaruvchi funksiyani qabul qilish uchun `loader` oʻrniga `stream` xususiyatidan foydalanadi.

Resource'larni sozlashdan oldin asinxron tayyorgarlik yoki dinamik importlarni bajarish kerak boʻlsa, `resources` funksiyasi `async` boʻlishi va `Promise` qaytarishi ham mumkin:

```ts
resources: async (ctx) => {
  const injector = inject(Injector);
  const {fetchUserData} = await import('./user-api');
  return {
    user: resource({
      params: () => ctx.params()['id'],
      loader: ({params: id}) => fetchUserData(id),
      injector,
    }),
  };
},
```

## Signallar bilan nozik oʻzgarishlarni kuzatish {#fine-grained-change-tracking-with-signals}

Resource oʻzining `params` funksiyasi oʻqiydigan signallarni kuzatadi. Resource faqat oʻsha qiymat oʻzgarganda qayta yuklanishi uchun aynan kerakli qiymatni oʻqing:

```ts
resources: (ctx) => ({
  products: resource({
    // Tracks only the 'category' query parameter
    params: () => ctx.queryParams()['category'],
    loader: ({params: category}) => fetchProducts(category),
  }),
}),
```

`?sort=desc` yoki `?page=2` kabi aloqasi boʻlmagan soʻrov parametrini oʻzgartiruvchi navigatsiya `category` ni oʻzgartirmaydi, shuning uchun resource qayta yuklanmaydi.

TIP: `ctx.params()` kabi butun parametrlar obyektini qaytarish oʻrniga `ctx.params()['id']` kabi aniq xususiyatlarni oʻqing. Router har bir navigatsiyada yangi obyekt yaratadi, shuning uchun butun obyektni qaytarish alohida qiymatlar oʻzgarmagan boʻlsa ham resource'ni qayta yuklaydi.

## Parallel bajarilish {#parallel-execution}

Maʼlumot resolver'lari ota marshrutdan bola marshrutga ketma-ket bajariladi. Agar ota marshrut resolver'i 200ms, bola marshrut resolver'i esa 300ms vaqt olsa, navigatsiya 500ms davomida bloklanadi.

Mos kelgan marshrut ierarxiyasidagi marshrut resource'lari parallel ishlaydi, shuning uchun oʻsha navigatsiya 300ms — eng sekin resource vaqti — ichida yakunlanadi.

## Bloklaydigan va bloklamaydigan resource'lar {#blocking-and-non-blocking-resources}

Sukut boʻyicha `resources` dan qaytarilgan har bir resource bloklaydigan hisoblanadi: router marshrut va komponentni faollashtirishdan oldin maʼlumot toʻliq yuklanishini kutadi.

Bloklaydigan resource uchun router hal qilingan qiymatni komponent input'iga bogʻlaydi, shuning uchun input turi `Resource<T>` oʻrniga `T` boʻladi. Komponent hech qachon `loading` holatini kuzatmaydi, chunki router resource yuklanishigacha navigatsiyani bloklaydi, va hech qachon `error` holatini kuzatmaydi, chunki resource'da xato yuz berganda router navigatsiyani bekor qiladi.

Buning oʻrniga yuklanish holatlarini UI'da boshqarish uchun resource'ni `nonBlocking()` ga oʻrang. Router komponentni darhol faollashtiradi va toʻliq `Resource<T>` obyektini komponent input'iga bogʻlaydi; bu sizga `isLoading()`, `error()` va boshqa resource signallariga kirish imkonini beradi.

```angular-ts
import {Component, input, Resource, resource} from '@angular/core';
import {Routes, nonBlocking} from '@angular/router';

const routes: Routes = [
  {
    path: 'reports',
    component: Reports,
    resources: () => ({
      reportData: nonBlocking(
        resource({
          loader: () => fetchHeavyReportData(),
        }),
      ),
    }),
  },
];

@Component({
  template: `
    @if (reportData().isLoading()) {
      <p>Loading...</p>
    } @else if (reportData().error()) {
      <p>Error loading report.</p>
    } @else if (reportData().hasValue()) {
      <report-view [data]="reportData().value()" />
    }
  `,
})
export class Reports {
  reportData = input.required<Resource<ReportData>>();
}
```

NOTE: Agar bloklaydigan resource'da xato yuz bersa, router navigatsiyani bekor qiladi va `NavigationError` hodisasini yuboradi. `nonBlocking()` ga oʻralgan resource navigatsiyani yakunlaydi va xatoni oʻzining `error()` signali orqali taqdim etadi.

### Resource'dan qayta yoʻnaltirish {#redirecting-from-a-resource}

Agar bloklaydigan resource foydalanuvchini qayta yoʻnaltirishi kerak boʻlsa (masalan, element topilmaganda), resource loader'i ichida `RedirectCommand` ni throw qiling. Router joriy navigatsiyani bekor qiladi va koʻrsatilgan URL'ga qayta yoʻnaltiradi:

```ts
import {inject, resource} from '@angular/core';
import {RedirectCommand, Router, Routes} from '@angular/router';

const routes: Routes = [
  {
    path: 'user/:id',
    component: UserProfile,
    resources: (ctx) => {
      const router = inject(Router);

      return {
        user: resource({
          params: () => ctx.params()['id'],
          loader: async ({params: id}) => {
            const user = await fetchUser(id);
            if (!user) {
              throw new RedirectCommand(router.parseUrl('/not-found'));
            }
            return user;
          },
        }),
      };
    },
  },
];
```

## Resource'larni qayta navigatsiyasiz qayta yuklash {#reloading-resources-without-renavigation}

Maʼlumot resolver'lari bilan maʼlumotni qayta olish marshrut navigatsiyasini talab qiladi (masalan, `onSameUrlNavigation: 'reload'` bilan navigatsiya qilish), bu esa marshrutlarni qayta moslashtiradi va guard'lar hamda resolver'larni qayta ishga tushiradi.

Marshrut resource'lari maʼlumotni joyida yangilashning ikki usulini qoʻllab-quvvatlaydi:

1. **Dasturiy qayta yuklash**: `Resource` nusxasida `.reload()` ni chaqiring.
2. **Reaktiv qayta yuklash**: Resource'ning `params` funksiyasi oʻqiydigan signalni, masalan, ilova filtri yoki holat signalini yangilang; bu loader'ni qayta ishga tushiradi.

Router bloklaydigan resource'ning faqat qiymatini komponent input'iga bogʻlagani uchun, `.reload()` ni chaqirish yoki holat signallarini koʻrish kerak boʻlganda `Resource` nusxasini `ActivatedRoute` yoki `ActivatedRouteSnapshot` dan oʻqing:

```angular-ts
import {Component, inject, input} from '@angular/core';
import {ActivatedRoute} from '@angular/router';

@Component({
  template: `
    <p>User: {{ user().name }}</p>
    <button (click)="refreshUser()">Refresh</button>
  `,
})
export class UserProfile {
  user = input.required<User>();
  private userResource = inject(ActivatedRoute).resources?.['user'];

  refreshUser() {
    // Reloads only this specific resource without renavigating the route
    this.userResource?.reload();
  }
}
```

## Kutilayotgan navigatsiyalar davomidagi oʻtish holatlari {#transitional-states-during-pending-navigations}

Navigatsiya kutilayotgan paytda router `ActivatedRoute` da taqdim etadigan resource'larni muzlatib qoʻyadi, bu esa oraliq `loading` va `reloading` holatlarini yashiradi.

Agar `/user/1` dan `/user/2` ga navigatsiya qilsangiz va router `UserProfile` komponentini qayta ishlatsa, komponent `/user/2` hal qilinmaguncha `/user/1` maʼlumotlarini render qilishda davom etadi. Keyin router resource'larni muzlatishdan chiqaradi va UI yuklanish miltillashisiz bevosita yangi maʼlumotlarga oʻtadi.

Router bu resource'larni faqat oʻqish uchun (read-only) taqdim etadi, hatto `resources` funksiyasi `resource()` kabi yozish mumkin boʻlgan resource qaytarsa ham. Resource signallarini oʻqishingiz va `reload()` ni chaqirishingiz mumkin, lekin `set()` yoki `update()` ni emas. Faol navigatsiya yoki orqaga qaytarish (rollback) tiklanishi davomida chaqirilgan `reload()` router oʻtishini kuzatishga xalaqit bera olmasligi uchun `false` qaytaradi.

### Bekor qilishda orqaga qaytarish orqali tiklanish {#rollback-recovery-on-cancellation}

Agar navigatsiya bekor qilinsa (masalan, guard tomonidan), router holat daraxtini oldingi holatga qaytaradi. Bu qaytarish resource'ning signal bogʻliqliklari, masalan, marshrut parametrlarining oldingi qiymatlariga qaytishiga sabab boʻlishi mumkin.

Parametrlar orqaga qaytgani uchun resource eski parametrlar uchun maʼlumot olish maqsadida avtomatik yangi yuklashni ishga tushirishi mumkin. Allaqachon koʻrinib turgan maʼlumot uchun yuklanish holati miltillashining oldini olish maqsadida router resource qaytarilgan holatda barqarorlashmaguncha oldingi resource suratini (snapshot) UI'da saqlab qoladi.

TIP: Resource loader'i taqdim etgan `abortSignal` ni asinxron chaqiruvlaringizga (masalan, `fetch`) uzating. Router parametrlarni orqaga qaytarganda yoki navigatsiyalarni almashtirganda kutilayotgan soʻrov toza bekor qilinadi: `loader: ({params: id, abortSignal}) => fetchUser(id, {signal: abortSignal})`.
