# Pipe'lar

Pipe'lar — shablonlarda maʼlumotlarni oʻzgartirish uchun ishlatiladigan funksiyalar. Umuman olganda, pipe'lar yon taʼsirlarga olib kelmaydigan "sof" (pure) funksiyalardir. Angular'da komponentlaringizga import qilib ishlatishingiz mumkin boʻlgan bir qancha foydali oʻrnatilgan pipe'lar mavjud. Shuningdek, maxsus pipe yaratishingiz ham mumkin.

NOTE: [Chuqur qoʻllanmada pipe'lar](/guide/templates/pipes) haqida koʻproq bilib oling.

Bu mashgʻulotda pipe'ni import qilib, shablonda ishlatasiz.

<hr>

Shablonda pipe'dan foydalanish uchun uni interpolyatsiya ifodasiga kiriting. Mana bu misolga qarang:

```angular-ts {highlight:[1,5,6]}
import {UpperCasePipe} from '@angular/common';

@Component({
  ...
  template: `{{ loudMessage | uppercase }}`,
  imports: [UpperCasePipe],
})
export class App {
  loudMessage = 'we think you are doing great!'
}
```

Endi oʻzingiz sinab koʻrish navbati:

<docs-workflow>

<docs-step title="`LowerCase` pipe'ini import qiling {#import-the-lowercase-pipe}">
Avval `app.ts` faylini `@angular/common`'dan `LowerCasePipe` uchun fayl darajasidagi importni qoʻshish orqali yangilang.

```ts
import {LowerCasePipe} from '@angular/common';
```

</docs-step>

<docs-step title="Pipe'ni shablon importlariga qoʻshing {#add-the-pipe-to-the-template-imports}">
Keyin `@Component()` dekoratorining `imports` qismini `LowerCasePipe`'ga havolani oʻz ichiga olishi uchun yangilang

```ts {highlight:[3]}
@Component({
  ...
  imports: [LowerCasePipe]
})
```

</docs-step>

<docs-step title="Pipe'ni shablonga qoʻshing {#add-the-pipe-to-the-template}">
Nihoyat, `app.ts` faylida shablonni `lowercase` pipe'ini oʻz ichiga olishi uchun yangilang:

```angular-html
template: `{{ username | lowercase }}`
```

</docs-step>

</docs-workflow>

Pipe'lar oʻz chiqishini sozlash uchun ishlatilishi mumkin boʻlgan parametrlarni ham qabul qilishi mumkin. Keyingi mashgʻulotda bu haqda koʻproq bilib oling.

P.S. siz ajoyib ketyapsiz ⭐️
