# Maʼlumot resolver'lari

Maʼlumot resolver'lari (data resolvers) marshrutga oʻtishdan oldin maʼlumotlarni yuklab olish imkonini beradi va komponentlaringiz render qilinishidan oldin kerakli maʼlumotlarni olishini taʼminlaydi. Bu yuklanish holatlariga ehtiyojni bartaraf etishga va muhim maʼlumotlarni oldindan yuklash orqali foydalanuvchi tajribasini yaxshilashga yordam beradi.

TIP: Ilovangiz Angular Signals'dan foydalansa, `Resource` API'lari bilan reaktiv maʼlumot yuklash va bloklamaydigan maʼlumot yuklashni oʻrnatilgan tarzda qoʻllab-quvvatlash uchun [marshrut resurslaridan](/guide/routing/data-fetching-with-resources) foydalanishni koʻrib chiqing.

## Maʼlumot resolver'lari nima? {#what-are-data-resolvers}

Maʼlumot resolver'i — `ResolveFn` funksiyasini amalga oshiruvchi servis. U marshrut faollashishidan oldin ishga tushadi va API'lar, maʼlumotlar bazalari yoki boshqa manbalardan maʼlumot yuklab olishi mumkin. Olingan (resolved) maʼlumot komponentga `ActivatedRoute` orqali taqdim etiladi.

Maʼlumot resolver'lari [marshrut darajasida taqdim etilgan servislarga](guide/di/defining-dependency-providers#route-providers), shuningdek `route` argumenti orqali marshrutga xos maʼlumotlarga murojaat qila oladi.

## Nega maʼlumot resolver'laridan foydalanish kerak? {#why-use-data-resolvers}

Maʼlumot resolver'lari marshrutlashdagi keng tarqalgan muammolarni hal qiladi:

- **Boʻsh holatlarning oldini olish**: Komponentlar yuklanishi bilanoq maʼlumotlarni oladi
- **Yaxshiroq foydalanuvchi tajribasi**: Muhim maʼlumotlar uchun yuklanish spinner'lari yoʻq
- **Xatolarga ishlov berish**: Maʼlumot yuklash xatolariga navigatsiyadan oldin ishlov bering
- **Maʼlumotlar izchilligi**: Render qilishdan oldin zarur maʼlumotlar mavjudligini taʼminlaydi, bu SSR uchun muhim

## Resolver yaratish {#creating-a-resolver}

Resolver'ni `ResolveFn` turidagi funksiya yozish orqali yaratasiz.

U parametr sifatida `ActivatedRouteSnapshot` va `RouterStateSnapshot`'ni qabul qiladi.

Quyida [`inject`](api/core/inject) funksiyasidan foydalanib, marshrutni render qilishdan oldin foydalanuvchi maʼlumotlarini oladigan resolver keltirilgan:

```ts
import {inject} from '@angular/core';
import {UserStore, SettingsStore} from './user-store';
import type {ActivatedRouteSnapshot, ResolveFn, RouterStateSnapshot} from '@angular/router';
import type {User, Settings} from './types';

export const userResolver: ResolveFn<User> = (
  route: ActivatedRouteSnapshot,
  state: RouterStateSnapshot,
) => {
  const userStore = inject(UserStore);
  const userId = route.paramMap.get('id')!;
  return userStore.getUser(userId);
};

export const settingsResolver: ResolveFn<Settings> = (
  route: ActivatedRouteSnapshot,
  state: RouterStateSnapshot,
) => {
  const settingsStore = inject(SettingsStore);
  const userId = route.paramMap.get('id')!;
  return settingsStore.getUserSettings(userId);
};
```

## Marshrutlarni resolver'lar bilan sozlash {#configuring-routes-with-resolvers}

Marshrutga bir yoki bir nechta maʼlumot resolver'ini qoʻshmoqchi boʻlsangiz, ularni marshrut konfiguratsiyasidagi `resolve` kaliti ostiga qoʻshishingiz mumkin. `Routes` turi marshrut konfiguratsiyalarining tuzilmasini belgilaydi:

```ts
import {Routes} from '@angular/router';

export const routes: Routes = [
  {
    path: 'user/:id',
    component: UserDetail,
    resolve: {
      user: userResolver,
      settings: settingsResolver,
    },
  },
];
```

