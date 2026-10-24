# Router hayot sikli va hodisalari

Angular Router navigatsiya oʻzgarishlariga javob berish va marshrutlash jarayonida maxsus mantiqni bajarish imkonini beruvchi hayot sikli hook'lari va hodisalarining toʻliq toʻplamini taqdim etadi.

## Keng tarqalgan router hodisalari {#common-router-events}

Angular Router navigatsiya hayot siklini kuzatish uchun obuna boʻlishingiz mumkin boʻlgan navigatsiya hodisalarini yuboradi. Bu hodisalar `Router.events` observable'i orqali mavjud. Bu boʻlim navigatsiya va xatolarni kuzatish uchun keng tarqalgan marshrutlash hayot sikli hodisalarini (xronologik tartibda) qamrab oladi.

| Hodisalar                                           | Tavsif                                                                                                   |
| --------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| [`NavigationStart`](api/router/NavigationStart)     | Navigatsiya boshlanganda yuz beradi va soʻralgan URL'ni oʻz ichiga oladi.                                |
| [`RoutesRecognized`](api/router/RoutesRecognized)   | Router URL'ga qaysi marshrut mos kelishini aniqlagandan keyin yuz beradi va marshrut holati maʼlumotini oʻz ichiga oladi. |
| [`GuardsCheckStart`](api/router/GuardsCheckStart)   | Marshrut guard'lari bosqichini boshlaydi. Router `canActivate` va `canDeactivate` kabi marshrut guard'larini baholaydi. |
| [`GuardsCheckEnd`](api/router/GuardsCheckEnd)       | Guard'larni baholash yakunlanganini bildiradi. Natijani (ruxsat berilgan/rad etilgan) oʻz ichiga oladi.  |
| [`ResolveStart`](api/router/ResolveStart)           | Maʼlumotlarni hal qilish bosqichini boshlaydi. Marshrut resolver'lari va resource'lari maʼlumot olishni boshlaydi. |
| [`ResolveEnd`](api/router/ResolveEnd)               | Maʼlumotlarni hal qilish yakunlanadi. Barcha kerakli maʼlumotlar va bloklaydigan resource'lar mavjud boʻladi. |
| [`NavigationEnd`](api/router/NavigationEnd)         | Navigatsiya muvaffaqiyatli yakunlanganda yuz beradigan yakuniy hodisa. Router URL'ni yangilaydi.         |
| [`NavigationSkipped`](api/router/NavigationSkipped) | Router navigatsiyani oʻtkazib yuborganda yuz beradi (masalan, bir xil URL'ga navigatsiya).               |

Quyidagilar keng tarqalgan xato hodisalari:

| Hodisa                                            | Tavsif                                                                                                         |
| ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| [`NavigationCancel`](api/router/NavigationCancel) | Router navigatsiyani bekor qilganda yuz beradi. Koʻpincha guard false qaytargani sababli.                      |
| [`NavigationError`](api/router/NavigationError)   | Navigatsiya muvaffaqiyatsiz boʻlganda yuz beradi. Notoʻgʻri marshrutlar, resolver xatolari yoki rad etilgan bloklaydigan resource'lar sabab boʻlishi mumkin. |

Barcha hayot sikli hodisalari roʻyxati uchun [bu qoʻllanmaning toʻliq jadvaliga](#all-router-events) qarang.

## Router hodisalariga qanday obuna boʻlish {#how-to-subscribe-to-router-events}

Navigatsiya hayot siklining maʼlum hodisalari davomida kod bajarmoqchi boʻlsangiz, bunga `router.events` ga obuna boʻlib va hodisaning nusxasini (instance) tekshirib erishishingiz mumkin:

```ts
// Example of subscribing to router events
import {Component, inject, signal, effect} from '@angular/core';
import {Event, Router, NavigationStart, NavigationEnd} from '@angular/router';
import {takeUntilDestroyed} from '@angular/core/rxjs-interop';

@Component(/* ... */)
export class RouterEvents {
  private readonly router = inject(Router);

  constructor() {
    // Subscribe to router events and react to events
    this.router.events.pipe(takeUntilDestroyed()).subscribe((event: Event) => {
      if (event instanceof NavigationStart) {
        // Navigation starting
        console.log('Navigation starting:', event.url);
      }
      if (event instanceof NavigationEnd) {
        // Navigation completed
        console.log('Navigation completed:', event.url);
      }
    });
  }
}
```

NOTE: `@angular/router` dagi [`Event`](api/router/Event) turi odatiy global [`Event`](https://developer.mozilla.org/en-US/docs/Web/API/Event) turi bilan bir xil nomlangan, lekin u [`RouterEvent`](api/router/RouterEvent) turidan farq qiladi.

## Marshrutlash hodisalarini qanday tuzatish (debug) {#how-to-debug-routing-events}

Hodisalar ketma-ketligini koʻrmasdan router navigatsiyasi muammolarini tuzatish (debug) qiyin boʻlishi mumkin. Angular barcha router hodisalarini konsolga yozib boradigan oʻrnatilgan debag imkoniyatini taqdim etadi; bu navigatsiya oqimini tushunish va muammolar qayerda yuz berayotganini aniqlashga yordam beradi.

Router hodisalari ketma-ketligini koʻrish kerak boʻlganda, tuzatish (debug) uchun ichki navigatsiya hodisalarini yozib borishni yoqishingiz mumkin. Buni barcha marshrutlash hodisalarining konsolga batafsil yozilishini yoqadigan konfiguratsiya opsiyasini (`withDebugTracing()`) uzatish orqali sozlashingiz mumkin.

```ts
import {provideRouter, Routes, withDebugTracing} from '@angular/router';

const appRoutes: Routes = [];
bootstrapApplication(App, {
  providers: [provideRouter(appRoutes, withDebugTracing())],
});
```

Koʻproq maʼlumot uchun [`withDebugTracing`](api/router/withDebugTracing) boʻyicha rasmiy hujjatlarga qarang.

## Keng tarqalgan foydalanish holatlari {#common-use-cases}

Router hodisalari haqiqiy ilovalarda koʻplab amaliy imkoniyatlarni yaratish imkonini beradi. Quyida router hodisalari bilan ishlatiladigan baʼzi keng tarqalgan patternlar keltirilgan.

### Yuklanish indikatorlari {#loading-indicators}

Navigatsiya davomida yuklanish indikatorlarini koʻrsatish:

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

### Analitika kuzatuvi {#analytics-tracking}

Analitika uchun sahifa koʻrishlarini kuzatish:

```ts
import {takeUntilDestroyed} from '@angular/core/rxjs-interop';
import {inject, DestroyRef, Service} from '@angular/core';
import {Router, NavigationEnd} from '@angular/router';

@Service()
export class AnalyticsService {
  private router = inject(Router);
  private destroyRef = inject(DestroyRef);

  startTracking() {
    this.router.events.pipe(takeUntilDestroyed(this.destroyRef)).subscribe((event) => {
      // Track page views when URL changes
      if (event instanceof NavigationEnd) {
        // Send page view to analytics
        this.analytics.trackPageView(event.url);
      }
    });
  }

  private analytics = {
    trackPageView: (url: string) => {
      console.log('Page view tracked:', url);
    },
  };
}
```

### Xatolarni boshqarish {#error-handling}

Navigatsiya xatolarini toʻgʻri boshqarish va foydalanuvchiga xabar berish:

```angular-ts
import {Component, inject, signal} from '@angular/core';
import {
  Router,
  NavigationStart,
  NavigationError,
  NavigationCancel,
  NavigationCancellationCode,
} from '@angular/router';
import {takeUntilDestroyed} from '@angular/core/rxjs-interop';

@Component({
  selector: 'app-error-handler',
  template: `
    @if (errorMessage()) {
      <div class="error-banner">
        {{ errorMessage() }}
        <button (click)="dismissError()">Dismiss</button>
      </div>
    }
  `,
})
export class ErrorHandler {
  private router = inject(Router);
  readonly errorMessage = signal('');

  constructor() {
    this.router.events.pipe(takeUntilDestroyed()).subscribe((event) => {
      if (event instanceof NavigationStart) {
        this.errorMessage.set('');
      } else if (event instanceof NavigationError) {
        console.error('Navigation error:', event.error);
        this.errorMessage.set('Failed to load page. Please try again.');
      } else if (event instanceof NavigationCancel) {
        console.warn('Navigation cancelled:', event.reason);
        if (event.code === NavigationCancellationCode.GuardRejected) {
          this.errorMessage.set('Access denied. Please check your permissions.');
        }
      }
    });
  }

  dismissError() {
    this.errorMessage.set('');
  }
}
```

## Barcha router hodisalari {#all-router-events}

Maʼlumot uchun, quyida Angular'da mavjud barcha router hodisalarining toʻliq roʻyxati keltirilgan. Bu hodisalar toifalar boʻyicha guruhlangan va navigatsiya davomida odatda yuz berish tartibida joylashtirilgan.

### Navigatsiya hodisalari {#navigation-events}

Bu hodisalar asosiy navigatsiya jarayonini boshidan marshrutni aniqlash, guard tekshiruvlari va maʼlumotlarni hal qilishgacha kuzatadi. Ular navigatsiya hayot siklining har bir bosqichini koʻrish imkonini beradi.

| Hodisa                                                    | Tavsif                                                          |
| --------------------------------------------------------- | --------------------------------------------------------------- |
| [`NavigationStart`](api/router/NavigationStart)           | Navigatsiya boshlanganda yuz beradi                             |
| [`RouteConfigLoadStart`](api/router/RouteConfigLoadStart) | Marshrut konfiguratsiyasi lazy loading bilan yuklanishidan oldin yuz beradi |
| [`RouteConfigLoadEnd`](api/router/RouteConfigLoadEnd)     | Lazy loading bilan yuklanadigan marshrut konfiguratsiyasi yuklangandan keyin yuz beradi |
| [`RoutesRecognized`](api/router/RoutesRecognized)         | Router URL'ni tahlil qilib, marshrutlarni aniqlaganda yuz beradi |
| [`GuardsCheckStart`](api/router/GuardsCheckStart)         | Guard bosqichining boshida yuz beradi                           |
| [`GuardsCheckEnd`](api/router/GuardsCheckEnd)             | Guard bosqichining oxirida yuz beradi                           |
| [`ResolveStart`](api/router/ResolveStart)                 | Hal qilish (resolve) bosqichining boshida yuz beradi            |
| [`ResolveEnd`](api/router/ResolveEnd)                     | Hal qilish bosqichining oxirida yuz beradi                      |

### Faollashtirish hodisalari {#activation-events}

Bu hodisalar marshrut komponentlari yaratilayotgan va ishga tushirilayotgan faollashtirish bosqichida yuz beradi. Faollashtirish hodisalari marshrut daraxtidagi har bir marshrut, jumladan ota va bola marshrutlar uchun ishga tushadi.

| Hodisa                                                    | Tavsif                                        |
| --------------------------------------------------------- | --------------------------------------------- |
| [`ActivationStart`](api/router/ActivationStart)           | Marshrutni faollashtirish boshida yuz beradi  |
| [`ChildActivationStart`](api/router/ChildActivationStart) | Bola marshrutni faollashtirish boshida yuz beradi |
| [`ActivationEnd`](api/router/ActivationEnd)               | Marshrutni faollashtirish oxirida yuz beradi  |
| [`ChildActivationEnd`](api/router/ChildActivationEnd)     | Bola marshrutni faollashtirish oxirida yuz beradi |

### Navigatsiya yakunlanish hodisalari {#navigation-completion-events}

Bu hodisalar navigatsiya urinishining yakuniy natijasini ifodalaydi. Har bir navigatsiya aynan shu hodisalardan biri bilan tugaydi va u muvaffaqiyatli boʻlganini, bekor qilinganini, muvaffaqiyatsiz boʻlganini yoki oʻtkazib yuborilganini bildiradi.

| Hodisa                                              | Tavsif                                                              |
| --------------------------------------------------- | ------------------------------------------------------------------- |
| [`NavigationEnd`](api/router/NavigationEnd)         | Navigatsiya muvaffaqiyatli tugaganda yuz beradi                     |
| [`NavigationCancel`](api/router/NavigationCancel)   | Router navigatsiyani bekor qilganda yuz beradi                      |
| [`NavigationError`](api/router/NavigationError)     | Kutilmagan xato sababli navigatsiya muvaffaqiyatsiz boʻlganda yuz beradi |
| [`NavigationSkipped`](api/router/NavigationSkipped) | Router navigatsiyani oʻtkazib yuborganda yuz beradi (masalan, bir xil URL'ga navigatsiya) |

### Boshqa hodisalar {#other-events}

Asosiy navigatsiya hayot siklidan tashqarida yuz beradigan, lekin router hodisalar tizimining bir qismi boʻlgan yana bitta qoʻshimcha hodisa mavjud.

| Hodisa                        | Tavsif                      |
| ----------------------------- | --------------------------- |
| [`Scroll`](api/router/Scroll) | Skroll qilish davomida yuz beradi |

## Keyingi qadamlar {#next-steps}

[Marshrut guard'lari](/guide/routing/route-guards), [resource'lar bilan maʼlumot olish](/guide/routing/data-fetching-with-resources) va [keng tarqalgan router vazifalari](/guide/routing/common-router-tasks) haqida koʻproq bilib oling.
