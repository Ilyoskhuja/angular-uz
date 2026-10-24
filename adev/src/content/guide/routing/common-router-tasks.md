# Boshqa keng tarqalgan marshrutlash vazifalari

Bu qoʻllanma ilovangizda Angular router'dan foydalanish bilan bogʻliq boshqa baʼzi keng tarqalgan vazifalarni qamrab oladi.

## Marshrut maʼlumotlarini olish {#getting-route-information}

Koʻpincha foydalanuvchi ilovangiz boʻylab navigatsiya qilganda maʼlumotni bir komponentdan boshqasiga uzatishni xohlaysiz.
Masalan, oziq-ovqat mahsulotlarining xarid roʻyxatini koʻrsatadigan ilovani koʻrib chiqaylik.
Roʻyxatdagi har bir mahsulot noyob `id` ga ega.
Mahsulotni tahrirlash uchun foydalanuvchilar Edit tugmasini bosadi, bu `EditGroceryItem` komponentini ochadi.
Bu komponent foydalanuvchiga toʻgʻri maʼlumotni koʻrsata olishi uchun mahsulotning `id` sini olishini xohlaysiz.

Bunday maʼlumotni ilova komponentlaringizga uzatish uchun marshrutdan foydalaning.
Buning uchun `provideRouter` bilan `withComponentInputBinding` imkoniyatidan yoki `RouterModule.forRoot` ning `bindToComponentInputs` opsiyasidan foydalanasiz.

Marshrutdan maʼlumot olish uchun:

<docs-workflow>

<docs-step title="`withComponentInputBinding` ni qoʻshing">

`provideRouter` metodiga `withComponentInputBinding` imkoniyatini qoʻshing.

```ts
providers: [provideRouter(appRoutes, withComponentInputBinding())];
```

</docs-step>

<docs-step title="Komponentga `input` qoʻshing">

Komponentni parametr nomiga mos keladigan `input()` xususiyatiga ega boʻladigan tarzda yangilang.

```ts
id = input.required<string>();
hero = computed(() => this.service.getHero(this.id()));
```

</docs-step>
<docs-step title="Ixtiyoriy: Sukut boʻyicha qiymatdan foydalaning">
`withComponentInputBinding` yoqilganda router joriy marshrutga asoslanib barcha input'larga qiymat tayinlaydi.
Agar input kalitiga mos marshrut maʼlumoti boʻlmasa, masalan, ixtiyoriy soʻrov parametri yoʻq boʻlsa, router `undefined` tayinlaydi.
Input marshrutga mos kelmasligi ehtimoli boʻlganda `input` turiga `undefined` ni kiritishingiz kerak.

Sukut boʻyicha qiymatni input'dagi `transform` opsiyasidan foydalanib yoki `linkedSignal` bilan lokal holatni boshqarib taqdim eting.

```ts
id = input.required({
  transform: (maybeUndefined: string | undefined) => maybeUndefined ?? '0',
});
// or
id = input<string | undefined>();
internalId = linkedSignal(() => this.id() ?? getDefaultId());
```

</docs-step>
</docs-workflow>

NOTE: Kalit-qiymat juftliklariga ega barcha marshrut maʼlumotlarini komponent input'lariga bogʻlashingiz mumkin: marshrut resource'lari, statik yoki hal qilingan marshrut maʼlumotlari, yoʻl parametrlari, matritsa parametrlari va soʻrov parametrlari.

### Input bogʻlash ustuvorligi {#input-binding-priority}

Bir nechta marshrut manbalari bir xil kalitlarni aniqlasa, router toʻqnashuvlarni quyidagi ustuvorlik tartibida (eng yuqoridan eng pastga) hal qiladi:

1. **Marshrut resource'lari**: Marshrutning `resources` xaritasida aniqlangan qiymatlar. Bloklaydigan resource'lar oʻzining ochilgan qiymatini (`resource.value()`) bogʻlaydi, bloklamaydigan resource'lar esa `Resource` nusxasini bogʻlaydi.
2. **Marshrut maʼlumotlari va resolver'lar**: `data` da aniqlangan statik maʼlumotlar yoki `resolve` orqali hal qilingan qiymatlar.
3. **Yoʻl parametrlari va matritsa parametrlari**: URL yoʻlidagi parametrlar (masalan, `:id`) va matritsa parametrlari.
4. **Soʻrov parametrlari**: Soʻrov satridagi parametrlar (masalan, `?id=123`).

Masalan, marshrutda `:id` yoʻl parametri ham, `?id=...` soʻrov parametri ham boʻlsa, komponentning `id` input'iga yoʻl parametri qiymati bogʻlanadi. Agar marshrut `id` nomli resource'ni ham aniqlasa, resource qiymati ikkalasidan ham ustun turadi.

### Soʻrov parametrlarini bogʻlashni oʻchirish {#disable-query-parameter-binding}

Soʻrov parametrlarini alohida boshqarsangiz, soʻrov parametrlarini bogʻlashni oʻchirish uchun `ComponentInputBindingOptions` dan foydalaning:

