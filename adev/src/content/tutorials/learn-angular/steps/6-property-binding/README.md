# Angular'da xususiyatlarni bogʻlash

Angular'da xususiyatlarni bogʻlash (property binding) HTML elementlari, Angular komponentlari va boshqalarning xususiyatlariga qiymat oʻrnatish imkonini beradi.

Xususiyatlar va atributlarga dinamik tarzda qiymat oʻrnatish uchun xususiyatlarni bogʻlashdan foydalaning. Tugma imkoniyatlarini yoqish/oʻchirish, rasm yoʻllarini programmaviy tarzda oʻrnatish va komponentlar oʻrtasida qiymatlarni almashish kabi ishlarni bajarishingiz mumkin.

NOTE: [Asoslar qoʻllanmasida dinamik xususiyatlar va atributlarni oʻrnatish](/essentials/templates#setting-dynamic-properties-and-attributes) haqida koʻproq bilib oling.

Bu mashgʻulotda shablonlarda xususiyatlarni bogʻlashdan qanday foydalanishni oʻrganasiz.

<hr />

Element atributiga bogʻlash uchun atribut nomini kvadrat qavslar ichiga oling. Misol:

```angular-html
<img alt="photo" [src]="imageURL" />
```

Bu misolda `src` atributining qiymati `imageURL` klass xususiyatiga bogʻlanadi. `imageURL` qanday qiymatga ega boʻlsa, u `img` tegining `src` atributi sifatida oʻrnatiladi.

<docs-workflow>

<docs-step title="`isEditable` nomli xususiyat qoʻshing {#add-a-property-called-iseditable}" header="app.ts" language="ts">
`app.ts`'dagi kodni `App` klassiga boshlangʻich qiymati `true` boʻlgan `isEditable` nomli xususiyat qoʻshib yangilang.

```ts {highlight:[2]}
export class App {
  isEditable = true;
}
```

</docs-step>

<docs-step title="`contentEditable`'ga bogʻlang {#bind-to-contenteditable}" header="app.ts" language="ts">
Keyin <code aria-label="square brackets">[]</code> sintaksisidan foydalanib, `div`'ning `contentEditable` atributini `isEditable` xususiyatiga bogʻlang.

```angular-ts {highlight:[3]}
@Component({
  ...
  template: `<div [contentEditable]="isEditable"></div>`,
})
```

</docs-step>

</docs-workflow>

Endi div tahrirlanadigan boʻldi. Ajoyib ish 👍

Xususiyatlarni bogʻlash Angular'ning koʻplab kuchli imkoniyatlaridan biri. Koʻproq bilmoqchi boʻlsangiz, [Angular hujjatlariga](guide/templates/binding#css-class-and-style-property-bindings) qarang.
