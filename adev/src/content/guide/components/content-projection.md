# ng-content bilan kontent proyeksiyasi

TIP: Bu qoʻllanma siz [Asoslar qoʻllanmasini](essentials) allaqachon oʻqigansiz deb hisoblaydi. Angular'da yangi boʻlsangiz, avval oʻshani oʻqing.

Koʻpincha turli xil kontent uchun konteyner vazifasini bajaruvchi komponentlar yaratish kerak boʻladi. Masalan, maxsus karta (card) komponentini yaratmoqchi boʻlishingiz mumkin:

```angular-ts
@Component({
  selector: 'custom-card',
  template: '<div class="card-shadow"> <!-- card content goes here --> </div>',
})
export class CustomCard {
  /* ... */
}
```

**Kontent qayerga joylashishi kerakligini belgilash uchun `<ng-content>` elementidan toʻldiruvchi (placeholder) sifatida foydalanishingiz mumkin**:

```angular-ts
@Component({
  selector: 'custom-card',
  template: '<div class="card-shadow"> <ng-content/> </div>',
})
export class CustomCard {
  /* ... */
}
```

TIP: `<ng-content>` [oʻrnatilgan `<slot>` elementiga](https://developer.mozilla.org/docs/Web/HTML/Element/slot) oʻxshash ishlaydi, lekin Angular'ga xos baʼzi qoʻshimcha imkoniyatlarga ega.

`<ng-content>` ega komponentdan foydalanganingizda komponent host elementining har qanday bolalari oʻsha `<ng-content>` joylashgan oʻrinda render qilinadi, yaʼni **proyeksiya qilinadi**:

```angular-ts
// Component source
@Component({
  selector: 'custom-card',
  template: `
    <div class="card-shadow">
      <ng-content />
    </div>
  `,
})
export class CustomCard {
  /* ... */
}
```

```angular-html
<!-- Using the component -->
<custom-card>
  <p>This is the projected content</p>
</custom-card>
```

```angular-html
<!-- The rendered DOM -->
<custom-card>
  <div class="card-shadow">
    <p>This is the projected content</p>
  </div>
</custom-card>
```

Angular komponentga shu tarzda uzatilgan har qanday bolalarni oʻsha komponentning **kontenti** deb ataydi. Bu komponentning **view**'idan farq qiladi — view komponent shablonida aniqlangan elementlarni anglatadi.

**`<ng-content>` elementi komponent ham, DOM elementi ham emas**. Buning oʻrniga, u Angular'ga kontentni qayerda render qilish kerakligini aytuvchi maxsus toʻldiruvchidir. Angular kompilyatori barcha `<ng-content>` elementlarini build vaqtida qayta ishlaydi. `<ng-content>`'ni ish vaqtida (run time) qoʻshish, olib tashlash yoki oʻzgartirish mumkin emas. `<ng-content>`'ga direktivalar, stillar yoki ixtiyoriy atributlar qoʻshish mumkin emas.

IMPORTANT: `<ng-content>`'ni `@if`, `@for` yoki `@switch` bilan shartli ravishda qoʻshmasligingiz kerak. Angular `<ng-content>` toʻldiruvchisiga render qilinadigan kontent uchun DOM tugunlarini doimo yaratadi va nusxalaydi (instantiate), hatto oʻsha `<ng-content>` toʻldiruvchisi yashirilgan boʻlsa ham. Komponent kontentini shartli render qilish uchun [Shablon fragmentlari](api/core/ng-template) boʻlimiga qarang.

## Bir nechta kontent toʻldiruvchilari {#multiple-content-placeholders}

Angular CSS selektoriga asoslanib bir nechta turli elementlarni turli `<ng-content>` toʻldiruvchilariga proyeksiya qilishni qoʻllab-quvvatlaydi. Yuqoridagi karta misolini kengaytirib, `select` atributi yordamida karta sarlavhasi va karta tanasi uchun ikkita toʻldiruvchi yaratishingiz mumkin:

```angular-ts
@Component({
  selector: 'card-title',
  template: `<ng-content>card-title</ng-content>`,
})
export class CardTitle {}

@Component({
  selector: 'card-body',
  template: `<ng-content>card-body</ng-content>`,
})
export class CardBody {}
```

```angular-ts
<!-- Component template -->
@Component({
  selector: 'custom-card',
  template: `
  <div class="card-shadow">
    <ng-content select="card-title" />
    <div class="card-divider"></div>
    <ng-content select="card-body" />
  </div>
  `,
})
export class CustomCard {}
```

```angular-ts
<!-- Using the component -->
@Component({
  selector: 'app-root',
  imports: [CustomCard, CardTitle, CardBody],
  template: `
    <custom-card>
      <card-title>Hello</card-title>
      <card-body>Welcome to the example</card-body>
    </custom-card>
`,
})
export class App {}
```

```angular-html
<!-- Rendered DOM -->
<custom-card>
  <div class="card-shadow">
    <card-title>Hello</card-title>
    <div class="card-divider"></div>
    <card-body>Welcome to the example</card-body>
  </div>
</custom-card>
```

`<ng-content>` toʻldiruvchisi [komponent selektorlari](guide/components/selectors) bilan bir xil CSS selektorlarini qoʻllab-quvvatlaydi.

Agar `select` atributiga ega bir yoki bir nechta `<ng-content>` toʻldiruvchisi va `select` atributisiz bitta `<ng-content>` toʻldiruvchisini qoʻshsangiz, ikkinchisi `select` atributiga mos kelmagan barcha elementlarni qamrab oladi:

```angular-html
<!-- Component template -->
<div class="card-shadow">
  <ng-content select="card-title" />
  <div class="card-divider"></div>
  <!-- capture anything except "card-title" -->
  <ng-content />
</div>
```

```angular-html
<!-- Using the component -->
<custom-card>
  <card-title>Hello</card-title>
  <img src="..." />
  <p>Welcome to the example</p>
</custom-card>
```

```angular-html
<!-- Rendered DOM -->
<custom-card>
  <div class="card-shadow">
    <card-title>Hello</card-title>
    <div class="card-divider"></div>
    <img src="..." />
    <p>Welcome to the example</p>
  </div>
</custom-card>
```

Agar komponentda `select` atributisiz `<ng-content>` toʻldiruvchisi boʻlmasa, komponent toʻldiruvchilaridan birortasiga mos kelmagan elementlar DOM'ga render qilinmaydi.

## Zaxira kontent {#fallback-content}

Agar komponentda mos keladigan bola kontent boʻlmasa, Angular komponentning `<ng-content>` toʻldiruvchisi uchun _zaxira kontentni_ (fallback content) koʻrsatishi mumkin. Zaxira kontentni `<ng-content>` elementining oʻziga bola kontent qoʻshish orqali belgilashingiz mumkin.

```angular-html
<!-- Component template -->
<div class="card-shadow">
  <ng-content select="card-title">Default Title</ng-content>
  <div class="card-divider"></div>
  <ng-content select="card-body">Default Body</ng-content>
</div>
```

```angular-html
<!-- Using the component -->
<custom-card>
  <card-title>Hello</card-title>
  <!-- No card-body provided -->
</custom-card>
```

```angular-html
<!-- Rendered DOM -->
<custom-card>
  <div class="card-shadow">
    <card-title>Hello</card-title>
    <div class="card-divider"></div>
    Default Body
  </div>
</custom-card>
```

## Proyeksiya uchun kontentga taxallus berish {#aliasing-content-for-projection}

Angular har qanday elementda CSS selektorini koʻrsatish imkonini beruvchi maxsus `ngProjectAs` atributini qoʻllab-quvvatlaydi. `ngProjectAs` atributiga ega element `<ng-content>` toʻldiruvchisiga moslik uchun tekshirilganda Angular elementning oʻzi oʻrniga `ngProjectAs` qiymati bilan solishtiradi:

```angular-html
<!-- Component template -->
<div class="card-shadow">
  <ng-content select="card-title" />
  <div class="card-divider"></div>
  <ng-content />
</div>
```

```angular-html
<!-- Using the component -->
<custom-card>
  <h3 ngProjectAs="card-title">Hello</h3>

  <p>Welcome to the example</p>
</custom-card>
```

```angular-html
<!-- Rendered DOM -->
<custom-card>
  <div class="card-shadow">
    <h3>Hello</h3>
    <div class="card-divider"></div>
    <p>Welcome to the example</p>
  </div>
</custom-card>
```

`ngProjectAs` faqat statik qiymatlarni qoʻllab-quvvatlaydi va uni dinamik ifodalarga bogʻlash mumkin emas.

## Eʼtiborga olish kerak boʻlgan jihatlar {#caveats}

### Proyeksiya qilingan kontent ota komponentning view'ida yashaydi {#projected-content-lives-in-the-parents-view}

Proyeksiya qilingan kontent qabul qiluvchi komponent ichida _render qilinsa_ ham, u hali ham uni eʼlon qilgan komponentga tegishli boʻlib qoladi. Angular uni ota komponent view'ining bir qismi sifatida kuzatadi, bu esa bilish foydali boʻlgan bir nechta yon taʼsirlarga olib keladi.

**Oʻzgarishlarni aniqlash:** Proyeksiya qilingan kontent _ota_ komponent oʻzgarishlarni aniqlashni bajarganda tekshiriladi. Agar qabul qiluvchi komponent `OnPush` ishlatsa, Angular oʻsha komponentning oʻz shablonini tekshirishni oʻtkazib yuborishi mumkin — lekin proyeksiya qilingan kontentni oʻtkazib yubormaydi, chunki u ota komponentga tegishli.

```angular-html
<!-- Parent template (default change detection) -->
<onpush-wrapper>
  <!-- Still checked on every parent cycle, OnPush doesn't help here -->
  <expensive-component />
</onpush-wrapper>
```

**Bogʻliqliklarni inyeksiya qilish:** Proyeksiya qilingan kontent oʻz bogʻliqliklarini qabul qiluvchi komponentning `viewProviders`'idan emas, ota komponentning injector'idan oladi. Batafsil maʼlumot uchun [Providers va viewProviders](guide/di/hierarchical-dependency-injection) boʻlimiga qarang.

### Baʼzi kutubxona komponentlari proyeksiya qilingan bolalarni qoʻllab-quvvatlamaydi {#some-library-components-dont-support-projected-children}

Ayrim komponentlar — menyular, tab'lar, roʻyxatlar — oʻz bolalarini topish va klaviatura orqali navigatsiya, fokusni boshqarish yoki ARIA atributlari kabi xatti-harakatlarni ulash uchun `ContentChildren`'dan foydalanadi. Ular oʻz bolalariga bevosita egalik qiladi degan taxmin bilan yozilgan, shuning uchun ularga tashqi kontentni proyeksiya qilish koʻpincha ishlashni nozik tarzda buzadi.

Masalan, `<mat-menu-item>` elementlarini qoʻshimcha qatlamga oʻrab, ularni `<mat-menu>` ichiga proyeksiya qilish klaviatura orqali navigatsiya va ekran oʻquvchisi (screen reader) qoʻllab-quvvatlashini sezdirmasdan buzishi mumkin. Soʻrov elementlarni hali ham topadi, lekin elementlar boshqa view kontekstidan kelganda ularni interaktiv qiladigan ichki sozlash toʻgʻri ishlamasligi mumkin.

Agar kutubxona komponenti oʻz bolalarining xatti-harakatini boshqarsa, kontent proyeksiyasiga murojaat qilishdan oldin uning hujjatlarini tekshiring — bu qoʻllab-quvvatlanmasligi mumkin.
