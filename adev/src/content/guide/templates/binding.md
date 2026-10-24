# Dinamik matn, xususiyat va atributlarni bogʻlash

Angular'da **bogʻlash (binding)** komponent shabloni va uning maʼlumotlari oʻrtasida dinamik aloqa yaratadi. Bu aloqa komponent maʼlumotlaridagi oʻzgarishlar render qilingan shablonni avtomatik yangilashini taʼminlaydi.

## Matn interpolyatsiyasi bilan dinamik matnni render qilish {#render-dynamic-text-with-text-interpolation}

Shablonlarda dinamik matnni ikkita jingalak qavs bilan bogʻlashingiz mumkin; bu Angular'ga ichidagi ifoda uchun u javobgar ekanini va uning toʻgʻri yangilanishini taʼminlashi kerakligini bildiradi. Bu **matn interpolyatsiyasi** deb ataladi.

```angular-ts
@Component({
  template: `
    <p>Your color preference is {{ theme }}.</p>
  `,
  ...
})
export class App {
  theme = 'dark';
}
```

Bu misolda, fragment sahifaga render qilinganda Angular `{{ theme }}`'ni `dark` bilan almashtiradi.

```angular-html
<!-- Rendered Output -->
<p>Your color preference is dark.</p>
```

Vaqt oʻtishi bilan oʻzgaradigan bogʻlashlar qiymatlarni [signallardan](/guide/signals) oʻqishi kerak. Angular shablonda oʻqilgan signallarni kuzatib boradi va bu signallarning qiymatlari oʻzgarganda render qilingan sahifani yangilaydi.

```angular-ts
@Component({
  template: `
    <!-- Does not necessarily update when `welcomeMessage` changes. -->
    <p>{{ welcomeMessage }}</p>

    <p>Your color preference is {{ theme() }}.</p> <!-- Always updates when the value of the `theme` signal changes. -->
  `
  ...
})
export class App {
  welcomeMessage = "Welcome, enjoy this app that we built for you";
  theme = signal('dark');
}
```

Batafsil maʼlumot uchun [Signallar qoʻllanmasiga](/guide/signals) qarang.

Mavzu (theme) misolini davom ettirsak, agar foydalanuvchi sahifa yuklangandan keyin `theme` signalini `'light'` qiymatiga yangilovchi tugmani bossa, sahifa shunga mos ravishda quyidagicha yangilanadi:

```angular-html
<!-- Rendered Output -->
<p>Your color preference is light.</p>
```

Matn interpolyatsiyasidan HTML'da odatda matn yozadigan har qanday joyda foydalanishingiz mumkin.

Barcha ifoda qiymatlari satrga (string) aylantiriladi. Obyektlar va massivlar qiymatning `toString` metodi yordamida aylantiriladi.

## Dinamik xususiyat va atributlarni bogʻlash {#binding-dynamic-properties-and-attributes}

Angular dinamik qiymatlarni obyekt xususiyatlari va HTML atributlariga kvadrat qavslar bilan bogʻlashni qoʻllab-quvvatlaydi.

HTML elementining DOM nusxasidagi, [komponent](/guide/components) nusxasidagi yoki [direktiva](/guide/directives) nusxasidagi xususiyatlarga bogʻlashingiz mumkin.

### Native element xususiyatlari {#native-element-properties}

Har bir HTML elementi oʻziga mos DOM koʻrinishiga ega. Masalan, har bir `<button>` HTML elementi DOM'da `HTMLButtonElement` nusxasiga mos keladi. Angular'da xususiyat bogʻlashlaridan (property binding) qiymatlarni toʻgʻridan-toʻgʻri elementning DOM koʻrinishiga oʻrnatish uchun foydalanasiz.

```angular-html
<!-- Bind the `disabled` property on the button element's DOM object -->
<button [disabled]="isFormValid()">Save</button>
```

Bu misolda `isFormValid` har safar oʻzgarganda Angular `HTMLButtonElement` nusxasining `disabled` xususiyatini avtomatik oʻrnatadi.

### Komponent va direktiva xususiyatlari {#component-and-directive-properties}

Element Angular komponenti boʻlsa, xuddi shu kvadrat qavs sintaksisi bilan xususiyat bogʻlashlaridan komponentning input xususiyatlarini oʻrnatish uchun foydalanishingiz mumkin.

```angular-html
<!-- Bind the `value` property on the `MyListbox` component instance. -->
<my-listbox [value]="mySelection()" />
```

Bu misolda `mySelection` har safar oʻzgarganda Angular `MyListbox` nusxasining `value` xususiyatini avtomatik oʻrnatadi.

Direktiva xususiyatlariga ham bogʻlashingiz mumkin.