```ts
provideRouter(appRoutes, withComponentInputBinding({queryParams: false}));
```

### Router maʼlumotlarida mavjud boʻlmagan input'lar uchun xatti-harakatni sozlash {#configure-behavior-for-inputs-not-available-in-router-data}

Sukut boʻyicha, navigatsiya davomida input router maʼlumotlarida mavjud boʻlmasa, router uni `undefined` ga oʻrnatadi. Bu eskirgan maʼlumotlarning saqlanib qolmasligini taʼminlaydi.

Faol komponent nusxasi uchun router maʼlumotlarida _hech qachon_ mavjud boʻlmagan input'larga `undefined` oʻrnatilishidan qochmoqchi boʻlsangiz, `unmatchedInputBehavior` opsiyasini `'undefinedIfStale'` ga oʻrnatishingiz mumkin:

```ts
provideRouter(appRoutes, withComponentInputBinding({unmatchedInputBehavior: 'undefinedIfStale'}));
```

`unmatchedInputBehavior: 'undefinedIfStale'` ni `queryParams: false` bilan birlashtirganingizda, input'lar router tomonidan aniq taqdim etilmaguncha oʻzining boshlangʻich qiymatlarini saqlab qoladi. Istisno — matritsa parametrlari: agar matritsa parametri bir navigatsiyada taqdim etilib, keyingisida olib tashlansa, router eskirgan maʼlumotlarning saqlanib qolishidan qochish uchun input'ni `undefined` ga oʻrnatadi.

```ts
provideRouter(
  appRoutes,
  withComponentInputBinding({
    queryParams: false,
    unmatchedInputBehavior: 'undefinedIfStale',
  }),
);
```

### Ota marshrut maʼlumotlarini meros qilib olish {#inherit-parent-route-data}

Sukut boʻyicha bola marshrutlar ota marshrutlardan parametrlar va maʼlumotlarni meros qilib oladi (`paramsInheritanceStrategy: 'always'` ga teng). Bu bola komponentlarda ota marshrut maʼlumotlariga bevosita murojaat qilishingiz mumkinligini anglatadi.

Parametrlar faqat boʻsh yoʻlli marshrutlardan meros qilib olinadigan eski xatti-harakatni tiklash kerak boʻlsa, `paramsInheritanceStrategy` ni `'emptyOnly'` ga oʻrnatishingiz mumkin:

```ts
provideRouter(routes, withRouterConfig({paramsInheritanceStrategy: 'emptyOnly'}));
```

