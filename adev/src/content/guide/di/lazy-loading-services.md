# Servislarni kechiktirib yuklash (lazy loading)

IMPORTANT: Kechiktirilgan yuklash (lazy loading) ishlashi uchun yuklayotgan servisingiz avtomatik taqdim etilgan boʻlishi kerak. Uni `@Injectable({providedIn: 'root'})` yoki [`@Service()`](guide/di/creating-and-using-services#using-the-service-vs-injectable-decorator) bilan dekoratsiyalang. Avtomatik taqdim etishsiz Angular servisni yuklangandan keyin yaratishning imkoniga ega boʻlmaydi.

Angular'ning `injectAsync` funksiyasi servisni talab boʻyicha, faqat u haqiqatan kerak boʻlganda yuklash imkonini beradi. Bu servis katta kutubxonaga yoki kamdan-kam ishlatiladigan imkoniyatga bogʻliq boʻlganda va siz buning uchun sahifaning dastlabki yuklanishida toʻlashni istamaganingizda foydali.

`injectAsync` ishlatganingizda, servisning kodi bundler tomonidan alohida JavaScript chunk'iga ajratiladi va nusxani birinchi marta soʻraganingizda yuklab olinadi. Yuklangandan soʻng Angular servisni odatiy DI tizimi orqali hal qiladi, shuning uchun u boshqa inyeksiya qilinadigan obyektlarga bogʻliq boʻlishi va har qanday boshqa singleton kabi ishlashi mumkin.

## Servisni kechiktirib inyeksiya qilish {#lazily-injecting-a-service}

Ogʻir elektron jadval kutubxonasiga bogʻliq boʻlgan `ReportExporter` servisini tasavvur qiling. Koʻpchilik foydalanuvchilar hisobotni ochadi; faqat baʼzilari **Export** tugmasini bosadi. Eksport qiluvchini talab boʻyicha yuklang:

```angular-ts
import {Component, injectAsync} from '@angular/core';

@Component({
  selector: 'app-report',
  template: `<button (click)="export()">Export</button>`,
})
export class Report {
  private exporter = injectAsync(() => import('./report-exporter').then((m) => m.ReportExporter));

  async export() {
    const exporter = await this.exporter();
    exporter.export();
  }
}
```

`this.exporter()` funksiyasining birinchi chaqiruvi dinamik importni ishga tushiradi va servisni DI'dan hal qiladi. Keyingi chaqiruvlar oʻsha promise'ni qayta ishlatadi, shuning uchun chunk faqat bir marta yuklab olinadi.

Agar kechiktirib yuklanadigan servis [default export](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/export#using_the_default_export) boʻlsa, dinamik importni bevosita uzating, Angular `default`'ni siz uchun oʻzi ajratib oladi:

```ts {header: "report-exporter.ts"}
@Service()
export default class ReportExporter {
  /* … */
}
```

```ts {header: "report.ts"}
private exporter = injectAsync(() => import('./report-exporter'));
```

## Bogʻliqlikni oldindan yuklash (prefetch) {#prefetching-the-dependency}

Sukut boʻyicha kechiktirilgan chunk faqat qaytarilgan funksiyani chaqirganingizda yuklab olinadi. Opsiyalarda `prefetch` triggerini uzatish orqali yuklab olishni oldinroq boshlashingiz mumkin. Trigger — `Promise` qaytaruvchi har qanday funksiya, u hal boʻlganda Angular yuklovchini ishga tushiradi.

Angular brauzer boʻsh (idle) holatga oʻtishini kutuvchi oʻrnatilgan `onIdle` triggeri bilan birga keladi:

```ts
import {Component, injectAsync, onIdle} from '@angular/core';

@Component({/* … */})
export class Report {
  private exporter = injectAsync(() => import('./report-exporter').then((m) => m.ReportExporter), {
    prefetch: onIdle,
  });
}
```

Shuningdek, oldindan yuklash band sahifalarda ham har doim maʼlum vaqt oraligʻida sodir boʻlishi uchun `onIdle`'ni maksimal kutish vaqti bilan sozlashingiz mumkin:

```ts
injectAsync(loader, {prefetch: () => onIdle({timeout: 1_000})});
```

NOTE: Oldindan yuklash imkoniyatga qarab amalga oshiriladi. Agar foydalanuvchi oldindan yuklash ishga tushishidan oldin imkoniyatni chaqirsa, Angular bogʻliqlikni baribir darhol yuklaydi va tayyor boʻlishi bilan `await`'ingizni hal qiladi.

## Maxsus prefetch triggerini taqdim etish {#provide-a-custom-prefetch-trigger}

`PrefetchTrigger` — bu shunchaki promise qaytaruvchi funksiya, yuklovchi promise hal boʻlishi bilanoq ishga tushadi. Bundan oldindan yuklashni oʻz signallaringiz, masalan, hover yoki planlashtiruvchi (scheduler) tiki bilan moslashtirish uchun foydalaning:

```ts
import {PrefetchTrigger} from '@angular/core';

export function onHover(target: HTMLElement): PrefetchTrigger {
  return () =>
    new Promise<void>((resolve) => {
      target.addEventListener('pointerenter', () => resolve(), {once: true});
    });
}
```