```angular-html
<!-- Bind to the `ngSrc` property of the `NgOptimizedImage` directive  -->
<img [ngSrc]="profilePhotoUrl()" alt="The current user's profile photo" />
```

### Atributlar {#attributes}

SVG atributlari kabi mos DOM xususiyatiga ega boʻlmagan HTML atributlarini oʻrnatish kerak boʻlganda, shablondagi elementlarga atributlarni `attr.` prefiksi bilan bogʻlashingiz mumkin.

<!-- prettier-ignore -->
```angular-html
<!-- Bind the `role` attribute on the `<ul>` element to the component's `listRole` property. -->
<ul [attr.role]="listRole()">
```

Bu misolda `listRole` har safar oʻzgarganda Angular `setAttribute`'ni chaqirib, `<ul>` elementining `role` atributini avtomatik oʻrnatadi.

Agar atribut bogʻlashining qiymati `null` boʻlsa, Angular `removeAttribute`'ni chaqirib, atributni olib tashlaydi.

### Xususiyat va atributlarda matn interpolyatsiyasi {#text-interpolation-in-properties-and-attributes}

Xususiyat yoki atribut nomi atrofida kvadrat qavslar oʻrniga ikkita jingalak qavs sintaksisidan foydalanib, xususiyat va atributlarda ham matn interpolyatsiyasi sintaksisini ishlatishingiz mumkin. Bu sintaksis ishlatilganda Angular tayinlashni xususiyat bogʻlashi sifatida qabul qiladi.

```angular-html
<!-- Binds a value to the `alt` property of the image element's DOM object. -->
<img src="profile-photo.jpg" alt="Profile photo of {{ firstName() }}" />
```

## CSS klass va stil xususiyatlarini bogʻlash {#css-class-and-style-property-bindings}

Angular elementlarga CSS klasslari va CSS stil xususiyatlarini bogʻlash uchun qoʻshimcha imkoniyatlarni qoʻllab-quvvatlaydi.

### CSS klasslari {#css-classes}

