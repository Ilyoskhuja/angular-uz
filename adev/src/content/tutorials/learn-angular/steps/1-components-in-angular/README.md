# Angular'da komponentlar

Komponentlar — har qanday Angular ilovasining asosiy qurilish bloklari. Har bir komponent uch qismdan iborat:

- TypeScript klassi
- HTML shabloni
- CSS stillari

NOTE: [Asoslar qoʻllanmasidagi komponentlar](/essentials/components) haqida koʻproq bilib oling.

Bu mashgʻulotda komponentning shabloni va stillarini qanday yangilashni oʻrganasiz.

<hr />

Bu Angular bilan ishlashni boshlash uchun ajoyib imkoniyat.

<docs-workflow>

<docs-step title="Komponent shablonini yangilang">
`template` xususiyatini `Hello Universe` deb oʻqiladigan qilib yangilang

```ts
template: `
  Hello Universe
`,
```

HTML shablonini oʻzgartirganingizda, oldindan koʻrish (preview) oynasi sizning xabaringiz bilan yangilandi. Keling, yana bir qadam oldinga boramiz: matn rangini oʻzgartiring.
</docs-step>

<docs-step title="Komponent stillarini yangilang">
Stillar qiymatini yangilang va `color` xususiyatini `blue`'dan `#a144eb`'ga oʻzgartiring.

```ts
styles: `
  :host {
    color: #a144eb;
  }
`,
```

Oldindan koʻrish oynasini tekshirsangiz, matn rangi oʻzgarganini koʻrasiz.
</docs-step>

</docs-workflow>

Angular'da brauzer qoʻllab-quvvatlaydigan barcha mavjud CSS va HTML'dan foydalanishingiz mumkin. Agar xohlasangiz, shablon va stillaringizni alohida fayllarda saqlashingiz mumkin.
