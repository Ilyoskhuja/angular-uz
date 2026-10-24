# DI amalda

Bu qoʻllanma Angular'da bogʻliqliklarni inyeksiya qilish (DI) tizimining qoʻshimcha imkoniyatlarini koʻrib chiqadi.

NOTE: InjectionToken va maxsus provider'lar haqida toʻliq maʼlumot olish uchun [bogʻliqlik provider'larini aniqlash qoʻllanmasiga](guide/di/defining-dependency-providers#injection-tokens) qarang.

## Komponentning DOM elementini inyeksiya qilish {#inject-the-components-dom-element}

Dasturchilar odatda bundan qochishsa-da, baʼzi vizual effektlar va uchinchi tomon vositalari DOM'ga bevosita murojaat qilishni talab qiladi.
Bunday hollarda sizga komponentning DOM elementiga murojaat qilish kerak boʻlishi mumkin.

Angular `@Component` yoki `@Directive`'ning asosidagi DOM elementini `ElementRef` tokeni yordamida inyeksiya qilish orqali taqdim etadi:

```ts {highlight:[7]}
import {Directive, ElementRef, inject} from '@angular/core';

@Directive({
  selector: '[appHighlight]',
})
export class HighlightDirective {
  private element = inject(ElementRef);

  update() {
    this.element.nativeElement.style.color = 'red';
  }
}
```

## Host elementning teg nomini inyeksiya qilish {#inject-the-host-elements-tag-name}

Host elementning teg nomini olish uchun uni `HOST_TAG_NAME` tokeni yordamida inyeksiya qiling.

```ts
import {Directive, HOST_TAG_NAME, inject} from '@angular/core';

@Directive({
  selector: '[roleButton]',
})
export class RoleButtonDirective {
  private tagName = inject(HOST_TAG_NAME);

  onAction() {
    switch (this.tagName) {
      case 'button':
        // Handle button action
        break;
      case 'a':
        // Handle anchor action
        break;
      default:
        // Handle other elements
        break;
    }
  }
}
```

NOTE: Agar host elementda teg nomi boʻlmasligi mumkin boʻlsa (masalan, `ng-container` yoki `ng-template`), inyeksiyani ixtiyoriy (optional) qiling.

## Siklik bogʻliqliklarni oldinga havola (forward reference) bilan hal qilish {#resolve-circular-dependencies-with-a-forward-reference}

TypeScript'da klasslarni eʼlon qilish tartibi muhim.
Klassni aniqlamaguningizcha unga bevosita murojaat qila olmaysiz.

Bu odatda muammo boʻlmaydi, ayniqsa tavsiya etilgan _har bir faylda bitta klass_ qoidasiga amal qilsangiz.
Biroq baʼzi hollarda siklik havolalardan qochib boʻlmaydi.
Masalan, agar 'A' klassi 'B' klassiga, 'B' klassi esa 'A' klassiga murojaat qilsa, ulardan biri birinchi aniqlanishi kerak.

Angular'ning `forwardRef()` funksiyasi Angular keyinroq hal qila oladigan _bilvosita_ havola yaratadi.

Klass _oʻziga havola qilganda_ ham shunga oʻxshash muammoga duch kelasiz.
Masalan, oʻzining `providers` massivida.
`providers` massivi `@Component()` dekorator funksiyasining xususiyati boʻlib, u klass taʼrifidan oldin kelishi kerak.
Bunday siklik havolalarni `forwardRef` yordamida hal qilish mumkin.

```typescript {header: 'app.component.ts', highlight: [4]}
providers: [
  {
    provide: PARENT_MENU_ITEM,
    useExisting: forwardRef(() => MenuItem),
  },
],
```
