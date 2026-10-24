# Pipe'lar

## Umumiy koʻrinish {#overview}

Pipe'lar — Angular shablon ifodalaridagi maxsus operatorlar boʻlib, ular shablonda maʼlumotlarni deklarativ tarzda oʻzgartirish imkonini beradi. Pipe'lar oʻzgartirish funksiyasini bir marta eʼlon qilib, keyin shu oʻzgartirishdan bir nechta shablonlarda foydalanish imkonini beradi. Angular pipe'lari [Unix pipe](<https://en.wikipedia.org/wiki/Pipeline_(Unix)>)'dan ilhomlanib, vertikal chiziq belgisidan (`|`) foydalanadi.

NOTE: Angular'ning pipe sintaksisi vertikal chiziq belgisini [bitli OR operatori](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Bitwise_OR) uchun ishlatadigan standart JavaScript'dan farq qiladi. Angular shablon ifodalari bitli operatorlarni qoʻllab-quvvatlamaydi.

Quyida Angular taqdim etadigan baʼzi oʻrnatilgan pipe'lardan foydalanish misoli keltirilgan:

```angular-ts
import {Component} from '@angular/core';
import {CurrencyPipe, DatePipe, TitleCasePipe} from '@angular/common';

@Component({
  selector: 'app-root',
  imports: [CurrencyPipe, DatePipe, TitleCasePipe],
  template: `
    <main>
      <!-- Transform the company name to title-case and
       transform the purchasedOn date to a locale-formatted string -->
      <h1>Purchases from {{ company | titlecase }} on {{ purchasedOn | date }}</h1>

      <!-- Transform the amount to a currency-formatted string -->
      <p>Total: {{ amount | currency }}</p>
    </main>
  `,
})
export class ShoppingCart {
  amount = 123.45;
  company = 'acme corporation';
  purchasedOn = '2024-07-08';
}
```

Angular komponentni render qilganda, sana formati va valyutaning foydalanuvchi lokaliga (locale) mos boʻlishini taʼminlaydi. Agar foydalanuvchi Qoʻshma Shtatlarda boʻlsa, natija quyidagicha render qilinadi:

```angular-html
<main>
  <h1>Purchases from Acme Corporation on Jul 8, 2024</h1>
  <p>Total: $123.45</p>
</main>
```

Angular qiymatlarni qanday lokalizatsiya qilishi haqida koʻproq bilish uchun [i18n boʻyicha chuqur qoʻllanma](/guide/i18n)ga qarang.

### Oʻrnatilgan pipe'lar {#built-in-pipes}

Angular `@angular/common` paketida oʻrnatilgan pipe'lar toʻplamini oʻz ichiga oladi:

| Nomi                                          | Tavsifi                                                                                              |
| --------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| [`AsyncPipe`](api/common/AsyncPipe)           | `Promise` yoki RxJS `Observable`'dan qiymatni oʻqiydi.                                               |
| [`CurrencyPipe`](api/common/CurrencyPipe)     | Sonni lokal qoidalariga mos formatlangan valyuta satriga oʻzgartiradi.                               |
| [`DatePipe`](api/common/DatePipe)             | `Date` qiymatini lokal qoidalariga mos formatlaydi.                                                  |
| [`DecimalPipe`](api/common/DecimalPipe)       | Sonni lokal qoidalariga mos formatlangan, oʻnlik nuqtali satrga oʻzgartiradi.                        |
| [`I18nPluralPipe`](api/common/I18nPluralPipe) | Qiymatni lokal qoidalariga mos ravishda koʻplik shaklini hosil qiladigan satrga moslashtiradi.       |
| [`I18nSelectPipe`](api/common/I18nSelectPipe) | Kalitni kerakli qiymatni qaytaradigan maxsus selektorga moslashtiradi.                               |
| [`JsonPipe`](api/common/JsonPipe)             | Obyektni `JSON.stringify` orqali satr koʻrinishiga oʻzgartiradi, nosozliklarni tuzatish uchun moʻljallangan. |
| [`KeyValuePipe`](api/common/KeyValuePipe)     | Object yoki Map'ni kalit-qiymat juftliklari massiviga oʻzgartiradi.                                  |
| [`LowerCasePipe`](api/common/LowerCasePipe)   | Matnni toʻliq kichik harflarga oʻzgartiradi.                                                         |
| [`PercentPipe`](api/common/PercentPipe)       | Sonni lokal qoidalariga mos formatlangan foiz satriga oʻzgartiradi.                                  |
| [`SlicePipe`](api/common/SlicePipe)           | Elementlarning bir qismini (slice) oʻz ichiga olgan yangi Array yoki String yaratadi.                |
| [`TitleCasePipe`](api/common/TitleCasePipe)   | Matnni har bir soʻzi bosh harf bilan boshlanadigan (title case) koʻrinishga oʻzgartiradi.            |
| [`UpperCasePipe`](api/common/UpperCasePipe)   | Matnni toʻliq katta harflarga oʻzgartiradi.                                                          |