Boshqa mavjud sozlamalar haqida batafsil maʼlumot uchun [router konfiguratsiya opsiyalariga](guide/routing/customizing-route-behavior#router-configuration-options) qarang.

## 404 sahifasini koʻrsatish {#displaying-a-404-page}

404 sahifasini koʻrsatish uchun `component` xususiyati 404 sahifangiz uchun ishlatmoqchi boʻlgan komponentga oʻrnatilgan [wildcard marshrutini](guide/routing/define-routes#wildcards) quyidagicha sozlang:

```ts
const routes: Routes = [
  {path: 'first-component', component: First},
  {path: 'second-component', component: Second},
  {path: '**', component: PageNotFound}, // Wildcard route for a 404 page
];
```

`path` qiymati `**` boʻlgan oxirgi marshrut — wildcard marshrut.
Soʻralgan URL roʻyxatdagi oldingi yoʻllarning hech biriga mos kelmasa, router shu marshrutni tanlaydi va foydalanuvchini `PageNotFound` ga yuboradi.

## Havola parametrlari massivi {#link-parameters-array}

Havola parametrlari massivi router navigatsiyasi uchun quyidagi tarkibiy qismlarni oʻz ichiga oladi:

- Maqsad komponentga olib boradigan marshrut yoʻli
- Marshrut URL'iga kiradigan majburiy va ixtiyoriy marshrut parametrlari

`RouterLink` direktivasini bunday massivga quyidagicha bogʻlang:

```angular-html
<a [routerLink]="['/heroes']">Heroes</a>
```

Quyida marshrut parametri koʻrsatilgan ikki elementli massiv:

```angular-html
<a [routerLink]="['/hero', hero.id]">
  <span class="badge">{{ hero.id }}</span
  >{{ hero.name }}
</a>
```

Ixtiyoriy marshrut parametrlarini `{ foo: 'foo' }` kabi obyektda taqdim eting:

```angular-html
<a [routerLink]="['/crisis-center', {foo: 'foo'}]">Crisis Center</a>
```

Bu sintaksis matritsa parametrlarini uzatadi — ular maʼlum URL segmentiga bogʻlangan ixtiyoriy parametrlardir. [Matritsa parametrlari](/guide/routing/read-route-state#matrix-parameters) haqida koʻproq bilib oling.

Bu uchta misol bir darajali marshrutlashga ega ilovaning ehtiyojlarini qoplaydi.
Biroq, krizis markazidagi kabi bola router bilan yangi havola massivi imkoniyatlarini yaratasiz.

Quyidagi minimal `RouterLink` misoli krizis markazi uchun koʻrsatilgan sukut boʻyicha bola marshrutga asoslanadi.

```angular-html
<a [routerLink]="['/crisis-center']">Crisis Center</a>
```

Quyidagilarni koʻrib chiqing:

- Massivdagi birinchi element ota marshrutni aniqlaydi \(`/crisis-center`\)
- Bu ota marshrut uchun parametrlar yoʻq
- Bola marshrut uchun sukut boʻyicha qiymat yoʻq, shuning uchun birini tanlashingiz kerak
- Marshrut yoʻli `/` boʻlgan `CrisisList` ga navigatsiya qilyapsiz, lekin qiya chiziqni aniq qoʻshishingiz shart emas

Ilovaning ildizidan Dragon Crisis'gacha navigatsiya qiladigan quyidagi router havolasini koʻrib chiqing:

```angular-html
<a [routerLink]="['/crisis-center', 1]">Dragon Crisis</a>
```

- Massivdagi birinchi element ota marshrutni aniqlaydi \(`/crisis-center`\)
- Bu ota marshrut uchun parametrlar yoʻq
- Ikkinchi element maʼlum krizis tafsilotlari uchun bola marshrutni aniqlaydi \(`/:id`\)
- Tafsilotlar bola marshruti `id` marshrut parametrini talab qiladi
- Dragon Crisis'ning `id` sini massivning ikkinchi elementi sifatida qoʻshdingiz \(`1`\)
- Natijaviy yoʻl — `/crisis-center/1`

`App` shablonini faqat Crisis Center marshrutlari bilan qayta aniqlashingiz ham mumkin:

```angular-ts
@Component({
  template: `
    <h1 class="title">Angular Router</h1>
    <nav>
      <a [routerLink]="['/crisis-center']">Crisis Center</a>
      <a [routerLink]="['/crisis-center/1', {foo: 'foo'}]">Dragon Crisis</a>
      <a [routerLink]="['/crisis-center/2']">Shark Crisis</a>
    </nav>
    <router-outlet />
  `,
})
export class App {}
```

Xulosa qilib aytganda, bir, ikki yoki undan koʻp darajali marshrutlashga ega ilovalar yozishingiz mumkin.
Havola parametrlari massivi har qanday marshrutlash chuqurligini va marshrut yoʻllari, \(majburiy\) router parametrlari va \(ixtiyoriy\) marshrut parametrlari obyektlarining har qanday ruxsat etilgan ketma-ketligini ifodalash uchun moslashuvchanlik beradi.

## `LocationStrategy` va brauzer URL uslublari {#locationstrategy-and-browser-url-styles}

Router yangi komponent koʻrinishiga (view) navigatsiya qilganda, u brauzerning joylashuvi (location) va tarixini (history) oʻsha koʻrinish uchun URL bilan yangilaydi.

Zamonaviy HTML5 brauzerlari [history.pushState](https://developer.mozilla.org/docs/Web/API/History_API/Working_with_the_History_API#adding_and_modifying_history_entries 'HTML5 browser history push-state') ni qoʻllab-quvvatlaydi — bu serverga sahifa soʻrovini yubormasdan brauzerning joylashuvi va tarixini oʻzgartiradigan usul.
Router boshqa holatda sahifani yuklashni talab qiladigan URL'dan farqlanmaydigan "tabiiy" URL tuzishi mumkin.

Mana, Crisis Center URL'i shu "HTML5 pushState" uslubida:

```text
localhost:3002/crisis-center
```

Eski brauzerlar joylashuv URL'i oʻzgarganda, agar oʻzgarish "#" \("hash" deb ataladi\) dan keyin yuz bermasa, serverga sahifa soʻrovlarini yuboradi.
Router'lar ilova ichidagi marshrut URL'larini hash'lar bilan tuzib, bu istisnodan foydalanishi mumkin.
Mana, Crisis Center'ga marshrutlaydigan "hash URL":

```text
localhost:3002/src/#/crisis-center
```

Router ikkala uslubni ham ikkita `LocationStrategy` provider'i bilan qoʻllab-quvvatlaydi:

| Provider'lar           | Tafsilotlar                                   |
| :--------------------- | :-------------------------------------------- |
| `PathLocationStrategy` | Sukut boʻyicha "HTML5 pushState" uslubi.      |
| `HashLocationStrategy` | "Hash URL" uslubi.                            |

`RouterModule.forRoot()` funksiyasi `LocationStrategy` ni `PathLocationStrategy` ga oʻrnatadi, bu uni sukut boʻyicha strategiya qiladi.
Shuningdek, bootstrap jarayonida qayta aniqlash (override) orqali `HashLocationStrategy` ga oʻtish imkoniyatiga ham egasiz.

HELPFUL: Provider'lar va bootstrap jarayoni haqida koʻproq maʼlumot uchun [Bogʻliqliklarni inyeksiya qilish](guide/di/defining-dependency-providers) boʻlimiga qarang.
