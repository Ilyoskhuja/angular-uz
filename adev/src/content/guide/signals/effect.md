# Effect'lar

Signallar foydali, chunki ular oʻzgarganda manfaatdor isteʼmolchilarni xabardor qiladi. **Effect** — bir yoki bir nechta signal qiymati oʻzgarganda ishga tushadigan operatsiya. Effect'ni `effect` funksiyasi bilan yaratishingiz mumkin:

```ts
import {effect} from '@angular/core';

effect(() => {
  console.log(`The current count is: ${count()}`);
});
```

Effect'lar har doim **kamida bir marta** ishga tushadi. Effect ishga tushganda, u har qanday signal qiymati oʻqilishini kuzatadi. Bu signal qiymatlaridan birortasi oʻzgarganda effect yana ishga tushadi. Hisoblangan signallarga oʻxshab, effect'lar oʻz bogʻliqliklarini dinamik tarzda kuzatib boradi va faqat eng soʻnggi bajarilishda oʻqilgan signallarni kuzatadi.

Effect'lar har doim oʻzgarishlarni aniqlash jarayoni davomida **asinxron** bajariladi.

## Effect'lardan foydalanish holatlari {#use-cases-for-effects}

Effect'lar siz murojaat qiladigan eng soʻnggi API boʻlishi kerak. Hosil qilingan qiymatlar uchun har doim `computed()`'ni, hosil qilinishi ham, qoʻlda oʻrnatilishi ham mumkin boʻlgan qiymatlar uchun esa `linkedSignal()`'ni afzal koʻring. Agar effect yordamida maʼlumotlarni bir signaldan boshqasiga nusxalayotganingizni sezsangiz, bu haqiqat manbaingizni (source of truth) yuqoriroqqa koʻchirib, oʻrniga `computed()` yoki `linkedSignal()`'dan foydalanishingiz kerakligining belgisidir. Effect'lar signal holatini imperativ, signal boʻlmagan API'lar bilan sinxronlashtirish uchun eng mos keladi.

TIP: Effect yaxshi boʻlgan vaziyatlar yoʻq, faqat u oʻrinli boʻlgan vaziyatlar bor.

- Signal qiymatlarini analitika uchun yoki debug vositasi sifatida logga yozish.
- Maʼlumotlarni turli xil saqlash joylari bilan sinxron holda ushlab turish: `window.localStorage`, session storage, cookie'lar va h.k.
- Shablon sintaksisi bilan ifodalab boʻlmaydigan maxsus DOM xatti-harakatini qoʻshish.
- `<canvas>` elementiga, diagramma kutubxonasiga yoki boshqa uchinchi tomon UI kutubxonasiga maxsus render qilishni bajarish.

<docs-callout critical title="Effect'lardan qachon foydalanmaslik kerak">
Holat oʻzgarishlarini tarqatish uchun effect'lardan foydalanmang. Bu `ExpressionChangedAfterItHasBeenChecked` xatolariga, cheksiz aylanma yangilanishlarga yoki keraksiz oʻzgarishlarni aniqlash sikllariga olib kelishi mumkin.

Buning oʻrniga, boshqa holatga bogʻliq boʻlgan holatni modellashtirish uchun `computed` signallaridan foydalaning.
</docs-callout>

## Inyeksiya konteksti {#injection-context}

Sukut boʻyicha `effect()`'ni faqat [inyeksiya konteksti](guide/di/dependency-injection-context) ichida (`inject` funksiyasiga kirish imkoniga ega boʻlgan joyda) yaratishingiz mumkin. Bu talabni qondirishning eng oson yoʻli — `effect`'ni komponent, direktiva yoki servisning `constructor`'i ichida chaqirish:

```ts
@Component(/* ... */)
export class EffectiveCounter {
  readonly count = signal(0);

  constructor() {
    // Register a new effect.
    effect(() => {
      console.log(`The count is: ${this.count()}`);
    });
  }
}
```

Effect'ni konstruktordan tashqarida yaratish uchun `effect`'ga uning opsiyalari orqali `Injector` uzatishingiz mumkin:

```ts
@Component(/* ... */)
export class EffectiveCounter {
  readonly count = signal(0);
  private injector = inject(Injector);

  initializeLogging(): void {
    effect(
      () => {
        console.log(`The count is: ${this.count()}`);
      },
      {injector: this.injector},
    );
  }
}
```

## Effect'larning bajarilishi {#execution-of-effects}

Angular effect'lari uchun, ular yaratilgan kontekstga qarab, ikki xil yashirin (implicit) xatti-harakatni belgilaydi.