## Pipe'lardan foydalanish {#using-pipes}

Angular'ning pipe operatori shablon ifodasi ichida vertikal chiziq belgisidan (`|`) foydalanadi. Pipe operatori — binar operator: chap tomondagi operand oʻzgartirish funksiyasiga uzatiladigan qiymat, oʻng tomondagi operand esa pipe nomi va har qanday qoʻshimcha argumentlar (quyida tavsiflangan).

```angular-html
<p>Total: {{ amount | currency }}</p>
```

Bu misolda `amount` qiymati nomi `currency` boʻlgan `CurrencyPipe`'ga uzatiladi. Keyin u foydalanuvchi lokali uchun sukut boʻyicha valyutani render qiladi.

### Bir ifodada bir nechta pipe'ni birlashtirish {#combining-multiple-pipes-in-the-same-expression}

Bir nechta pipe operatoridan foydalanib, qiymatga bir nechta oʻzgartirish qoʻllashingiz mumkin. Angular pipe'larni chapdan oʻngga bajaradi.

Quyidagi misol lokalizatsiya qilingan sanani toʻliq katta harflarda koʻrsatish uchun pipe'lar kombinatsiyasini namoyish etadi:

```angular-html
<p>The event will occur on {{ scheduledOn | date | uppercase }}.</p>
```

### Pipe'larga parametrlar uzatish {#passing-parameters-to-pipes}

Baʼzi pipe'lar oʻzgartirishni sozlash uchun parametrlar qabul qiladi. Parametrni koʻrsatish uchun pipe nomidan keyin ikki nuqta (`:`) va parametr qiymatini yozing.

Masalan, `DatePipe` sanani maʼlum bir tarzda formatlash uchun parametrlar qabul qila oladi.

```angular-html
<p>The event will occur at {{ scheduledOn | date: 'hh:mm' }}.</p>
```

Baʼzi pipe'lar bir nechta parametr qabul qilishi mumkin. Qoʻshimcha parametr qiymatlarini ikki nuqta belgisi (`:`) bilan ajratib koʻrsatishingiz mumkin.

Masalan, vaqt mintaqasini boshqarish uchun ikkinchi ixtiyoriy parametrni ham uzatishimiz mumkin.

```angular-html
<p>The event will occur at {{ scheduledOn | date: 'hh:mm' : 'UTC' }}.</p>
```

## Pipe'lar qanday ishlaydi {#how-pipes-work}

Konseptual jihatdan pipe'lar — kiruvchi qiymatni qabul qilib, oʻzgartirilgan qiymatni qaytaradigan funksiyalar.

```angular-ts
import {Component} from '@angular/core';
import {CurrencyPipe} from '@angular/common';

@Component({
  selector: 'app-root',
  imports: [CurrencyPipe],
  template: `
    <main>
      <p>Total: {{ amount | currency }}</p>
    </main>
  `,
})
export class AppComponent {
  amount = 123.45;
}
```

Bu misolda:

1. `CurrencyPipe` `@angular/common`'dan import qilinadi
1. `CurrencyPipe` `imports` massiviga qoʻshiladi
1. `amount` maʼlumoti `currency` pipe'iga uzatiladi

### Pipe operatorining ustuvorligi {#pipe-operator-precedence}

Pipe operatori `+`, `-`, `*`, `/`, `%`, `&&`, `||` va `??` kabi boshqa binar operatorlarga nisbatan pastroq ustuvorlikka ega.

```angular-html
<!-- firstName and lastName are concatenated before the result is passed to the uppercase pipe -->
{{ firstName + lastName | uppercase }}
```

Pipe operatori shartli (ternar) operatorga nisbatan yuqoriroq ustuvorlikka ega.

```angular-html
{{ (isAdmin ? 'Access granted' : 'Access denied') | uppercase }}
```

Agar xuddi shu ifoda qavslarsiz yozilsa:

<!-- prettier-ignore -->
```angular-html
{{ isAdmin ? 'Access granted' : 'Access denied' | uppercase }}
```

U oʻrniga quyidagicha tahlil qilinadi:

```angular-html
{{ isAdmin ? 'Access granted' : ('Access denied' | uppercase) }}
```

Operatorlar ustuvorligi noaniq boʻlishi mumkin boʻlgan hollarda ifodalaringizda doimo qavslardan foydalaning.

