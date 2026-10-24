<docs-decorative-header title="Angular Signals" imgSrc="adev/src/assets/images/signals.svg"> <!-- markdownlint-disable-line -->
Angular Signals — holatingiz ilova boʻylab qanday va qayerda ishlatilishini aniq (granulyar) kuzatib boruvchi tizim boʻlib, bu freymvorkka render yangilanishlarini optimallashtirish imkonini beradi.
</docs-decorative-header>

TIP: Bu toʻliq qoʻllanmaga shoʻngʻishdan oldin Angular'ning [Asoslari](essentials/signals) bilan tanishib chiqing.

## Signallar nima? {#what-are-signals}

**Signal** — qiymat atrofidagi oʻram boʻlib, u qiymat oʻzgarganda manfaatdor isteʼmolchilarni (consumers) xabardor qiladi. Signallar istalgan qiymatni — primitivlardan murakkab maʼlumot tuzilmalarigacha — saqlashi mumkin.

Signalning qiymatini uning getter funksiyasini chaqirish orqali oʻqiysiz; bu Angular'ga signal qayerda ishlatilayotganini kuzatish imkonini beradi.

Signallar _yoziladigan_ (writable) yoki _faqat oʻqish uchun_ (read-only) boʻlishi mumkin.

### Yoziladigan signallar {#writable-signals}

Yoziladigan signallar oʻz qiymatlarini bevosita yangilash uchun API taqdim etadi. Yoziladigan signallarni `signal` funksiyasini signalning boshlangʻich qiymati bilan chaqirib yaratasiz:

```ts
const count = signal(0);

// Signals are getter functions - calling them reads their value.
console.log('The count is: ' + count());
```

Yoziladigan signalning qiymatini oʻzgartirish uchun uni bevosita `.set()` qiling:

```ts
count.set(3);
```

yoki oldingi qiymatdan yangi qiymatni hisoblash uchun `.update()` operatsiyasidan foydalaning:

```ts
// Increment the count by 1.
count.update((value) => value + 1);
```

Yoziladigan signallar `WritableSignal` turiga ega.

#### Yoziladigan signallarni faqat oʻqish uchun signalga aylantirish {#converting-writable-signals-to-readonly}

`WritableSignal` signalning faqat oʻqish uchun versiyasini qaytaruvchi `asReadonly()` metodini taqdim etadi. Bu signal qiymatini isteʼmolchilarga, ularga uni bevosita oʻzgartirish imkonini bermasdan, ochmoqchi boʻlganingizda foydali:

```ts
@Service()
export class CounterState {
  // Private writable state
  private readonly _count = signal(0);

  readonly count = this._count.asReadonly(); // public readonly

  increment() {
    this._count.update((v) => v + 1);
  }
}

@Component({/* ... */})
export class AwesomeCounter {
  state = inject(CounterState);

  count = this.state.count; // can read but not modify

  increment() {
    this.state.increment();
  }
}
```

Faqat oʻqish uchun signal asl yoziladigan signalga kiritilgan har qanday oʻzgarishni aks ettiradi, lekin uni `set()` yoki `update()` metodlari bilan oʻzgartirib boʻlmaydi.

IMPORTANT: Faqat oʻqish uchun signallarda ularning qiymatini chuqur oʻzgartirishdan (deep-mutation) himoya qiladigan hech qanday oʻrnatilgan mexanizm **yoʻq**.

### Hisoblangan signallar (computed) {#computed-signals}

**Hisoblangan signallar** (computed signals) — qiymatini boshqa signallardan hosil qiluvchi, faqat oʻqish uchun signallar. Hisoblangan signallarni `computed` funksiyasi yordamida, hosil qilish (derivation) funksiyasini koʻrsatib aniqlaysiz:

```typescript
const count: WritableSignal<number> = signal(0);
const doubleCount: Signal<number> = computed(() => count() * 2);
```

`doubleCount` signali `count` signaliga bogʻliq. `count` yangilanganda Angular `doubleCount` ham yangilanishi kerakligini biladi.

#### Hisoblangan signallar dangasa hisoblanadi va memoizatsiya qilinadi {#computed-signals-are-both-lazily-evaluated-and-memoized}