[`resolve` konfiguratsiyasi haqida API hujjatlarida](api/router/Route#resolve) koʻproq bilib olishingiz mumkin.

## Komponentlarda olingan maʼlumotlarga murojaat qilish {#accessing-resolved-data-in-components}

### ActivatedRoute'dan foydalanish {#using-activatedroute}

Komponentda olingan maʼlumotlarga `ActivatedRoute`'dagi `data` observable'ini `toSignal` funksiyasi yordamida signalga aylantirish orqali murojaat qilishingiz mumkin:

```angular-ts
import {Component, inject, computed} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {toSignal} from '@angular/core/rxjs-interop';
import type {User, Settings} from './types';

@Component({
  template: `
    <h1>{{ user().name }}</h1>
    <p>{{ user().email }}</p>
    <div>Theme: {{ settings().theme }}</div>
  `,
})
export class UserDetail {
  private route = inject(ActivatedRoute);
  private data = toSignal(this.route.data, {requireSync: true});
  user = computed(() => this.data().user as User);
  settings = computed(() => this.data().settings as Settings);
}
```

### withComponentInputBinding'dan foydalanish {#using-withcomponentinputbinding}

Olingan maʼlumotlarga murojaat qilishning boshqa yoʻli — router'ni `provideRouter` bilan sozlashda `withComponentInputBinding()`'dan foydalanish. Bu olingan maʼlumotlarni toʻgʻridan-toʻgʻri komponent input'lari sifatida uzatish imkonini beradi:

```ts
import {bootstrapApplication} from '@angular/platform-browser';
import {provideRouter, withComponentInputBinding} from '@angular/router';
import {routes} from './app.routes';

bootstrapApplication(App, {
  providers: [provideRouter(routes, withComponentInputBinding())],
});
```

Bu konfiguratsiya bilan komponentingizda resolver kalitlariga mos keluvchi input'larni `input` funksiyasi va majburiy input'lar uchun `input.required` yordamida aniqlashingiz mumkin:

```angular-ts
import {Component, input} from '@angular/core';
import type {User, Settings} from './types';

@Component({
  template: `
    <h1>{{ user().name }}</h1>
    <p>{{ user().email }}</p>
    <div>Theme: {{ settings().theme }}</div>
  `,
})
export class UserDetail {
  user = input.required<User>();
  settings = input.required<Settings>();
}
```

Bu yondashuv yaxshiroq tur xavfsizligini taʼminlaydi va faqat olingan maʼlumotlarga murojaat qilish uchun `ActivatedRoute`'ni inyeksiya qilish zaruratini bartaraf etadi.

## Resolver'larda xatolarga ishlov berish {#error-handling-in-resolvers}

Navigatsiya muvaffaqiyatsiz boʻlgan hollarda maʼlumot resolver'laringizda xatolarga toʻgʻri ishlov berish muhim. Aks holda `NavigationError` yuz beradi va joriy marshrutga navigatsiya muvaffaqiyatsiz tugaydi, bu esa foydalanuvchilaringiz uchun yomon tajribaga olib keladi.

Maʼlumot resolver'lari bilan xatolarga ishlov berishning uchta asosiy usuli mavjud:

1. Xatolarga ishlov berishni `withNavigationErrorHandler`'da markazlashtirish
2. Xatolarni router hodisalariga obuna orqali boshqarish
3. Xatolarga toʻgʻridan-toʻgʻri resolver ichida ishlov berish

### Xatolarga ishlov berishni `withNavigationErrorHandler`'da markazlashtirish {#centralize-error-handling-in-withnavigationerrorhandler}

[`withNavigationErrorHandler`](api/router/withNavigationErrorHandler) imkoniyati barcha navigatsiya xatolariga, jumladan muvaffaqiyatsiz maʼlumot resolver'laridan kelib chiqqan xatolarga ishlov berishning markazlashgan usulini taqdim etadi. Bu yondashuv xatolarga ishlov berish logikasini bir joyda saqlaydi va resolver'lar boʻylab xatolarga ishlov beruvchi kodning takrorlanishini oldini oladi.

```ts
import {bootstrapApplication} from '@angular/platform-browser';
import {provideRouter, Router, withNavigationErrorHandler} from '@angular/router';
import {inject} from '@angular/core';
import {routes} from './app.routes';

bootstrapApplication(App, {
  providers: [
    provideRouter(
      routes,
      withNavigationErrorHandler((error) => {
        const router = inject(Router);

        if (error.error?.message) {
          console.error('Navigation error occurred:', error.error.message);
        }

        router.navigate(['/error']);
      }),
    ),
  ],
});
```

Bu konfiguratsiya bilan resolver'laringiz maʼlumot yuklashga eʼtibor qaratishi mumkin, xato holatlarini esa markazlashgan ishlov beruvchi boshqaradi:

```ts
export const userResolver: ResolveFn<User> = (route) => {
  const userStore = inject(UserStore);
  const userId = route.paramMap.get('id')!;
  // No need for explicit error handling - let it bubble up
  return userStore.getUser(userId);
};
```

### Xatolarni router hodisalariga obuna orqali boshqarish {#managing-errors-through-a-subscription-to-router-events}

Resolver xatolariga router hodisalariga obuna boʻlib, `NavigationError` hodisalarini tinglash orqali ham ishlov berishingiz mumkin. Bu yondashuv xatolarga ishlov berish ustidan yanada aniq nazoratni beradi va maxsus xatodan tiklanish logikasini amalga oshirish imkonini yaratadi.

```angular-ts
import {Component, inject, signal} from '@angular/core';
import {Router, NavigationError} from '@angular/router';
import {toSignal} from '@angular/core/rxjs-interop';
import {map} from 'rxjs';

@Component({
  selector: 'app-root',
  template: `
    @if (errorMessage()) {
      <div class="error-banner">
        {{ errorMessage() }}
        <button (click)="retryNavigation()">Retry</button>
      </div>
    }
    <router-outlet />
  `,
})
export class App {
  private router = inject(Router);
  private lastFailedUrl = signal('');

  private navigationErrors = toSignal(
    this.router.events.pipe(
      map((event) => {
        if (event instanceof NavigationError) {
          this.lastFailedUrl.set(event.url);

          if (event.error) {
            console.error('Navigation error', event.error);
          }

          return 'Navigation failed. Please try again.';
        }
        return '';
      }),
    ),
    {initialValue: ''},
  );

  errorMessage = this.navigationErrors;

  retryNavigation() {
    if (this.lastFailedUrl()) {
      this.router.navigateByUrl(this.lastFailedUrl());
    }
  }
}
```

Bu yondashuv quyidagilar kerak boʻlganda ayniqsa foydali:

- Muvaffaqiyatsiz navigatsiya uchun maxsus qayta urinish logikasini amalga oshirish
- Xato turiga qarab muayyan xato xabarlarini koʻrsatish
- Analitika maqsadida navigatsiya xatolarini kuzatish

### Xatolarga toʻgʻridan-toʻgʻri resolver ichida ishlov berish {#handling-errors-directly-in-the-resolver}

Quyida xatoni jurnalga yozib, `Router` servisi yordamida umumiy `/users` sahifasiga qaytib navigatsiya qiladigan `userResolver`'ning yangilangan misoli keltirilgan:

```ts
import {inject} from '@angular/core';
import {ResolveFn, RedirectCommand, Router} from '@angular/router';
import {catchError, of, EMPTY} from 'rxjs';
import {UserStore} from './user-store';
import type {User} from './types';

export const userResolver: ResolveFn<User | RedirectCommand> = (route) => {
  const userStore = inject(UserStore);
  const router = inject(Router);
  const userId = route.paramMap.get('id')!;

  return userStore.getUser(userId).pipe(
    catchError((error) => {
      console.error('Failed to load user:', error);
      return of(new RedirectCommand(router.parseUrl('/users')));
    }),
  );
};
```

## Navigatsiya yuklanishi bilan bogʻliq mulohazalar {#navigation-loading-considerations}

Maʼlumot resolver'lari komponentlar ichidagi yuklanish holatlarining oldini olsa-da, ular boshqa bir UX masalasini keltirib chiqaradi: resolver'lar bajarilayotgan vaqtda navigatsiya bloklanadi. Foydalanuvchilar havolani bosish va yangi marshrutni koʻrish oʻrtasida, ayniqsa sekin tarmoq soʻrovlarida, kechikishlarni sezishi mumkin.

TIP: Navigatsiyani bloklamaslik va komponentlarni skelet yoki yuklanish indikatorlari bilan darhol render qilish uchun [bloklamaydigan marshrut resurslaridan](/guide/routing/data-fetching-with-resources#blocking-and-non-blocking-resources) foydalaning.

### Navigatsiya haqida fikr bildirish {#providing-navigation-feedback}

Resolver bajarilishi davomida foydalanuvchi tajribasini yaxshilash uchun router hodisalarini tinglab, yuklanish indikatorlarini koʻrsatishingiz mumkin:

```angular-ts
import {Component, computed, inject} from '@angular/core';
import {Router} from '@angular/router';

@Component({
  selector: 'app-root',
  template: `
    @if (isNavigating()) {
      <div class="loading-bar">Loading...</div>
    }
    <router-outlet />
  `,
})
export class App {
  private router = inject(Router);
  isNavigating = computed(() => !!this.router.currentNavigation());
}
```

Bu yondashuv resolver'lar maʼlumot yuklayotgan vaqtda foydalanuvchilar navigatsiya davom etayotgani haqida vizual fikr olishini taʼminlaydi.

## Eng yaxshi amaliyotlar {#best-practices}

- **Resolver'larni yengil saqlang**: Resolver'lar sahifaga kerak boʻlishi mumkin boʻlgan hamma narsani emas, faqat zarur maʼlumotlarni yuklashi kerak
- **Xatolarga ishlov bering**: Foydalanuvchilarga eng yaxshi tajribani taqdim etish uchun xatolarga toʻgʻri ishlov berishni doimo unutmang
- **Keshlashdan foydalaning**: Unumdorlikni oshirish uchun olingan maʼlumotlarni keshlashni koʻrib chiqing
- **Navigatsiya UX'ini hisobga oling**: Maʼlumot yuklash vaqtida navigatsiya bloklangani uchun resolver bajarilishiga yuklanish indikatorlarini qoʻshing
- **Oqilona timeout'lar oʻrnating**: Cheksiz osilib qolishi va navigatsiyani bloklashi mumkin boʻlgan resolver'lardan qoching
- **Tur xavfsizligi**: Olingan maʼlumotlar uchun TypeScript interfeyslaridan foydalaning

## Bola resolver'larda ota marshrutning olingan maʼlumotlarini oʻqish {#reading-parent-resolved-data-in-child-resolvers}

Resolver'lar otadan bolaga ketma-ket bajariladi. Ota marshrut resolver aniqlaganda, uning olingan maʼlumotlari keyin ishga tushadigan bola resolver'lar uchun mavjud boʻladi.

NOTE: Resolver'lar otadan bolaga ketma-ket bajarilgani uchun har bir ichki daraja umumiy navigatsiya kutish vaqtini oshiradi (tarmoq sharsharasi — network waterfall). Bola marshrutlaringiz ota maʼlumotlariga bogʻliq boʻlmasa, barcha marshrutlar boʻylab bir vaqtda bajariladigan [marshrut resurslarini](/guide/routing/data-fetching-with-resources) koʻrib chiqing.

```ts
import {inject} from '@angular/core';
import {provideRouter, ActivatedRouteSnapshot} from '@angular/router';
import {userResolver} from './resolvers';
import {UserPosts} from './pages';
import {PostService} from './services';
import type {User} from './types';

provideRouter([
  {
    path: 'users/:id',
    resolve: {user: userResolver}, // user resolver in the parent route
    children: [
      {
        path: 'posts',
        component: UserPosts,
        // route.data.user is available here while this resolver runs
        resolve: {
          posts: (route: ActivatedRouteSnapshot) => {
            const postService = inject(PostService);
            const user = route.parent?.data['user'] as User; // parent data
            const userId = user.id;
            return postService.getPostByUser(userId);
          },
        },
      },
    ],
  },
]);
```

## Keyingi qadamlar {#next-steps}

<docs-pill-row>
  <docs-pill href="/guide/routing/data-fetching-with-resources" title="Resurslar bilan maʼlumot yuklash"/>
  <docs-pill href="/guide/routing/route-guards" title="Guard'lar bilan marshrutga kirishni boshqarish"/>
</docs-pill-row>
