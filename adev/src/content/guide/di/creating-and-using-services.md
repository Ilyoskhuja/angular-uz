# Servislarni yaratish va ulardan foydalanish

Servislar — Angular ilovangiz boʻylab ulashishingiz mumkin boʻlgan qayta ishlatiladigan kod boʻlaklari. Siz ulardan odatda maʼlumotlarni olish, biznes mantiq yoki bir nechta komponentlar foydalanishi kerak boʻlgan boshqa funksionallik bilan ishlash uchun foydalanasiz.

## Servis yaratish {#creating-a-service}

[Angular CLI](tools/cli) yordamida quyidagi buyruq bilan servis yaratishingiz mumkin:

```bash
ng generate service CUSTOM_NAME
```

Bu buyruq `src` papkangizda alohida `CUSTOM_NAME.ts` faylini yaratadi.

Shuningdek, TypeScript klassiga `@Service()` dekoratorini qoʻshish orqali servisni qoʻlda ham yaratishingiz mumkin. Bu Angular'ga klassni inyeksiya qilinadigan bogʻliqlik sifatida ishlatish mumkinligini bildiradi.

Quyidagi misol foydalanuvchilarga maʼlumot qoʻshish va olish imkonini beruvchi servisni aniqlaydi:

```ts {header: "src/app/basic-data-store.ts"}
import {Service} from '@angular/core';

@Service()
export class BasicDataStore {
  private data: string[] = [];

  addData(item: string): void {
    this.data.push(item);
  }

  getData(): string[] {
    return [...this.data];
  }
}
```

## Servislar qanday mavjud boʻladi {#how-services-become-available}

Servislar sukut boʻyicha root darajasida taqdim etiladi. Servis global taqdim etilganda, Angular uchta asosiy afzallikni kafolatlaydi:

- **Singleton nusxa:** butun ilova uchun yagona, umumiy nusxa yaratadi.
- **Global mavjudlik:** provider'ni qoʻlda roʻyxatdan oʻtkazmasdan istalgan joydan avtomatik foydalanish mumkin.
- **Tree-shaking imkoniyati:** agar kodingiz servisni hech qayerda aniq ishlatmasa, uning yakuniy production bundle'dan chiqarib tashlanishini taʼminlaydi.

### `@Service` va `@Injectable` dekoratorlaridan foydalanish {#using-the-service-vs-injectable-decorator}

`@Service` dekoratori anʼanaviy `@Injectable({ providedIn: 'root' })` sintaksisi uchun zamonaviy, qulay qisqa yozuv vazifasini bajaradi.

Qaysi dekorator sizning holatingizga mos kelishini aniqlash uchun ushbu qisqa maʼlumotnomadan foydalaning:

| Imkoniyat / Talab                                      | `@Service` | `@Injectable`                              |
| ------------------------------------------------------ | ---------- | ------------------------------------------ |
| **`inject()` funksiyasini qoʻllab-quvvatlash**         | Ha         | Ha                                         |
| **Konstruktor asosidagi DI**                           | ❌ Yoʻq    | Ha                                         |
| **Yashirin root singleton provider**                   | Ha         | ❌ Yoʻq (`{providedIn: 'root'}` talab qilinadi) |
| **Kengaytirilgan provider kalitlari (`useClass` va h.k.)** | ❌ Yoʻq | Ha                                         |
| **Maxsus initsializatsiya fabrikalari**                | Ha         | Ha                                         |
| **Root boʻlmagan qamrovlar (`platform` va h.k.)**      | ❌ Yoʻq    | Ha                                         |

### Realizatsiyani fabrika bilan almashtirish {#replacing-the-implementation-with-a-factory}

Agar singleton qanday yaratilishini boshqarishingiz kerak boʻlsa, masalan, muhitga qarab boshqa realizatsiyani qoʻyish uchun, `factory` funksiyasini uzating.

Fabrika [inyeksiya kontekstida](guide/di/dependency-injection-context) ishlaydi, shuning uchun boshqa bogʻliqliklarni oʻqish uchun uning ichida [`inject()`](api/core/inject) funksiyasidan foydalanishingiz mumkin.

Quyidagi `Analytics` servisi lokal muhitda hech narsa qilmaydi (no-op), shunda ishlab chiqish davomida hodisalar konsolni toʻldirmaydi. Production'da fabrika `ANALYTICS_ENABLED` tokenini oʻqiydi va hodisalarni haqiqiy kuzatuvchiga yoʻnaltiruvchi `GoogleAnalytics` subklassini qaytaradi:

```ts {header: "src/app/analytics.ts"}
import {inject, InjectionToken, Service} from '@angular/core';
import {ANALYTICS_ENABLED} from './token';

@Service({
  factory: () => (inject(ANALYTICS_ENABLED) ? new GoogleAnalytics() : new Analytics()),
})
export class Analytics {
  track(event: string, payload?: Record<string, unknown>) {
    // No-op by default.
  }
}

class GoogleAnalytics extends Analytics {
  override track(event: string, payload?: Record<string, unknown>) {
    // Dispatches an analytics event to Google Analytics
  }
}
```

NOTE: `factory` opsiyasi `@Injectable`'ning `useClass`, `useValue`, `useExisting` va `useFactory` opsiyalarining oʻrnini bosadi. Agar sizga ulardan birortasi kerak boʻlsa, `@Injectable`'dan foydalanishda davom eting.

### Avtomatik taqdim etishdan voz kechish {#opting-out-of-automatic-provisioning}

Sukut boʻyicha `@Service` klassni root injector'da taqdim etadi. Agar uni qoʻlda taqdim etmoqchi boʻlsangiz, masalan, uni muayyan marshrut yoki komponent bilan cheklash uchun, `autoProvided: false` qiymatini oʻrnating:

```ts {header: "src/app/analytics-logger.ts"}
import {Service} from '@angular/core';

@Service({autoProvided: false})
export class AnalyticsLogger {
  trackEvent(name: string) {
    console.log('event:', name);
  }
}
```

Shundan soʻng, oddiy `@Injectable()` bilan boʻlgani kabi, servisni `providers` massiviga qoʻshish uchun siz javobgar boʻlasiz:

### Qachon `@Service`, qachon `@Injectable` ishlatish kerak {#when-to-use-service-vs-injectable}

Bogʻliqliklari uchun `inject()` ishlatuvchi yangi singleton klass yaratayotganingizda `@Service`'ni tanlang. Quyidagilardan birortasi kerak boʻlganda `@Injectable`'dan foydalanishda davom eting:

- **Konstruktor asosida bogʻliqliklarni inyeksiya qilish.** `@Service` faqat [`inject()`](api/core/inject) funksiyasini qoʻllab-quvvatlaydi.
- **Kengaytirilgan provider konfiguratsiyasi**, masalan `useClass`, `useValue`, `useExisting` yoki `useFactory`. `@Service` buning oʻrniga yagona `factory` opsiyasini taqdim etadi.
- **Root boʻlmagan qamrovlar**, masalan `providedIn: 'platform'`.

## Servisni inyeksiya qilish {#injecting-a-service}

`providedIn: 'root'` bilan servis yaratganingizdan soʻng, uni `@angular/core`'dagi `inject()` funksiyasi yordamida ilovangizning istalgan joyiga inyeksiya qilishingiz mumkin.

### Komponentga inyeksiya qilish {#injecting-into-a-component}

```angular-ts
import {Component, inject} from '@angular/core';
import {BasicDataStore} from './basic-data-store';

@Component({
  selector: 'app-example',
  template: `
    <div>
      <p>{{ dataStore.getData() }}</p>
      <button (click)="dataStore.addData('More data')">Add more data</button>
    </div>
  `,
})
export class Example {
  dataStore = inject(BasicDataStore);
}
```

### Boshqa servisga inyeksiya qilish {#injecting-into-another-service}

```ts
import {inject, Service} from '@angular/core';
import {AdvancedDataStore} from './advanced-data-store';

@Service()
export class BasicDataStore {
  private advancedDataStore = inject(AdvancedDataStore);
  private data: string[] = [];

  addData(item: string): void {
    this.data.push(item);
  }

  getData(): string[] {
    return [...this.data, ...this.advancedDataStore.getData()];
  }
}
```

## Keyingi qadamlar {#next-steps}

`providedIn: 'root'` koʻpchilik foydalanish holatlarini qamrab olsa-da, Angular yanada maxsus stsenariylar uchun servislarni sozlashning qoʻshimcha usullarini ham taqdim etadi:

- **Komponentga xos nusxalar** - komponentlarga oʻzlarining alohida servis nusxalari kerak boʻlganda
- **Qoʻlda sozlash** - ishga tushirish vaqtida sozlashni talab qiluvchi servislar uchun
- **Fabrika provider'lari** - ishga tushirish vaqtidagi shartlarga asoslanib servislarni dinamik yaratish uchun
- **Qiymat provider'lari** - konfiguratsiya obyektlari yoki konstantalarni taqdim etish uchun

Bu kengaytirilgan namunalar haqida keyingi qoʻllanmada koʻproq bilib olishingiz mumkin: [bogʻliqlik provider'larini aniqlash](/guide/di/defining-dependency-providers).
