# Strukturaviy direktivalar

Strukturaviy direktivalar — bu `<ng-template>` elementiga qoʻllanadigan va oʻsha `<ng-template>` mazmunini shartli yoki takroriy render qiladigan direktivalar.

Kundalik shartli va takroriy render qilish uchun Angular'ning oʻrnatilgan [boshqaruv oqimi bloklaridan](guide/templates/control-flow) (`@if`, `@for` va `@switch`) foydalaning. Strukturaviy direktivani boshqaruv oqimi qamrab olmaydigan qayta ishlatiladigan render xatti-harakati kerak boʻlganda yozing, masalan, kontentni ruxsat tekshiruvi orqasiga yashirish yoki shablonni tashqi manbadan olingan maʼlumotlar bilan taʼminlash.

## Misol holat {#example-use-case}

Bu qoʻllanma davomida `SelectDirective` deb nomlangan direktiva misol sifatida ishlatiladi. Direktiva berilgan maʼlumot manbasidan maʼlumotlarni oladi va maʼlumotlar tayyor boʻlganda oʻz shablonini render qiladi. U SQL'dagi `SELECT` kalit soʻzi sharafiga nomlangan va `[select]` atribut selektori bilan moslanadi.

`SelectDirective` ishlatiladigan maʼlumot manbasini koʻrsatuvchi `selectFrom` nomli input'ga ega. Bu input'dagi `select` prefiksi [qisqartirilgan sintaksis](#structural-directive-shorthand) uchun muhim. Direktiva oʻz `<ng-template>`'ini tanlangan maʼlumotlarni taqdim etuvchi shablon konteksti bilan yaratadi.

Bu direktivani bevosita `<ng-template>`'da ishlatish quyidagicha koʻrinadi:

```angular-html
<ng-template select let-data [selectFrom]="source">
  <p>The data is: {{ data }}</p>
</ng-template>
```

Strukturaviy direktiva maʼlumotlar tayyor boʻlishini kutib, soʻngra oʻz `<ng-template>`'ini render qilishi mumkin.

HELPFUL: Angular'ning `<ng-template>` elementi sukut boʻyicha hech narsa render qilmaydigan shablonni aniqlaydi. Agar elementlarni strukturaviy direktiva qoʻllamasdan `<ng-template>` ichiga olsangiz, bu elementlar render qilinmaydi.

Koʻproq maʼlumot uchun [ng-template API](api/core/ng-template) hujjatlariga qarang.

## Strukturaviy direktivaning qisqartirilgan sintaksisi {#structural-directive-shorthand}

Angular strukturaviy direktivalar uchun `<ng-template>` elementini aniq yozish zaruratidan xalos qiluvchi qisqartirilgan sintaksisni qoʻllab-quvvatlaydi.

Strukturaviy direktivalarni direktiva atribut selektori oldiga yulduzcha (`*`) qoʻyish orqali bevosita elementga qoʻllash mumkin, masalan, `*select`. Angular strukturaviy direktiva oldidagi yulduzchani direktivani joylashtiruvchi va elementni hamda uning avlodlarini oʻrab turuvchi `<ng-template>`'ga aylantiradi.

Buni `SelectDirective` bilan quyidagicha ishlatishingiz mumkin:

```angular-html
<p *select="let data; from: source">The data is: {{ data }}</p>
```

Bu misol baʼzan _mikrosintaksis_ deb ham ataladigan strukturaviy direktivaning qisqartirilgan sintaksisi qanchalik moslashuvchan ekanini koʻrsatadi.

Shu tarzda ishlatilganda `<ng-template>`'ga faqat strukturaviy direktiva va uning bogʻlashlari qoʻllanadi. `<p>` tegidagi boshqa har qanday atributlar yoki bogʻlashlar oʻz joyida qoladi. Masalan, bu ikki shakl bir-biriga ekvivalent:

```angular-html
<!-- Shorthand syntax: -->
<p class="data-view" *select="let data; from: source">The data is: {{ data }}</p>

<!-- Long-form syntax: -->
<ng-template select let-data [selectFrom]="source">
  <p class="data-view">The data is: {{ data }}</p>
</ng-template>
```

Qisqartirilgan sintaksis bir qator qoidalar orqali yoyiladi. Toʻliqroq [grammatika](#structural-directive-syntax-reference) quyida aniqlangan, lekin yuqoridagi misolda bu oʻzgartirishni quyidagicha tushuntirish mumkin:

`*select` ifodasining birinchi qismi — `let data`, u `data` shablon oʻzgaruvchisini eʼlon qiladi. Undan keyin tayinlash kelmagani uchun shablon oʻzgaruvchisi shablon kontekstining `$implicit` xususiyatiga bogʻlanadi.

Sintaksisning ikkinchi qismi — kalit-ifoda juftligi, `from source`. `from` — bogʻlash kaliti, `source` esa odatiy shablon ifodasi. Bogʻlash kalitlari PascalCase koʻrinishiga oʻtkazilib, oldiga strukturaviy direktiva selektori qoʻshilishi orqali xususiyatlarga moslanadi. `from` kaliti `selectFrom`'ga moslanadi, u esa `source` ifodasiga bogʻlanadi. Shu sababli koʻp strukturaviy direktivalarning input'lari strukturaviy direktiva selektori bilan prefikslangan boʻladi.

## Har bir elementga bitta strukturaviy direktiva {#one-structural-directive-per-element}

Qisqartirilgan sintaksisdan foydalanganda har bir elementga faqat bitta strukturaviy direktiva qoʻllashingiz mumkin. Buning sababi — direktiva yoyiladigan `<ng-template>` elementi faqat bitta. Bir nechta direktiva bir nechta ichma-ich `<ng-template>` talab qilardi va qaysi direktiva birinchi boʻlishi kerakligi noaniq boʻlardi. Bir xil jismoniy DOM elementi yoki komponenti atrofida bir nechta strukturaviy direktiva qoʻllash kerak boʻlganda oʻram qatlamlarini yaratish uchun `<ng-container>`'dan foydalanish mumkin, bu foydalanuvchiga ichma-ich tuzilmani oʻzi aniqlash imkonini beradi.

## Strukturaviy direktiva yaratish {#creating-a-structural-directive}

Strukturaviy direktiva — bu ikkita bogʻliqlikni inyeksiya qiluvchi direktiva klassi:

- [`TemplateRef`](api/core/TemplateRef) direktivaga u qoʻllangan `<ng-template>` mazmuniga kirish imkonini beradi.
- [`ViewContainerRef`](api/core/ViewContainerRef) direktiva oʻsha shablonni render qilishi mumkin boʻlgan DOM'dagi joyni ifodalaydi.

Direktiva render qilishni view konteynerida shablondan ichki (embedded) view'lar yaratish yoki yaratmaslik orqali boshqaradi. Toʻliq `SelectDirective` quyidagicha koʻrinadi:

```ts
import {Directive, TemplateRef, ViewContainerRef, inject, input} from '@angular/core';

export interface DataSource<T> {
  load(): Promise<T>;
}

@Directive({
  selector: '[select]',
})
export class SelectDirective {
  private templateRef = inject(TemplateRef);
  private viewContainerRef = inject(ViewContainerRef);

  selectFrom = input.required<DataSource<unknown>>();

  async ngOnInit() {
    const data = await this.selectFrom().load();
    this.viewContainerRef.createEmbeddedView(this.templateRef, {
      // Create the embedded view with a context object that contains
      // the data via the key `$implicit`.
      $implicit: data,
    });
  }
}
```

`selectFrom` input'i direktiva maʼlumot oʻqiydigan manbani koʻrsatadi. U [`input.required()`](guide/components/inputs#required-inputs)'dan foydalanadi, chunki direktiva maʼlumot manbasisiz hech qanday foydali ish qila olmaydi.

Angular direktivani ishga tushirganda u maʼlumotlarni yuklaydi va soʻngra `createEmbeddedView()`'ni chaqirib shablonni render qiladi. Ikkinchi argument — shablonning _kontekst obyekti_: shablon `let` eʼlonlari orqali bogʻlanishi mumkin boʻlgan qiymatlar. Maʼlumotlarni `$implicit` kalitiga tayinlash uni `let-data` (yoki qisqartirilgan sintaksisda `let data`) qabul qiladigan sukut boʻyicha qiymatga aylantiradi.

NOTE: Bu misol oʻz shablonini bir marta, direktiva ishga tushganda render qiladi. Bogʻlangan maʼlumot manbasi oʻzgarganda u qayta render qilinmaydi.

Direktiva ishlagach, [shablon turlarini tekshirishni qoʻllab-quvvatlashni qoʻshishni](#typing-the-directives-context) koʻrib chiqing.

HELPFUL: [`ng generate directive`](tools/cli/schematics) CLI buyrugʻi direktivani uning test fayli bilan birga yaratib beradi.

## Strukturaviy direktiva sintaksisi boʻyicha maʼlumotnoma {#structural-directive-syntax-reference}

Oʻz strukturaviy direktivalaringizni yozganda quyidagi sintaksisdan foydalaning:

```ts {hideCopy}
_: prefix = "( :let | :expression ) (';' | ',')? ( :let | :as | :keyExp )_";
```

Quyidagi naqshlar strukturaviy direktiva grammatikasining har bir qismini tasvirlaydi:

```ts
as = :export "as" :local ";"?
keyExp = :key ":"? :expression ("as" :local)? ";"?
let = "let" :local "=" :export ";"?
```

| Kalit soʻz   | Tafsilotlar                                             |
| :----------- | :------------------------------------------------------ |
| `prefix`     | HTML atribut kaliti                                     |
| `key`        | HTML atribut kaliti                                     |
| `local`      | Shablonda ishlatiladigan lokal oʻzgaruvchi nomi        |
| `export`     | Direktiva tomonidan berilgan nom ostida eksport qilingan qiymat |
| `expression` | Standart Angular ifodasi                                |

### Angular qisqartirilgan sintaksisni qanday oʻgiradi {#how-angular-translates-shorthand}

Angular strukturaviy direktivaning qisqartirilgan sintaksisini odatiy bogʻlash sintaksisiga quyidagicha oʻgiradi:

| Qisqartirilgan shakl              | Oʻgirilgan shakl                                                  |
| :-------------------------------- | :---------------------------------------------------------------- |
| `prefix` va yalangʻoch `expression` | `[prefix]="expression"`                                          |
| `keyExp`                          | `[prefixKey]="expression"` (`key` oldiga `prefix` qoʻshiladi)      |
| `let local`                       | `let-local="export"`                                              |

### Qisqartirilgan sintaksis misollari {#shorthand-examples}

Quyidagi jadvalda qisqartirilgan sintaksis misollari keltirilgan:

| Qisqartirilgan shakl                                                  | Angular sintaksisni qanday talqin qiladi                                                                      |
| :-------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------ |
| `*myDir="let item of [1,2,3]"`                                        | `<ng-template myDir let-item [myDirOf]="[1, 2, 3]">`                                                          |
| `*myDir="let item of [1,2,3] as items; trackBy: myTrack; index as i"` | `<ng-template myDir let-item [myDirOf]="[1,2,3]" let-items="myDirOf" [myDirTrackBy]="myTrack" let-i="index">` |
| `*ngComponentOutlet="componentClass"`                                 | `<ng-template [ngComponentOutlet]="componentClass">`                                                          |
| `*ngComponentOutlet="componentClass; inputs: myInputs"`               | `<ng-template [ngComponentOutlet]="componentClass" [ngComponentOutletInputs]="myInputs">`                     |
| `*myDir="exp as value"`                                               | `<ng-template [myDir]="exp" let-value="myDir">`                                                               |

## Maxsus direktivalar uchun shablon turlarini tekshirishni yaxshilash {#improving-template-type-checking-for-custom-directives}

Direktiva taʼrifiga shablon himoyachilarini (template guard) qoʻshish orqali maxsus direktivalar uchun shablon turlarini tekshirishni yaxshilashingiz mumkin.
Bu himoyachilar Angular shablon turlarini tekshiruvchisiga kompilyatsiya vaqtida shablondagi xatolarni topishga yordam beradi, bu esa ish vaqtidagi xatolarning oldini olishi mumkin.
Himoyachilarning ikki xil turi mavjud:

- `ngTemplateGuard_(input)` muayyan input turiga asoslanib input ifodasi qanday toraytirilishini boshqarish imkonini beradi.
- `ngTemplateContextGuard` direktivaning oʻz turiga asoslanib, shablon uchun kontekst obyektining turini aniqlashda ishlatiladi.

Bu boʻlimda himoyachilarning ikkala turi uchun ham misollar keltirilgan.
Koʻproq maʼlumot uchun [Shablon turlarini tekshirish](tools/cli/template-typecheck 'Template type-checking guide') boʻlimiga qarang.

### Shablon himoyachilari bilan turlarni toraytirish {#type-narrowing-with-template-guards}

Shablondagi strukturaviy direktiva oʻsha shablon ish vaqtida render qilinishini boshqaradi. Baʼzi strukturaviy direktivalar input ifodasining turiga asoslanib turni toraytirishni amalga oshirmoqchi boʻladi.

Input himoyachilari bilan ikki xil toraytirish mumkin:

- Input ifodasini TypeScript tur tasdiqlash (type assertion) funksiyasiga asoslanib toraytirish.
- Input ifodasini uning truthy ekaniga asoslanib toraytirish.

Input ifodasini tur tasdiqlash funksiyasini aniqlash orqali toraytirish uchun:

```ts
// This directive only renders its template if the actor is a user.
// You want to assert that within the template, the type of the `actor`
// expression is narrowed to `User`.
@Directive(...)
class ActorIsUser {
  actor = input<User | Robot>();

  static ngTemplateGuard_actor(dir: ActorIsUser, expr: User | Robot): expr is User {
    // The return statement is unnecessary in practice, but included to
    // prevent TypeScript errors.
    return true;
  }
}
```

Turlarni tekshirish shablon ichida xuddi `ngTemplateGuard_actor` input'ga bogʻlangan ifodaga nisbatan tasdiqlangandek ishlaydi.

Baʼzi direktivalar oʻz shablonlarini faqat input truthy boʻlganda render qiladi. Truthy ekanlikning toʻliq semantikasini tur tasdiqlash funksiyasida ifodalash mumkin emas, shuning uchun uning oʻrniga shablon turlarini tekshiruvchisiga bogʻlash ifodasining oʻzi himoyachi sifatida ishlatilishi kerakligini bildirish uchun `'binding'` literal turidan foydalanish mumkin:

```ts
@Directive(...)
class CustomIf {
  condition = input.required<boolean>();

  static ngTemplateGuard_condition: 'binding';
}
```

Shablon turlarini tekshiruvchisi `condition`'ga bogʻlangan ifoda shablon ichida truthy deb tasdiqlangandek ishlaydi.

### Direktiva kontekstiga tur berish {#typing-the-directives-context}

Agar strukturaviy direktivangiz yaratilgan shablonga kontekst taqdim etsa, statik `ngTemplateContextGuard` tur tasdiqlash funksiyasini taqdim etish orqali unga shablon ichida toʻgʻri tur berishingiz mumkin. Bu funksiya kontekst turini aniqlash uchun direktiva turidan foydalanishi mumkin, bu direktiva turi generik boʻlganda foydalidir.

Yuqorida tasvirlangan `SelectDirective` uchun maʼlumot manbasi generik boʻlsa ham, maʼlumot turini toʻgʻri koʻrsatish uchun `ngTemplateContextGuard`'ni amalga oshirishingiz mumkin.

```ts
// Declare an interface for the template context:
export interface SelectTemplateContext<T> {
  $implicit: T;
}

@Directive(...)
export class SelectDirective<T> {
  // The directive's generic type `T` will be inferred from the `DataSource` type
  // passed to the input.
  selectFrom = input.required<DataSource<T>>();

  // Narrow the type of the context using the generic type of the directive.
  static ngTemplateContextGuard<T>(dir: SelectDirective<T>, ctx: any): ctx is SelectTemplateContext<T> {
    // As before the guard body is not used at runtime, and included only to avoid
    // TypeScript errors.
    return true;
  }
}
```

## Keyingi qadamlar {#whats-next}

<docs-pill-row>
  <docs-pill href="guide/directives/directive-composition-api" title="Direktivalar kompozitsiyasi API'si"/>
  <docs-pill href="guide/templates/ng-template" title="ng-template"/>
  <docs-pill href="guide/templates/control-flow" title="Boshqaruv oqimi"/>
</docs-pill-row>