`doubleCount`'ning hosil qilish funksiyasi siz `doubleCount`'ni birinchi marta oʻqimaguningizcha uning qiymatini hisoblash uchun ishga tushmaydi. Hisoblangan qiymat keyin keshlanadi va `doubleCount`'ni yana oʻqisangiz, u qayta hisoblamasdan keshlangan qiymatni qaytaradi.

Agar keyin `count`'ni oʻzgartirsangiz, Angular `doubleCount`'ning keshlangan qiymati endi yaroqsiz ekanini biladi va `doubleCount`'ni keyingi safar oʻqiganingizda uning yangi qiymati hisoblanadi.

Natijada, hisoblangan signallarda massivlarni filtrlash kabi hisoblash jihatidan qimmat hosil qilishlarni xavfsiz bajarishingiz mumkin.

#### Hisoblangan signallar yoziladigan signallar emas {#computed-signals-are-not-writable-signals}

Hisoblangan signalga bevosita qiymat tayinlay olmaysiz. Yaʼni,

```ts
doubleCount.set(3);
```

kompilyatsiya xatosiga olib keladi, chunki `doubleCount` `WritableSignal` emas.

#### Hisoblangan signalning bogʻliqliklari dinamik {#computed-signal-dependencies-are-dynamic}

Faqat hosil qilish davomida haqiqatda oʻqilgan signallar kuzatiladi. Masalan, ushbu `computed`'da `count` signali faqat `showCount` signali true boʻlganda oʻqiladi:

```ts
const showCount = signal(false);
const count = signal(0);
const conditionalCount = computed(() => {
  if (showCount()) {
    return `The count is ${count()}.`;
  } else {
    return 'Nothing to see here!';
  }
});
```

`conditionalCount`'ni oʻqiganingizda, agar `showCount` `false` boʻlsa, "Nothing to see here!" xabari `count` signalini oʻqimasdan qaytariladi. Bu shuni anglatadiki, keyinroq `count`'ni yangilasangiz, bu `conditionalCount`'ning qayta hisoblanishiga olib kelmaydi.

Agar `showCount`'ni `true` qilib oʻrnatib, keyin `conditionalCount`'ni yana oʻqisangiz, hosil qilish qayta bajariladi va `showCount` `true` boʻlgan shoxobchaga oʻtib, `count` qiymatini koʻrsatuvchi xabarni qaytaradi. Shundan keyin `count`'ni oʻzgartirish `conditionalCount`'ning keshlangan qiymatini yaroqsiz qiladi.

Eʼtibor bering, hosil qilish davomida bogʻliqliklar qoʻshilishi bilan birga olib tashlanishi ham mumkin. Agar keyinroq `showCount`'ni yana `false` qilib oʻrnatsangiz, `count` endi `conditionalCount`'ning bogʻliqligi hisoblanmaydi.

## Reaktiv kontekstlar {#reactive-contexts}

**Reaktiv kontekst** — Angular bogʻliqlik oʻrnatish uchun signal oʻqishlarini kuzatadigan ishga tushish vaqti (runtime) holati. Signalni oʻqiyotgan kod — _isteʼmolchi_ (consumer), oʻqilayotgan signal esa — _ishlab chiqaruvchi_ (producer).

Angular quyidagi hollarda avtomatik ravishda reaktiv kontekstga kiradi:

- `effect`, `afterRenderEffect` callback'ini bajarishda.
- `computed` signalini hisoblashda.
- `linkedSignal`'ni hisoblashda.
- `resource`'ning params funksiyasini hisoblashda.
- Komponent shablonini render qilishda (shu jumladan [host xususiyatidagi](guide/components/host-elements#binding-to-the-host-element) bogʻlashlar).

Ushbu operatsiyalar davomida Angular _jonli_ aloqa yaratadi. Agar kuzatilayotgan signal oʻzgarsa, Angular isteʼmolchini _oxir-oqibat_ qayta ishga tushiradi.

### Reaktiv kontekstni tekshirish (assert) {#asserts-the-reactive-context}

Angular kodning reaktiv kontekst ichida bajarilmayotganini tasdiqlash (assert) uchun `assertNotInReactiveContext` yordamchi funksiyasini taqdim etadi. Chaqiruvchi funksiyaga havola uzating, shunda tekshiruv muvaffaqiyatsiz boʻlganda xato xabari toʻgʻri API kirish nuqtasiga ishora qiladi. Bu umumiy reaktiv kontekst xatosiga nisbatan aniqroq va amaliy xato xabarini beradi.

```ts
import {assertNotInReactiveContext} from '@angular/core';

function subscribeToEvents() {
  assertNotInReactiveContext(subscribeToEvents);
  // Safe to proceed - subscription logic here
}
```

### Bogʻliqliklarni kuzatmasdan oʻqish {#reading-without-tracking-dependencies}

Kamdan-kam hollarda `computed` yoki `effect` kabi reaktiv funksiya ichida signallarni oʻqishi mumkin boʻlgan kodni bogʻliqlik yaratmasdan bajarishni istashingiz mumkin.

Masalan, `currentUser` oʻzgarganda `counter` qiymati logga yozilishi kerak deb faraz qilaylik. Ikkala signalni ham oʻqiydigan `effect` yaratishingiz mumkin edi:

```ts
effect(() => {
  console.log(`User set to ${currentUser()} and the counter is ${counter()}`);
});
```

Bu misol `currentUser` _yoki_ `counter` oʻzgarganda xabarni logga yozadi. Biroq, agar effect faqat `currentUser` oʻzgarganda ishga tushishi kerak boʻlsa, `counter`'ni oʻqish shunchaki tasodifiy boʻlib, `counter`'dagi oʻzgarishlar yangi xabarni logga yozmasligi kerak.

Signal oʻqilishining kuzatilishini uning getter'ini `untracked` bilan chaqirish orqali oldini olishingiz mumkin:

```ts
effect(() => {
  console.log(`User set to ${currentUser()} and the counter is ${untracked(counter)}`);
});
```

`untracked` effect bogʻliqlik sifatida qaralmasligi kerak boʻlgan tashqi kodni chaqirishi kerak boʻlganda ham foydali:

```ts
effect(() => {
  const user = currentUser();
  untracked(() => {
    // If the `loggingService` reads signals, they won't be counted as
    // dependencies of this effect.
    this.loggingService.log(`User set to ${user}`);
  });
});
```

### Reaktiv kontekst va asinxron operatsiyalar {#reactive-context-and-async-operations}

Reaktiv kontekst faqat sinxron kod uchun faol. Asinxron chegaradan keyin sodir boʻladigan har qanday signal oʻqishlari bogʻliqlik sifatida kuzatilmaydi.

```ts {avoid}
effect(async () => {
  const data = await fetchUserData();
  // Reactive context is lost here - theme() won't be tracked
  console.log(`User: ${data.name}, Theme: ${theme()}`);
});
```

Barcha signal oʻqishlari kuzatilishini taʼminlash uchun signallarni `await`'dan oldin oʻqing. Bunga ularni kutilayotgan (awaited) funksiyaga argument sifatida uzatish ham kiradi, chunki argumentlar sinxron hisoblanadi:

```ts {prefer}
effect(async () => {
  const currentTheme = theme(); // Read before await
  const data = await fetchUserData();
  console.log(`User: ${data.name}, Theme: ${currentTheme}`);
});
```

```ts {prefer}
effect(async () => {
  // Also works: signal is read before await (as function argument)
  await renderContent(docContent());
});
```

## Murakkab hosil qilishlar {#advanced-derivations}

`computed` oddiy faqat oʻqish uchun hosil qilishlarni hal qilsa-da, sizga boshqa signallarga bogʻliq boʻlgan yoziladigan holat kerak boʻlib qolishi mumkin.
Koʻproq maʼlumot uchun [linkedSignal bilan bogʻliq holat](/guide/signals/linked-signal) qoʻllanmasiga qarang.

Barcha signal API'lari sinxron — `signal`, `computed`, `input` va boshqalar. Biroq ilovalar koʻpincha asinxron tarzda mavjud boʻladigan maʼlumotlar bilan ishlashi kerak. `Resource` asinxron maʼlumotlarni ilovangizning signallarga asoslangan kodiga kiritish va shunga qaramay uning maʼlumotlariga sinxron tarzda kirish imkonini beradi. Koʻproq maʼlumot uchun [Resource'lar bilan asinxron reaktivlik](/guide/signals/resource) qoʻllanmasiga qarang.

## Reaktiv boʻlmagan API'larda yon taʼsirlarni bajarish {#executing-side-effects-on-non-reactive-apis}

Holat oʻzgarishlariga javob berishni istaganimizda sinxron yoki asinxron hosil qilishlar tavsiya etiladi. Biroq bu barcha mumkin boʻlgan holatlarni qamrab olmaydi va baʼzan reaktiv boʻlmagan API'larda signal oʻzgarishlariga javob berish zarur boʻlgan vaziyatga tushib qolasiz. Bunday maxsus holatlar uchun `effect` yoki `afterRenderEffect`'dan foydalaning. Koʻproq maʼlumot uchun [Reaktiv boʻlmagan API'lar uchun yon taʼsirlar](/guide/signals/effect) qoʻllanmasiga qarang.

## `OnPush` komponentlarida signallarni oʻqish {#reading-signals-in-onpush-components}

`OnPush` komponentining shablonida signalni oʻqiganingizda, Angular bu signalni oʻsha komponentning bogʻliqligi sifatida kuzatadi. Bu signalning qiymati oʻzgarganda Angular komponentni avtomatik ravishda [belgilaydi](api/core/ChangeDetectorRef#markForCheck), shunda u oʻzgarishlarni aniqlash keyingi safar ishga tushganda yangilanadi. `OnPush` komponentlari haqida koʻproq maʼlumot olish uchun [Komponent pastki daraxtlarini oʻtkazib yuborish](best-practices/skipping-subtrees) qoʻllanmasiga qarang.

## Qoʻshimcha mavzular {#advanced-topics}

### Signal tenglik funksiyalari {#signal-equality-functions}

Signal yaratishda ixtiyoriy ravishda tenglik funksiyasini berishingiz mumkin; u yangi qiymat oldingisidan haqiqatda farq qiladimi-yoʻqmi tekshirish uchun ishlatiladi.

```ts
import isEqual from 'lodash/isEqual';

const data = signal(['test'], {equal: isEqual});

// Even though this is a different array instance, the deep equality
// function will consider the values to be equal, and the signal won't
// trigger any updates.
data.set(['test']);
```

Tenglik funksiyalarini yoziladigan signallarga ham, hisoblangan signallarga ham berish mumkin.

HELPFUL: Sukut boʻyicha signallar referens tengligidan ([`Object.is()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object/is) taqqoslashidan) foydalanadi.

### Signallarning turini tekshirish {#type-checking-signals}

Qiymat `Signal` ekanini tekshirish uchun `isSignal`'dan foydalanishingiz mumkin:

```ts
const count = signal(0);
const doubled = computed(() => count() * 2);

isSignal(count); // true
isSignal(doubled); // true
isSignal(42); // false
```

Signal yoziladigan ekanini aniq tekshirish uchun `isWritableSignal`'dan foydalaning:

```ts
const count = signal(0);
const doubled = computed(() => count() * 2);

isWritableSignal(count); // true
isWritableSignal(doubled); // false
```

## Signallardan RxJS bilan foydalanish {#using-signals-with-rxjs}

Signallar va RxJS oʻrtasidagi oʻzaro muvofiqlik (interoperability) haqida batafsil maʼlumot uchun [Angular signallari bilan RxJS interop](ecosystem/rxjs-interop) sahifasiga qarang.

## Signallarni debug qilish {#debugging-signals}

Angular DevTools komponent yoki direktivaning signal grafigini vizuallashtirib, uning signallari, computed'lari, effect'lari va boshqa reaktiv tugunlari bir-biriga qanday bogʻliq ekanini koʻrsatishi mumkin.
Grafikni qanday ochish, oʻqish va tekshirishni bilish uchun [Signal grafigini debug qilish](tools/devtools/signals) sahifasiga qarang.