### Pipe'lar bilan oʻzgarishlarni aniqlash {#change-detection-with-pipes}

Sukut boʻyicha barcha pipe'lar `pure` (toza) hisoblanadi, yaʼni ular faqat primitiv kiruvchi qiymat (`String`, `Number`, `Boolean` yoki `Symbol` kabi) yoki obyekt havolasi (`Array`, `Object`, `Function` yoki `Date` kabi) oʻzgarganda bajariladi. Toza pipe'lar unumdorlik jihatidan afzallik beradi, chunki uzatilgan qiymat oʻzgarmagan boʻlsa, Angular oʻzgartirish funksiyasini chaqirmasligi mumkin.

Natijada, bu obyekt xususiyatlari yoki massiv elementlaridagi mutatsiyalar butun obyekt yoki massiv havolasi boshqa nusxa bilan almashtirilmaguncha aniqlanmasligini anglatadi. Agar sizga oʻzgarishlarni aniqlashning shu darajasi kerak boʻlsa, [massivlar yoki obyektlar ichidagi oʻzgarishlarni aniqlash](#detecting-change-within-arrays-or-objects) boʻlimiga qarang.

## Maxsus pipe'lar yaratish {#creating-custom-pipes}

`@Pipe` dekoratori bilan TypeScript klassini amalga oshirish orqali maxsus pipe aniqlashingiz mumkin. Pipe ikki narsaga ega boʻlishi shart:

- Pipe dekoratorida koʻrsatilgan nom
- Qiymatni oʻzgartirishni bajaradigan `transform` nomli metod.

Bundan tashqari, TypeScript klassi pipe uchun tur signaturasini qanoatlantirishini taʼminlash uchun `PipeTransform` interfeysini amalga oshirishi kerak.

Quyida satrlarni kebab-case koʻrinishiga oʻzgartiradigan maxsus pipe misoli keltirilgan:

```angular-ts {header: "kebab-case.pipe.ts"}
import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
  name: 'kebabCase',
})
export class KebabCasePipe implements PipeTransform {
  transform(value: string): string {
    return value.toLowerCase().replace(/ /g, '-');
  }
}
```

### `@Pipe` dekoratoridan foydalanish {#using-the-pipe-decorator}

Maxsus pipe yaratganda `@angular/core` paketidan `Pipe`'ni import qiling va undan TypeScript klassi uchun dekorator sifatida foydalaning.

```angular-ts
import {Pipe} from '@angular/core';

@Pipe({
  name: 'myCustomTransformation',
})
export class MyCustomTransformationPipe {}
```

`@Pipe` dekoratori pipe'ning shablonda qanday ishlatilishini boshqaradigan `name`'ni talab qiladi.

### Maxsus pipe'lar uchun nomlash qoidalari {#naming-convention-for-custom-pipes}

Maxsus pipe'larni nomlash qoidalari ikki qoidadan iborat:

- `name` - camelCase tavsiya etiladi. Defislardan foydalanmang.
- `klass nomi` - `name`'ning PascalCase koʻrinishi, oxiriga `Pipe` qoʻshilgan holda

### `PipeTransform` interfeysini amalga oshirish {#implement-the-pipetransform-interface}

`@Pipe` dekoratoridan tashqari, maxsus pipe'lar doimo `@angular/core`'dagi `PipeTransform` interfeysini amalga oshirishi kerak.

```angular-ts
import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
  name: 'myCustomTransformation',
})
export class MyCustomTransformationPipe implements PipeTransform {}
```

Bu interfeysni amalga oshirish pipe klassingizning toʻgʻri tuzilmaga ega boʻlishini taʼminlaydi.

### Pipe qiymatini oʻzgartirish {#transforming-the-value-of-a-pipe}

Har bir oʻzgartirish `transform` metodi orqali chaqiriladi: birinchi parametr — uzatilayotgan qiymat, qaytariladigan qiymat esa — oʻzgartirilgan qiymat.

```angular-ts
import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
  name: 'myCustomTransformation',
})
export class MyCustomTransformationPipe implements PipeTransform {
  transform(value: string): string {
    return `My custom transformation of ${value}.`;
  }
}
```

### Maxsus pipe'ga parametrlar qoʻshish {#adding-parameters-to-a-custom-pipe}

`transform` metodiga qoʻshimcha parametrlar qoʻshish orqali oʻzgartirishingizga parametrlar qoʻshishingiz mumkin:

```angular-ts
import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
  name: 'myCustomTransformation',
})
export class MyCustomTransformationPipe implements PipeTransform {
  transform(value: string, format: string): string {
    let msg = `My custom transformation of ${value}.`;

    if (format === 'uppercase') {
      return msg.toUpperCase();
    } else {
      return msg;
    }
  }
}
```

### Massivlar yoki obyektlar ichidagi oʻzgarishlarni aniqlash {#detecting-change-within-arrays-or-objects}

Pipe massivlar yoki obyektlar ichidagi oʻzgarishlarni aniqlashini istasangiz, `pure` bayrogʻini `false` qiymati bilan uzatib, uni toza boʻlmagan (impure) funksiya sifatida belgilash kerak.

IMPORTANT: Mutlaqo zarur boʻlmasa, toza boʻlmagan pipe'lar yaratishdan qoching, chunki ehtiyotsiz ishlatilganda ular unumdorlikka jiddiy zarar yetkazishi mumkin.

```angular-ts
import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
  name: 'joinNamesImpure',
  pure: false,
})
export class JoinNamesImpurePipe implements PipeTransform {
  transform(names: string[]): string {
    return names.join();
  }
}
```

Angular dasturchilari boshqa dasturchilarga unumdorlik bilan bogʻliq ehtimoliy muammoni koʻrsatish uchun pipe `name`'i va klass nomiga `Impure` soʻzini qoʻshish qoidasini koʻpincha qabul qiladi.

## Pipe logikasidan shablonlardan tashqarida foydalanish {#using-pipe-logic-outside-templates}

Pipe'lar — shablonlarda maʼlumotlarni deklarativ tarzda oʻzgartirish uchun moʻljallangan shablon operatorlari. Xuddi shu oʻzgartirish logikasi servisda, yordamchi klassda yoki shablon boʻlmagan boshqa har qanday kontekstda kerak boʻlganda, **pipe klassini inyeksiya qilishdan qoching**. Pipe'lar inyeksiya qilinadigan servislar sifatida moʻljallanmagan.

### Logikani maxsus pipe'lardan ajratib oling {#extract-the-logic-from-custom-pipes}

Maxsus pipe yaratganda oʻzgartirishni mustaqil funksiyaga ajratib oling. Pipe'ning `transform()` metodi shu funksiyaga murojaat qilsin (delegate), va funksiyani kerak boʻlgan boshqa har qanday joyda toʻgʻridan-toʻgʻri import qiling.

```ts {header: "kebab-case.ts"}
export function toKebabCase(value: string): string {
  return value.toLowerCase().replace(/ /g, '-');
}
```

```ts {header: "kebab-case.pipe.ts" , prefer}
import {Pipe, PipeTransform} from '@angular/core';
import {toKebabCase} from './kebab-case';

@Pipe({name: 'kebabCase'})
export class KebabCasePipe implements PipeTransform {
  transform(value: string): string {
    return toKebabCase(value);
  }
}
```

```ts {header: "formatter.service.ts" , prefer}
import {Service} from '@angular/core';
import {toKebabCase} from './kebab-case';

@Service()
export class FormatterService {
  formatSlug(title: string): string {
    return toKebabCase(title);
  }
}
```

```ts {header: "formatter.service.ts" , avoid}
import {inject, Service} from '@angular/core';
import {KebabCasePipe} from './kebab-case.pipe';

@Service()
export class FormatterService {
  // Avoid injecting the pipe class into services or other classes.
  private kebabCasePipe = inject(KebabCasePipe);

  formatSlug(title: string): string {
    return this.kebabCasePipe.transform(title);
  }
}
```

### Oʻrnatilgan pipe'lar uchun formatlash funksiyalaridan foydalaning {#use-formatting-functions-for-built-in-pipes}

Angular'ning lokalni hisobga oladigan oʻrnatilgan pipe'larining har biri `@angular/common`'dan eksport qilinadigan mos mustaqil formatlash funksiyasiga ega. Pipe klassini inyeksiya qilish oʻrniga shu funksiyalardan foydalaning.

| Pipe           | Mustaqil funksiya   |
| -------------- | ------------------- |
| `DatePipe`     | `formatDate`        |
| `CurrencyPipe` | `formatCurrency`    |
| `DecimalPipe`  | `formatNumber`      |
| `PercentPipe`  | `formatPercent`     |

```ts {prefer}
import {Service, LOCALE_ID, inject} from '@angular/core';
import {formatNumber} from '@angular/common';

@Service()
export class PriceService {
  private locale = inject(LOCALE_ID);

  format(value: number) {
    return formatNumber(value, this.locale, '1.2-2');
  }
}
```

```ts {avoid}
import {inject, Service} from '@angular/core';
import {DecimalPipe} from '@angular/common';

@Service()
export class PriceService {
  private decimalPipe = inject(DecimalPipe);

  format(value: number) {
    return this.decimalPipe.transform(value, '1.2-2');
  }
}
```