Bogʻlangan qiymat [truthy yoki falsy](https://developer.mozilla.org/en-US/docs/Glossary/Truthy) boʻlishiga qarab elementga CSS klassini shartli qoʻshish yoki olib tashlash uchun CSS klass bogʻlashini yaratishingiz mumkin.

<!-- prettier-ignore -->
```angular-html
<!-- When `isExpanded` is truthy, add the `expanded` CSS class. -->
<ul [class.expanded]="isExpanded()">
```

Shuningdek, toʻgʻridan-toʻgʻri `class` xususiyatiga ham bogʻlashingiz mumkin. Angular uch turdagi qiymatni qabul qiladi:

| `class` qiymatining tavsifi                                                                                                                                       | TypeScript turi       |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| Boʻshliq bilan ajratilgan bir yoki bir nechta CSS klassini oʻz ichiga olgan satr                                                                                  | `string`              |
| CSS klass satrlaridan tashkil topgan massiv                                                                                                                       | `string[]`            |
| Har bir xususiyat nomi CSS klass nomi boʻlgan va har bir mos qiymat truthy boʻlishiga qarab shu klassning elementga qoʻllanishini belgilaydigan obyekt.           | `Record<string, any>` |

```angular-ts
@Component({
  template: `
    <ul [class]="listClasses"> ... </ul>
    <section [class]="sectionClasses()"> ... </section>
    <button [class]="buttonClasses()"> ... </button>
  `,
  ...
})
export class UserProfile {
  listClasses = 'full-width outlined';
  sectionClasses = signal(['expandable', 'elevated']);
  buttonClasses = signal({
    highlighted: true,
    embiggened: false,
  });
}
```

Yuqoridagi misol quyidagi DOM'ni render qiladi:

<!-- prettier-ignore -->
```angular-html
<ul class="full-width outlined"> ... </ul>
<section class="expandable elevated"> ... </section>
<button class="highlighted"> ... </button>
```

Angular yaroqli CSS klass nomi boʻlmagan har qanday satr qiymatlarini eʼtiborsiz qoldiradi.

Statik CSS klasslari, toʻgʻridan-toʻgʻri `class` bogʻlashi va alohida klasslarni bogʻlash birga ishlatilganda Angular render natijasida barcha klasslarni aqlli tarzda birlashtiradi.

```angular-ts
@Component({
  template: `<ul class="list" [class]="listType()" [class.expanded]="isExpanded()"> ...`,
  ...
})
export class Listbox {
  listType = signal('box');
  isExpanded = signal(true);
}
```

Yuqoridagi misolda Angular `ul` elementini uchala CSS klassi bilan render qiladi.

<!-- prettier-ignore -->
```angular-html
<ul class="list box expanded">
```

Angular render qilingan elementlardagi CSS klasslarining aniq tartibini kafolatlamaydi.

`class`'ni massiv yoki obyektga bogʻlaganda Angular oldingi qiymatni joriy qiymat bilan uchlik tenglik operatori (`===`) orqali solishtiradi. Angular yangilanishlarni qoʻllashi uchun bu qiymatlarni oʻzgartirganda yangi obyekt yoki massiv nusxasini yaratishingiz shart.

Agar elementda bir xil CSS klassi uchun bir nechta bogʻlash boʻlsa, Angular toʻqnashuvlarni oʻzining stil ustuvorligi tartibiga koʻra hal qiladi.

NOTE: Klass bogʻlashlari bitta kalitda boʻshliq bilan ajratilgan klass nomlarini qoʻllab-quvvatlamaydi. Shuningdek, bogʻlashning havolasi (reference) oʻzgarmay qolgani uchun ular obyektlardagi mutatsiyalarni ham qoʻllab-quvvatlamaydi. Agar sizga bulardan biri kerak boʻlsa, [ngClass](/api/common/NgClass) direktivasidan foydalaning.

### CSS stil xususiyatlari {#css-style-properties}

Shuningdek, elementdagi CSS stil xususiyatlariga toʻgʻridan-toʻgʻri bogʻlashingiz mumkin.

<!-- prettier-ignore -->
```angular-html
<!-- Set the CSS `display` property based on the `isExpanded` property. -->
<section [style.display]="isExpanded() ? 'block' : 'none'">
```

Oʻlchov birligini qabul qiladigan CSS xususiyatlari uchun birlikni ham qoʻshimcha koʻrsatishingiz mumkin.

<!-- prettier-ignore -->
```angular-html
<!-- Set the CSS `height` property to a pixel value based on the `sectionHeightInPixels` property. -->
<section [style.height.px]="sectionHeightInPixels()">
```

Bir bogʻlashda bir nechta stil qiymatini ham oʻrnatishingiz mumkin. Angular quyidagi turdagi qiymatlarni qabul qiladi:

| `style` qiymatining tavsifi                                                                                               | TypeScript turi       |
| ------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| Nol yoki undan koʻp CSS eʼlonini oʻz ichiga olgan satr, masalan `"display: flex; margin: 8px"`.                            | `string`              |
| Har bir xususiyat nomi CSS xususiyati nomi boʻlgan va har bir mos qiymat shu CSS xususiyatining qiymati boʻlgan obyekt.    | `Record<string, any>` |

```angular-ts
@Component({
  template: `
    <ul [style]="listStyles()"> ... </ul>
    <section [style]="sectionStyles()"> ... </section>
  `,
  ...
})
export class UserProfile {
  listStyles = signal('display: flex; padding: 8px');
  sectionStyles = signal({
    border: '1px solid black',
    'font-weight': 'bold',
  });
}
```

Yuqoridagi misol quyidagi DOM'ni render qiladi.

<!-- prettier-ignore -->
```angular-html
<ul style="display: flex; padding: 8px"> ... </ul>
<section style="border: 1px solid black; font-weight: bold"> ... </section>
```

`style`'ni obyektga bogʻlaganda Angular oldingi qiymatni joriy qiymat bilan uchlik tenglik operatori (`===`) orqali solishtiradi. Angular yangilanishlarni qoʻllashi uchun bu qiymatlarni oʻzgartirganda yangi obyekt nusxasini yaratishingiz shart.

Agar elementda bir xil stil xususiyati uchun bir nechta bogʻlash boʻlsa, Angular toʻqnashuvlarni oʻzining stil ustuvorligi tartibiga koʻra hal qiladi.

## ARIA atributlari {#aria-attributes}

Angular satr qiymatlarini ARIA atributlariga bogʻlashni qoʻllab-quvvatlaydi.

```angular-html
<button type="button" [aria-label]="actionLabel()">
  {{ actionLabel() }}
</button>
```

Angular satr qiymatini elementning `aria-label` atributiga yozadi va bogʻlangan qiymat `null` boʻlganda uni olib tashlaydi.

Baʼzi ARIA imkoniyatlari strukturali qiymatlarni (masalan, element havolalarini) qabul qiladigan DOM xususiyatlari yoki direktiva input'larini taqdim etadi. Bunday holatlar uchun standart xususiyat bogʻlashlaridan foydalaning. Misollar va qoʻshimcha koʻrsatmalar uchun [accessibility qoʻllanmasiga](/best-practices/a11y#aria-attributes-and-properties) qarang.
