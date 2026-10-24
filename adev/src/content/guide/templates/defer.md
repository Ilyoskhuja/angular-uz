# `@defer` bilan kechiktirilgan yuklash

Kechiktiriladigan view'lar (deferrable views), yaʼni `@defer` bloklari, sahifaning dastlabki render qilinishi uchun mutlaqo zarur boʻlmagan kodning yuklanishini kechiktirish orqali ilovangizning dastlabki bundle hajmini kamaytiradi. Bu koʻpincha dastlabki yuklanishning tezlashishiga va Core Web Vitals (CWV), asosan Largest Contentful Paint (LCP) va Time to First Byte (TTFB) koʻrsatkichlarining yaxshilanishiga olib keladi.

Bu imkoniyatdan foydalanish uchun shablonningizning bir qismini deklarativ tarzda @defer blokiga oʻrashingiz mumkin:

```angular-html
@defer {
  <large-component />
}
```

`@defer` bloki ichidagi har qanday komponent, direktiva va pipe'larning kodi alohida JavaScript fayliga ajratiladi va faqat zarur boʻlganda, shablonning qolgan qismi render qilingandan keyin yuklanadi.

Kechiktiriladigan view'lar turli triggerlarni, oldindan yuklash (prefetching) variantlarini, shuningdek, toʻldiruvchi (placeholder), yuklanish va xato holatlarini boshqarish uchun ichki bloklarni qoʻllab-quvvatlaydi.

## Qaysi bogʻliqliklar kechiktiriladi? {#which-dependencies-are-deferred}

Ilovani yuklashda komponentlar, direktivalar, pipe'lar va har qanday komponent CSS stillari kechiktirilishi mumkin.

`@defer` bloki ichidagi bogʻliqliklar kechiktirilishi uchun ular ikki shartga javob berishi kerak:

1. **Ular standalone boʻlishi shart.** Standalone boʻlmagan bogʻliqliklar kechiktirilmaydi va `@defer` bloklari ichida boʻlsa ham, baribir darhol (eagerly) yuklanadi.
1. **Ularga xuddi shu fayl ichida `@defer` bloklaridan tashqarida murojaat qilinmasligi kerak.** Agar ularga `@defer` blokidan tashqarida yoki ViewChild soʻrovlari ichida murojaat qilinsa, bogʻliqliklar darhol yuklanadi.

`@defer` blokida ishlatiladigan komponentlar, direktivalar va pipe'larning _tranzitiv_ bogʻliqliklari standalone boʻlishi shart emas; tranzitiv bogʻliqliklar `NgModule`'da eʼlon qilingan boʻlib, kechiktirilgan yuklashda ishtirok etishi mumkin.

Angular kompilyatori `@defer` blokida ishlatiladigan har bir komponent, direktiva va pipe uchun [dinamik import](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/import) ifodasini hosil qiladi. Blokning asosiy kontenti barcha importlar hal boʻlgandan keyin render qilinadi. Angular bu importlar uchun hech qanday maʼlum tartibni kafolatlamaydi.

## Kechiktirilgan yuklashning turli bosqichlarini qanday boshqarish {#how-to-manage-different-stages-of-deferred-loading}

`@defer` bloklari kechiktirilgan yuklash jarayonining turli bosqichlarini muammosiz boshqarish imkonini beruvchi bir nechta ichki bloklarga ega.

### `@defer`

