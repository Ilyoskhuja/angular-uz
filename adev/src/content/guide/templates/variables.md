# Shablonlardagi oʻzgaruvchilar

Angular shablonlarida oʻzgaruvchi eʼlon qilishning ikki turi mavjud: lokal shablon oʻzgaruvchilari (local template variables) va shablon referens oʻzgaruvchilari (template reference variables).

HELPFUL: Bu qoʻllanmada "shablon" deganda butun HTML shablon fayli nazarda tutilmaydi. Bu faqat fayl ichidagi maʼlum bir shablon konstruksiyasi yoki ifodani anglatadi.

## `@let` bilan lokal shablon oʻzgaruvchilari {#local-template-variables-with-let}

Angular'ning `@let` sintaksisi [JavaScript'dagi `let` sintaksisiga](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/let) oʻxshab, lokal oʻzgaruvchi aniqlash va undan shablon boʻylab qayta foydalanish imkonini beradi.

### `@let`'dan foydalanish {#using-let}

Qiymati shablon ifodasining natijasiga asoslangan oʻzgaruvchini eʼlon qilish uchun `@let`'dan foydalaning. Angular [bogʻlashlar (bindings)](/guide/templates/binding) kabi oʻzgaruvchining qiymatini berilgan ifoda bilan avtomatik ravishda yangilangan holda saqlaydi.

```angular-html
@let name = user.name;
@let greeting = 'Hello, ' + name;
@let data = data$ | async;
@let pi = 3.14159;
@let coordinates = {x: 50, y: 100};
@let longExpression =
  'Lorem ipsum dolor sit amet, consectetur adipiscing elit ' +
  'sed do eiusmod tempor incididunt ut labore et dolore magna ' +
  'Ut enim ad minim veniam...';
```

Har bir `@let` bloki roppa-rosa bitta oʻzgaruvchi eʼlon qilishi mumkin. Bitta blokda vergul orqali bir nechta oʻzgaruvchi eʼlon qila olmaysiz.

### `@let` qiymatiga murojaat qilish {#referencing-the-value-of-let}

Oʻzgaruvchini `@let` bilan eʼlon qilganingizdan soʻng, undan oʻsha shablonda qayta foydalanishingiz mumkin:

```angular-html
@let user = user$ | async;

@if (user) {
  <h1>Hello, {{ user.name }}</h1>
  <user-avatar [photo]="user.photo" />

  <ul>
    @for (snack of user.favoriteSnacks; track snack.id) {
      <li>{{ snack.name }}</li>
    }
  </ul>

  <button (click)="update(user)">Update profile</button>
}
```

### Qayta tayinlash imkoniyati {#assignability}

`@let` va JavaScript'dagi `let` oʻrtasidagi asosiy farq shundaki, `@let` eʼlon qilingandan soʻng qayta tayinlanishi mumkin emas. Biroq Angular oʻzgaruvchining qiymatini berilgan ifoda bilan avtomatik ravishda yangilangan holda saqlaydi.

```angular-html
@let value = 1;

<!-- Invalid - This does not work! -->
<button (click)="value = value + 1">Increment the value</button>
```

### Oʻzgaruvchi koʻlami {#variable-scope}

`@let` eʼlonlari joriy view va uning avlodlari koʻlami (scope) bilan cheklangan. Angular komponent chegaralarida va shablon dinamik kontentni oʻz ichiga olishi mumkin boʻlgan har bir joyda, masalan, boshqaruv oqimi bloklari, `@defer` bloklari yoki strukturaviy direktivalarda yangi view yaratadi.

`@let` eʼlonlari yuqoriga koʻtarilmagani (hoisted emas) uchun ularga ota view'lar yoki qoʻshni view'lardan murojaat qilish **mumkin emas**:

```angular-html
@let topLevel = value;

<div>
  @let insideDiv = value;
</div>

<!-- Valid -->
{{ topLevel }}
<!-- Valid -->
{{ insideDiv }}

@if (condition) {
  <!-- Valid -->
  {{ topLevel + insideDiv }}

  @let nested = value;

  @if (condition) {
    <!-- Valid -->
    {{ topLevel + insideDiv + nested }}
  }
}

<!-- Error, not hoisted from @if -->
{{ nested }}
```

