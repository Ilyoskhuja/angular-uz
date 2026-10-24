# Hodisalarga ishlov berish

Hodisalarga ishlov berish veb-ilovalarda interaktiv imkoniyatlarni taʼminlaydi. U sizga dasturchi sifatida tugma bosilishi, forma yuborilishi va boshqa foydalanuvchi harakatlariga javob berish imkonini beradi.

NOTE: [Asoslar qoʻllanmasida foydalanuvchi bilan oʻzaro taʼsirga ishlov berish](/essentials/templates#handling-user-interaction) haqida koʻproq bilib oling.

Bu mashgʻulotda hodisa ishlov beruvchisini qanday qoʻshishni oʻrganasiz.

<hr />

Angular'da hodisalarga qavslar sintaksisi `()` yordamida bogʻlanasiz. Berilgan elementda bogʻlamoqchi boʻlgan hodisani qavslar ichiga oling va hodisa ishlov beruvchisini oʻrnating. Quyidagi `button` misolini koʻrib chiqing:

```angular-ts
@Component({
  ...
  template: `<button (click)="greet()">`
})
export class App {
  greet() {
    console.log('Hello, there 👋');
  }
}
```

Bu misolda tugma har safar bosilganda `greet()` funksiyasi ishga tushadi. `greet()` sintaksisida oxirida qavslar borligiga eʼtibor bering.

Xoʻsh, endi oʻzingiz sinab koʻring:

<docs-workflow>

<docs-step title="Hodisa ishlov beruvchisini qoʻshing">
`App` klassida mavjud `showSecretMessage()` metodining tanasini quyidagi kod bilan toʻldiring:

```ts
this.message = 'Way to go 🚀';
```

</docs-step>

<docs-step title="Shablondagi hodisaga bogʻlang">
`app.ts`'dagi shablon kodini `section` elementining `mouseover` hodisasiga bogʻlanadigan qilib yangilang.

<!-- prettier-ignore -->
```angular-html
<section (mouseover)="showSecretMessage()">
```

</docs-step>

</docs-workflow>

Shunday qilib, koddagi bir necha qadam bilan Angular'da birinchi hodisa ishlov beruvchingizni yaratdingiz. Bu ishda ancha mahorat orttirayotganga oʻxshaysiz, shu zaylda davom eting.
