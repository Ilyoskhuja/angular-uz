# Marshrutlash haqida umumiy koʻrinish

Koʻpchilik ilovalar uchun ilova bitta sahifadan koʻproqni talab qiladigan payt keladi. Bu muqarrar payt kelganda, marshrutlash foydalanuvchilar uchun unumdorlik masalasining katta qismiga aylanadi.

NOTE: [Chuqur qoʻllanmada marshrutlash](/guide/routing) haqida koʻproq bilib oling.

Bu mashgʻulotda ilovangizni Angular Router'dan foydalanish uchun qanday oʻrnatish va sozlashni oʻrganasiz.

<hr>

<docs-workflow>

<docs-step title="app.routes.ts faylini yarating {#create-an-approutests-file}">

`app.routes.ts` ichida quyidagi oʻzgarishlarni kiriting:

1. `@angular/router` paketidan `Routes`'ni import qiling.
2. `Routes` turidagi `routes` nomli konstantani eksport qiling va unga qiymat sifatida `[]` bering.

```ts
import {Routes} from '@angular/router';

export const routes: Routes = [];
```

</docs-step>

<docs-step title="Provider'ga marshrutlashni qoʻshing {#add-routing-to-provider}">

`app.config.ts`'da quyidagi qadamlar bilan ilovani Angular Router'ga sozlang:

1. `@angular/router`'dan `provideRouter` funksiyasini import qiling.
1. `./app.routes.ts`'dan `routes`'ni import qiling.
1. `providers` massivida `routes`'ni argument sifatida uzatib, `provideRouter` funksiyasini chaqiring.

```ts {highlight:[2,3,6]}
import {ApplicationConfig} from '@angular/core';
import {provideRouter} from '@angular/router';
import {routes} from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [provideRouter(routes)],
};
```

</docs-step>

<docs-step title="Komponentga `RouterOutlet`'ni import qiling {#import-routeroutlet-in-the-component}">

Nihoyat, ilovangiz Angular Router'dan foydalanishga tayyor boʻlishini taʼminlash uchun ilovaga router kerakli kontentni qayerda koʻrsatishini kutayotganingizni aytishingiz kerak. Bunga `@angular/router`'dagi `RouterOutlet` direktivasidan foydalanib erishing.

`App` shablonini `<router-outlet />` qoʻshib yangilang

```angular-ts {highlight:[9]}
@Component({
...
template: `
    <nav>
      <a href="/">Home</a>
      |
      <a href="/user">User</a>
    </nav>
    <router-outlet />
  `,
imports: [RouterOutlet],
})
export class App {}
```

</docs-step>

</docs-workflow>

Ilovangiz endi Angular Router'dan foydalanishga sozlandi. Ajoyib ish! 🙌

Ilovamiz uchun marshrutlarni aniqlash boʻlgan keyingi qadamni oʻrganish uchun shu zaylda davom eting.