"View Effect" — komponentni yaratish (instantiation) kontekstida yaratilgan `effect`. Bunga komponent injector'lariga bogʻlangan servislar tomonidan yaratilgan effect'lar ham kiradi.<br>
"Root Effect" — root darajasida taqdim etilgan servisni yaratish kontekstida yaratiladi.

`effect`'ning ikkala turining bajarilishi ham oʻzgarishlarni aniqlash jarayoniga bogʻlangan.

- "View effect"lar oʻzlariga tegishli komponent oʻzgarishlarni aniqlash jarayoni tomonidan tekshirilishidan _oldin_ bajariladi.
- "Root effect"lar barcha komponentlar oʻzgarishlarni aniqlash jarayoni tomonidan tekshirilishidan oldin bajariladi.

Ikkala holatda ham, agar effect bajarilishi davomida effect bogʻliqliklaridan kamida bittasi oʻzgargan boʻlsa, oʻzgarishlarni aniqlash jarayoni davom etishidan oldin effect qayta ishga tushadi.

## Effect'larni yoʻq qilish {#destroying-effects}

Komponent yoki direktiva yoʻq qilinganda Angular unga tegishli barcha effect'larni avtomatik ravishda tozalaydi.

`effect` qachon yoʻq qilinishiga taʼsir qiluvchi ikki xil kontekstda yaratilishi mumkin:

- "View effect" komponent yoʻq qilinganda yoʻq qilinadi.
- "Root effect" ilova yoʻq qilinganda yoʻq qilinadi.

Effect'lar `EffectRef` qaytaradi. Effect'ni qoʻlda yoʻq qilish uchun ref'ning `destroy` metodidan foydalanishingiz mumkin. Avtomatik tozalashni oʻchirish uchun buni effect yaratishdagi `manualCleanup` opsiyasi bilan birlashtirishingiz mumkin. Bunday effect'lar endi kerak boʻlmaganda ularni haqiqatan ham yoʻq qilishga eʼtibor bering.

## Effect tozalash funksiyalari {#effect-cleanup-functions}

Komponent yoki direktiva yoʻq qilinganda Angular unga tegishli barcha effect'larni avtomatik ravishda tozalaydi.
Effect'lar uzoq davom etadigan operatsiyalarni boshlashi mumkin; agar effect yoʻq qilinsa yoki birinchi operatsiya tugashidan oldin qayta ishga tushsa, ularni bekor qilishingiz kerak. Effect yaratganingizda, funksiyangiz ixtiyoriy ravishda birinchi parametr sifatida `onCleanup` funksiyasini qabul qilishi mumkin. Bu `onCleanup` funksiyasi effect'ning keyingi ishga tushishi boshlanishidan oldin yoki effect yoʻq qilinganda chaqiriladigan callback'ni roʻyxatdan oʻtkazish imkonini beradi.

```ts
effect((onCleanup) => {
  const user = currentUser();

  const timer = setTimeout(() => {
    console.log(`1 second ago, the user became ${user}`);
  }, 1000);

  onCleanup(() => {
    clearTimeout(timer);
  });
});
```

## DOM elementlaridagi yon taʼsirlar {#side-effects-on-dom-elements}

`effect` funksiyasi — signal oʻzgarishlariga javoban kod bajarish uchun umumiy maqsadli vosita. Biroq u Angular DOM'ni yangilashidan _oldin_ ishga tushadi. Baʼzi vaziyatlarda DOM'ni qoʻlda tekshirish yoki oʻzgartirish, yoki DOM'ga bevosita kirishni talab qiladigan uchinchi tomon kutubxonasini integratsiya qilish kerak boʻlishi mumkin.

Bunday vaziyatlar uchun `afterRenderEffect`'dan foydalanishingiz mumkin. U `effect` kabi ishlaydi, lekin Angular render qilishni tugatib, oʻzgarishlarini DOM'ga kiritganidan keyin ishga tushadi.

```ts
@Component(/* ... */)
export class MyFancyChart {
  chartData = input.required<ChartData>();
  canvas = viewChild.required<ElementRef<HTMLCanvasElement>>('canvas');
  chart: ChartInstance;

  constructor() {
    // Run a single time to create the chart instance
    afterNextRender({
      write: () => {
        this.chart = initializeChart(this.canvas().nativeElement, this.chartData());
      },
    });

    // Re-run after DOM has been updated whenever `chartData` changes
    afterRenderEffect(() => {
      this.chart.updateData(this.chartData());
    });
  }
}
```

