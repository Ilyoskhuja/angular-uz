# Komponent klassini yangilash

Angular'da komponentning logikasi va xatti-harakati komponentning TypeScript klassida aniqlanadi.

NOTE: [Asoslar qoʻllanmasida dinamik matnni koʻrsatish](/essentials/templates#showing-dynamic-text) haqida koʻproq bilib oling.

Bu mashgʻulotda komponent klassini qanday yangilashni va [interpolatsiyadan](/guide/templates/binding#render-dynamic-text-with-text-interpolation) qanday foydalanishni oʻrganasiz.

<hr />

<docs-workflow>

<docs-step title="`city` nomli xususiyat qoʻshing">
`App` klassiga `city` nomli xususiyat qoʻshib, komponent klassini yangilang.

```ts
export class App {
  city = 'San Francisco';
}
```

`city` xususiyati `string` turiga ega, lekin [TypeScript'dagi tur xulosasi (type inference)](https://www.typescriptlang.org/docs/handbook/type-inference.html) tufayli turni koʻrsatmasligingiz ham mumkin. `city` xususiyatidan `App` klassida foydalanish va komponent shablonida unga murojaat qilish mumkin.

<br>

Shablonda klass xususiyatidan foydalanish uchun `{{ }}` sintaksisidan foydalanishingiz kerak.
</docs-step>

<docs-step title="Komponent shablonini yangilang">
`template` xususiyatini quyidagi HTML'ga mos keladigan qilib yangilang:

```ts
template: `Hello {{ city }}`,
```

Bu interpolatsiyaga misol boʻlib, Angular shablon sintaksisining bir qismidir. U shablonga dinamik matn joylashtirishdan ham koʻproq ishlarni bajarish imkonini beradi. Bu sintaksisdan funksiyalarni chaqirish, ifodalar yozish va boshqa ishlar uchun ham foydalanishingiz mumkin.
</docs-step>

<docs-step title="Interpolatsiya bilan koʻproq amaliyot">
Buni sinab koʻring — ichida `1 + 1` boʻlgan yana bir `{{ }}` juftligini qoʻshing:

```ts
template: `Hello {{ city }}, {{ 1 + 1 }}`,
```

Angular `{{ }}` ichidagi ifodani hisoblab, natijani shablonda render qiladi.
</docs-step>

</docs-workflow>

Bu Angular shablonlari bilan qilish mumkin boʻlgan ishlarning boshlanishi xolos; koʻproq bilish uchun oʻrganishda davom eting.
