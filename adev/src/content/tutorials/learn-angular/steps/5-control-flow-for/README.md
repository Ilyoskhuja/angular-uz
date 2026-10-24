# Komponentlarda boshqaruv oqimi - `@for`

Veb-ilovalar yaratishda koʻpincha baʼzi kodni maʼlum sonda takrorlashingiz kerak boʻladi — masalan, ismlar massivi berilganda, har bir ismni `<p>` tegida koʻrsatmoqchi boʻlishingiz mumkin.

NOTE: [Asoslar qoʻllanmasida boshqaruv oqimi](/essentials/templates#control-flow-with-if-and-for) haqida koʻproq bilib oling.

Bu mashgʻulotda shablonda elementlarni takrorlash uchun `@for`'dan qanday foydalanishni oʻrganasiz.

<hr/>

Shablonda elementlarni takrorlash imkonini beradigan sintaksis — `@for`.

Komponentda `@for` sintaksisidan qanday foydalanishga misol:

```angular-ts
@Component({
  ...
  template: `
    @for (os of operatingSystems; track os.id) {
      {{ os.name }}
    }
  `,
})
export class App {
  operatingSystems = [{id: 'win', name: 'Windows'}, {id: 'osx', name: 'macOS'}, {id: 'linux', name: 'Linux'}];
}
```

Eʼtibor berish kerak boʻlgan ikki narsa:

- `for` oldida `@` prefiksi bor, chunki bu [Angular shablon sintaksisi](guide/templates) deb nomlanadigan maxsus sintaksis
- Hali ham `*ngFor`'dan foydalanadigan ilovalar uchun [NgFor boʻyicha Angular hujjatlariga](guide/directives/structural-directives) murojaat qiling

<docs-workflow>

<docs-step title="`users` xususiyatini qoʻshing">
`App` klassiga foydalanuvchilar va ularning ismlarini oʻz ichiga olgan `users` nomli xususiyat qoʻshing.

```ts
[
  {id: 0, name: 'Sarah'},
  {id: 1, name: 'Amy'},
  {id: 2, name: 'Rachel'},
  {id: 3, name: 'Jessica'},
  {id: 4, name: 'Poornima'},
];
```

</docs-step>

<docs-step title="Shablonni yangilang">
`@for` shablon sintaksisidan foydalanib, har bir foydalanuvchi ismini `p` elementida koʻrsatadigan qilib shablonni yangilang.

```angular-html
@for (user of users; track user.id) {
  <p>{{ user.name }}</p>
}
```

NOTE: `track`'dan foydalanish shart, `id` yoki boshqa biror unikal identifikatordan foydalanishingiz mumkin.

</docs-step>

</docs-workflow>

Bu turdagi funksionallik boshqaruv oqimi deb ataladi. Keyingi qadamda komponentlarni sozlash va ular bilan muloqot qilishni oʻrganasiz — aytgancha, hozircha ajoyib ishlayapsiz.