Bu misolda `afterRenderEffect` uchinchi tomon kutubxonasi tomonidan yaratilgan diagrammani yangilash uchun ishlatilgan.

TIP: DOM oʻzgarishlarini tekshirish uchun koʻpincha `afterRenderEffect` kerak boʻlmaydi. Imkon boʻlganda `ResizeObserver`, `MutationObserver` va `IntersectionObserver` kabi API'lar `effect` yoki `afterRenderEffect`'dan afzal koʻriladi.

### Render fazalari {#render-phases}

DOM'ga kirish va uni oʻzgartirish ilovangiz unumdorligiga taʼsir qilishi mumkin, masalan, juda koʻp keraksiz [reflow](https://developer.mozilla.org/en-US/docs/Glossary/Reflow)'larni keltirib chiqarish orqali.

Bu operatsiyalarni optimallashtirish uchun `afterRenderEffect` callback'larni guruhlash va ularni optimallashtirilgan tartibda bajarish uchun toʻrtta fazani taklif qiladi.

Fazalar quyidagilar:

| Faza             | Tavsif                                                                                                                                                                                                              |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `earlyRead`      | Bu fazadan keyingi yozish callback'idan oldin DOM'dan oʻqish uchun foydalaning, masalan, brauzer tabiiy ravishda qoʻllab-quvvatlamaydigan maxsus layout'ni bajarish uchun. Agar oʻqish kutishi mumkin boʻlsa, read fazasini afzal koʻring. |
| `write`          | Bu fazadan DOM'ga yozish uchun foydalaning. Bu fazada DOM'dan **hech qachon** oʻqimang.                                                                                                                             |
| `mixedReadWrite` | Bu fazadan DOM'dan oʻqish va unga yozishni bir vaqtda bajarish uchun foydalaning. Agar ishni boshqa fazalar oʻrtasida taqsimlash mumkin boʻlsa, bu fazadan hech qachon foydalanmang.                                 |
| `read`           | Bu fazadan DOM'dan oʻqish uchun foydalaning. Bu fazada DOM'ga **hech qachon** yozmang.                                                                                                                              |

Bu fazalardan foydalanish layout thrashing'ning oldini olishga yordam beradi va DOM operatsiyalaringiz xavfsiz va samarali tarzda bajarilishini taʼminlaydi.

Fazalarni `afterRenderEffect`'ga har bir faza uchun callback'ga ega obyekt uzatish orqali koʻrsatishingiz mumkin:

```ts
afterRenderEffect({
  earlyRead: (cleanupFn) => {
    /* ... */
  },
  write: (previousPhaseValue, cleanupFn) => {
    /* ... */
  },
  mixedReadWrite: (previousPhaseValue, cleanupFn) => {
    /* ... */
  },
  read: (previousPhaseValue, cleanupFn) => {
    /* ... */
  },
});
```

CRITICAL: Agar fazani koʻrsatmasangiz, `afterRenderEffect` callback'larni `mixedReadWrite` fazasida ishga tushiradi. Bu qoʻshimcha DOM reflow'larini keltirib chiqarib, ilova unumdorligini yomonlashtirishi mumkin.

#### Fazalarning bajarilishi {#phase-executions}

`earlyRead` fazasining callback'i faqat tozalash funksiyasini qabul qiladi. Har bir keyingi faza oldingi faza callback'ining qaytargan qiymatini Signal sifatida qabul qiladi. Bundan fazalar oʻrtasidagi ishni muvofiqlashtirish uchun foydalanishingiz mumkin.

Effect'lar quyidagi faza tartibida ishga tushadi:

1. `earlyRead`
2. `write`
3. `mixedReadWrite`
4. `read`

Agar fazalardan biri `afterRenderEffect` tomonidan kuzatilayotgan signal qiymatini oʻzgartirsa, taʼsirlangan fazalar yana bajariladi.

#### Tozalash {#cleanup}

Har bir faza argument sifatida tozalash callback funksiyasini taqdim etadi. Tozalash callback'lari `afterRenderEffect` yoʻq qilinganda yoki faza effect'lari qayta ishga tushishidan oldin bajariladi.

### Server tomonida render qilish bilan bogʻliq eslatmalar {#server-side-rendering-caveats}

`afterRenderEffect`, `afterNextRender`/`afterEveryRender` kabi, faqat klientda ishga tushadi.

NOTE: Callback ishga tushishidan oldin komponentlar [gidratsiya qilingan](/guide/hydration) boʻlishi kafolatlanmaydi. DOM va layout'ni bevosita oʻqish yoki yozishda ehtiyot boʻlishingiz kerak.