Bu lazy tarzda yuklanadigan kontent qismini belgilaydigan asosiy blok. U dastlab render qilinmaydi: kechiktirilgan kontent koʻrsatilgan [trigger](#controlling-deferred-content-loading-with-triggers) ishga tushganda yoki `when` sharti bajarilganda yuklanadi va render qilinadi.

Sukut boʻyicha `@defer` bloki brauzer holati [boʻsh (idle)](/guide/templates/defer#idle) boʻlganda ishga tushadi.

```angular-html
@defer {
  <large-component />
}
```

### `@placeholder` bilan toʻldiruvchi kontentni koʻrsatish {#show-placeholder-content-with-placeholder}

Sukut boʻyicha defer bloklari ishga tushishidan oldin hech qanday kontentni render qilmaydi.

`@placeholder` — `@defer` bloki ishga tushishidan oldin qanday kontent koʻrsatilishini eʼlon qiladigan ixtiyoriy blok.

```angular-html
@defer {
  <large-component />
} @placeholder {
  <p>Placeholder content</p>
}
```

Ixtiyoriy boʻlsa-da, baʼzi triggerlar ishlashi uchun `@placeholder` yoki [shablon havola oʻzgaruvchisi (template reference variable)](/guide/templates/variables#template-reference-variables) mavjud boʻlishini talab qilishi mumkin. Batafsil maʼlumot uchun [Triggerlar](#controlling-deferred-content-loading-with-triggers) boʻlimiga qarang.

Yuklash tugagach, Angular toʻldiruvchi kontentni asosiy kontent bilan almashtiradi. Toʻldiruvchi boʻlimida oddiy HTML, komponentlar, direktivalar va pipe'lar kabi istalgan kontentdan foydalanishingiz mumkin. Yodda tuting: _toʻldiruvchi blokining bogʻliqliklari darhol yuklanadi_.

`@placeholder` bloki toʻldiruvchi kontent dastlab render qilingandan keyin ushbu toʻldiruvchi koʻrsatilishi kerak boʻlgan `minimum` vaqtni belgilash uchun ixtiyoriy parametrni qabul qiladi.

```angular-html
@defer {
  <large-component />
} @placeholder (minimum 500ms) {
  <p>Placeholder content</p>
}
```

Bu `minimum` parametri millisekund (ms) yoki sekund (s) vaqt birliklarida koʻrsatiladi. Kechiktirilgan bogʻliqliklar tez yuklab olingan hollarda toʻldiruvchi kontentning tez miltillashini oldini olish uchun bu parametrdan foydalanishingiz mumkin.

### `@loading` bilan yuklanish kontentini koʻrsatish {#show-loading-content-with-loading}

`@loading` bloki — kechiktirilgan bogʻliqliklar yuklanayotgan vaqtda koʻrsatiladigan kontentni eʼlon qilish imkonini beruvchi ixtiyoriy blok. Yuklash ishga tushgach, u `@placeholder` blokini almashtiradi.

```angular-html
@defer {
  <large-component />
} @loading {
  <img alt="loading..." src="loading.gif" />
} @placeholder {
  <p>Placeholder content</p>
}
```

Uning bogʻliqliklari darhol yuklanadi (`@placeholder`'ga oʻxshab).

`@loading` bloki kechiktirilgan bogʻliqliklar tez yuklab olinganda yuzaga kelishi mumkin boʻlgan kontentning tez miltillashini oldini olishga yordam beradigan ikki ixtiyoriy parametrni qabul qiladi:

- `minimum` - ushbu toʻldiruvchi koʻrsatilishi kerak boʻlgan minimal vaqt
- `after` - yuklash boshlangandan keyin yuklanish shablonini koʻrsatishdan oldin kutish vaqti

```angular-html
@defer {
  <large-component />
} @loading (after 100ms; minimum 1s) {
  <img alt="loading..." src="loading.gif" />
}
```

Ikkala parametr ham millisekund (ms) yoki sekund (s) vaqt birliklarida koʻrsatiladi. Bundan tashqari, ikkala parametr uchun taymerlar yuklash ishga tushgandan keyin darhol boshlanadi.

### Kechiktirilgan yuklash muvaffaqiyatsiz boʻlganda `@error` bilan xato holatini koʻrsatish {#show-error-state-when-deferred-loading-fails-with-error}

`@error` bloki — kechiktirilgan yuklash muvaffaqiyatsiz boʻlganda koʻrsatiladigan ixtiyoriy blok. `@placeholder` va `@loading`'ga oʻxshab, @error blokining bogʻliqliklari darhol yuklanadi.

```angular-html
@defer {
  <large-component />
} @error {
  <p>Failed to load large component.</p>
}
```

## Kechiktirilgan kontent yuklanishini triggerlar bilan boshqarish {#controlling-deferred-content-loading-with-triggers}

Angular kechiktirilgan kontentni qachon yuklashi va koʻrsatishini boshqaradigan **triggerlarni** belgilashingiz mumkin.

`@defer` bloki ishga tushganda, u toʻldiruvchi kontentni lazy tarzda yuklangan kontent bilan almashtiradi.

Bir nechta hodisa triggerlarini nuqta-vergul `;` bilan ajratib belgilash mumkin va ular OR shartlari sifatida hisoblanadi.

Triggerlarning ikki turi mavjud: `on` va `when`.

### `on`

`on` `@defer` bloki qachon ishga tushishi shartini belgilaydi.

Mavjud triggerlar quyidagilar:

| Trigger                       | Tavsifi                                                                              |
| ----------------------------- | ------------------------------------------------------------------------------------ |
| [`idle`](#idle)               | Brauzer boʻsh boʻlganda ishga tushadi. Ixtiyoriy timeout'ni qoʻllab-quvvatlaydi.     |
| [`viewport`](#viewport)       | Koʻrsatilgan kontent viewport'ga kirganda ishga tushadi                              |
| [`interaction`](#interaction) | Foydalanuvchi koʻrsatilgan element bilan oʻzaro aloqa qilganda ishga tushadi         |
| [`hover`](#hover)             | Sichqoncha koʻrsatilgan hudud ustiga kelganda ishga tushadi                          |
| [`immediate`](#immediate)     | Kechiktirilmagan kontent render qilinib tugagandan keyin darhol ishga tushadi        |
| [`timer`](#timer)             | Belgilangan vaqt oʻtgandan keyin ishga tushadi                                       |

#### `idle`

`idle` triggeri requestIdleCallback asosida brauzer boʻsh holatga oʻtgach kechiktirilgan kontentni yuklaydi. Bu defer bloki uchun sukut boʻyicha xatti-harakat.

Ixtiyoriy ravishda [`requestIdleCallback`](https://developer.mozilla.org/docs/Web/API/Window/requestIdleCallback)'ga uzatiladigan timeout'ni millisekundlarda belgilashingiz mumkin. Agar brauzer callback'ni yetarlicha tez rejalashtirmasa, ish belgilangan timeout'dan kechikmasdan bajariladi.

```angular-html
<!-- @defer (on idle) -->
@defer {
  <large-cmp />
} @placeholder {
  <div>Large component placeholder</div>
}

<!-- With a 500ms timeout -->
@defer (on idle(500)) {
  <large-cmp />
}
```

##### `idle` xatti-harakatini sozlash {#customizing-idle-behavior}

Oʻzingizning `IdleService` amalga oshirishingizni taqdim etib va uni ilovangiz provider'larida `provideIdleServiceWith` orqali roʻyxatdan oʻtkazib, `idle` triggerini sozlashingiz mumkin.

```ts
@Service()
class CustomIdleService implements IdleService {
  requestOnIdle(callback: (deadline?: IdleDeadline) => void, options?: IdleRequestOptions): number {
    // Custom idle scheduling logic can be implemented here.
    return requestIdleCallback(callback, options);
  }

  cancelOnIdle(id: number) {
    // Implement custom idle cancellation here.
  }
}

bootstrapApplication(App, {
  providers: [provideIdleServiceWith(CustomIdleService)],
});
```

#### `viewport`

`viewport` triggeri [Intersection Observer API](https://developer.mozilla.org/docs/Web/API/Intersection_Observer_API)'dan foydalanib, koʻrsatilgan kontent viewport'ga kirganda kechiktirilgan kontentni yuklaydi. Kuzatilayotgan kontent `@placeholder` kontenti yoki aniq element havolasi boʻlishi mumkin.

Sukut boʻyicha `@defer` toʻldiruvchining viewport'ga kirishini kuzatadi. Shu tarzda ishlatiladigan toʻldiruvchilar yagona ildiz elementga ega boʻlishi shart.

```angular-html
@defer (on viewport) {
  <large-cmp />
} @placeholder {
  <div>Large component placeholder</div>
}
```

Muqobil ravishda, `@defer` bloki bilan bir xil shablondagi [shablon havola oʻzgaruvchisini](/guide/templates/variables) viewport'ga kirishi kuzatiladigan element sifatida belgilashingiz mumkin. Bu oʻzgaruvchi viewport triggeriga parametr sifatida uzatiladi.

```angular-html
<div #greeting>Hello!</div>
@defer (on viewport(greeting)) {
  <greetings-cmp />
}
```

Agar `IntersectionObserver` variantlarini sozlamoqchi boʻlsangiz, `viewport` triggeri obyekt literalini uzatishni qoʻllab-quvvatlaydi. Literal `IntersectionObserver`'ning ikkinchi parametridagi `root`'dan tashqari barcha xususiyatlarni qoʻllab-quvvatlaydi. Obyekt literali yozuvidan foydalanganda triggeringizni `trigger` xususiyati orqali uzatishingiz kerak.

```angular-html
<div #greeting>Hello!</div>

<!-- With options and a trigger -->
@defer (
  on viewport({trigger: greeting, rootMargin: '100px', scrollMargin: '50px', threshold: 0.5})
) {
  <greetings-cmp />
}

<!-- With options and an implied trigger -->
@defer (on viewport({rootMargin: '100px', scrollMargin: '50px', threshold: 0.5})) {
  <greetings-cmp />
} @placeholder {
  <div>Implied trigger</div>
}
```

#### `interaction`

`interaction` triggeri foydalanuvchi koʻrsatilgan element bilan `click` yoki `keydown` hodisalari orqali oʻzaro aloqa qilganda kechiktirilgan kontentni yuklaydi.

Sukut boʻyicha toʻldiruvchi oʻzaro aloqa elementi vazifasini bajaradi. Shu tarzda ishlatiladigan toʻldiruvchilar yagona ildiz elementga ega boʻlishi shart.

```angular-html
@defer (on interaction) {
  <large-cmp />
} @placeholder {
  <div>Large component placeholder</div>
}
```

Muqobil ravishda, `@defer` bloki bilan bir xil shablondagi [shablon havola oʻzgaruvchisini](/guide/templates/variables) oʻzaro aloqalar kuzatiladigan element sifatida belgilashingiz mumkin. Bu oʻzgaruvchi interaction triggeriga parametr sifatida uzatiladi.

```angular-html
<div #greeting>Hello!</div>
@defer (on interaction(greeting)) {
  <greetings-cmp />
}
```

#### `hover`

`hover` triggeri sichqoncha `mouseover` va `focusin` hodisalari orqali trigger hududi ustiga kelganda kechiktirilgan kontentni yuklaydi.

Sukut boʻyicha toʻldiruvchi oʻzaro aloqa elementi vazifasini bajaradi. Shu tarzda ishlatiladigan toʻldiruvchilar yagona ildiz elementga ega boʻlishi shart.

```angular-html
@defer (on hover) {
  <large-cmp />
} @placeholder {
  <div>Large component placeholder</div>
}
```

Muqobil ravishda, `@defer` bloki bilan bir xil shablondagi [shablon havola oʻzgaruvchisini](/guide/templates/variables) sichqoncha ustiga keladigan element sifatida belgilashingiz mumkin. Bu oʻzgaruvchi hover triggeriga parametr sifatida uzatiladi.

```angular-html
<div #greeting>Hello!</div>
@defer (on hover(greeting)) {
  <greetings-cmp />
}
```

#### `immediate`

`immediate` triggeri kechiktirilgan kontentni darhol yuklaydi. Bu kechiktirilgan blok boshqa barcha kechiktirilmagan kontent render qilinib tugashi bilanoq yuklanishini anglatadi.

```angular-html
@defer (on immediate) {
  <large-cmp />
} @placeholder {
  <div>Large component placeholder</div>
}
```

#### `timer`

`timer` triggeri kechiktirilgan kontentni belgilangan vaqt oʻtgandan keyin yuklaydi.

```angular-html
@defer (on timer(500ms)) {
  <large-cmp />
} @placeholder {
  <div>Large component placeholder</div>
}
```

Davomiylik parametri millisekund (`ms`) yoki sekund (`s`) birligida koʻrsatilishi shart.

### `when`

`when` triggeri maxsus shartli ifodani qabul qiladi va shart truthy boʻlganda kechiktirilgan kontentni yuklaydi.

```angular-html
@defer (when condition) {
  <large-cmp />
} @placeholder {
  <div>Large component placeholder</div>
}
```

Bu bir martalik amal: shart truthy boʻlgandan keyin falsy qiymatga oʻzgarsa, `@defer` bloki toʻldiruvchiga qaytib oʻtmaydi.

## `prefetch` bilan maʼlumotlarni oldindan yuklash {#prefetching-data-with-prefetch}

Kechiktirilgan kontent qachon koʻrsatilishini belgilaydigan shartdan tashqari, ixtiyoriy ravishda **prefetch triggerini** ham belgilashingiz mumkin. Bu trigger `@defer` bloki bilan bogʻliq JavaScript'ni kechiktirilgan kontent koʻrsatilishidan oldin yuklash imkonini beradi.

Oldindan yuklash yanada ilgʻor xatti-harakatlarni taʼminlaydi, masalan, foydalanuvchi defer blokini hali koʻrmagan yoki u bilan oʻzaro aloqa qilmagan, lekin tez orada aloqa qilishi mumkin boʻlgan paytda resurslarni oldindan yuklashni boshlash orqali resurslarni tezroq tayyor holga keltirish imkonini beradi.

Prefetch triggerini blokning asosiy triggeriga oʻxshab, lekin `prefetch` kalit soʻzi prefiksi bilan belgilashingiz mumkin. Blokning asosiy triggeri va prefetch triggeri nuqta-vergul belgisi (`;`) bilan ajratiladi.

Quyidagi misolda oldindan yuklash brauzer boʻsh boʻlganda boshlanadi, blok kontenti esa faqat foydalanuvchi toʻldiruvchi bilan oʻzaro aloqa qilgandan keyin render qilinadi.

```angular-html
@defer (on interaction; prefetch on idle) {
  <large-cmp />
} @placeholder {
  <div>Large component placeholder</div>
}

<!-- Prefetching with a 500ms idle timeout -->
@defer (on interaction; prefetch on idle(500)) {
  <large-cmp />
}
```

## `@defer` bloklarini testlash {#testing-defer-blocks}

Angular `@defer` bloklarini testlash va test davomida turli holatlarni ishga tushirish jarayonini soddalashtirish uchun TestBed API'larini taqdim etadi. Sukut boʻyicha testlardagi `@defer` bloklari haqiqiy ilovadagi defer bloki kabi ishlaydi. Agar holatlar boʻylab qoʻlda oʻtmoqchi boʻlsangiz, TestBed konfiguratsiyasida defer bloki xatti-harakatini `Manual` rejimiga oʻtkazishingiz mumkin.

```angular-ts
it('should render a defer block in different states', async () => {
  // configures the defer block behavior to start in "paused" state for manual control.
  TestBed.configureTestingModule({deferBlockBehavior: DeferBlockBehavior.Manual});
  @Component({
    // ...
    template: `
      @defer {
        <large-component />
      } @placeholder {
        Placeholder
      } @loading {
        Loading...
      }
    `,
  })
  class ExampleA {}
  // Create component fixture.
  const componentFixture = TestBed.createComponent(ExampleA);
  // Retrieve the list of all defer block fixtures and get the first block.
  const deferBlockFixture = (await componentFixture.getDeferBlocks())[0];
  // Renders placeholder state by default.
  expect(componentFixture.nativeElement.innerHTML).toContain('Placeholder');
  // Render loading state and verify rendered output.
  await deferBlockFixture.render(DeferBlockState.Loading);
  expect(componentFixture.nativeElement.innerHTML).toContain('Loading');
  // Render final state and verify the output.
  await deferBlockFixture.render(DeferBlockState.Complete);
  expect(componentFixture.nativeElement.innerHTML).toContain('large works!');
});
```

## `@defer` `NgModule` bilan ishlaydimi? {#does-defer-work-with-ngmodule}

`@defer` bloklari standalone komponentlar, direktivalar va pipe'lar bilan ham, NgModule'ga asoslanganlar bilan ham mos. Biroq **faqat standalone komponentlar, direktivalar va pipe'lar kechiktirilishi mumkin**. NgModule'ga asoslangan bogʻliqliklar kechiktirilmaydi va darhol yuklanadigan bundle'ga kiritiladi.

## `@defer` bloklari va Hot Module Reload (HMR) oʻrtasidagi moslik {#compatibility-between-defer-blocks-and-hot-module-reload-hmr}

Hot Module Replacement (HMR) faol boʻlganda, barcha `@defer` blok chunk'lari sozlangan har qanday triggerlardan qatʼi nazar darhol yuklab olinadi. Standart trigger xatti-harakatini tiklash uchun ilovangizni `--no-hmr` bayrogʻi bilan ishga tushirib, HMR'ni oʻchirib qoʻyishingiz kerak.

## `@defer` server tomonida render qilish (SSR) va statik sayt generatsiyasi (SSG) bilan qanday ishlaydi? {#how-does-defer-work-with-server-side-rendering-ssr-and-static-site-generation-ssg}

Sukut boʻyicha ilova serverda render qilinganda (SSR yoki SSG yordamida), defer bloklari doimo oʻz `@placeholder`'ini (yoki toʻldiruvchi koʻrsatilmagan boʻlsa, hech narsani) render qiladi va triggerlar chaqirilmaydi. Klientda `@placeholder` kontenti gidratsiya qilinadi va triggerlar faollashtiriladi.

`@defer` bloklarining asosiy kontentini serverda (SSR ham, SSG ham) render qilish uchun [Bosqichma-bosqich gidratsiya (Incremental Hydration) imkoniyatini](/guide/incremental-hydration) yoqib, zarur bloklar uchun `hydrate` triggerlarini sozlashingiz mumkin.

## Barrel fayllar va lazy chunk'lar {#barrel-files-and-lazy-chunks}

Agar `@defer`'dan foydalanayotgan boʻlsangiz, lekin build natijasida alohida lazy chunk koʻrmasangiz, kechiktirilgan komponentni qanday import qilayotganingizni tekshiring. Barrel fayl (`index.ts`) orqali import qilish — keng tarqalgan sabab: bundler'lar barrel'ni yagona modul sifatida koʻradi va uning barcha eksportlarini birga saqlaydi, shuning uchun komponentingiz `@defer`'dan qatʼi nazar asosiy bundle'ga tushib qoladi.

```typescript {header: "index.ts"}
export {HeavyComponent} from './heavy.component';
export {OtherComponent} from './other.component';
```

```typescript {header: "parent.component.ts"}
import {HeavyComponent} from './index'; // pulls in OtherComponent too

@Component({
  imports: [HeavyComponent],
  template: `@defer {
    <heavy-component />
  }`,
})
export class ParentComponent {}
```

Yechimi oddiy — komponentning oʻz faylidan toʻgʻridan-toʻgʻri import qiling:

```typescript
import {HeavyComponent} from './heavy.component';
```

Bundler'ning uni alohida chunk'ga ajratishi va trigger ishga tushganda lazy tarzda yuklashi uchun shuning oʻzi kifoya.

## View'larni kechiktirish boʻyicha eng yaxshi amaliyotlar {#best-practices-for-deferring-views}

### Ichma-ich `@defer` bloklari bilan kaskadli yuklanishlardan qoching {#avoid-cascading-loads-with-nested-defer-blocks}

Ichma-ich `@defer` bloklaringiz boʻlsa, bir vaqtda yuklanishdan qochish uchun ular turli triggerlarga ega boʻlishi kerak, chunki bir vaqtda yuklanish kaskadli soʻrovlarga olib keladi va sahifa yuklanish unumdorligiga salbiy taʼsir koʻrsatishi mumkin.

### Layout siljishlaridan qoching {#avoid-layout-shifts}

Dastlabki yuklanishda foydalanuvchi viewport'ida koʻrinadigan komponentlarni kechiktirishdan qoching. Bunday qilish yigʻilgan layout siljishini (cumulative layout shift, CLS) oshirib, Core Web Vitals'ga salbiy taʼsir koʻrsatishi mumkin.

Bu zarur boʻlgan hollarda, kontentning sahifaning dastlabki render qilinishi vaqtida yuklanishiga sabab boʻladigan `immediate`, `timer`, `viewport` va maxsus `when` triggerlaridan qoching.

### Foydalanish imkoniyatini (accessibility) yodda tuting {#keep-accessibility-in-mind}

`@defer` bloklaridan foydalanganda ekran oʻquvchilari (screen readers) kabi yordamchi texnologiyalardan foydalanuvchi odamlarga taʼsirini hisobga oling.
Kechiktirilgan boʻlimga fokuslangan ekran oʻquvchilari dastlab toʻldiruvchi yoki yuklanish kontentini oʻqiydi, lekin kechiktirilgan kontent yuklanganda oʻzgarishlarni eʼlon qilmasligi mumkin.

Kechiktirilgan kontent oʻzgarishlari ekran oʻquvchilariga eʼlon qilinishini taʼminlash uchun `@defer` blokingizni live region'ga ega elementga oʻrashingiz mumkin:

```angular-html
<div aria-live="polite" aria-atomic="true">
  @defer (on timer(2000)) {
    <user-profile [user]="currentUser" />
  } @placeholder {
    Loading user profile...
  } @loading {
    Please wait...
  } @error {
    Failed to load profile
  }
</div>
```

Bu oʻtishlar (toʻldiruvchi &rarr; yuklanish &rarr; kontent/xato) sodir boʻlganda oʻzgarishlar foydalanuvchiga eʼlon qilinishini taʼminlaydi.
