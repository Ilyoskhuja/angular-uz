# Marshrutni aniqlash

Ilovani Angular Router'dan foydalanishga sozlab olganingizdan soʻng, endi marshrutlarni aniqlashingiz kerak.

NOTE: [Chuqur qoʻllanmada asosiy marshrutni aniqlash](/guide/routing/define-routes) haqida koʻproq bilib oling.

Bu mashgʻulotda ilovangizga marshrutlarni qanday qoʻshish va sozlashni oʻrganasiz.

<hr>

<docs-workflow>

<docs-step title="`app.routes.ts` faylida marshrutni aniqlang {#define-a-route-in-approutests}">

Ilovangizda koʻrsatish uchun ikkita sahifa bor: (1) Bosh sahifa (Home Page) va (2) Foydalanuvchi sahifasi (User Page).

Marshrutni aniqlash uchun `app.routes.ts` faylidagi `routes` massiviga quyidagilarni oʻz ichiga olgan marshrut obyektini qoʻshing:

- Marshrutning `path` qiymati (u avtomatik tarzda ildiz yoʻldan (yaʼni `/`) boshlanadi)
- Marshrut koʻrsatishi kerak boʻlgan `component`

```ts
import {Routes} from '@angular/router';
import {Home} from './home/home';

export const routes: Routes = [
  {
    path: '',
    component: Home,
  },
];
```

Yuqoridagi kod `Home` komponentini marshrut sifatida qanday qoʻshish mumkinligiga misol. Endi buni `User` bilan birga playground'da amalga oshiring.

`User` uchun yoʻl (path) sifatida `'user'` qiymatidan foydalaning.

</docs-step>

<docs-step title="Marshrut taʼrifiga sarlavha qoʻshing {#add-title-to-route-definition}">

Marshrutlarni toʻgʻri aniqlashdan tashqari, Angular Router har bir marshrutga `title` xususiyatini qoʻshish orqali foydalanuvchilar navigatsiya qilayotganda sahifa sarlavhasini oʻrnatish imkonini ham beradi.

`app.routes.ts` faylida sukut boʻyicha marshrutga (`path: ''`) va `user` marshrutiga `title` xususiyatini qoʻshing. Mana bir misol:

```ts {highlight:[7]}
import {Routes} from '@angular/router';
import {Home} from './home/home';

export const routes: Routes = [
  {
    path: '',
    title: 'App Home Page',
    component: Home,
  },
];
```

</docs-step>

</docs-workflow>

Bu mashgʻulotda Angular ilovangizda marshrutlarni qanday aniqlash va sozlashni oʻrgandingiz. Ajoyib ish. 🙌

Ilovangizda marshrutlashni toʻliq yoqish yoʻli deyarli yakunlandi, davom eting.