### Toʻliq sintaksis {#full-syntax}

`@let` sintaksisi rasmiy ravishda quyidagicha aniqlanadi:

- `@let` kalit soʻzi.
- Keyin bir yoki bir nechta boʻsh joy belgisi (yangi qator belgilaridan tashqari).
- Keyin yaroqli JavaScript nomi va nol yoki undan koʻp boʻsh joy belgisi.
- Keyin = belgisi va nol yoki undan koʻp boʻsh joy belgisi.
- Keyin koʻp qatorli boʻlishi mumkin boʻlgan Angular ifodasi.
- `;` belgisi bilan yakunlanadi.

## Shablon referens oʻzgaruvchilari {#template-reference-variables}

Shablon referens oʻzgaruvchilari shablondagi elementdan olingan qiymatga murojaat qiluvchi oʻzgaruvchini eʼlon qilish imkonini beradi.

Shablon referens oʻzgaruvchisi quyidagilarga murojaat qilishi mumkin:

- shablon ichidagi DOM elementi ([maxsus elementlar (custom elements)](https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_custom_elements) ham kiradi)
- Angular komponenti yoki direktivasi
- [ng-template](/api/core/ng-template)'dan olingan [TemplateRef](/api/core/TemplateRef)

Shablon referens oʻzgaruvchilaridan shablonning bir qismidagi maʼlumotni oʻsha shablonning boshqa qismida oʻqish uchun foydalanishingiz mumkin.

### Shablon referens oʻzgaruvchisini eʼlon qilish {#declaring-a-template-reference-variable}

Shablondagi elementda oʻzgaruvchini eʼlon qilish uchun unga xesh belgisi (`#`) bilan boshlanib, undan keyin oʻzgaruvchi nomi keladigan atribut qoʻshing.

```angular-html
<!-- Create a template reference variable named "taskInput", referring to the HTMLInputElement. -->
<input #taskInput placeholder="Enter task name" />
```

### Shablon referens oʻzgaruvchilariga qiymat tayinlash {#assigning-values-to-template-reference-variables}

Angular shablon oʻzgaruvchilariga qiymatni oʻzgaruvchi eʼlon qilingan elementga qarab tayinlaydi.

Agar oʻzgaruvchini Angular komponentida eʼlon qilsangiz, oʻzgaruvchi komponent nusxasiga (instance) murojaat qiladi.

```angular-html
<!-- The `startDate` variable is assigned the instance of `MyDatepicker`. -->
<my-datepicker #startDate />
```

