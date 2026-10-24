<docs-decorative-header title="Direktivalar" imgSrc="adev/src/assets/images/directives.svg"> <!-- markdownlint-disable-line -->
Direktivalar Angular ilovalaringizdagi elementlar va komponentlarga xatti-harakat qoʻshadi.
</docs-decorative-header>

Direktiva elementning koʻrinishini, xatti-harakatini yoki DOM'da qanday joylashishini oʻzgartirishi mumkin. Angular bir nechta oʻrnatilgan direktivalar bilan birga keladi, shuningdek, siz oʻzingiznikini ham yozishingiz mumkin.

## Direktivadan qachon foydalanish kerak {#when-to-use-a-directive}

Direktivalar mavjud element yoki komponentga qoʻllamoqchi boʻlgan **qayta ishlatiladigan** xatti-harakatni inkapsulyatsiya qilganda eng samarali boʻladi.

Keng tarqalgan misollar:

- Koʻplab elementlarga bir xil koʻrinish yoki xatti-harakatni qoʻllash, masalan, autofocus yoki tooltip.
- Host elementning DOM'idan, atributlaridan yoki klasslaridan oʻqish yoki ularga yozish.
- Sizga tegishli boʻlmagan komponentga uning manba kodini oʻzgartirmasdan xatti-harakat qoʻshish.

Agar oʻz markup'ingizni render qilishingiz yoki UI'ning oʻz shabloniga ega boʻlgan qismini boshqarishingiz kerak boʻlsa, [komponentga](guide/components) — oʻz shabloniga ega boʻlgan maxsus direktivaga murojaat qiling.

## Qisqa misol {#a-quick-example}

Faraz qiling, foydalanuvchi sichqonchani elementlar ustiga olib borganda ular ajralib turishini, yaʼni fon rangi sariqqa oʻzgarishini istaysiz. Har bir elementda bir xil hodisaga ishlov berish logikasini takrorlash oʻrniga, bu xatti-harakatni direktivaga joylashtirib, kerak boʻlgan har qanday joyda qoʻllashingiz mumkin.

Quyidagi `appHighlight` direktivasi sichqoncha element ustiga kelganda host elementning fon rangini oʻrnatadi va sichqoncha ketganda uni tozalaydi:

```ts
import {Directive, signal} from '@angular/core';

@Directive({
  selector: '[appHighlight]',
  host: {
    '(mouseenter)': 'isHovered.set(true)',
    '(mouseleave)': 'isHovered.set(false)',
    '[style.background-color]': 'isHovered() ? "yellow" : null',
  },
})
export class HighlightDirective {
  protected isHovered = signal(false);
}
```

`host` metamaʼlumotlari `isHovered` signalini yangilash uchun sichqoncha hodisalarini tinglaydi va host elementning `background-color` stilini signal qiymatiga bogʻlaydi.

Direktivani qoʻllash uchun uning selektorini elementga atribut sifatida qoʻshing:

```angular-html
<p appHighlight>Highlight me!</p>
```

`appHighlight` atributiga ega boʻlgan har bir element bir xil hover xatti-harakatiga ega boʻladi, logika esa bir joyda aniqlanadi.

## Direktiva turlari {#types-of-directives}

Angular'da direktivalarning uchta asosiy turi mavjud:

| Direktiva turi                                                     | Tafsilotlar                                                                             |
| :----------------------------------------------------------------- | :-------------------------------------------------------------------------------------- |
| [Komponentlar](guide/components)                                   | Oʻz shabloniga ega qayta ishlatiladigan UI'ni aniqlaydi.                               |
| [Atribut direktivalari](guide/directives/attribute-directives)     | Element, komponent yoki boshqa direktivaning koʻrinishi yoki xatti-harakatini oʻzgartiradi. |
| [Strukturaviy direktivalar](guide/directives/structural-directives) | DOM elementlarini qoʻshish va olib tashlash orqali DOM tuzilmasini oʻzgartiradi.       |

## Keyingi qadamlar {#whats-next}

Direktivalarning har bir turi haqida quyidagi qoʻllanmalarda koʻproq bilib oling.

<docs-pill-row>
  <docs-pill href="guide/directives/attribute-directives" title="Atribut direktivalari"/>
  <docs-pill href="guide/directives/structural-directives" title="Strukturaviy direktivalar"/>
  <docs-pill href="guide/directives/directive-composition-api" title="Direktivalar kompozitsiyasi API'si"/>
</docs-pill-row>
