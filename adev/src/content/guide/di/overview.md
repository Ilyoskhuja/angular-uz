<docs-decorative-header title="Angular'da bogʻliqliklarni inyeksiya qilish" imgSrc="adev/src/assets/images/dependency_injection.svg"> <!-- markdownlint-disable-line -->

Bogʻliqliklarni inyeksiya qilish (Dependency Injection, DI) — bogʻliqliklarni klass ichida yaratish oʻrniga ularni klassga tashqaridan taqdim etish orqali kodni ilovangiz boʻylab tartibga solish va ulashish uchun ishlatiladigan dizayn namunasi.
</docs-decorative-header>

TIP: Bu keng qamrovli qoʻllanmaga kirishdan oldin Angular'ning [Asoslar](essentials/dependency-injection) boʻlimi bilan tanishib chiqing.

Ilova kattalashgani sari dasturchilar koʻpincha funksionallikni kod bazasining turli qismlarida qayta ishlatish va ulashishga ehtiyoj sezadilar. [Bogʻliqliklarni inyeksiya qilish (DI)](https://en.wikipedia.org/wiki/Dependency_injection) bogʻliqliklarni klass ichida bevosita yaratish oʻrniga ularni klassga taqdim etish imkonini berib, bunga erishishga yordam beradi. Bu ilovaning turli qismlarini koʻproq qayta ishlatiladigan va boshqarish uchun osonroq qiladi.

Bogʻliqliklarni inyeksiya qilish mashhur namuna, chunki u dasturchilarga quyidagi kabi keng tarqalgan muammolarni hal qilish imkonini beradi:

- **Kodni qoʻllab-quvvatlash osonlashadi**: bogʻliqliklarni inyeksiya qilish masʼuliyatlarning aniq ajratilishiga yordam beradi, bu kodni refaktoring qilishni osonlashtiradi va takrorlanishni kamaytiradi.
- **Masshtablanuvchanlik**: modulli funksionallikni ilovaning turli qismlarida qayta ishlatishingiz mumkin, bu masshtablashni osonlashtiradi.
- **Yaxshiroq testlash**: DI unit testlarga zarur boʻlganda haqiqiy realizatsiyalar oʻrniga [test dublyorlaridan (test doubles)](https://en.wikipedia.org/wiki/Test_double) foydalanish imkonini beradi.

## Angular'da bogʻliqliklarni inyeksiya qilish qanday ishlaydi? {#how-does-dependency-injection-work-in-angular}

Bogʻliqlik — klass ishlashi uchun zarur boʻlgan, lekin oʻzi yaratmaydigan har qanday obyekt, qiymat, funksiya yoki servis. Buning oʻrniga siz uni tashqaridan taqdim etasiz va shu bilan ilovaning turli qismlari oʻrtasida aniq munosabat yaratasiz.

Siz bogʻliqliklarni inyeksiya qilish tizimi bilan ikki asosiy yoʻl bilan ishlaysiz:

- Qiymatlarni _taqdim etishingiz_ (provide), yaʼni mavjud qilishingiz mumkin.
- Oʻsha qiymatlarni bogʻliqlik sifatida _inyeksiya qilishingiz_, yaʼni soʻrashingiz mumkin.

Bu kontekstda "qiymatlar" deganda har qanday JavaScript qiymati, jumladan obyektlar, funksiyalar yoki klass nusxalari tushuniladi. Inyeksiya qilinadigan bogʻliqliklarning keng tarqalgan turlari quyidagilar:

- **Konfiguratsiya qiymatlari**: muhitga xos konstantalar, API URL'lari, feature flag'lar va h.k.
- **Fabrikalar (factories)**: ishga tushirish vaqtidagi shartlarga qarab obyekt yoki qiymatlar yaratuvchi funksiyalar
- **Servislar**: umumiy funksionallik, biznes mantiq yoki holatni taqdim etuvchi klasslar

Angular komponentlari va direktivalari DI'da avtomatik ishtirok etadi, yaʼni siz ularga bogʻliqliklarni inyeksiya qilishingiz va ularni inyeksiya uchun mavjud qilishingiz mumkin.

## Servislar nima? {#what-are-services}

Angular _servisi_ — `@Service` bilan dekoratsiyalangan TypeScript klassi boʻlib, u klass nusxasini bogʻliqlik sifatida inyeksiya qilish imkonini beradi. Servislar ilova boʻylab maʼlumot va funksionallikni ulashishning eng keng tarqalgan usuli.

Servislarning keng tarqalgan turlari quyidagilar:

- **Maʼlumot klientlari:** maʼlumotlarni olish va oʻzgartirish uchun serverga soʻrov yuborish tafsilotlarini abstraktlashtiradi
- **Holatni boshqarish:** bir nechta komponent yoki sahifalar oʻrtasida ulashiladigan holatni aniqlaydi
- **Autentifikatsiya va avtorizatsiya:** foydalanuvchi autentifikatsiyasi, tokenlarni saqlash va kirishni nazorat qilishni boshqaradi
- **Loglash va xatolarga ishlov berish:** loglash yoki xato holatlarini foydalanuvchiga yetkazish uchun umumiy API oʻrnatadi
- **Hodisalarga ishlov berish va tarqatish:** [observer namunasiga](https://en.wikipedia.org/wiki/Observer_pattern) amal qilib, muayyan komponentga bogʻliq boʻlmagan hodisa yoki bildirishnomalarga ishlov beradi yoki hodisa va bildirishnomalarni komponentlarga tarqatadi
- **Yordamchi funksiyalar:** maʼlumotlarni formatlash, validatsiya yoki hisob-kitoblar kabi qayta ishlatiladigan yordamchi funksiyalarni taqdim etadi

Quyidagi misol `AnalyticsLogger` nomli servisni eʼlon qiladi:

```ts
import {Service} from '@angular/core';

@Service()
export class AnalyticsLogger {
  trackEvent(category: string, value: string) {
    console.log('Analytics event logged:', {
      category,
      value,
      timestamp: new Date().toISOString(),
    });
  }
}
```

NOTE: `@Service` bu servisni butun ilovangiz boʻylab singleton sifatida mavjud qiladi. Bu koʻpchilik servislar uchun tavsiya etilgan yondashuv.

HELPFUL: [`@Service`](guide/di/creating-and-using-services#using-the-service-vs-injectable-decorator) dekoratori `@Injectable({providedIn: 'root'})` uchun qulay qisqa yozuv.

## `inject()` yordamida bogʻliqliklarni inyeksiya qilish {#injecting-dependencies-with-inject}

Bogʻliqliklarni Angular'ning `inject()` funksiyasi yordamida inyeksiya qilishingiz mumkin.

Quyida foydalanuvchilarga hodisani kuzatib borish bilan birga boshqa sahifaga oʻtish imkonini berish uchun `AnalyticsLogger` va Angular'ning `Router` servisini inyeksiya qiluvchi navigatsiya paneliga misol keltirilgan.

```angular-ts
import {Component, inject} from '@angular/core';
import {Router} from '@angular/router';
import {AnalyticsLogger} from './analytics-logger';

@Component({
  selector: 'app-navbar',
  template: `<a href="#" (click)="navigateToDetail($event)">Detail Page</a>`,
})
export class Navbar {
  private router = inject(Router);
  private analytics = inject(AnalyticsLogger);

  navigateToDetail(event: Event) {
    event.preventDefault();
    this.analytics.trackEvent('navigation', '/details');
    this.router.navigate(['/details']);
  }
}
```

### `inject()` qayerda ishlatilishi mumkin? {#where-can-inject-be-used}

Bogʻliqliklarni komponent, direktiva yoki servis yaratilayotgan paytda inyeksiya qilishingiz mumkin. [`inject`](/api/core/inject) chaqiruvi `constructor` ichida ham, maydon initsializatorida ham boʻlishi mumkin. Quyida bir nechta keng tarqalgan misollar keltirilgan:

```ts
@Component(/* ... */)
export class MyComponent {
  // ✅ In class field initializer
  private service = inject(MyService);

  // ✅ In constructor body
  private anotherService: MyService;

  constructor() {
    this.anotherService = inject(MyService);
  }
}
```

```ts
@Directive({...})
export class MyDirective {
  // ✅ In class field initializer
  private element = inject(ElementRef);
}
```

```ts
import {Service, inject} from '@angular/core';
import {HttpClient} from '@angular/common/http';

@Service()
export class MyService {
  // ✅ In a service
  private http = inject(HttpClient);
}
```

```ts
export const authGuard = () => {
  // ✅ In a route guard
  const auth = inject(AuthService);
  return auth.isAuthenticated();
};
```

Angular kodingizda [`inject`](/api/core/inject) chaqirish mumkin boʻlgan har qanday joyni tavsiflash uchun "inyeksiya konteksti" (injection context) atamasini ishlatadi. Komponent, direktiva va servis yaratilishi eng keng tarqalgan holat boʻlsa-da, batafsil maʼlumot uchun [inyeksiya kontekstlari](/guide/di/dependency-injection-context) boʻlimiga qarang.

Koʻproq maʼlumot uchun [inject API hujjatlariga](api/core/inject#usage-notes) qarang.

## Keyingi qadamlar {#next-steps}

Endi siz Angular'da bogʻliqliklarni inyeksiya qilish asoslarini tushunganingizdan soʻng, oʻz servislaringizni qanday yaratishni oʻrganishga tayyorsiz.

Keyingi qoʻllanma, [Servislarni yaratish va ulardan foydalanish](guide/di/creating-and-using-services), sizga quyidagilarni koʻrsatadi:

- Angular CLI yordamida yoki qoʻlda servisni qanday yaratish
- `providedIn: 'root'` namunasi qanday ishlaydi
- Servislarni komponentlar va boshqa servislarga qanday inyeksiya qilish

Bu Angular ilovalarida servislarning eng keng tarqalgan foydalanish holatini qamrab oladi.