Agar oʻzgaruvchini `<ng-template>` elementida eʼlon qilsangiz, oʻzgaruvchi shablonni ifodalovchi TemplateRef nusxasiga murojaat qiladi. Koʻproq maʼlumot uchun [Strukturaviy direktivalar](/guide/directives/structural-directives) qoʻllanmasidagi [Angular yulduzcha (\*) sintaksisidan qanday foydalanadi](/guide/directives/structural-directives#structural-directive-shorthand) boʻlimiga qarang.

```angular-html
<!-- The `myFragment` variable is assigned the `TemplateRef` instance corresponding to this template fragment. -->
<ng-template #myFragment>
  <p>This is a template fragment</p>
</ng-template>
```

Agar oʻzgaruvchini boshqa har qanday koʻrsatiladigan elementda eʼlon qilsangiz, oʻzgaruvchi `HTMLElement` nusxasiga murojaat qiladi.

```angular-html
<!-- The "taskInput" variable refers to the HTMLInputElement instance. -->
<input #taskInput placeholder="Enter task name" />
```

#### Angular direktivasiga referens tayinlash {#assigning-a-reference-to-an-angular-directive}

Angular direktivalari shablonda direktivaga murojaat qilish uchun ishlatiladigan nomni belgilovchi `exportAs` xususiyatiga ega boʻlishi mumkin:

```angular-ts
@Directive({
  selector: '[dropZone]',
  exportAs: 'dropZone',
})
export class DropZone {
  /* ... */
}
```

Elementda shablon oʻzgaruvchisini eʼlon qilganingizda, shu `exportAs` nomini koʻrsatib, oʻzgaruvchiga direktiva nusxasini tayinlashingiz mumkin:

```angular-html
<!-- The `firstZone` variable refers to the `DropZone` directive instance. -->
<section dropZone #firstZone="dropZone">...</section>
```

`exportAs` nomini koʻrsatmagan direktivaga murojaat qila olmaysiz.

### Shablon referens oʻzgaruvchilaridan soʻrovlar bilan foydalanish {#using-template-reference-variables-with-queries}

Shablon oʻzgaruvchilaridan oʻsha shablonning boshqa qismidagi qiymatlarni oʻqish uchun foydalanishdan tashqari, oʻzgaruvchi eʼlon qilishning bu usulidan [komponent va direktiva soʻrovlari](/guide/components/queries) uchun elementni "belgilash"da ham foydalanishingiz mumkin.

Shablondagi maʼlum bir elementni soʻrov orqali olmoqchi boʻlsangiz, oʻsha elementda shablon oʻzgaruvchisini eʼlon qilib, soʻngra elementni oʻzgaruvchi nomi boʻyicha soʻrashingiz mumkin.

```angular-html
<input #description value="Original description" />
```

```angular-ts
@Component({
  /* ... */,
  template: `<input #description value="Original description">`,
})
export class AppComponent {
  // Query for the input element based on the template variable name.
  @ViewChild('description') input: ElementRef | undefined;
}
```

Soʻrovlar haqida koʻproq maʼlumot uchun [Bola elementlarga soʻrovlar orqali murojaat qilish](/guide/components/queries) boʻlimiga qarang.

### Shablon oʻzgaruvchisi koʻlami {#template-variable-scope}

JavaScript yoki TypeScript kodidagi oʻzgaruvchilar kabi, shablon oʻzgaruvchilari ham ularni eʼlon qilgan shablon koʻlami bilan cheklangan.

Shunga oʻxshab, `@if` va `@for` kabi [boshqaruv oqimi bloklari](guide/templates/control-flow), [strukturaviy direktivalar](guide/directives/structural-directives) va `<ng-template>` eʼlonlari yangi ichki shablon koʻlamini yaratadi — JavaScript'dagi `if` va `for` kabi boshqaruv oqimi operatorlari yangi leksik koʻlam yaratgani kabi. Bu ichki shablonlardan biridagi shablon oʻzgaruvchilariga uning chegaralaridan tashqaridan murojaat qila olmaysiz.

HELPFUL: Runtime qiymati bashorat qilinadigan boʻlib qolishi uchun oʻzgaruvchini shablonda faqat bir marta aniqlang.

#### Ichki shablonda murojaat qilish {#accessing-in-a-nested-template}

Ichki shablon tashqi shablon aniqlagan shablon oʻzgaruvchilariga murojaat qila oladi.

Quyidagi misolda `<input>`'dagi matnni oʻzgartirish `<span>`'dagi qiymatni oʻzgartiradi, chunki Angular oʻzgarishlarni `ref1` shablon oʻzgaruvchisi orqali darhol yangilaydi.

```angular-html
<input #ref1 type="text" [(ngModel)]="firstExample" />

@if (true) {
  <span>Value: {{ ref1.value }}</span>
}
```

Bu holda `@if` bloki ota koʻlamdagi `ref1` oʻzgaruvchisini oʻz ichiga olgan yangi shablon koʻlamini yaratadi.

Biroq bola koʻlamdagi shablon oʻzgaruvchisiga ota shablondan murojaat qilish ishlamaydi:

```angular-html {avoid}
@if (true) {
  <input #ref2 type="text" [(ngModel)]="secondExample" />
}

<span>Value: {{ ref2?.value }}</span>
```

Bu yerda `ref2` `@if` yaratgan bola koʻlamda eʼlon qilingan va ota shablondan unga murojaat qilish mumkin emas.
