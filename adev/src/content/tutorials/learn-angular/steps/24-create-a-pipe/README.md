# Maxsus pipe yaratish

Maʼlumotlarni oʻzgartirish ehtiyojlaringizga mos keladigan maxsus pipe'larni Angular'da yaratishingiz mumkin.

NOTE: [Chuqur qoʻllanmada maxsus pipe'lar yaratish](/guide/templates/pipes#creating-custom-pipes) haqida koʻproq bilib oling.

Bu mashgʻulotda maxsus pipe yaratib, uni shablonda ishlatasiz.

<hr>

Pipe — bu `@Pipe` dekoratoriga ega TypeScript klassi. Mana bir misol:

```ts
import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
  name: 'star',
})
export class StarPipe implements PipeTransform {
  transform(value: string): string {
    return `⭐️ ${value} ⭐️`;
  }
}
```

`StarPipe` satr qiymatini qabul qiladi va shu satrni atrofida yulduzchalar bilan qaytaradi. Eʼtibor bering:

- `@Pipe` dekoratori konfiguratsiyasidagi nom shablonda ishlatiladigan nomdir
- `transform` funksiyasi — mantiqingizni joylashtiradigan joy

Xoʻsh, endi oʻzingiz sinab koʻrish navbati — `ReversePipe`'ni yaratasiz:

<docs-workflow>

<docs-step title="`ReversePipe`'ni yarating">

`reverse.pipe.ts` faylida `ReversePipe` klassiga `@Pipe` dekoratorini qoʻshing va quyidagi konfiguratsiyani bering:

```ts
@Pipe({
  name: 'reverse'
})
```

</docs-step>

<docs-step title="`transform` funksiyasini amalga oshiring">

Endi `ReversePipe` klassi pipe boʻldi. Teskari aylantirish mantiqini qoʻshish uchun `transform` funksiyasini yangilang:

```ts {highlight:[3,4,5,6,7,8,9]}
export class ReversePipe implements PipeTransform {
  transform(value: string): string {
    let reverse = '';

    for (let i = value.length - 1; i >= 0; i--) {
      reverse += value[i];
    }

    return reverse;
  }
}
```

</docs-step>

<docs-step title="Shablonda `ReversePipe`'dan foydalaning">
Pipe mantiqi amalga oshirilgach, oxirgi qadam — uni shablonda ishlatish. `app.ts` faylida pipe'ni shablonga kiriting va uni komponent importlariga qoʻshing:

```angular-ts {highlight:[3,4]}
@Component({
  ...
  template: `Reverse Machine: {{ word | reverse }}`,
  imports: [ReversePipe]
})
```

</docs-step>

</docs-workflow>

Shu bilan hammasi tayyor. Bu mashgʻulotni yakunlaganingiz bilan tabriklaymiz. Endi pipe'lardan qanday foydalanishni va hatto oʻzingizning maxsus pipe'laringizni qanday amalga oshirishni bilasiz.
