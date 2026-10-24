# Komponentlarda boshqaruv oqimi - `@if`

Foydalanuvchiga ekranda nimani koʻrsatishni hal qilish ilova yaratishda keng tarqalgan vazifa. Koʻp hollarda bu qaror shartlar yordamida programmaviy tarzda qabul qilinadi.

Shablonlarda shartli koʻrsatishni ifodalash uchun Angular `@if` shablon sintaksisidan foydalanadi.

NOTE: [Asoslar qoʻllanmasida boshqaruv oqimi](/essentials/templates#control-flow-with-if-and-for) haqida koʻproq bilib oling.

Bu mashgʻulotda shablonlarda shartlardan qanday foydalanishni oʻrganasiz.

<hr/>

Shablonda elementlarni shartli koʻrsatish imkonini beradigan sintaksis — `@if`.

Komponentda `@if` sintaksisidan qanday foydalanishga misol:

```angular-ts
@Component({
  ...
  template: `
    @if (isLoggedIn) {
      <p>Welcome back, Friend!</p>
    }
  `,
})
export class App {
  isLoggedIn = true;
}
```

Eʼtibor berish kerak boʻlgan ikki narsa:

- `if` oldida `@` prefiksi bor, chunki bu [Angular shablon sintaksisi](guide/templates) deb nomlanadigan maxsus sintaksis turi
- Hali ham `*ngIf`'dan foydalanadigan ilovalar uchun koʻproq maʼlumot olish maqsadida [NgIf boʻyicha Angular hujjatlariga](guide/directives/structural-directives) murojaat qiling.

<docs-workflow>

<docs-step title="`isServerRunning` nomli xususiyat yarating">
`App` klassiga `isServerRunning` nomli `boolean` xususiyat qoʻshing va boshlangʻich qiymatini `true` qilib belgilang.
</docs-step>

<docs-step title="Shablonda `@if`'dan foydalaning">
`isServerRunning` qiymati `true` boʻlsa, `Yes, the server is running` xabarini koʻrsatadigan qilib shablonni yangilang.

</docs-step>

<docs-step title="Shablonda `@else`'dan foydalaning">
Endi Angular else holatini aniqlash uchun `@else` sintaksisi bilan tabiiy (native) shablon sintaksisini qoʻllab-quvvatlaydi. Shablonni else holati sifatida `No, the server is not running` xabarini koʻrsatadigan qilib yangilang.

Misol:

```angular-html
template: `
@if (isServerRunning) {
  ...
} @else {
  ...
}
`;
```

Yetishmayotgan markup'ni toʻldirish uchun kodingizni qoʻshing.

</docs-step>

</docs-workflow>

Bu turdagi funksionallik shartli boshqaruv oqimi deb ataladi. Keyingi qadamda shablonda elementlarni qanday takrorlashni oʻrganasiz.
