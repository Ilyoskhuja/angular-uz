# Atribut direktivalari

Atribut direktivalari DOM elementlari va Angular komponentlarining koʻrinishi yoki xatti-harakatini oʻzgartiradi.

## Bir martalik xatti-harakat uchun shablon bogʻlashlaridan foydalaning {#use-template-bindings-for-one-off-behavior}

Angular'ning shablon sintaksisi bitta elementning klasslari, stillari, xususiyatlari va hodisalarini oʻzgartirishni allaqachon qamrab oladi:

- [Klass va stil bogʻlashlari](guide/templates/binding#css-class-and-style-property-bindings) CSS klasslari va inline stillarni qoʻshadi va olib tashlaydi.
- [Xususiyat va atribut bogʻlashlari](guide/templates/binding) DOM xususiyatlari va HTML atributlarini oʻrnatadi.
- [Hodisa tinglovchilari](guide/templates/event-listeners) foydalanuvchi bilan oʻzaro aloqaga javob beradi.

Atribut direktivalari bunday xatti-harakatni istalgan element yoki komponentga qoʻllash mumkin boʻlgan qayta ishlatiladigan birlikka joylashtirmoqchi boʻlganingizda foydalidir.

## Atribut direktivasini yaratish {#building-an-attribute-directive}

Maxsus atribut direktivasi — bu `@Directive()` dekoratoriga ega JavaScript klassi. Dekoratorning `selector` xususiyati direktivani qoʻllaydigan atributni aniqlaydi. Kvadrat qavslar buni atribut selektoriga aylantiradi, shuning uchun direktiva shu atributga ega elementlarga mos keladi. Nomlar toʻqnashuvining oldini olish uchun odatda `app` kabi prefiks ishlatiladi:

```ts
import {Directive} from '@angular/core';

@Directive({
  selector: '[appHighlight]',
})
export class HighlightDirective {}
```

HELPFUL: [`ng generate directive`](tools/cli/schematics) CLI buyrugʻi direktivani uning test fayli bilan birga yaratib beradi.

Direktiva oʻz host elementini host bogʻlashlari orqali deklarativ tarzda yoki host elementga havola orqali imperativ tarzda oʻzgartirishi mumkin. Bu misol [`ElementRef`](api/core/ElementRef)'ni [inyeksiya qiladi](guide/di) va fonni sariq rangga oʻrnatish uchun elementga uning `nativeElement` xususiyati orqali murojaat qiladi:

<docs-code header="highlight.directive.ts" path="adev/src/content/examples/attribute-directives/src/app/highlight.directive.1.ts"/>

IMPORTANT: Direktivalar nomlar fazosini (namespace) _qoʻllab-quvvatlamaydi_.

```angular-html {avoid}
<p app:Highlight>This is invalid</p>
```

## Atribut direktivasini qoʻllash {#applying-an-attribute-directive}

Direktivani qoʻllash uchun uning selektorini elementga atribut sifatida qoʻshing:

<docs-code header="app.component.html" path="adev/src/content/examples/attribute-directives/src/app/app.component.1.html" region="applied"/>

Angular oʻsha `<p>` elementi uchun `HighlightDirective` nusxasini yaratadi, elementga havolani inyeksiya qiladi va uning fonini sariq rangga oʻrnatadi.

## Foydalanuvchi hodisalariga ishlov berish {#handling-user-events}

Foydalanuvchi bilan oʻzaro aloqaga javob berish uchun host element hodisalarini `@Directive()` dekoratorining `host` xususiyati orqali ishlov beruvchi metodlarga bogʻlang. Quyidagi direktiva kursor host element ustida turganda uni ajratib koʻrsatadi va kursor ketganda ajratishni tozalaydi:

<docs-code header="highlight.directive.ts" path="adev/src/content/examples/attribute-directives/src/app/highlight.directive.2.ts"/>

`host` xususiyati `mouseenter` va `mouseleave` hodisalarini `onMouseEnter()` va `onMouseLeave()` metodlariga moslaydi, ular esa host elementda fon rangini oʻrnatuvchi `highlight()` yordamchi metodiga murojaat qiladi. Host hodisa bogʻlashlari haqida koʻproq bilish uchun [host elementga bogʻlash](guide/components/host-elements#binding-to-the-host-element) boʻlimiga qarang.

## Input qiymatlarini qabul qilish {#accepting-input-values}

Komponentlar kabi direktivalar ham input'larni [`input()`](guide/components/inputs) funksiyasi orqali qabul qiladi. Input'ga selektor bilan bir xil nom bering, shunda bitta bogʻlash direktivani ham qoʻllaydi, ham unga qiymat uzatadi:

<docs-code header="highlight.directive.ts" path="adev/src/content/examples/attribute-directives/src/app/highlight.directive.3.ts" region="input"/>

Input'ni signal sifatida chaqirib oʻqing va rang oʻrnatilmagan boʻlsa, sukut boʻyicha qiymatga qayting:

<docs-code header="highlight.directive.ts" path="adev/src/content/examples/attribute-directives/src/app/highlight.directive.3.ts" region="mouse-enter"/>

Shablonda qiymatni selektorga bogʻlang. Input selektor bilan bir xil nomga ega boʻlgani uchun `[appHighlight]` direktivani ham qoʻllaydi, ham uning qiymatini oʻrnatadi. Bu yerda bogʻlangan `color` — komponentdagi xususiyat:

<docs-code header="app.component.html" path="adev/src/content/examples/attribute-directives/src/app/app.component.html" region="color"/>

<docs-code header="app.component.ts" path="adev/src/content/examples/attribute-directives/src/app/app.component.ts" region="class"/>

Direktiva bir nechta input eʼlon qilishi mumkin. Quyidagi direktiva `defaultColor` input'ini qoʻshadi, soʻngra navbat bilan `appHighlight`, `defaultColor` va oxirida `red` qiymatlariga qaytadi:

<docs-code header="highlight.directive.ts" path="adev/src/content/examples/attribute-directives/src/app/highlight.directive.ts"/>

Ikkala input'ni ham bir xil elementga bogʻlang. `defaultColor` dinamik ifoda emas, balki statik satr qabul qilgani uchun unga kvadrat qavslar kerak emas:

<docs-code header="app.component.html" path="adev/src/content/examples/attribute-directives/src/app/app.component.html" region="defaultColor"/>

## `NgNonBindable` bilan Angular ishlovini oʻchirish {#deactivating-angular-processing-with-ngnonbindable}

Brauzerda ifodaning hisoblanishining oldini olish uchun host elementga `ngNonBindable` qoʻshing.
`ngNonBindable` shablonlarda interpolyatsiya, direktivalar va bogʻlashni oʻchiradi.

Quyidagi misolda `{{ 1 + 1 }}` ifodasi kod muharriringizda qanday koʻrinsa, xuddi shunday render qilinadi va `2` koʻrsatilmaydi.

<docs-code header="app.component.html" path="adev/src/content/examples/attribute-directives/src/app/app.component.html" region="ngNonBindable"/>

Elementga `ngNonBindable` qoʻllash oʻsha elementning bola elementlari uchun bogʻlashni toʻxtatadi.
Biroq `ngNonBindable` siz uni qoʻllagan elementning oʻzida direktivalar ishlashiga ruxsat beradi.
Quyidagi misolda `appHighlight` direktivasi hali ham faol, lekin Angular `{{ 1 + 1 }}` ifodasini hisoblamaydi.

<docs-code header="app.component.html" path="adev/src/content/examples/attribute-directives/src/app/app.component.html" region="ngNonBindable-with-directive"/>

Agar `ngNonBindable`'ni ota elementga qoʻllasangiz, Angular oʻsha elementning bolalari uchun interpolyatsiya va har qanday turdagi bogʻlashni, masalan, xususiyat bogʻlash yoki hodisa bogʻlashni oʻchiradi.

## Keyingi qadamlar {#whats-next}

<docs-pill-row>
  <docs-pill href="guide/directives/structural-directives" title="Strukturaviy direktivalar"/>
  <docs-pill href="guide/directives/directive-composition-api" title="Direktivalar kompozitsiyasi API'si"/>
</docs-pill-row>
